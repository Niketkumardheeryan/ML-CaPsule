# Weapon and Financial Items Object Detection

This repository contains a complete single-stage object detection pipeline for tracking threat objects and financial items. The project spans from foundational bounding box regression concepts using custom Convolutional Neural Networks (CNNs) to production-ready deployment with Ultralytics YOLOv8.

---

## Project Directory Structure


.
├── Basic-Single-Stage-ObjectDetection.ipynb   # Introduction to localization & single-object regression
├── YOLOv8-and-problems-in-creating-such-architectures.ipynb  # Multi-object detection grid concepts & YOLOv8
├── data.yaml                                  # Dataset configuration file (classes, paths)
├── requirements.txt                           # Python dependencies installation file
├── weapon-detection/                          # Dataset Directory
│   ├── train/                                 # Training split
│   │   ├── images/
│   │   └── labels/
│   ├── val/                                   # Validation split
│   │   ├── images/
│   │   └── labels/
│   └── test/                                  # Test split
│       ├── images/
│       └── labels/
└── runs/                                      # Automatically generated training & prediction outputs
    └── detect/
        ├── train/                             # Initial training run logs and weights
        │   └── weights/                       # Contains best.pt and last.pt
        ├── train-2/                           # Subsequent training run logs and weights
        │   └── weights/
        └── predict/                           # Inference outputs with bounding boxes drawn
        
        
## Dataset Configuration (data.yaml)
The dataset is structured to detect items typically found in pockets or bags. It contains 6 unique classes (nc: 6):

pistol (Handguns / Firearms)

smartphone (Mobile Devices)

knife (Bladed Weapons)

monedero (Purse / Wallet)

billete (Banknotes / Paper Currency)

tarjeta (Credit / Debit Cards)

## Setup & Installation
Ensure you have Python 3.10+ installed. Clone the repository, navigate to the project directory, and install the dependencies:

# Install all required libraries
pip install -r requirements.txt

Dependency Stack (requirements.txt)

torch & torchvision (Deep learning backend infrastructure)
ultralytics (YOLOv8 framework engine)
matplotlib & pillow (Visualization and image manipulation tools)
tqdm & ipython (Progress tracking and interactive utility wrappers)

Architectural Concepts Covered
1. Basic Single-Stage LocalizationLocated in Basic-Single-Stage-ObjectDetection.ipynb, this notebook guides you through the transition from traditional image classification to basic bounding box regression. It explores how a standard regression head can output coordinates $[x_c, y_c, w, h]$ to track a single primary object inside an image boundary.

2. Multi-Object Grid DiscretizationLocated in YOLOv8-and-problems-in-creating-such-architectures.ipynb, this covers how advanced models scale up to handle multiple overlapping targets. By discretizing the input image into an $S \times S$ matrix of cells, the network transforms global regression into parallelized, local target predictions.For this specific 6-class dataset, the output tensor channel layout maps out as an 11-variable structure per cell: 
Channel 0: Object Confidence (0.0 to 1.0) 
Channels 1–4: Localized Box Coordinates ($x_c, y_c, w, h$) 
Channels 5–10: Class probability mappings (pistol, smartphone, knife, monedero, billete, tarjeta)
