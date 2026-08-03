"""
Multi-camera ANPR system with Firebase gate control (REST, single barrier)
Supports entry and exit cameras, but both write to the same /barrier node.
"""

import argparse
import json
import os
import queue
import threading
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional

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


def draw_overlay(frame, detections, fps: float, camera_type: str = ""):
    """Draw detection overlay on frame"""
    for det in detections:
        x1, y1, x2, y2 = map(int, det["bbox"])
        # Use display_text for camera overlay (includes waiting message), plate_text for logs
        text = det.get("display_text", det.get("plate_text", ""))
        conf = det.get("confidence", 0.0)
        matched = det.get("matched_plate") is not None
        color = (0, 255, 0) if det.get("valid", False) else (0, 165, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        label = f"{text} {conf:.2f}"
        if matched:
            label += " ✓ MATCHED"
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

    status_text = (
        f"FPS: {fps:.1f} | Plates: {len(detections)} | Camera: {camera_type.upper()}"
    )
    cv2.putText(
        frame,
        status_text,
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2,
        cv2.LINE_AA,
    )
    return frame


def write_logs(csv_path, jsonl_path, row):
    """Write detection logs to CSV and JSONL"""
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    os.makedirs(os.path.dirname(jsonl_path), exist_ok=True)
    import csv

    write_header = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(
                [
                    "timestamp",
                    "plate_text",
                    "confidence",
                    "x1",
                    "y1",
                    "x2",
                    "y2",
                    "camera_type",
                    "matched",
                ]
            )
        w.writerow(
            [
                row["timestamp"],
                row["plate_text"],
                f"{row['confidence']:.3f}",
                *row["bbox"],
                row.get("camera_type", ""),
                row.get("matched_plate") is not None,
            ]
        )
    with open(jsonl_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_gate_access_log(log_path, vehicle_number, approved=True):
    """Write gate access logs for approved vehicles only"""
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    import csv
    from datetime import datetime

    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    day_str = now.strftime("%A")
    time_str = now.strftime("%H-%M-%S")
    
    # Check if file exists and if today's date header exists
    file_exists = os.path.exists(log_path)
    needs_date_header = True
    
    if file_exists:
        # Check if today's date is already in the file
        with open(log_path, "r", newline="", encoding="utf-8") as f:
            last_lines = f.readlines()
            if last_lines:
                # Check last few lines for today's date
                for line in reversed(last_lines[-10:]):  # Check last 10 lines
                    if date_str in line:
                        needs_date_header = False
                        break
    
    with open(log_path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        
        # Write column headers only if file is new
        if not file_exists:
            w.writerow(["Gate Access Log - Approved Vehicles Only"])
            w.writerow([])  # Empty row for spacing
        
        # Write date header if it's a new day
        if needs_date_header:
            w.writerow([])  # Empty row for spacing between days
            w.writerow([f"Date: {date_str} ({day_str})"])
        
        # Write the access entry
        status = "Approved" if approved else "Denied"
        w.writerow([f"{time_str}", vehicle_number, status])


def load_config(path: str):
    """Load YAML configuration file"""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)




def open_camera_source(source):
    """Open camera source (IP camera, USB camera, or video file)"""
    if isinstance(source, int) or (isinstance(source, str) and source.isdigit()):
        # USB camera or device ID
        cap = cv2.VideoCapture(int(source))
        if cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        return cap
    else:
        # IP camera or video file
        src_str = str(source)
        # For RTSP streams, force FFMPEG backend and set buffer size to reduce latency
        if src_str.lower().startswith("rtsp://"):
            # Use CAP_FFMPEG to avoid CAP_IMAGES backend errors on long RTSP URLs
            cap = cv2.VideoCapture(src_str, cv2.CAP_FFMPEG)
            if cap.isOpened():
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            return cap
        # Non-RTSP sources use default backend
        cap = cv2.VideoCapture(src_str)
        return cap


def process_camera(
    camera_name: str,
    camera_config: Dict[str, Any],
    detector: PlateDetector,
    recognizer: Optional[OCRRecognizer],
    permanent_parking_db: Dict,
    session_csv_path: str,
    cfg: Dict,
    stop_flag: threading.Event,
    auto_close_delay: int = 5,
):
    """Process a single camera stream"""
    source = camera_config.get("source")
    camera_type = camera_config.get("camera_type", "in")
    enabled = camera_config.get("enabled", True)

    if not enabled:
        print(f"Camera {camera_name} is disabled")
        return

    print(f"Starting camera {camera_name} ({camera_type}) from source: {source}")
    cap = open_camera_source(source)

    if not cap.isOpened():
        print(f"❌ Failed to open camera {camera_name} from source: {source}")
        return

    inf = cfg.get("inference", {})
    frame_skip = inf.get("frame_skip", 2)
    detector_only = inf.get("detector_only", False)
    mode = cfg.get("io", {}).get("output_mode", "both")

    # Photo capture configuration (shared across threads)
    capture_enabled = False  # Disabled for open source
    captured_plates = set()  # Track plates already captured today

    q_frames = queue.Queue(maxsize=5)
    q_results = queue.Queue(maxsize=5)

    last_gate_open_time = {}  # Track when gate was last opened per plate

    def capture_thread():
        idx = 0
        while not stop_flag.is_set():
            try:
                ok, frame = cap.read()
                if not ok:
                    time.sleep(0.1)
                    continue
            except Exception as e:
                print(f"Camera capture error: {e}")
                time.sleep(1.0)
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
        fps = 0.0
        # DELAY CONFIGURATION: Change 2.0 to your desired delay in seconds
        OCR_DELAY_SECONDS = 2.0  # <-- EDIT THIS LINE TO CHANGE DELAY (currently 2 seconds)

        # Pause detection after valid match (5 seconds pause)
        pause_until = 0.0  # Timestamp until which detection/OCR is paused
        PAUSE_DURATION = 5.0  # Pause for 5 seconds after valid match
        last_matched_plate = None  # Track last matched plate to prevent re-trigger
        last_match_time = 0.0  # Track when last match was found

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
            current_time = time.time()
            
            # Check if detection is paused
            if current_time < pause_until:
                # Show paused message on overlay
                detections = []
                remaining = pause_until - current_time
                pause_msg = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "plate_text": "",
                    "display_text": f"PAUSED ({remaining:.1f}s)",
                    "confidence": 1.0,
                    "bbox": [10, 10, 200, 50],
                    "valid": False,
                    "matched_plate": None,
                    "original_text": "",
                    "camera_type": camera_type,
                    "camera_name": camera_name,
                    "frame": None,
                    "crop": None,
                }
                detections.append(pause_msg)
                try:
                    q_results.put((frame, detections, fps), timeout=0.1)
                except queue.Full:
                    pass
                continue  # Skip detection and OCR while paused
            
            boxes, scores = detector.detect(frame)
            detections = []

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
                    ok, val_text = validate_with_state_priority(txt, original_text)
                    plate_text = val_text
                    plate_conf = c

                    # Check if plate matches database (with 1-2 char tolerance)
                    if ok and plate_text and permanent_parking_db:
                        matched_data = find_matching_plate(
                            plate_text, permanent_parking_db, max_distance=2
                        )
                        if matched_data:
                            plate_text = matched_data["vehicle_number"]
                            matched_plate = matched_data
                            # PAUSE DETECTION: Valid match found, pause for 5 seconds
                            # Only trigger pause if it's a different plate or >10 seconds since last match
                            if plate_text != last_matched_plate or (current_time - last_match_time) > 10.0:
                                pause_until = current_time + PAUSE_DURATION
                                last_matched_plate = plate_text
                                last_match_time = current_time
                                # Clear all tracked cars to start fresh after pause
                                tracked_cars.clear()
                                print(f"✅ Valid match found: {plate_text} - Pausing detection for {PAUSE_DURATION}s")
                        else:
                            matched_plate = None
                    else:
                        matched_plate = None

                    # Update tracking state - if valid plate detected, stop OCRing for this car
                    # Check if car still exists in tracking (may have been cleared during pause trigger)
                    if matched_car_id is not None and matched_car_id in tracked_cars:
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
                    "matched_plate": matched_plate,
                    "original_text": original_text,
                    "camera_type": camera_type,
                    "camera_name": camera_name,
                    "frame": frame.copy() if ok and plate_text and capture_enabled else None,  # Store frame for photo capture
                    "crop": crop.copy() if ok and plate_text and capture_enabled else None,  # Store crop for photo capture
                }
                detections.append(record)

                # Gate control logic (only after OCR has run, i.e., after delay)
                # Gate control removed for open source release

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
        window_name = f"ANPR-{camera_name.upper()}"

        while not stop_flag.is_set():
            try:
                frame, detections, fps = q_results.get(timeout=0.1)
            except queue.Empty:
                continue

            for det in detections:
                # Skip logging PAUSED messages
                if det.get("display_text", "").startswith("PAUSED"):
                    continue
                
                # Create a copy without frame/crop for logging (numpy arrays aren't JSON serializable)
                det_for_log = {k: v for k, v in det.items() if k not in ["frame", "crop"]}
                    
                if mode in ("json", "both"):
                    print(f"[{camera_name}] Detection: {det_for_log}")

                if det.get("plate_text", "").strip():
                    write_logs(csv_path, jsonl_path, det_for_log)

                    # Update session CSV if matched
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
                        
                        # Photo capture (background thread - no performance impact)

            if overlay:
                out = draw_overlay(frame.copy(), detections, fps, camera_type)
                cv2.imshow(window_name, out)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    stop_flag.set()
            elif not json_only:
                cv2.imshow(window_name, frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    stop_flag.set()

    # Start threads
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


def main():
    parser = argparse.ArgumentParser(
        description="Multi-camera ANPR system with Firebase gate control (REST)"
    )
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
    firebase_cfg = cfg.get("firebase", {})

    # Initialize detector and recognizer
    detector = PlateDetector(
        model_pt_path=cfg["models"]["detector_pt"],
        model_onnx_path=cfg["models"].get("detector_onnx"),
        model_hef_path=cfg["models"].get("detector_hef"),  # Hailo model
        device=inf.get("device", "auto"),
        conf_threshold=inf.get("conf_threshold", 0.5),
        iou_threshold=inf.get("iou_threshold", 0.5),
        input_size=inf.get("input_size", 640),
        use_onnx=inf.get("use_onnx", True),
        use_hailo=inf.get("use_hailo", False),  # Enable Hailo acceleration
    )

    recognizer = None
    if not inf.get("detector_only", False):
        recognizer = OCRRecognizer(
            backend=cfg["models"].get("ocr_backend", "easyocr"),
            langs=cfg["models"].get("ocr_langs", ["en"]),
            model_pt_path=cfg["models"].get("ocr_pt"),
            model_onnx_path=cfg["models"].get("ocr_onnx"),
            model_hef_path=cfg["models"].get("ocr_hef"),  # Hailo model
            device=inf.get("device", "auto"),
            use_onnx=inf.get("use_onnx", True),
            use_hailo=inf.get("use_hailo", False),  # Enable Hailo acceleration
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

    # Initialize Firebase if enabled (REST, no auth)

    # Check if multi-camera mode is enabled
    multi_camera = io.get("multi_camera", False)

    if multi_camera:
        # Multi-camera mode
        cameras = io.get("cameras", {})
        stop_flags = {}
        threads = []

        print(f"\n🚀 Starting multi-camera mode with {len(cameras)} cameras\n")

        for camera_name, camera_config in cameras.items():
            stop_flag = threading.Event()
            stop_flags[camera_name] = stop_flag

            thread = threading.Thread(
                target=process_camera,
                args=(
                    camera_name,
                    camera_config,
                    detector,
                    recognizer,
                    permanent_parking_db,
                    session_csv_path,
                    cfg,
                    stop_flag,
                    auto_close_delay,
                ),
                daemon=True,
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads
        try:
            while any(t.is_alive() for t in threads):
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n⚠️  Stopping all cameras...")
            for stop_flag in stop_flags.values():
                stop_flag.set()
            for thread in threads:
                thread.join(timeout=1.0)
    else:
        # Single camera mode (legacy)
        print("⚠️  Single camera mode - Use multi_camera: true in config for multi-camera support")
        source = io.get("source", 0)
        cap = cv2.VideoCapture(0 if str(source).isdigit() else source)
        if str(source).isdigit():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        stop_flag = threading.Event()

        # Create dummy camera config for single camera
        camera_config = {"source": source, "camera_type": "in", "enabled": True}

        process_camera(
            "single",
            camera_config,
            detector,
            recognizer,
            permanent_parking_db,
            session_csv_path,
            cfg,
            stop_flag,
            auto_close_delay,
        )


if __name__ == "__main__":
    main()


