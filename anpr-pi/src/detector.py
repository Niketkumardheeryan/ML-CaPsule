import os
import torch
import numpy as np

try:
    from ultralytics import YOLO
except Exception:
    YOLO = None

try:
    import onnxruntime as ort
except Exception:
    ort = None

try:
    from src.hailo_detector import HailoYOLODetector, HAILO_AVAILABLE
except Exception:
    HailoYOLODetector = None
    HAILO_AVAILABLE = False


class PlateDetector:
    def __init__(self, model_pt_path: str, model_onnx_path: str = None, model_hef_path: str = None, device: str = "auto", conf_threshold: float = 0.5, iou_threshold: float = 0.5, input_size: int = 640, use_onnx: bool = True, use_hailo: bool = False):
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.input_size = input_size
        
        # Priority: Hailo > ONNX > PyTorch
        self.use_hailo = use_hailo and model_hef_path and os.path.exists(model_hef_path) and HAILO_AVAILABLE
        self.use_onnx = (not self.use_hailo) and use_onnx and model_onnx_path and os.path.exists(model_onnx_path) and ort is not None

        if device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        self.hailo_detector = None
        self.ort_session = None
        self.yolo = None

        if self.use_hailo:
            # Hailo-8 accelerated inference (Raspberry Pi 5)
            print("🚀 Using Hailo-8 accelerator for detection")
            self.hailo_detector = HailoYOLODetector(
                hef_path=model_hef_path,
                conf_threshold=conf_threshold,
                iou_threshold=iou_threshold,
                input_size=input_size
            )
        elif self.use_onnx:
            providers = [
                ("CUDAExecutionProvider", {"arena_extend_strategy": "kNextPowerOfTwo"}),
                "CPUExecutionProvider",
            ] if self.device == "cuda" else ["CPUExecutionProvider"]
            self.ort_session = ort.InferenceSession(model_onnx_path, providers=providers)
        else:
            if YOLO is None:
                raise RuntimeError("Ultralytics YOLO not available and no ONNX/HEF model provided")
            self.yolo = YOLO(model_pt_path)
            self.yolo.fuse()

    def _preprocess(self, image_bgr: np.ndarray) -> np.ndarray:
        import cv2
        img = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        h, w = img.shape[:2]
        scale = self.input_size / max(h, w)
        nh, nw = int(h * scale), int(w * scale)
        resized = cv2.resize(img, (nw, nh))
        padded = np.full((self.input_size, self.input_size, 3), 114, dtype=np.uint8)
        padded[:nh, :nw] = resized
        padded = padded.astype(np.float32) / 255.0
        padded = padded.transpose(2, 0, 1)[None]
        return padded, scale

    def detect(self, image_bgr: np.ndarray):
        if self.use_onnx:
            blob, scale = self._preprocess(image_bgr)
            outputs = self.ort_session.run(None, {self.ort_session.get_inputs()[0].name: blob})
            preds = outputs[0]
            boxes, scores = self._postprocess_yolo_like(preds, image_bgr.shape, scale)
            return boxes, scores
        else:
            # Use smaller input size for speed
            results = self.yolo.predict(
                source=image_bgr, 
                imgsz=416,  # Smaller for speed
                conf=self.conf_threshold, 
                iou=self.iou_threshold, 
                verbose=False, 
                device=0 if self.device == "cuda" else None,
                half=True if self.device == "cuda" else False  # Use FP16 for speed
            )
            boxes = []
            scores = []
            
            # TWO-STAGE APPROACH: Detect CARS first, then crop plate region
            vehicle_classes = [2]  # car=2 in COCO
            
            for r in results:
                if r.boxes is None:
                    continue
                for b in r.boxes:
                    xyxy = b.xyxy[0].cpu().numpy().tolist()
                    conf = float(b.conf[0].cpu().numpy())
                    cls = int(b.cls[0].cpu().numpy()) if hasattr(b, 'cls') else 0
                    
                    # Only process CARS (class 2)
                    if conf >= self.conf_threshold and cls in vehicle_classes:
                        x1, y1, x2, y2 = xyxy
                        w = x2 - x1
                        h = y2 - y1
                        
                        # WIDER PLATE CROP - Capture full bumper area
                        # VERTICAL: 55-85% of car height (30% band for full plate)
                        plate_y1 = y1 + h * 0.55  # Start higher
                        plate_y2 = y1 + h * 0.85  # End lower (full bumper)
                        
                        # HORIZONTAL: 20-80% (60% width to ensure full plate)
                        plate_x1 = x1 + w * 0.20
                        plate_x2 = x1 + w * 0.80
                        
                        # Add 15% padding for OCR context
                        crop_w = plate_x2 - plate_x1
                        crop_h = plate_y2 - plate_y1
                        padding_x = int(crop_w * 0.15)
                        padding_y = int(crop_h * 0.15)
                        
                        plate_x1 = plate_x1 - padding_x
                        plate_x2 = plate_x2 + padding_x
                        plate_y1 = plate_y1 - padding_y
                        plate_y2 = plate_y2 + padding_y
                        
                        # Ensure valid coordinates
                        plate_x1 = max(0, int(plate_x1))
                        plate_y1 = max(0, int(plate_y1))
                        plate_x2 = min(image_bgr.shape[1], int(plate_x2))
                        plate_y2 = min(image_bgr.shape[0], int(plate_y2))
                        
                        # Calculate final dimensions
                        plate_w = plate_x2 - plate_x1
                        plate_h = plate_y2 - plate_y1
                        
                        # Validate: minimum size (60x25) for OCR
                        if plate_w >= 60 and plate_h >= 25:
                            aspect_ratio = plate_w / plate_h if plate_h > 0 else 0
                            if 1.2 <= aspect_ratio <= 8.0:  # More lenient
                                boxes.append([plate_x1, plate_y1, plate_x2, plate_y2])
                                scores.append(conf)
            
            # OLD CODE - COMMENTED OUT (was used for car detection + 30% crop)
            # vehicle_classes = [2]  # car=2, motorcycle=3 (commented out)
            # for r in results:
            #     if r.boxes is None:
            #         continue
            #     for b in r.boxes:
            #         xyxy = b.xyxy[0].cpu().numpy().tolist()
            #         conf = float(b.conf[0].cpu().numpy())
            #         cls = int(b.cls[0].cpu().numpy()) if hasattr(b, 'cls') else 0
            #         # Detect ALL cars (full bounding box check, including side views)
            #         if conf >= self.conf_threshold and cls in vehicle_classes:
            #             x1, y1, x2, y2 = xyxy
            #             h = y2 - y1
            #             w = x2 - x1
            #             
            #             # For OCR: Use lower 30% of detected car for plate recognition
            #             # Detection uses full box, but plate region is bottom 30%
            #             plate_box = [
            #                 max(0, x1),
            #                 max(0, y1 + h*0.70),  # Lower 30% for plate OCR
            #                 min(image_bgr.shape[1], x2),
            #                 min(image_bgr.shape[0], y2)
            #             ]
            #             boxes.append(plate_box)
            #             scores.append(conf)
            return boxes, scores

    def _postprocess_yolo_like(self, preds: np.ndarray, shape, scale: float):
        # This method expects YOLO-style output (N, num_boxes, 85) -> adapt per model
        # For portability, assume boxes already filtered. If custom ONNX, adjust decoding.
        # Here we treat preds as [num, 6] -> x1,y1,x2,y2,conf,cls
        h, w = shape[:2]
        boxes = []
        scores = []
        if preds.ndim == 3:
            preds = preds[0]
        for row in preds:
            if len(row) < 6:
                continue
            x1, y1, x2, y2, conf, cls = row[:6]
            if conf < self.conf_threshold:
                continue
            # Undo letterbox scaling
            inv = 1.0 / scale
            x1 = float(np.clip(x1 * inv, 0, w - 1))
            y1 = float(np.clip(y1 * inv, 0, h - 1))
            x2 = float(np.clip(x2 * inv, 0, w - 1))
            y2 = float(np.clip(y2 * inv, 0, h - 1))
            boxes.append([x1, y1, x2, y2])
            scores.append(float(conf))
        return boxes, scores
