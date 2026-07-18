# Dog vs Cat Classification using CNN and Streamlit

A beginner-friendly Deep Learning project that classifies images as **Dog** or **Cat** using a custom Convolutional Neural Network (CNN) built from scratch, with an interactive **Streamlit web app** for real-time predictions.

---

##  Project Structure

```
Dog_vs_Cat_CNN_Streamlit/
├── dog-vs-cat.ipynb           ← Complete training notebook (run this first)
├── app.py                      ← Streamlit web application
├── requirements.txt            ← Python dependencies
└── README.md                   ← This file
```

> After running the notebook, these files are auto-generated:
> `dog_vs_cat_model.keras`, `sample_predictions.png`, `training_history.png`, `confusion_matrix.png`

---

## 🔄 Complete Workflow

```
Dataset Download (kagglehub) → EDA → Augmentation → CNN Training → Evaluation → Streamlit App
```

---

##  Dataset

- **Source:** [Microsoft Cats vs Dogs — Kaggle](https://www.kaggle.com/datasets/shaunthesheep/microsoft-catsvsdogs-dataset)
- **Downloaded via:** `kagglehub` (auto-download in notebook)
- **Training set:** 8,000 dogs + 8,000 cats = **16,000 images**
- **Test set:** 2,000 dogs + 2,000 cats = **4,000 images**
- Corrupted images are automatically filtered before training

---

##  Exploratory Data Analysis

- 10 sample training images (5 dogs + 5 cats)
- Class distribution bar charts (train + test)
- Augmented image preview (8 samples)

---

##  Data Augmentation

| Technique | Value |
|---|---|
| Rescale | 1/255 |
| Rotation range | ±20° |
| Width / Height shift | 20% |
| Shear range | 20% |
| Zoom range | 20% |
| Horizontal flip | Yes |
| Fill mode | Nearest |

---

##  CNN Architecture (Custom — 3 Blocks)

```
Input (150 × 150 × 3)
        ↓
Block 1: Conv2D(32) → BatchNorm → Conv2D(32) → MaxPool(2×2) → Dropout(0.25)
        ↓
Block 2: Conv2D(64) → BatchNorm → Conv2D(64) → MaxPool(2×2) → Dropout(0.25)
        ↓
Block 3: Conv2D(128) → BatchNorm → Conv2D(128) → MaxPool(2×2) → Dropout(0.25)
        ↓
Flatten → Dense(512) → BatchNorm → Dropout(0.5)
        ↓
Dense(1, sigmoid) → Dog (1) or Cat (0)
```

**Total parameters:** 21,524,641 (82.11 MB)

---

##  Training Configuration

| Parameter | Value |
|---|---|
| Optimizer | Adam |
| Loss | Binary Crossentropy |
| Max Epochs | 20 |
| Early Stopping | patience = 5 (monitors val_accuracy) |
| Batch Size | 32 |
| Image Size | 150 × 150 |
| GPU | Tesla T4 (2× GPUs) |

### Epoch Progress

| Epoch | Train Accuracy | Val Accuracy |
|---|---|---|
| 1 | 56.93% | 60.65% |
| 2 | 66.76% | 71.13% |
| 3 | 72.16% | 73.18% |
| 5 | 76.15% | 82.20% ✅ best checkpoint |
| ... | ... | ... |
| Final | — | **91.53%** |

---

##  Results

| Metric | Value |
|---|---|
| **Test Accuracy** | **91.53%** |
| **Test Loss** | **0.2055** |

### Classification Report

| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Cat | 0.92 | 0.91 | 0.91 | 2,000 |
| Dog | 0.91 | 0.92 | 0.92 | 2,000 |
| **Weighted Avg** | **0.92** | **0.92** | **0.92** | **4,000** |

---


##  How to Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Get Kaggle API key
- Go to `kaggle.com` → Profile → Settings → **Create New Token**
- This downloads `kaggle.json` — place it in `~/.kaggle/kaggle.json`

### Step 3 — Train the model
```bash
jupyter notebook dog-vs-cat.ipynb
```
Run all cells. The notebook auto-downloads the dataset via `kagglehub`, restructures it, trains the CNN, and saves `dog_vs_cat_model.keras`.

### Step 4 — Launch the Streamlit app
```bash
streamlit run app.py
```
Opens at `http://localhost:8501` 🚀

---

## 🛠️ Technologies Used

| Library | Purpose |
|---|---|
| `TensorFlow 2.19 / Keras` | CNN model building and training |
| `kagglehub` | Auto-download dataset from Kaggle |
| `NumPy` | Array operations |
| `Matplotlib / Seaborn` | Training history, confusion matrix |
| `Scikit-learn` | Classification report, confusion matrix |
| `Streamlit` | Interactive web application |
| `Pillow` | Image loading and preprocessing |

---


##  Dataset

[Microsoft Cats vs Dogs on Kaggle](https://www.kaggle.com/datasets/shaunthesheep/microsoft-catsvsdogs-dataset)

---

##  Author

**Siddharth** — [GitHub @siddharth277](https://github.com/siddharth277)
Contributed as part of **GSSoC 2026**

