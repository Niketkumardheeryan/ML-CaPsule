# 🩺 Chronic Kidney Disease Prediction

A Machine Learning + Deep Learning project that predicts **Chronic Kidney Disease (CKD)** using an Artificial Neural Network, achieving **98% accuracy**, and includes an interactive **Streamlit web application** for real-time predictions.

---

## 📌 Project Description

Chronic Kidney Disease (CKD) affects approximately **10% of the global population**, yet **90% of cases go undiagnosed** until advanced stages. This project builds and compares multiple ML models alongside an ANN to enable early, accurate CKD detection.

**Models implemented:**

| Model | Type |
|-------|------|
| Artificial Neural Network (ANN) | Deep Learning — **98% accuracy** |
| Extra Trees Classifier | Ensemble ML |
| Other ML classifiers | For comparison |

**Two notebooks are included:**

| Notebook | Purpose |
|----------|---------|
| `Chronic_Kidney_Disease.ipynb` | Streamlit interactive web app + ExtraTreesClassifier |
| `Chronic_kidney_disease_prediction.ipynb` | Full EDA, ANN model training and evaluation |

---

## 📂 Dataset

- **Name:** Chronic Kidney Disease Dataset
- **Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/chronic_kidney_disease) — also available on [Kaggle](https://www.kaggle.com/datasets/mansoordaku/ckdisease)
- **Authors:** L. Rubini, P. Soundarapandian, P. Eswaran (2015)
- **License:** CC BY 4.0
- **File used in code:** `kidney_disease_dataset.csv` (included in the project folder)
- **Instances:** 400 patients | **Features:** 24 + 1 target

### Key Features

| Feature | Description |
|---------|-------------|
| `age` | Age in years |
| `bp` | Blood Pressure (mm/Hg) |
| `su` | Sugar level (0–5) |
| `sc` | Serum Creatinine (mgs/dl) |
| `hemo` | Haemoglobin (gms) |
| `dm` | Diabetes Mellitus (yes/no) |
| `htn` | Hypertension (yes/no) |
| `classification` | Target — CKD / Not CKD |

> ✅ `kidney_disease_dataset.csv` is already included in the project folder — no external download needed.

---

## 🛠️ Dependencies

### For `Chronic_kidney_disease_prediction.ipynb` (EDA + ANN)

```bash
pip install pandas numpy matplotlib seaborn plotly mlxtend scikit-learn tensorflow keras
```

| Library | Version |
|---------|---------|
| `pandas` | 1.5.3 |
| `numpy` | 1.23.5 |
| `matplotlib` | 3.6.3 |
| `seaborn` | 0.12.2 |
| `plotly` | 5.13.1 |
| `mlxtend` | 0.21.0 |
| `scikit-learn` | 1.2.2 |
| `tensorflow` | 2.11.0 |

### For `Chronic_Kidney_Disease.ipynb` (Streamlit App)

```bash
pip install streamlit pandas numpy plotly scikit-learn jupyter nbconvert
```

| Library | Version |
|---------|---------|
| `streamlit` | 1.20.0 |
| `pandas` | 1.5.3 |
| `numpy` | 1.23.5 |
| `plotly` | 5.13.1 |
| `scikit-learn` | 1.2.2 |

> 💡 Check your installed versions with `pip show <library-name>`

---

## 🚀 How to Run

### Part 1 — EDA + ANN Model (Jupyter / Colab)

> ✅ Works on **Google Colab** or **local Jupyter Notebook**

**Option A — Google Colab:**
1. Open [colab.research.google.com](https://colab.research.google.com/)
2. Upload `Chronic_kidney_disease_prediction.ipynb`
3. Upload `kidney_disease_dataset.csv` to the Colab session
4. Run all cells via `Runtime` → `Run all`

**Option B — Local Jupyter:**
```bash
git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
cd "ML-CaPsule/Chronic Kidney Disease Prediction"
pip install pandas numpy matplotlib seaborn plotly mlxtend scikit-learn tensorflow keras
jupyter notebook Chronic_kidney_disease_prediction.ipynb
```

---

### Part 2 — Streamlit Web App

> ✅ Run **locally** (Streamlit does not run directly on Colab without a tunnel)

**Step 1 — Install dependencies:**
```bash
pip install streamlit pandas numpy plotly scikit-learn jupyter nbconvert
```

**Step 2 — Convert the notebook to a Python script:**
```bash
jupyter nbconvert --to script Chronic_Kidney_Disease.ipynb
```
This automatically generates `Chronic_Kidney_Disease.py`

**Step 3 — Launch the Streamlit app:**
```bash
streamlit run Chronic_Kidney_Disease.py
```

**Step 4 — Open in browser:**

The app will launch at `http://localhost:8501`

Enter medical parameters and get an instant CKD risk prediction with visualizations.

> ⚠️ Note: The Streamlit app is documented based on the imports found in the notebook. If you encounter errors after conversion, the app may require further testing.

---

## 📊 Sample Output

### Streamlit App Interface

The interactive app accepts the following inputs:

| Input | Description |
|-------|-------------|
| Age | Patient's age in years |
| Blood Pressure | In mm/Hg |
| Sugar Level | Scale 0–5 |
| Serum Creatinine | In mgs/dl |
| Haemoglobin | In gms |

And outputs:
- ✅ **CKD / Not CKD** prediction
- 📊 Graphical visualizations of dataset distributions
- 📈 Feature importance chart

### Model Performance

| Model | Accuracy |
|-------|----------|
| Artificial Neural Network | **98%** |
| Extra Trees Classifier | High (see notebook) |

---

## 📁 Project Structure

```
Chronic Kidney Disease Prediction/
├── Chronic_Kidney_Disease.ipynb            ← Streamlit app + ExtraTreesClassifier
├── Chronic_kidney_disease_prediction.ipynb ← EDA + ANN model
├── kidney_disease_dataset.csv              ← CKD dataset (400 patients, 24 features)
└── README.md
```

---

## 👤 Contributor

- README added as part of [ML-CaPsule](https://github.com/Niketkumardheeryan/ML-CaPsule) open-source contribution
