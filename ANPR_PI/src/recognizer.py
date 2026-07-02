import os
import numpy as np
import torch

try:
    import onnxruntime as ort
except Exception:
    ort = None

try:
    import easyocr
except Exception:
    easyocr = None

try:
    from paddleocr import PaddleOCR
except Exception:
    PaddleOCR = None

try:
    from src.hailo_ocr import HailoOCR, HAILO_AVAILABLE
except Exception:
    HailoOCR = None
    HAILO_AVAILABLE = False


def apply_clahe(img_bgr):
    import cv2
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


class OCRRecognizer:
    def __init__(self, backend: str = "easyocr", langs=None, model_pt_path: str = None, model_onnx_path: str = None, model_hef_path: str = None, device: str = "auto", use_onnx: bool = True, use_hailo: bool = False, apply_clahe_opt: bool = True):
        if langs is None:
            langs = ["en"]
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.backend = backend
        self.apply_clahe_opt = apply_clahe_opt

        # Priority: Hailo > ONNX > PyTorch backends
        self.use_hailo = use_hailo and model_hef_path and os.path.exists(model_hef_path) and HAILO_AVAILABLE
        self.use_onnx = (not self.use_hailo) and use_onnx and model_onnx_path and os.path.exists(model_onnx_path) and ort is not None
        
        self.hailo_ocr = None
        self.ort_session = None
        self.reader = None
        self.paddle_ocr = None

        if self.use_hailo:
            # Hailo-8 accelerated inference (Raspberry Pi 5)
            print("🚀 Using Hailo-8 accelerator for OCR")
            self.hailo_ocr = HailoOCR(
                hef_path=model_hef_path,
                apply_clahe=apply_clahe_opt
            )
        elif self.use_onnx:
            # ONNX Runtime inference
            providers = ["CUDAExecutionProvider", "CPUExecutionProvider"] if self.device == "cuda" else ["CPUExecutionProvider"]
            self.ort_session = ort.InferenceSession(model_onnx_path, providers=providers)
        else:
            # Fallback to PaddleOCR, EasyOCR or custom backends
            if self.backend == "paddleocr":
                if PaddleOCR is None:
                    raise RuntimeError("paddleocr not installed. Run: pip install paddleocr paddlepaddle")
                # PaddleOCR for license plates (better than EasyOCR)
                # Minimal parameters - newer PaddleOCR is stricter
                self.paddle_ocr = PaddleOCR(
                    use_angle_cls=False,  # Plates are horizontal
                    lang='en'
                )
            elif self.backend == "easyocr":
                if easyocr is None:
                    raise RuntimeError("easyocr not installed. Install or provide ONNX/HEF model.")
                gpu = self.device == "cuda"
                self.reader = easyocr.Reader(langs, gpu=gpu, verbose=False)
            else:
                # Placeholder for custom CRNN; for now fallback to EasyOCR if available
                if easyocr is None:
                    raise RuntimeError("CRNN backend not implemented; install easyocr or provide ONNX/HEF model.")
                gpu = self.device == "cuda"
                self.reader = easyocr.Reader(langs, gpu=gpu, verbose=False)

    def recognize(self, image_bgr: np.ndarray):
        import cv2
        crop = image_bgr
        
        if crop.size == 0:
            return "", 0.0
        
        # Hailo backend (highest priority)
        if self.use_hailo:
            return self.hailo_ocr.recognize(crop)
        
        # PaddleOCR backend (better for license plates)
        if self.paddle_ocr is not None:
            try:
                result = self.paddle_ocr.ocr(crop, cls=False)
                if result and len(result) > 0 and result[0]:
                    # PaddleOCR returns [[[bbox], (text, confidence)]]
                    texts = []
                    confidences = []
                    for line in result[0]:
                        if len(line) >= 2:
                            text, conf = line[1]
                            texts.append(text)
                            confidences.append(conf)
                    if texts:
                        full_text = ''.join(texts).strip()
                        avg_conf = sum(confidences) / len(confidences)
                        return full_text, avg_conf
            except Exception as e:
                print(f"PaddleOCR error: {e}")
            return "", 0.0
            
        # Resize for better OCR (maintain aspect ratio)
        h, w = crop.shape[:2]
        if h < 50 or w < 150:
            scale = max(50/h, 150/w)
            new_h, new_w = int(h * scale), int(w * scale)
            crop = cv2.resize(crop, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
        
        # MINIMAL PREPROCESSING - Just basic cleanup
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        
        # Simple CLAHE for contrast
        if self.apply_clahe_opt:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            gray = clahe.apply(gray)
        
        # Convert back to BGR for EasyOCR
        crop = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
        if self.ort_session is not None:
            # ONNX model processing
            img_gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            img_resized = cv2.resize(img_gray, (160, 32))
            img_normalized = img_resized.astype(np.float32) / 255.0
            img_normalized = (img_normalized - 0.5) / 0.5
            img_input = img_normalized[None, None, :, :]
            
            outputs = self.ort_session.run(None, {self.ort_session.get_inputs()[0].name: img_input})
            text = str(outputs[0][0]) if len(outputs) > 0 else ""
            conf = float(outputs[1][0]) if len(outputs) > 1 else 0.0
            return text, conf
        else:
            # Enhanced EasyOCR processing with better settings for letter detection
            # Try multiple passes with different settings to catch tricky letters like W
            results = []
            
            # Pass 1: Standard settings
            result1 = self.reader.readtext(
                crop, 
                detail=1, 
                paragraph=False, 
                contrast_ths=0.1,
                text_threshold=0.3,
                low_text=0.3,
                link_threshold=0.3,
                width_ths=0.5,
                height_ths=0.5,
                mag_ratio=1.5,
                min_size=10,
                allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            )
            if result1:
                results.extend(result1)
            
            # Pass 2: Even more lenient for catching W (which is often missed)
            result2 = self.reader.readtext(
                crop,
                detail=1,
                paragraph=False,
                contrast_ths=0.05,  # Very low for faint W
                text_threshold=0.2,  # Very low
                low_text=0.2,
                link_threshold=0.2,
                width_ths=0.3,  # Very lenient
                height_ths=0.3,
                mag_ratio=2.0,  # Scale up more
                min_size=8,  # Detect even smaller
                allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            )
            if result2:
                results.extend(result2)
            
            if not results:
                return "", 0.0
            
            # Return the best result (highest confidence)
            best = max(results, key=lambda r: r[2])
            text = best[1].strip()
            conf = float(best[2])
            
            # Only return if it looks like a license plate
            if len(text) >= 3 and conf > 0.3:
                return text, conf
            return "", 0.0


