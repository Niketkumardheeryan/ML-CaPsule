# 🏦 Portuguese Bank Marketing: Term Deposit Prediction

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Jupyter Notebook](https://img.shields.io/badge/Jupyter-Notebook-orange)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Model_Building-yellow)
![XGBoost](https://img.shields.io/badge/XGBoost-Gradient_Boosting-green)
![Imbalance-Learn](https://img.shields.io/badge/Imbalance--Learn-SMOTE-blueviolet)

The goal of this **Supervised Machine Learning – Binary Classification** project is to build a robust classification model to predict whether a client will subscribe to a term deposit based on demographic and campaign features. 

---

## 📑 Table of Contents
- [Project Overview & Key Changes](#project-overview--key-changes)
- [Dataset Details](#dataset-details)
- [Key Features & Methodology](#key-features--methodology)
- [Tech Stack](#tech-stack)
- [Usage & Inference](#usage--inference)
  - [1. Running the Notebook](#1-running-the-notebook)
  - [2. Command Line Inference (`predict.py`)](#2-command-line-inference-predictpy)
- [Model Evaluation Results](#model-evaluation-results)
- [Class Imbalance Resolution (SMOTE)](#class-imbalance-resolution-smote)

---

## 🚀 Project Overview & Key Changes (Issue #2049)

In this update, we address the severe class imbalance present in the Portuguese Bank Marketing dataset. 
- **Class Imbalance Resolution**: Integrated **SMOTE** (Synthetic Minority Over-sampling Technique) to oversample the minority class during training. We also compared SMOTE against **Random Over-sampler (ROS)** and **Random Under-sampler (RUS)**.
- **Unified Visualizations PDF**: All EDA and modeling visualization plots have been compiled into a single, comprehensive PDF document: [SMOTE_Class_Imbalance_Report.pdf](file:///d:/GSSoC/ML-CaPsule/ML-CaPsule/Portuguese_Bank_Marketing/SMOTE_Class_Imbalance_Report.pdf). This keeps the repository clean by removing multiple loose PNG files.
- **Model Evaluation**: Retrained and evaluated 7 classification models across the resampling scenarios.

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

- **Exploratory Data Analysis (EDA)**: Analyzed Class Imbalance, Age Distribution, Campaign Diminishing Returns, and Feature Correlation.
- **Feature Engineering**: Engineered insightful features:
  - `previously_contacted`
  - `campaign_log`
  - `campaign_level`
  - `previous_campaign_interaction`
- **Preprocessing**: Robust scaling, categorical encoding, and handling missing data in a unified Scikit-Learn `Pipeline`.
- **Resampling**: Applied SMOTE only to the training set to prevent data leakage.
- **Model Training**: Evaluated Logistic Regression, KNN, SVM, Decision Tree, Random Forest, Gradient Boosting, and XGBoost.
- **Evaluation**: Optimized models based on **Recall** and **F1-Score** for the minority class, alongside **ROC-AUC**.

---

## 🛠 Tech Stack

- **Data Processing**: `pandas`, `numpy`
- **Visualization**: `seaborn`, `matplotlib`
- **Machine Learning**: `scikit-learn`, `xgboost`, `imbalanced-learn`
- **Utilities**: `gdown`, `joblib`, `reportlab` (for PDF report compilation)

---

## 💻 Usage & Inference

### 1. Running the Notebook

To replicate the training process:
1. Open `Portuguese_Bank_Marketing.ipynb` in Jupyter Notebook or Google Colab.
2. Run all cells. (This will download the dataset, perform preprocessing, resample with SMOTE, train the models, and export the best model).

### 2. Command Line Inference (`predict.py`)

An inference script, `predict.py`, utilizes the saved `gradient_boosting_model.pkl` pipeline to run predictions on new client data.

**Example Usage**:
```bash
python predict.py --data '{"age": 30, "job": "management", "marital": "married", "education": "tertiary", "default": "no", "balance": 1500, "housing": "yes", "loan": "no", "contact": "cellular", "day": 5, "month": "may", "duration": 250, "campaign": 1, "pdays": -1, "previous": 0, "poutcome": "unknown"}'
```

---

## 📈 Model Evaluation Results

After addressing class imbalance using SMOTE, the models were evaluated. Below is the performance comparison of the top-performing models on the test dataset:

### Scenario Comparison (Gradient Boosting)

| Scenario | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **SMOTE (Selected)** | **89.63%** | **0.543** | **0.710** | **0.616** | **0.9251** |
| Original (Unbalanced) | 90.83% | 0.654 | 0.460 | 0.540 | 0.9294 |
| ROS (Over-sampler) | 85.33% | 0.436 | 0.867 | 0.580 | 0.9291 |
| RUS (Under-sampler) | 84.33% | 0.419 | 0.875 | 0.567 | 0.9264 |

### Final Model Standings (Trained with SMOTE)

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gradient Boosting** | **89.63%** | **0.543** | **0.710** | **0.616** | **0.9251** |
| XGBoost | 89.05% | 0.523 | 0.723 | 0.607 | 0.9234 |
| Random Forest | 87.12% | 0.469 | 0.768 | 0.583 | 0.9179 |
| Logistic Regression | 84.70% | 0.419 | 0.802 | 0.551 | 0.9062 |
| Decision Tree | 85.50% | 0.431 | 0.750 | 0.548 | 0.8635 |
| K-Nearest Neighbors | 83.83% | 0.398 | 0.750 | 0.520 | 0.8611 |
| Support Vector Machine | 54.74% | 0.180 | 0.806 | 0.294 | 0.7452 |

*Note: SMOTE-based training yields a much higher Recall (0.710 vs. 0.460 originally) for the positive class (subscribed), resolving the class imbalance challenge effectively.*

For the complete set of visual analyses and metric explanations, please refer to [SMOTE_Class_Imbalance_Report.pdf](file:///d:/GSSoC/ML-CaPsule/ML-CaPsule/Portuguese_Bank_Marketing/SMOTE_Class_Imbalance_Report.pdf).

