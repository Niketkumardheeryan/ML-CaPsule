# Pothole-Detection-YOLOv8

## Dataset
- Source: Pothole Detection Dataset by andrewmvd (Kaggle), License: CC BY 4.0
- The notebook downloads the dataset as `pothole_dataset.zip` via `gdown`:
- Link: https://drive.google.com/file/d/1HDxVke5roWa5BETF_RtUAgK82lLvOoSM/view?usp=sharing

This project fine-tunes a **YOLOv8n** (nano) model on a labeled pothole detection dataset to identify road defects in images. The dataset contains 665 annotated road images in Pascal VOC format, which the notebook automatically converts to YOLOv8 format. The goal is to support road safety monitoring, especially relevant to the Indian road infrastructure context.

## Key Features
1. Dataset download via `gdown` (no API key required)
2. Automatic Pascal VOC to YOLOv8 format conversion
3. 80/10/10 train/val/test split with reproducible random seed
4. Exploratory Data Analysis — sample images with ground truth bounding boxes and split distribution chart
5. YOLOv8n fine-tuning using Ultralytics (30 epochs, imgsz=640)
6. Evaluation with mAP@50, Precision, and Recall metrics
7. Training and validation loss curve visualization
8. Bounding box inference on test images
9. Optional dashcam video inference block

## Tech Stack
- Python
- Ultralytics YOLOv8
- OpenCV
- Matplotlib (visualization)
- gdown (dataset download)
- Google Colab (recommended runtime with T4 GPU)

## Usage
1. Open `Pothole_Detection_YOLOv8.ipynb` in Google Colab.
2. Set runtime to GPU: Runtime → Change runtime type → T4 GPU.
3. Run all cells — `gdown` will automatically download and extract the dataset.
4. Review EDA plots, training curves, evaluation metrics, and test image predictions.
