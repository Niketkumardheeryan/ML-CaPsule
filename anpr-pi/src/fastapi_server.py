from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn
import cv2
import numpy as np
import os
import yaml
from datetime import datetime

from src.detector import PlateDetector
from src.recognizer import OCRRecognizer
from src.postprocess import validate


def load_config(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


cfg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "configs", "config.yaml")
cfg = load_config(cfg_path)
inf = cfg.get("inference", {})

detector = PlateDetector(
    model_pt_path=cfg["models"]["detector_pt"],
    model_onnx_path=cfg["models"].get("detector_onnx"),
    device=inf.get("device", "auto"),
    conf_threshold=inf.get("conf_threshold", 0.5),
    iou_threshold=inf.get("iou_threshold", 0.5),
    input_size=inf.get("input_size", 640),
    use_onnx=inf.get("use_onnx", True),
)

recognizer = OCRRecognizer(
    backend=cfg["models"].get("ocr_backend", "easyocr"),
    langs=cfg["models"].get("ocr_langs", ["en"]),
    model_pt_path=cfg["models"].get("ocr_pt"),
    model_onnx_path=cfg["models"].get("ocr_onnx"),
    device=inf.get("device", "auto"),
    use_onnx=inf.get("use_onnx", True),
    apply_clahe_opt=inf.get("apply_clahe", True),
)

app = FastAPI()


@app.post("/infer")
async def infer(image: UploadFile = File(...)):
    data = np.frombuffer(await image.read(), dtype=np.uint8)
    bgr = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if bgr is None:
        return JSONResponse({"error": "Invalid image"}, status_code=400)
    boxes, scores = detector.detect(bgr)
    detections = []
    for b, s in zip(boxes, scores):
        x1, y1, x2, y2 = map(int, b)
        crop = bgr[max(0, y1):max(0, y2), max(0, x1):max(0, x2)]
        txt, c = recognizer.recognize(crop) if crop.size > 0 else ("", 0.0)
        ok, val_text = validate(txt)
        detections.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "plate_text": val_text,
            "confidence": float(min(1.0, max(0.0, 0.5 * s + 0.5 * c))),
            "bbox": [x1, y1, x2, y2],
            "valid": ok,
        })
    return {"detections": detections}


if __name__ == "__main__":
    uvicorn.run(app, host=cfg["server"].get("host", "0.0.0.0"), port=cfg["server"].get("port", 8000))


