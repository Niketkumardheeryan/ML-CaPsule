# 🤟 Real-Time Sign Language to Speech Translation

> **Accessibility-focused AI** — Transformer-based gesture recognition that converts ASL hand signs into text and speech in real time using MediaPipe + PyTorch.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1%2B-EE4C2C)](https://pytorch.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10%2B-green)](https://mediapipe.dev)
[![Gradio](https://img.shields.io/badge/Gradio-4.x-orange)](https://gradio.app)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Quick Start](#quick-start)
- [Dataset Setup](#dataset-setup)
- [Training](#training)
- [Inference](#inference)
- [Web Interface](#web-interface)
- [Model Details](#model-details)
- [Results](#results)
- [Contributing](#contributing)

---

## Overview

This project implements an end-to-end pipeline for converting American Sign Language (ASL) hand gestures into readable text and synthesised speech. The system is designed for accessibility and real-world deployment, supporting both single-frame alphabet recognition and temporal sequence modelling for word-level prediction.

```
Webcam → MediaPipe Landmarks → Transformer Encoder → Text → TTS → 🔊 Speech
```

---

## Architecture

```
Input Frame (640×480)
       │
       ▼
┌──────────────────┐
│   MediaPipe      │  21 hand landmarks (x, y, z)
│   Hands Model   │  → normalised 63-D feature vector
└──────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│   SignLanguageTransformer            │
│                                      │
│  Input projection  (63 → 128)        │
│  [CLS] token prepend                 │
│  Positional encoding                 │
│  ┌────────────────────────────────┐  │
│  │ TransformerEncoderLayer × 4    │  │
│  │   Multi-Head Self-Attention    │  │
│  │   (8 heads, d_model=128)       │  │
│  │   Feed-Forward  (128 → 512)    │  │
│  │   Pre-LayerNorm + GELU         │  │
│  └────────────────────────────────┘  │
│  CLS token → Classifier head         │
│  (128 → 64 → num_classes)            │
└──────────────────────────────────────┘
       │
       ▼
Predicted Label  +  Confidence Score
       │
       ▼
┌──────────────┐    ┌───────────────┐
│ Sentence     │    │  gTTS / pyttsx│
│ Accumulator  │───▶│  Speech Output│
└──────────────┘    └───────────────┘
```

---

## Features

| Feature | Status |
|---|---|
| Real-time webcam gesture detection | ✅ |
| MediaPipe 21-landmark extraction | ✅ |
| Transformer-based sequence modelling | ✅ |
| Single-frame alphabet recognition | ✅ |
| Temporal sequence word recognition | ✅ |
| Text-to-speech (gTTS + pyttsx3) | ✅ |
| Gradio web interface | ✅ |
| Attention visualisation heatmap | ✅ |
| Training metrics dashboard | ✅ |
| Mixed-precision training (AMP) | ✅ |
| Early stopping + cosine LR schedule | ✅ |
| Data augmentation (noise + rotation) | ✅ |
| Multi-language TTS output | 🔜 |
| Sentence-level CTC decoding | 🔜 |

---

## Repository Structure

```
Sign_Language_To_Speech/
│
├── README.md                    # This file
├── requirements.txt             # Python dependencies
│
├── dataset/                     # Raw and processed data (not committed)
│   ├── asl_alphabet_train/      # Kaggle ASL alphabet images
│   └── features.csv             # Extracted landmark features (generated)
│
├── notebooks/
│   ├── 01_eda.ipynb             # Exploratory data analysis
│   ├── 02_landmark_viz.ipynb    # MediaPipe landmark visualisation
│   └── 03_attention_viz.ipynb   # Transformer attention analysis
│
├── src/
│   ├── preprocessing.py         # Landmark extraction + dataset building
│   ├── train.py                 # Model definition + training loop
│   ├── inference.py             # Real-time webcam inference + TTS
│   └── app.py                   # Gradio web application
│
├── models/                      # Saved checkpoints (generated)
│   ├── best_model.pt
│   ├── label_encoder.json
│   └── history.json
│
└── results/                     # Evaluation outputs
    ├── classification_report.txt
    ├── confusion_matrix.png
    └── training_history.png
```

---

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/YourOrg/Sign_Language_To_Speech.git
cd Sign_Language_To_Speech
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Download dataset

```bash
# Option A — Kaggle ASL Alphabet (recommended, 87k images, 29 classes)
kaggle datasets download -d grassknoted/asl-alphabet
unzip asl-alphabet.zip -d dataset/

# Option B — Direct download via script
python -c "
import kaggle
kaggle.api.dataset_download_files('grassknoted/asl-alphabet', path='dataset/', unzip=True)
"
```

### 3. Preprocess

```bash
python src/preprocessing.py \
    --dataset_root dataset/asl_alphabet_train/asl_alphabet_train \
    --output dataset/features.csv
```

### 4. Train

```bash
python src/train.py \
    --data       dataset/features.csv \
    --model_dir  models/ \
    --epochs     80 \
    --d_model    128 \
    --nhead      8 \
    --num_layers 4
```

### 5. Launch the app

```bash
python src/app.py
# Open http://localhost:7860
```

### 6. Real-time webcam (headless)

```bash
python src/inference.py --camera 0 --threshold 0.80
# Press Q to quit | SPACE to speak sentence | C to clear
```

---

## Dataset Setup

### Recommended datasets

| Dataset | Classes | Size | Link |
|---|---|---|---|
| ASL Alphabet (Kaggle) | 29 | 87,000 images | [Link](https://www.kaggle.com/datasets/grassknoted/asl-alphabet) |
| Sign Language MNIST | 24 | 34,627 images | [Link](https://www.kaggle.com/datasets/datamunge/sign-language-mnist) |
| ASL Dataset (Kaggle) | 36 | 1,728 images | [Link](https://www.kaggle.com/datasets/ayuraj/asl-dataset) |

### Custom dataset

Organise images in class subdirectories:

```
my_dataset/
├── A/
│   ├── img_001.jpg
│   └── ...
├── B/
│   └── ...
└── hello/
    └── ...
```

Then run preprocessing as above with `--dataset_root my_dataset`.

---

## Training

### Key hyperparameters

| Parameter | Default | Description |
|---|---|---|
| `--d_model` | 128 | Transformer embedding dimension |
| `--nhead` | 8 | Number of attention heads |
| `--num_layers` | 4 | Number of encoder layers |
| `--dropout` | 0.1 | Dropout rate |
| `--lr` | 1e-3 | Initial learning rate |
| `--batch_size` | 64 | Training batch size |
| `--seq_len` | None | Sequence length (None = single-frame mode) |
| `--epochs` | 100 | Maximum training epochs |
| `--patience` | 10 | Early stopping patience |

### Example: temporal sequence training

```bash
# First, build sequence dataset from video
python src/preprocessing.py --dataset_root dataset/videos/ --output dataset/sequences.csv

# Train in sequence mode (30 frames per sign)
python src/train.py --data dataset/sequences.csv --seq_len 30 --num_layers 6
```

---

## Inference

### Options

```
--model          Path to checkpoint (default: models/best_model.pt)
--label_encoder  Path to label_encoder.json
--threshold      Minimum confidence to accept prediction (default: 0.80)
--seq_len        Sequence length (must match training; None = single-frame)
--camera         Webcam index (default: 0)
--image          Path to image for offline single-image inference
```

### Single image

```bash
python src/inference.py --image my_sign.jpg
# {"label": "A", "confidence": 0.9423}
```

---

## Web Interface

The Gradio app exposes four tabs:

- **Image Upload** — drag-and-drop any hand-sign image; get the predicted label, confidence, landmark overlay, and attention heatmap
- **Live Webcam** — stream directly from your camera with real-time landmark overlay and sentence accumulation
- **Model Metrics** — training loss/accuracy curves rendered from `models/history.json`
- **About** — pipeline explanation and usage instructions

---

## Model Details

### Parameter count

| Config | Parameters |
|---|---|
| d_model=64,  layers=2 | ~120k |
| d_model=128, layers=4 | ~460k |
| d_model=256, layers=6 | ~1.8M |

The default 128/4 configuration achieves strong accuracy with a very small footprint, making it suitable for CPU-only inference.

### Landmark normalisation

MediaPipe outputs landmark coordinates in image-relative space (0–1). We apply:
1. **Translation**: subtract wrist (landmark 0) so the hand is origin-centred
2. **Scale**: divide by the wrist–middle-MCP distance, making the representation invariant to hand size and camera distance

### Smoothing

A rolling window of 5 consecutive identical predictions is required before a sign is accepted, eliminating transient flicker from partial gestures.

---

## Results

Expected performance on the ASL Alphabet Kaggle dataset (29 classes):

| Metric | Value |
|---|---|
| Validation accuracy | ~97–99% |
| Inference speed (CPU) | ~25–30 FPS |
| Inference speed (GPU) | ~60 FPS |
| Model size | ~1.8 MB |

Detailed per-class results are written to `results/classification_report.txt` after evaluation.

---

## Contributing

Contributions are welcome under the GSSoC / open-source contribution guidelines.

### Good first issues

- Add multi-language TTS output (Hindi, Spanish, French)
- Implement CTC decoding for sentence-level prediction
- Add model quantisation for mobile deployment
- Collect and annotate a custom word-level gesture dataset
- Write unit tests for `preprocessing.py`

### Pull request checklist

- [ ] Code follows PEP 8 and is type-annotated
- [ ] New modules have docstrings
- [ ] Changes are tested locally
- [ ] `requirements.txt` is updated if new dependencies are added

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

*Made with ❤️ for accessibility. Sign language is a rich, complete language — this tool aims to bridge communication gaps, not replace the language itself.*
