# 🏦 Portuguese Bank Marketing: Term Deposit Prediction

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Jupyter Notebook](https://img.shields.io/badge/Jupyter-Notebook-orange)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Model_Building-yellow)
![XGBoost](https://img.shields.io/badge/XGBoost-Gradient_Boosting-green)
![Supervised Learning](https://img.shields.io/badge/ML-Binary_Classification-red)

The goal of this **Supervised Machine Learning – Binary Classification** project is to build a robust classification model to predict whether a client will subscribe to a term deposit based on demographic and campaign features. This empowers banks to optimize their marketing strategies by targeting customers with the highest likelihood to subscribe.

---

## 📑 Table of Contents
- [Dataset Details](#dataset-details)
- [Key Features & Methodology](#key-features--methodology)
- [Tech Stack](#tech-stack)
- [Usage & Inference](#usage--inference)
  - [1. Running the Notebook](#1-running-the-notebook)
  - [2. Command Line Inference (`predict.py`)](#2-command-line-inference-predictpy)
- [Model Evaluation Results](#model-evaluation-results)

---

## 📊 Dataset Details

- **Source**: UCI Portuguese Bank Marketing Dataset
- **Download**: The notebook automatically downloads the dataset as `bank-full.csv` via `gdown`.
- **Target Variable**: `y` (Has the client subscribed a term deposit? 'yes' or 'no')

### Features overview:
- **Demographics**: `age`, `job`, `marital`, `education`
- **Economic Indicators**: `default`, `balance`, `housing`, `loan`
- **Campaign Data**: `contact`, `day`, `month`, `duration`, `campaign`, `pdays`, `previous`, `poutcome`

---

## 🚀 Key Features & Methodology

- **Exploratory Data Analysis (EDA)**: Addressed Class Imbalance, Age Distribution, Campaign Diminishing Returns, and Feature Correlation.
- **Feature Engineering**: Engineered insightful features:
  - `previously_contacted`
  - `campaign_log`
  - `campaign_level`
  - `previous_campaign_interaction`
- **Preprocessing**: Robust scaling, categorical encoding, and handling missing data in a unified Scikit-Learn `Pipeline`.
- **Model Training**: Evaluated multiple algorithms including Logistic Regression, KNN, SVM, Decision Tree, Random Forest, Gradient Boosting, and XGBoost.
- **Evaluation**: Optimized models based on **ROC-AUC**, Precision, Recall, and F1-Score.

---

## 🛠 Tech Stack

- **Data Processing**: `pandas`, `numpy`
- **Visualization**: `seaborn`, `matplotlib`
- **Machine Learning**: `scikit-learn`, `xgboost`
- **Utilities**: `gdown` (dataset fetching), `joblib` (model persistence)

---

## 💻 Usage & Inference

### 1. Running the Notebook

To replicate the training process and view the EDA visualizations:
1. Open `Portuguese_Bank_Marketing.ipynb` in Jupyter Notebook or Google Colab.
2. Run all cells. (This will download `bank-full.csv` via `gdown`).
3. The notebook will process the data, train the models, and export the best model to `model/gradient_boosting_model.pkl`.

### 2. Command Line Inference (`predict.py`)

A new inference script, `predict.py`, is included to easily make predictions on new client data without opening the notebook. It utilizes the saved `gradient_boosting_model.pkl` pipeline.

**Example Usage**:
```bash
python predict.py --data '{"age": 30, "job": "management", "marital": "married", "education": "tertiary", "default": "no", "balance": 1500, "housing": "yes", "loan": "no", "contact": "cellular", "day": 5, "month": "may", "duration": 250, "campaign": 1, "pdays": -1, "previous": 0, "poutcome": "unknown"}'
```

**Output**:
```text
==================================================
🎯 PORTUGUESE BANK MARKETING - PREDICTION RESULT
==================================================
Prediction      : Subscribed (Yes)
Probability     : 72.45%
==================================================
```

---

## 📈 Model Evaluation Results

The models were evaluated using Accuracy and ROC-AUC. **Gradient Boosting** was selected as the final model due to its optimal balance of predictive power and precision.

| Model | Accuracy | ROC-AUC |
| :--- | :---: | :---: |
| **Gradient Boosting (Selected)** | **90.46%** | **0.8016** |
| XGBoost | 90.17% | 0.7963 |
| Random Forest | 90.11% | 0.7712 |
| Logistic Regression | 89.96% | 0.7675 |
| Support Vector Machine | 89.78% | 0.7511 |
| Decision Tree | 89.28% | 0.7390 |
| K-Nearest Neighbors | 89.10% | 0.7289 |
