import cv2
import numpy as np
from ultralytics import YOLO

# ============ DANGER MAP ============
DANGER_MAP = {
    "dog": "LOW",
    "cat": "LOW",
    "cow": "MEDIUM",
    "horse": "MEDIUM",
    "elephant": "HIGH",
    "bear": "HIGH",
    "lion": "HIGH",
    "tiger": "HIGH",
    "zebra": "MEDIUM",
    "giraffe": "LOW",
    "sheep": "LOW",
    "bird": "LOW",
}

DANGER_COLORS = {
    "HIGH":   (0, 0, 255),    # Red
    "MEDIUM": (0, 165, 255),  # Orange
    "LOW":    (0, 255, 0),    # Green
}

DANGER_EMOJI = {
    "HIGH":   "🔴",
    "MEDIUM": "🟡",
    "LOW":    "🟢",
}


def load_model(model_path: str = "yolov8n.pt") -> YOLO:
    return YOLO(model_path)


def detect_animals(model: YOLO, frame: np.ndarray, conf: float = 0.5):
    """
    Run YOLOv8 detection on a single frame.
    Returns annotated frame + list of detection dicts.
    """
    results = model(frame, conf=conf, verbose=False)
    annotated = results[0].plot()

    detections = []
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            confidence = float(box.conf[0])
            danger = DANGER_MAP.get(label, "LOW")
            x1, y1, x2, y2 = [int(v) for v in box.xyxy[0]]

            # Overlay danger text on frame
            color = DANGER_COLORS[danger]
            text_y = max(y1 - 30, 20)
            cv2.putText(annotated, f"Danger: {danger}",
                        (x1, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, color, 2)

            detections.append({
                "label": label,
                "confidence": round(confidence, 2),
                "danger": danger,
                "bbox": (x1, y1, x2, y2),
            })

    return annotated, detections


def get_highest_danger(detections: list) -> str:
    priority = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    if not detections:
        return "NONE"
    return max(detections, key=lambda d: priority[d["danger"]])["danger"]