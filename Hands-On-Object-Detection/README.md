## Hands On Object Detection:
---
This directory teaches you about Object - Detection with an Hands-on Example and helps you learn and solve the problems that we deal usually building such architectures this directory also includes,A complete single-stage object detection pipeline for identifying threat objects and financial items. The project progresses from foundational bounding box regression using custom CNNs to production-ready deployment with Ultralytics YOLOv8.

Directory Structure 
---
```
.
├── Basic-Single-Stage-ObjectDetection.ipynb
│   └── Localization & single-object regression
├── YOLOv8-and-problems-in-creating-such-architectures.ipynb
│   └── Multi-object detection & YOLOv8
├── data.yaml                        # Dataset config (classes, paths)
├── requirements.txt                 # Python dependencies
│
├── weapon-detection/                # Dataset root
│   ├── train/
│   │   ├── images/
│   │   └── labels/
│   ├── val/
│   │   ├── images/
│   │   └── labels/
│   └── test/
│       ├── images/
│       └── labels/
│
└── runs/                            # Auto-generated outputs
    └── detect/
        ├── train/
        │   └── weights/             # best.pt · last.pt
        ├── train-2/
        │   └── weights/
        └── predict/                 # Inference outputs with bounding boxes

```

Dataset Configuration — weapon-detection/data.yaml
---
Detects 6 classes of items typically found in pockets or bags (nc: 6):

- 0 — pistol · Handguns / Firearms
- 1 — smartphone · Mobile Devices
- 2 — knife · Bladed Weapons
- 3 — monedero · Purse / Wallet
- 4 — billete · Banknotes / Paper Currency
- 5 — tarjeta · Credit / Debit Cards


Setup & Installation
---
Requires Python 3.10+. Clone the repository, then run this command to install dependencies:

```
pip install -r requirements.txt
```

Dependency stack:
---

- torch / torchvision — Deep learning backend
- ultralytics — YOLOv8 framework
- matplotlib / pillow — Visualization & image I/O
- tqdm / ipython — Progress tracking & interactive utilities


Architectural Concepts
---
1. Basic Single-Stage Localization
Basic-Single-Stage-ObjectDetection.ipynb
Covers the transition from image classification to bounding box regression. A standard regression head outputs four coordinates $[x_c,\ y_c,\ w,\ h]$
to localize a single primary object within an image.
2. Multi-Object Grid Discretization
YOLOv8-and-problems-in-creating-such-architectures.ipynb
Covers scaling up to handle multiple overlapping targets. The input image is discretized into an S×SS \times S
S×S grid, transforming global regression into parallelized local predictions.
For this 6-class dataset, each grid cell produces an 11-channel output tensor:

- Ch. 0 · confidence — Objectness score (0.0 – 1.0)
- Ch. 1–4 · box — Bounding box coordinates $[x_c , y_c , w , \textit{h} ]$
- Ch. 5–10 · classes — pistol · smartphone · knife · monedero · billete · tarjeta

## Dataset 

Please download the dataset from the following source to continue reading through texts 
