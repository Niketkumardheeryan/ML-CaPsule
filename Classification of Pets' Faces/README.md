# 🐱🐶 Cat vs Dog Classifier

A modern, lightweight web application for classifying pet images as **cats** or **dogs** using MobileNetV2 transfer learning. Built with TensorFlow and Streamlit.

---

## ✨ Features

- **🎯 Accurate Classification** — MobileNetV2 transfer learning on 25,000+ Kaggle cat/dog images
- **🖥️ Modern Web UI** — Clean, responsive Streamlit interface with dark/light mode support
- **📊 Confidence Visualization** — Real-time probability bars and confidence scores
- **🖼️ Sample Images** — Built-in test images for quick demos
- **⚡ Fast Inference** — Optimized MobileNetV2 model (~9.6 MB)
- **🔧 Easy Training** — Reproducible training script with corrupt image handling

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd "Classification of Pets' Faces"

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Web App

```bash
# Option 1: Direct Streamlit
streamlit run app.py

# Option 2: Using the entry point
python main.py
```

The app will open at `http://localhost:8501`

---

## 🏗️ Project Structure

```
Classification of Pets' Faces/
├── app.py                 # Streamlit web application
├── train_model.py         # Training script (MobileNetV2 transfer learning)
├── main.py                # Entry point to launch the app
├── requirements.txt       # Python dependencies
├── pet_classifier.keras   # Trained model (9.6 MB)
├── class_names.json       # Class labels ["Cat", "Dog"]
├── .gitignore
├── .venv/                 # Virtual environment (ignored)
└── kagglecatsanddogs_3367a/
    └── PetImages/         # Training dataset (Cat/ and Dog/ folders)
```

---

## 🧠 Model Details

| Property | Value |
|----------|-------|
| **Architecture** | MobileNetV2 (ImageNet pre-trained) |
| **Input Size** | 160 × 160 × 3 |
| **Classes** | 2 (Cat, Dog) |
| **Training Data** | ~25,000 images (Kaggle Cats vs Dogs) |
| **Validation Split** | 20% |
| **Epochs** | 5 (with early stopping) |
| **Optimizer** | Adam (lr=1e-3) |
| **Loss** | Sparse Categorical Crossentropy |
| **Model Size** | ~9.6 MB |
| **Framework** | TensorFlow/Keras |

### Training Pipeline

1. **Data Cleaning** — Removes corrupt/unreadable images
2. **Data Loading** — `tf.keras.utils.image_dataset_from_directory` with 80/20 split
3. **Preprocessing** — MobileNetV2-specific normalization
4. **Transfer Learning** — Frozen MobileNetV2 backbone + custom classification head
5. **Training** — Early stopping on validation accuracy
6. **Fallback** — PIL-based loader for corrupt images

---

## 📦 Dependencies

```txt
streamlit>=1.28.0
tensorflow>=2.13.0
numpy>=1.24.0
pillow>=10.0.0
```

---

## 🎨 UI Highlights

- **Responsive Design** — Works on desktop and mobile
- **Dark/Light Mode** — Automatic via CSS `prefers-color-scheme`
- **Visual Feedback** — Color-coded results (🐱 orange / 🐶 blue)
- **Probability Bars** — Per-class confidence breakdown
- **Sample Buttons** — One-click demo with built-in images

---

## 🔧 Retraining the Model

To retrain with different hyperparameters or more epochs:

```bash
python train_model.py
```

Key configurable parameters in `train_model.py`:

```python
IMG_SIZE = (160, 160)      # Input resolution
BATCH_SIZE = 64            # Batch size
EPOCHS = 5                 # Max epochs (early stopping may stop earlier)
```

The script will:
1. Clean corrupt images from `kagglecatsanddogs_3367a/PetImages/Cat` and `Dog`
2. Load and preprocess the dataset
3. Build the MobileNetV2 transfer learning model
4. Train with early stopping (patience=2)
5. Save `pet_classifier.keras` and `class_names.json`

---

## 📊 Expected Performance

| Metric | Typical Value |
|--------|---------------|
| Training Accuracy | ~98%+ |
| Validation Accuracy | ~96-98% |
| Inference Time | ~50-100ms per image |

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Model not found` | Run `python train_model.py` first |
| `ModuleNotFoundError` | Activate venv and `pip install -r requirements.txt` |
| Corrupt image errors | Training script auto-handles; check console output |
| Slow inference | Ensure TensorFlow uses GPU if available |

---

## 📄 License

This project is part of an **AI & ML Internship Project**. The dataset is from [Kaggle Cats vs Dogs](https://www.kaggle.com/datasets/tongpython/cat-and-dog).

---

## 🙏 Acknowledgments

- **MobileNetV2** — Google Research
- **Kaggle Cats vs Dogs Dataset** — Microsoft Research / Kaggle
- **Streamlit** — For the beautiful web framework
- **TensorFlow/Keras** — For the ML framework

---

## 📬 Contact

Built with ❤️ for learning and demonstration purposes.