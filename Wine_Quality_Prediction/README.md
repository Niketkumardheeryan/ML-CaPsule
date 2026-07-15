# 🍷 Wine Quality Prediction using Machine Learning

A beginner-friendly Machine Learning project that analyzes the chemical properties of red wine and predicts whether a wine is of **good quality or not**, using Exploratory Data Analysis (EDA) and a **Random Forest Classifier**.

---

## 📌 Problem Statement

Wine quality is typically determined by experts through taste tests — a slow and subjective process. This project uses chemical measurements (acidity, alcohol, pH, etc.) to **predict wine quality automatically using ML**, making the process faster and objective.

---

## 📂 Project Structure

```
Wine_Quality_Prediction/
├── wine_quality_prediction.ipynb   ← Complete notebook (run this)
└── README.md                       ← This file
```

---

## 🔄 Workflow

```
Data Download → EDA & Visualisation → Data Cleaning → Model Building → Evaluation
```

### 1. Data Collection
- Dataset auto-downloaded from the **UCI Machine Learning Repository**
- **1,599 red wine samples** with 12 features

### 2. Exploratory Data Analysis
- Quality score distribution (count plot)
- Alcohol vs pH bar plot
- Alcohol content histogram with KDE
- Residual sugar boxplot grouped by quality
- Full correlation heatmap (10×10)
- Free vs total sulphur dioxide line plot

### 3. Data Analysis
- Statistical summaries (mean, std, min, max)
- Filtering: wines with pH > 3.5 and alcohol > 10
- Grouping by quality — mean & median of all features
- Mean citric acid: **0.27**
- Highest alcohol content wine: **14.9% — Quality score 5**

### 4. Data Cleaning
- Checked null values in `citric acid` column → **0 nulls found**
- Filled nulls with median (defensive step)
- Removed rows with null `residual sugar` values

### 5. Model Building
- Target: binarized quality → **Good (1)** if score ≥ 7, else **Bad (0)**
- Train/Test split: **1279 training / 320 test samples**
- Model: `RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=5)`

---

## 📊 Dataset Features

| Feature | Description |
|---|---|
| Fixed acidity | Tartaric acid concentration |
| Volatile acidity | Acetic acid — too high gives vinegar taste |
| Citric acid | Adds freshness and flavour |
| Residual sugar | Sugar remaining after fermentation |
| Chlorides | Salt content in wine |
| Free sulfur dioxide | Prevents microbial growth |
| Total sulfur dioxide | Free + bound SO₂ |
| Density | Depends on alcohol and sugar content |
| pH | Acidity level (0–14 scale) |
| Sulphates | Additive boosting SO₂ levels |
| Alcohol | % alcohol by volume |
| **Quality** | **Target variable — score 3 to 8** |

---

## 📈 Results

| Metric | Value |
|---|---|
| Training Accuracy | **0.94** |
| Test Accuracy | **0.92** |
| Precision (Good wine) | 0.72 |
| Recall (Good wine) | 0.49 |
| F1-Score (Good wine) | 0.58 |
| Overall F1 (weighted) | 0.91 |

> `max_depth=10` and `min_samples_leaf=5` were used to prevent overfitting.

---

## 🛠️ Technologies Used

| Library | Purpose |
|---|---|
| `pandas` | Data loading and manipulation |
| `numpy` | Numerical operations |
| `matplotlib` | Plotting charts |
| `seaborn` | Statistical visualisations |
| `scikit-learn` | ML model, train/test split, evaluation |

---

## ⚙️ How to Run

**1. Clone the repository**
```bash
git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
cd ML-CaPsule/Wine_Quality_Prediction
```

**2. Install dependencies**
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

**3. Open and run the notebook**
```bash
jupyter notebook wine_quality_prediction.ipynb
```

> The dataset is **auto-downloaded** from UCI — no manual download needed.  
> Run all cells: **Kernel → Restart & Run All**

---

## 🔗 Dataset

[UCI Wine Quality Dataset](https://archive.ics.uci.edu/ml/datasets/wine+quality) — Red wine variants from the Minho region of Portugal.  
**Citation:** P. Cortez et al., 2009.

---

## 👤 Author

**Siddharth** — [GitHub @siddharth277](https://github.com/siddharth277)  
Contributed as part of **GSSoC 2026**
