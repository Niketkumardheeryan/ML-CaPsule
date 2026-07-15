# ANPR-India: Real-time Automatic Number Plate Recognition (Indian plates)

This repository provides a complete real-time ANPR system optimized for Indian number plates. It uses YOLOv8 for plate detection and a fast OCR backend, with a threaded OpenCV pipeline for real-time inference from webcams or network streams. It supports GPU acceleration (CUDA) and ONNX Runtime inference.

## Features
- **YOLOv8 plate detector** (PyTorch) with optional ONNX Runtime inference
- **OCR recognizer** via EasyOCR (PyTorch) or custom CRNN+CTC (optional) with ONNX fallback
- **Real-time pipeline**: threaded capture → detect+OCR → display with FPS overlay
- **Indian plate rules**: regex validation, normalization, confusion correction (O↔0, I↔1, B↔8, S↔5)
- **Logging**: CSV and JSONL logging of recognized plates
- **FastAPI server**: for HTTP frame inference
- **Synthetic data**: Generator for Indian plate training data

## Repo Tree
```
models/
datasets/
src/
  detector.py
  recognizer.py
  postprocess.py
  video_infer.py
  fastapi_server.py
configs/config.yaml
tools/export_to_onnx.py
tools/generate_synthetic_plates.py
logs/
notebooks/demo.ipynb
README.md
```

## Installation

1. **Python 3.9+ recommended**. Create a venv:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   # Or install manually:
   # pip install ultralytics onnxruntime-gpu onnx opencv-python easyocr pyyaml fastapi uvicorn numpy pillow
   ```

3. **Install PyTorch**:
   Ensure you have PyTorch installed compatible with your CUDA version (for GPU support).
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

## Configuration

Edit `configs/config.yaml` to customize the system:
- **Model paths**: detection and OCR model weights
- **Input source**: camera index, file path, or RTSP URL
- **Output mode**: overlay, json, or both
- **Database**: CSV file paths for validation

## Database Integration

The system uses CSV files for checking authorized vehicles, but you can easily integrate your own database (SQL, NoSQL, etc.).

- **Default Behavior**: The system looks for `logs/parking_database.csv` (not included) to validate plates.
- **Testing**: If you just want to test the ANPR detection, you can run the system without any database file. The logs will simply show the detected plates in the terminal.
- **Customization**: To use your own database, modify `src/postprocess.py` to connect to your data source instead of loading the CSV.

## Real-time Inference

Optimized for speed and accuracy.

**Single Camera:**
```bash
python -m src.video_infer --source 0 --conf 0.4 --skip 2 --mode both
```

**Multi-Camera Mode:**
Enable `multi_camera: true` in `configs/config.yaml` and run:
```bash
python -m src.multi_camera_infer
```

**Other examples:**
```bash
# Video file
python -m src.video_infer --source path/to/video.mp4 --conf 0.4 --skip 2

# RTSP stream
python -m src.video_infer --source rtsp://user:pass@host/stream --conf 0.4

# JSON only (no display)
python -m src.video_infer --source 0 --mode json
```

## Models
- **Detector**: Default uses a YOLOv8 plate model path set in `configs/config.yaml`.
- **Recognizer**: Default uses EasyOCR. For best performance, train a plate-focused CRNN and point config to it.
- **Export to ONNX**:
  ```bash
  python tools/export_to_onnx.py --detector models/plate_yolov8.pt --ocr models/ocr_crnn.pt
  ```

## Indian Plate Rules
- **Normalization**: uppercase, remove spaces/dashes
- **Confusion correction**: O↔0, I↔1, B↔8, S↔5 (context-aware)
- **Regex validation**: See `src/postprocess.py` for full patterns (e.g., `^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$`).

## Training (High-level)
1. **Detector (YOLOv8)**:
   - Prepare dataset in YOLO format.
   - Train: `yolo detect train data=data.yaml model=yolov8n.pt imgsz=640 epochs=100`
2. **Recognizer (CRNN)**:
   - Prepare cropped plate images.
   - Train recognizer and update `config.yaml`.

## FastAPI Server
Run the HTTP API for single-frame inference:
```bash
uvicorn src.fastapi_server:app --host 0.0.0.0 --port 8000
```
POST `/infer` with `multipart/form-data` field `image`.

## Synthetic Data
Generate sample Indian license plates:
```bash
python tools/generate_synthetic_plates.py --out datasets/samples --num 10
```

## License
MIT License
