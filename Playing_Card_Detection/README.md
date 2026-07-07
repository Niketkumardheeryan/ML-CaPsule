# 🃏 Real-Time Playing Card Detection (YOLOv8)

## 📌 Project Overview
This project features a custom-trained **YOLOv8 Nano** object detection model capable of identifying standard playing cards in real-time through a webcam feed. It was trained on a comprehensive dataset of over 24,000 images to accurately classify cards (e.g., Ace of Spades, King of Hearts) under various lighting conditions and angles.

## 🚀 Features
- **Live Webcam Inference:** Detects cards instantly using `detect.py`.
- **High Accuracy:** Trained over 5 epochs specifically on playing card datasets.
- **Lightweight:** Uses the YOLOv8 Nano (`yolov8n.pt`) architecture for fast processing on standard hardware.

## 💻 How to Run Locally
1. Clone this repository and navigate to this folder.
2. Install the required dependencies:
   ```bash
   pip install ultralytics opencv-python