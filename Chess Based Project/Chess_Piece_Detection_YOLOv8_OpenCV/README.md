# Chess Piece Detection and Classification using YOLOv8 and OpenCV

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/Ultralytics-YOLOv8-orange?logo=pytorch)](https://docs.ultralytics.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green?logo=opencv)](https://opencv.org/)
[![Roboflow](https://img.shields.io/badge/Dataset-Roboflow-purple)](https://universe.roboflow.com/chess-pieces-nemtd/chess-pieces-detection)

> A complete end-to-end Jupyter notebook for detecting and classifying chess pieces from board images using YOLOv8 and OpenCV.

---

## Project Overview

This project trains a YOLOv8 object detection model to recognize 12 chess piece classes (white/black x king, queen, rook, bishop, knight, pawn) from board images in a single pass.

### Why YOLO?

| Approach | Pros | Cons |
|---|---|---|
| YOLOv8 (this project) | Single-pass detection + classification, fast, accurate | Needs GPU for fast training |
| CNN on cropped pieces | Simple classifier | Needs separate detector; two-stage pipeline |
| Template matching / HOG | No training needed | Fails on varied angles and lighting |

---

## Results

Run chess_piece_detection_yolo.ipynb end-to-end to generate result images. The notebook automatically saves the following to the results/ folder:

| Output file | Contents |
|---|---|
| batch_inference.png | 6-image grid with annotated bounding boxes |
| training_curves.png | Loss and mAP curves over epochs |
| per_class_metrics.png | Per-class AP@50 and AP@50-95 bar charts |
| confusion_matrix_display.png | Validation confusion matrix |
| detection_statistics.png | Piece count and confidence score distribution |

---

## Repository Structure

Chess_Piece_Detection_YOLOv8_OpenCV/
- chess_piece_detection_yolo.ipynb (main notebook, all steps)
- requirements.txt (Python dependencies)
- README.md (this file)

---

## Classes Detected

| ID | Class | Color |
|----|-------|-------|
| 0-5 | king, queen, rook, bishop, knight, pawn | White |
| 6-11 | king, queen, rook, bishop, knight, pawn | Black |

(Exact class IDs depend on the Roboflow dataset version.)

---

## Getting Started

### 1. Prerequisites

- Python 3.8+
- A GPU is strongly recommended for training (or use Google Colab)
- A free Roboflow API key (app.roboflow.com)

### 2. Installation
git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
cd "ML-CaPsule/Chess Based Project/Chess_Piece_Detection_YOLOv8_OpenCV"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
### 3. Get Your Roboflow API Key

1. Sign up for free at app.roboflow.com
2. Go to Settings then API Keys
3. Copy your key

### 4. Run the Notebook
jupyter notebook chess_piece_detection_yolo.ipynb

Open the notebook and paste your Roboflow API key into the ROBOFLOW_API_KEY variable in Section 2, then run all cells top to bottom.

---

## Notebook Walkthrough

| Section | Description |
|---------|-------------|
| 1. Dependencies | Import libraries, check GPU availability |
| 2. Dataset Download | Pull chess dataset from Roboflow in YOLOv8 format |
| 3. Model Training | Fine-tune yolov8n.pt with configurable epochs, batch size |
| 4. Evaluation | Compute mAP50, mAP50-95, precision, recall |
| 5. Inference & Visualization | Run detection on test images with bounding boxes |
| 6. Export | Export trained model to ONNX for deployment |
| 7. Summary | Results table, improvement ideas, references |

---

## Configuration

MODEL_WEIGHTS = yolov8n.pt
EPOCHS = 50
IMG_SIZE = 640
BATCH_SIZE = 16

---

## Dataset

- Source: Roboflow Universe - Chess Pieces Detection
- Format: YOLOv8 (images + YOLO label .txt files + data.yaml)
- License: Public, free download via Roboflow API
- Splits: Train / Validation / Test

---

## Possible Extensions

- Real-time webcam detection
- FEN string generation
- Mobile deployment (TFLite / CoreML)
- Game analysis with a chess engine
- More epochs and larger model for higher mAP

---

## References

- Ultralytics YOLOv8 Documentation: https://docs.ultralytics.com
- Roboflow Chess Dataset: https://universe.roboflow.com/chess-pieces-nemtd/chess-pieces-detection
- OpenCV Documentation: https://docs.opencv.org/4.x/
- GSSoC ML-CaPsule Issue 1501
