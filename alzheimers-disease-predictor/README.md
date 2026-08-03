# 🧠 Alzheimer's Disease Predictor

A Deep Learning CNN model that classifies Alzheimer's Disease stages from brain CT scan images, achieving **99.46% training accuracy** and **99.36% test accuracy**.

---

## 📌 Project Description

This project uses a Convolutional Neural Network (CNN) trained on brain CT scan images to classify Alzheimer's Disease into **5 stages**:

| Class | Description |
|-------|-------------|
| **AD** | Alzheimer's Disease |
| **CN** | Cognitively Normal |
| **EMCI** | Early Mild Cognitive Impairment |
| **LMCI** | Late Mild Cognitive Impairment |
| **MCI** | Mild Cognitive Impairment |

The model is neither overfit nor underfit, making it reliable for real-world CT scan classification.

---

## 📂 Dataset

- **Source:** [ADNI – Alzheimer's Disease Neuroimaging Initiative](https://adni.loni.usc.edu/)
- **Format:** JPEG brain CT scan images, organized by class
- **Actual folder structure used in the code:**

```
Alzheimers-ADNI/
└── train/
    └── Final AD JPEG/
        ├── AD (1).jpg
        ├── AD (2).jpg
        └── ...
```

> ⚠️ ADNI data requires free registration at [adni.loni.usc.edu](https://adni.loni.usc.edu/) to download.

---

## 🛠️ Dependencies

This project runs on **Google Colab**. The following libraries are used:

```python
tensorflow
keras
numpy
matplotlib
scikit-learn
opencv-python
```

No local installation is needed — Google Colab has most of these pre-installed.

---

## 🚀 How to Run

> ✅ This project is designed to run on **Google Colab**, not locally.

1. **Open Google Colab:** [colab.research.google.com](https://colab.research.google.com/)

2. **Upload the notebook:**
   - Click `File` → `Upload notebook`
   - Select `Alzheimer_Disease_predictor.ipynb`

3. **Upload the dataset:**
   - Upload the `Alzheimers-ADNI/` folder to your Google Drive
   - Or directly upload to Colab's `/content/` directory

4. **Make sure the path matches** what the code expects:
   ```
   /content/Alzheimer-Disease-Prediction/Alzheimers-ADNI/train/Final AD JPEG/
   ```

5. **Run all cells** using `Runtime` → `Run all`

---

## 📊 Sample Output

### Brain Scan Samples by Class

| AD | CN | EMCI |
|----|----|------|
| ![AD](https://github.com/srajan-kiyotaka/Alzheimer-Disease-Prediction/blob/master/Images/AD.png?raw=true) | ![CN](https://github.com/srajan-kiyotaka/Alzheimer-Disease-Prediction/blob/master/Images/CN.png?raw=true) | ![EMCI](https://github.com/srajan-kiyotaka/Alzheimer-Disease-Prediction/blob/master/Images/EMCI.png?raw=true) |

| LMCI | MCI |
|------|-----|
| ![LMCI](https://github.com/srajan-kiyotaka/Alzheimer-Disease-Prediction/blob/master/Images/LMCI.png?raw=true) | ![MCI](https://github.com/srajan-kiyotaka/Alzheimer-Disease-Prediction/blob/master/Images/MCI.png?raw=true) |

### Model Architecture

![Model Architecture](https://github.com/srajan-kiyotaka/Alzheimer-Disease-Prediction/blob/master/Images/Model.png?raw=true)

### Model Performance

| Metric | Value |
|--------|-------|
| Training Accuracy | **99.46%** |
| Test Accuracy | **99.36%** |
| Overfitting | ❌ None |

---

## 📁 Project Structure

```
Alzheimer's Disease Predictor/
├── Alzheimers-ADNI/
│   └── train/
│       └── Final AD JPEG/     ← Dataset images (AD (1).jpg, AD (2).jpg ...)
├── Images/                    ← Sample brain scan images
├── Alzheimer_Disease_predictor.ipynb  ← Main Colab notebook
├── Alzheimers-Disease.zip             ← Compressed dataset/model
└── README.md
```

---

## 👤 Contributor

- Original model by [Srajan](https://github.com/srajan-kiyotaka)
- README added as part of [ML-CaPsule](https://github.com/Niketkumardheeryan/ML-CaPsule) open-source contribution
