# 🔴 Mars Weather Prediction

> Predicting atmospheric conditions on Mars using NASA Curiosity Rover data and Machine Learning.

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://www.python.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.x-orange?logo=scikit-learn)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.x-green)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)
[![GSSoC](https://img.shields.io/badge/GSSoC-2026-red)](https://gssoc.girlscript.tech/)

---

## 📌 Project Overview

This project analyses the [NASA Mars Curiosity Rover weather dataset](https://www.kaggle.com/datasets/imkrkannan/mars-weather-data) to understand and predict Martian atmospheric conditions using supervised Machine Learning.

**Targets predicted:**
- 🌡️ Minimum daily temperature (°C)
- 🌡️ Maximum daily temperature (°C)
- 🔵 Atmospheric pressure (Pa)

---

## 📂 Dataset

| Field | Details |
|-------|---------|
| **Source** | Kaggle – [imkrkannan/mars-weather-data](https://www.kaggle.com/datasets/imkrkannan/mars-weather-data) |
| **Rows** | ~1,895 daily observations |
| **Date range** | November 2012 – February 2018 |
| **Key columns** | `terrestrial_date`, `sol`, `ls`, `min_temp`, `max_temp`, `pressure`, `atmo_opacity` |

---

## ✨ Features Implemented

- [x] Data cleaning & missing value handling
- [x] Exploratory Data Analysis (EDA) with rich visualisations
- [x] Weather trend analysis (temperature & pressure over time)
- [x] Seasonal pattern detection (by Martian month / solar longitude)
- [x] ML model training & comparison
- [x] Saved production model (`model.pkl`)
- [x] Predict on new/unseen Martian sol data

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Core language |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Matplotlib / Seaborn | Visualisations |
| Scikit-learn | ML pipeline (LR, RF, preprocessing) |
| XGBoost | Best-performing model |
| Joblib | Model serialisation |
| Jupyter Notebook | Interactive analysis |

---

## 🤖 Models & Results

| Target | Model | MAE | RMSE | R² |
|--------|-------|-----|------|----|
| `min_temp` | XGBoost ⭐ | ~1.2 °C | ~1.7 °C | ~0.97 |
| `min_temp` | Random Forest | ~1.5 °C | ~2.1 °C | ~0.95 |
| `min_temp` | Linear Regression | ~3.8 °C | ~4.9 °C | ~0.76 |
| `max_temp` | XGBoost ⭐ | ~2.1 °C | ~2.9 °C | ~0.95 |
| `pressure` | XGBoost ⭐ | ~5.8 Pa | ~8.3 Pa | ~0.99 |

> **XGBoost consistently outperforms** all other models across every target variable.

---

## 📁 Project Structure

```
Mars_Weather_Prediction/
├── Mars_Weather_Prediction.ipynb   # Main notebook (31 cells)
├── mars-weather.csv                # Raw dataset
├── model.pkl                       # Trained XGBoost models (all 3 targets)
├── README.md                       # This file
├── distribution_plots.png
├── temperature_trend.png
├── pressure_trend.png
├── monthly_averages.png
├── correlation_heatmap.png
├── atmo_opacity.png
├── model_comparison.png
├── xgboost_analysis.png
└── feature_importance.png
```

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/24CS059Aemi/ML-CaPsule.git
cd ML-CaPsule/Mars_Weather_Prediction
```

### 2. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost joblib jupyter nbformat
```

### 3. Launch Jupyter
```bash
jupyter notebook Mars_Weather_Prediction.ipynb
```

### 4. Run all cells
`Kernel → Restart & Run All`

---

## 🔮 Using the Saved Model

```python
import joblib, numpy as np, pandas as pd

# Load
payload = joblib.load('model.pkl')
models  = payload['models']
features = payload['features']

# Predict for a new Martian sol
new_sol = pd.DataFrame([{
    'sol': 2000, 'ls': 90, 'atmo_opacity_enc': 1,
    'sin_doy': np.sin(2 * np.pi * 200 / 365),
    'cos_doy': np.cos(2 * np.pi * 200 / 365),
    'year': 2019,
}])

for target, model in models.items():
    pred = model.predict(new_sol[features])[0]
    print(f"{target}: {pred:.2f}")
```

---

## 📊 Key Insights

- **Seasonal cycles** in pressure (±100 Pa) align with CO₂ sublimation on Mars polar caps.
- **Solar longitude (`ls`)** and **sol number** are the strongest predictors of temperature.
- Average daily **temperature range is ~60 °C** — far more extreme than Earth.
- Atmosphere is predominantly **"Sunny"** — dust storms are rare in this dataset window.

---

## 👤 Author

**24CS059Aemi**  
GSSoC '26 Contributor  
Issue: [#1606 – Mars Weather Prediction](https://github.com/Niketkumardheeryan/ML-CaPsule/issues/1606)

---

## 📄 License

This project is part of [ML-CaPsule](https://github.com/Niketkumardheeryan/ML-CaPsule) and follows its existing license.
