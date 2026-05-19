# Multi-Directional Car License Plate Detection using CNN and YOLO

## Overview
This project implements a YOLOv8-based car license plate detection system capable of detecting license plates under different orientations and viewing angles.

Traditional license plate detectors often fail on rotated or tilted plates. This project improves robustness using rotation-aware preprocessing and augmentation techniques.

---

## Features
- YOLOv8-based license plate detection
- Rotation-aware image augmentation
- Detection of tilted and multi-directional license plates
- Bounding box visualization
- IoU-based evaluation
- Inference notebook implementation

---

## Technologies Used
- Python
- PyTorch
- OpenCV
- YOLOv8
- NumPy
- Matplotlib

---

## Folder Structure

```text
Multi_Directional_Car_License_Plate_Detection/
│
├── README.md
├── license_plate_detection_yolo.ipynb
├── requirements.txt
└── sample_outputs/