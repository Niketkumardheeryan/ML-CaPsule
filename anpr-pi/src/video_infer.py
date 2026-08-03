import argparse
import json
import os
import queue
import threading
import time
from datetime import datetime

import cv2
import numpy as np
import yaml

from src.detector import PlateDetector
from src.recognizer import OCRRecognizer
from src.postprocess import (
    validate_with_state_priority,
    load_permanent_parking_db,
    find_matching_plate,
    update_session_csv,
)


def draw_overlay(frame, detections, fps: float):
    for det in detections:
        x1, y1, x2, y2 = map(int, det["bbox"])  # [x1,y1,x2,y2]
        # Use display_text for camera overlay (includes waiting message), plate_text for logs
        text = det.get("display_text", det.get("plate_text", ""))
        conf = det.get("confidence", 0.0)
        color = (0, 255, 0) if det.get("valid", False) else (0, 165, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        label = f"{text} {conf:.2f}"
        cv2.putText(
            frame,
            label,
            (x1, max(0, y1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
            cv2.LINE_AA,
        )
    cv2.putText(
        frame,
        f"FPS: {fps:.1f} | Plates: {len(detections)}",
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2,
        cv2.LINE_AA,
    )
    return frame


def write_logs(csv_path, jsonl_path, row):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    os.makedirs(os.path.dirname(jsonl_path), exist_ok=True)
    import csv

    write_header = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["timestamp", "plate_text", "confidence", "x1", "y1", "x2", "y2"])
        w.writerow(
            [row["timestamp"], row["plate_text"], f"{row['confidence']:.3f}", *row["bbox"]]
        )
    with open(jsonl_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_config(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, default=None, help="0 | path | rtsp/http url")
    parser.add_argument("--conf", type=float, default=None)
    parser.add_argument("--skip", type=int, default=None)
    parser.add_argument("--mode", type=str, default=None, choices=["overlay", "json", "both"])
    parser.add_argument("--detector-only", action="store_true")
    parser.add_argument(
        "--config",
        type=str,
        default=os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "configs", "config.yaml"
        ),
    )
    args = parser.parse_args()

    cfg = load_config(args.config)
    inf = cfg.get("inference", {})
    io = cfg.get("io", {})

    source = args.source if args.source is not None else io.get("source", 0)
    conf_th = args.conf if args.conf is not None else inf.get("conf_threshold", 0.5)
    frame_skip = args.skip if args.skip is not None else inf.get("frame_skip", 2)
    mode = args.mode if args.mode is not None else io.get("output_mode", "both")
    detector_only = args.detector_only or inf.get("detector_only", False)

    detector = PlateDetector(
        model_pt_path=cfg["models"]["detector_pt"],
        model_onnx_path=cfg["models"].get("detector_onnx"),
        device=inf.get("device", "auto"),
        conf_threshold=conf_th,
        iou_threshold=inf.get("iou_threshold", 0.5),
        input_size=inf.get("input_size", 640),
        use_onnx=inf.get("use_onnx", True),
    )

    recognizer = None
    if not detector_only:
        recognizer = OCRRecognizer(
            backend=cfg["models"].get("ocr_backend", "easyocr"),
            langs=cfg["models"].get("ocr_langs", ["en"]),
            model_pt_path=cfg["models"].get("ocr_pt"),
            model_onnx_path=cfg["models"].get("ocr_onnx"),
            device=inf.get("device", "auto"),
            use_onnx=inf.get("use_onnx", True),
            apply_clahe_opt=inf.get("apply_clahe", True),
        )

    # Load permanent parking database
    db_cfg = cfg.get("database", {})
    permanent_parking_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), db_cfg.get("path", "logs/parking_database.csv")
    )
    session_csv_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), db_cfg.get("session_path", "logs/session_log.csv")
    )
    permanent_parking_db = load_permanent_parking_db(permanent_parking_path)
    print(f"Loaded {len(permanent_parking_db)} plates from permanent parking database")


    # Check if multi-camera mode is enabled
    multi_camera = io.get("multi_camera", False)
    if multi_camera:
        print("⚠️  Multi-camera mode enabled. Please use: python -m src.multi_camera_infer")
        print("   Falling back to single camera mode...")

    cap = cv2.VideoCapture(0 if str(source).isdigit() else source)
    if str(source).isdigit():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    elif "rtsp" in str(source).lower():
        # Reduce latency for RTSP streams
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    q_frames = queue.Queue(maxsize=5)
    q_results = queue.Queue(maxsize=5)
    stop_flag = threading.Event()
    last_gate_open_time = {}  # Track when gate was last opened per plate
    

    # Photo capture settings 
    capture_enabled = False  # Disabled for open source release
    captured_plates = set() 

    def capture_thread():
        idx = 0
        while not stop_flag.is_set():
            ok, frame = cap.read()
            if not ok:
                time.sleep(0.01)
                continue
            if frame_skip > 1 and (idx % frame_skip) != 0:
                idx += 1
                continue
            idx += 1
            try:
                q_frames.put(frame, timeout=0.1)
            except queue.Full:
                pass

    def infer_thread():
        last_time = time.time()
        fps = 0.0
        # DELAY CONFIGURATION: Change 2.0 to your desired delay in seconds
        OCR_DELAY_SECONDS = 2.0  # <-- EDIT THIS LINE TO CHANGE DELAY (currently 2 seconds)

        # Track cars using IoU-based matching (handles moving cars better)
        # Structure: {car_id: {'first_time': float, 'bbox': [x1,y1,x2,y2],
        #                      'ocr_done': bool, 'ocr_failed': bool, 'last_seen': float,
        #                      'plate_text': str, 'plate_conf': float,
        #                      'matched_plate': dict, 'original_text': str, 'valid': bool}}
        tracked_cars = {}  # {car_id: car_info}
        next_car_id = 0

        def calculate_iou(box1, box2):
            """Calculate Intersection over Union of two boxes"""
            x1_1, y1_1, x2_1, y2_1 = box1
            x1_2, y1_2, x2_2, y2_2 = box2

            # Calculate intersection
            x1_i = max(x1_1, x1_2)
            y1_i = max(y1_1, y1_2)
            x2_i = min(x2_1, x2_2)
            y2_i = min(y2_1, y2_2)

            if x2_i <= x1_i or y2_i <= y1_i:
                return 0.0

            intersection = (x2_i - x1_i) * (y2_i - y1_i)
            area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
            area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
            union = area1 + area2 - intersection

            return intersection / union if union > 0 else 0.0

        def find_matching_car(current_box, tracked_cars, iou_threshold=0.3):
            """Find if current box matches any tracked car"""
            best_match = None
            best_iou = 0.0
            for car_id, car_info in tracked_cars.items():
                iou = calculate_iou(current_box, car_info["bbox"])
                if iou > best_iou and iou >= iou_threshold:
                    best_iou = iou
                    best_match = car_id
            return best_match

        while not stop_flag.is_set():
            try:
                frame = q_frames.get(timeout=0.1)
            except queue.Empty:
                continue
            start = time.time()
            boxes, scores = detector.detect(frame)
            detections = []
            current_time = time.time()

            # Clean up old tracked cars (not seen for 10 seconds)
            tracked_cars = {
                k: v for k, v in tracked_cars.items() if current_time - v["last_seen"] < 10.0
            }

            for b, s in zip(boxes, scores):
                x1, y1, x2, y2 = map(int, b)
                current_box = [x1, y1, x2, y2]
                crop = frame[max(0, y1) : max(0, y2), max(0, x1) : max(0, x2)]

                # Basic filters to suppress obvious side views / tiny distant boxes
                w = x2 - x1
                h = y2 - y1
                aspect = w / (h + 1e-6)
                frame_area = frame.shape[0] * frame.shape[1]
                if aspect > 3.5:
                    continue  # very wide => likely side view
                if w * h < 0.004 * frame_area:
                    continue  # too small => likely distant/irrelevant

                plate_text = ""  # For logs - empty when waiting
                display_text = ""  # For camera display - shows waiting message
                plate_conf = 0.0
                original_text = ""
                matched_plate = None

                # Find if this box matches an existing tracked car
                matched_car_id = find_matching_car(current_box, tracked_cars)

                if matched_car_id is not None:
                    # Existing car - use its tracking info
                    car_info = tracked_cars[matched_car_id]
                    car_info["bbox"] = current_box  # Update position
                    car_info["last_seen"] = current_time
                    first_detection_time = car_info["first_time"]
                    ocr_done = car_info.get("ocr_done", False)
                    ocr_failed = car_info.get("ocr_failed", False)
                    # If OCR already done, use stored results
                    if ocr_done:
                        plate_text = car_info.get("plate_text", "")
                        plate_conf = car_info.get("plate_conf", 0.0)
                        original_text = car_info.get("original_text", "")
                        matched_plate = car_info.get("matched_plate", None)
                        ok = car_info.get("valid", False)
                        display_text = plate_text  # Show plate on camera
                else:
                    # New car - create new tracking entry
                    car_id = next_car_id
                    next_car_id += 1
                    matched_car_id = car_id
                    tracked_cars[car_id] = {
                        "first_time": current_time,
                        "bbox": current_box,
                        "ocr_done": False,
                        "ocr_failed": False,
                        "last_seen": current_time,
                        "plate_text": "",
                        "plate_conf": 0.0,
                        "original_text": "",
                        "matched_plate": None,
                        "valid": False,
                    }
                    first_detection_time = current_time
                    ocr_done = False
                    ocr_failed = False

                # Calculate time since first detection
                time_since_detection = current_time - first_detection_time

                # Determine if we should run OCR
                should_run_ocr = False
                if not detector_only and crop.size > 0 and not ocr_done:
                    if ocr_failed:
                        # OCR failed before (no valid plate), retry immediately without delay
                        should_run_ocr = True
                    elif time_since_detection >= OCR_DELAY_SECONDS:
                        # First time OCR - delay has passed
                        should_run_ocr = True

                if should_run_ocr:
                    txt, c = recognizer.recognize(crop)
                    original_text = txt
                    # Use state priority validation (tries TN/KL first, then original)
                    ok, val_text = validate_with_state_priority(txt, original_text)
                    plate_text = val_text
                    plate_conf = c

                    # Check if plate matches database (with 1-2 char tolerance)
                    if ok and plate_text and permanent_parking_db:
                        matched_data = find_matching_plate(
                            plate_text, permanent_parking_db, max_distance=2
                        )
                        if matched_data:
                            # Use the matched plate from database (corrected version)
                            plate_text = matched_data["vehicle_number"]
                            matched_plate = matched_data
                        else:
                            matched_plate = None
                    else:
                        matched_plate = None

                    # Update tracking state - if valid plate detected, stop OCRing for this car
                    if matched_car_id is not None:
                        if ok and plate_text:
                            # Valid plate detected (any valid plate) - stop OCRing for this car
                            tracked_cars[matched_car_id]["ocr_done"] = True
                            tracked_cars[matched_car_id]["ocr_failed"] = False
                            tracked_cars[matched_car_id]["plate_text"] = plate_text
                            tracked_cars[matched_car_id]["plate_conf"] = plate_conf
                            tracked_cars[matched_car_id]["original_text"] = original_text
                            tracked_cars[matched_car_id]["matched_plate"] = matched_plate
                            tracked_cars[matched_car_id]["valid"] = ok
                            display_text = plate_text  # Show plate on camera
                        else:
                            # No valid plate - mark as failed, will retry on next frame
                            tracked_cars[matched_car_id]["ocr_failed"] = True
                            tracked_cars[matched_car_id]["ocr_done"] = False
                            display_text = ""  # No valid plate to display
                elif not ocr_done:
                    # Not running OCR - either waiting for delay or no crop
                    ok, _ = validate("")
                    # If waiting, show countdown on display but don't log it
                    if time_since_detection < OCR_DELAY_SECONDS:
                        display_text = (
                            f"Waiting... ({OCR_DELAY_SECONDS - time_since_detection:.1f}s)"
                        )
                        plate_text = ""  # Empty so it won't be logged
                    else:
                        display_text = ""
                        plate_text = ""

                record = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "plate_text": plate_text,  # Empty when waiting - won't be logged
                    "display_text": display_text,  # Shows waiting message on camera
                    "confidence": float(
                        min(
                            1.0,
                            max(
                                0.0,
                                s
                                if detector_only
                                else (0.5 * s + 0.5 * plate_conf),
                            ),
                        )
                    ),
                    "bbox": [int(x1), int(y1), int(x2), int(y2)],
                    "valid": ok,
                    "matched_plate": matched_plate,  # Store if matched with DB
                    "original_text": original_text,  # Store original OCR text
                    "frame": frame.copy() if ok and plate_text and capture_enabled else None,  # Store frame for photo capture
                    "crop": crop.copy() if ok and plate_text and capture_enabled else None,  # Store crop for photo capture
                }
                detections.append(record)
            end = time.time()
            dt = end - start
            fps = 1.0 / dt if dt > 0 else 0.0
            try:
                q_results.put((frame, detections, fps), timeout=0.1)
            except queue.Full:
                pass

    def display_thread():
        json_only = mode == "json"
        overlay = mode in ("overlay", "both")
        csv_path = cfg["io"]["save_csv"]
        jsonl_path = cfg["io"]["save_jsonl"]
        while not stop_flag.is_set():
            try:
                frame, detections, fps = q_results.get(timeout=0.1)
            except queue.Empty:
                continue
            for det in detections:
                # Log all detections for debugging, but only save plates with text
                if mode in ("json", "both"):
                    print(f"Detection: {det}")
                if det.get("plate_text", "").strip():
                    write_logs(csv_path, jsonl_path, det)

                    # If plate matched with permanent parking database, update session CSV
                    matched_data = det.get("matched_plate")
                    if matched_data and det.get("valid", False):
                        now = datetime.utcnow().isoformat() + "Z"
                        session_data = {
                            "permanent_parking_id": matched_data.get("id", ""),
                            "vehicle_number": matched_data.get(
                                "vehicle_number", det["plate_text"]
                            ),
                            "entry_time": det["timestamp"] if camera_type == "in" else "",
                            "exit_time": det["timestamp"] if camera_type == "out" else "",
                            "duration_minutes": "",
                            "created_at": now,
                            "updated_at": now,
                        }
                        update_session_csv(session_csv_path, session_data)
                        vehicle_number = matched_data.get(
                            "vehicle_number", det["plate_text"]
                        )
                        print(
                            f"✅ Matched plate {vehicle_number} (ID: {matched_data.get('id')}) - updated session CSV"
                        )

            if overlay:
                out = draw_overlay(frame.copy(), detections, fps)
                cv2.imshow("ANPR-India", out)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    stop_flag.set()
            elif not json_only:
                # both flags false shouldn't happen; default to showing raw
                cv2.imshow("ANPR-India", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    stop_flag.set()

    t_cap = threading.Thread(target=capture_thread, daemon=True)
    t_inf = threading.Thread(target=infer_thread, daemon=True)
    t_disp = threading.Thread(target=display_thread, daemon=True)
    t_cap.start()
    t_inf.start()
    t_disp.start()

    try:
        while t_disp.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        stop_flag.set()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()


