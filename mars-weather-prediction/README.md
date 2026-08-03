# 🔴 Mars Weather Prediction using XGBoost

> Predicting atmospheric conditions on Mars using NASA Curiosity Rover weather data and machine learning.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML%20Model-orange)](https://xgboost.readthedocs.io/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626)](https://jupyter.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📌 Project Overview

This project uses **NASA Mars Curiosity Rover** weather datasets to analyze and predict atmospheric conditions on Mars using Machine Learning techniques. The primary goal is to predict **minimum temperature** (`min_temp`) on Mars based on features like solar longitude (`ls`), atmospheric pressure, and wind speed.

The full pipeline covers:
- Data Loading & Exploration
- Exploratory Data Analysis (EDA) with visualizations
- Data Cleaning & Feature Engineering
- Model Training using **XGBoost Regressor**
- Model Evaluation (MSE, R² Score)
- Model Persistence (`model.pkl`)

---

## 📂 Dataset

- **Source:** [Kaggle — Mars Weather Data](https://www.kaggle.com/datasets/imkrkannan/mars-weather-data)
- **File:** `mars_weather.csv`
- **Rows:** ~1,895 daily weather records
- **Columns:**

| Column | Description |
|---|---|
| `id` | Record ID |
| `terrestrial_date` | Earth date |
| `sol` | Martian solar day |
| `ls` | Solar longitude (season indicator) |
| `month` | Martian month |
| `min_temp` | Minimum daily temperature (°C) — **Target** |
| `max_temp` | Maximum daily temperature (°C) |
| `pressure` | Atmospheric pressure (Pa) |
| `wind_speed` | Wind speed |
| `atmo_opacity` | Sky condition (Sunny/Cloudy) |

> **Note:** The dataset is loaded dynamically using `gdown` from a public Google Drive link. No CSV file is committed to this repository.

---

## ✨ Features Implemented

- [x] Data Cleaning & Missing Value Imputation
- [x] Exploratory Data Analysis (EDA)
- [x] Temperature Distribution Visualization
- [x] Temperature Trend Over Time
- [x] XGBoost Regressor Model
- [x] Model Evaluation (MSE & R² Score)
- [x] Saved Model (`model.pkl`)
- [ ] Interactive Dashboard *(planned)*
- [ ] ML Model Comparison *(planned)*

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.8+ | Core language |
| Pandas | Data manipulation |
| NumPy | Numerical computing |
| Matplotlib / Seaborn | Data visualization |
| Scikit-learn | Train/test split, metrics |
| XGBoost | ML model |
| Jupyter Notebook | Interactive development |
| gdown | Dataset download from Drive |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/24CS059Aemi/ML-CaPsule.git
cd ML-CaPsule/Mars_Weather_Prediction
```

### 2. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn xgboost scikit-learn gdown jupyter
```

### 3. Run the notebook
```bash
jupyter notebook Mars_Weather_Prediction.ipynb
```

The notebook will automatically download the dataset using `gdown` in the first cell.

---

## 📊 Model Results

| Metric | Score |
|---|---|
| Mean Squared Error (MSE) | ~30.5 |
| R² Score | ~0.91 |

The XGBoost model achieves over **91% variance explained (R²)** on the test set.

---

## 📁 Project Structure

```
Mars_Weather_Prediction/
├── Mars_Weather_Prediction.ipynb  # Main notebook (EDA + ML pipeline)
├── model.pkl                      # Trained XGBoost model
├── README.md                      # Project documentation
└── .gitignore                     # Excludes data files & checkpoints
```

---

## 📘 Deliverables

- `Mars_Weather_Prediction.ipynb` — Full end-to-end ML notebook with outputs
- `model.pkl` — Serialized trained model
- `README.md` — Project documentation

---

## 👤 Author

- **GitHub:** [@24CS059Aemi](https://github.com/24CS059Aemi)
- **Program:** GirlScript Summer of Code (GSSoC '26)
- **Issue:** [#1606](https://github.com/Niketkumardheeryan/ML-CaPsule/issues/1606)
