# Water Potability Prediction Using Machine Learning

## 📌 Project Overview

This project predicts whether a water sample is **potable (safe for drinking)** or **not potable** using machine learning classification algorithms.

The notebook performs exploratory data analysis (EDA), handles missing values, addresses class imbalance using **SMOTE**, applies feature scaling, and compares multiple classification models using several evaluation metrics.

## 🎯 Objective

Build a machine learning classification pipeline that can predict the `Potability` of water based on its physical and chemical properties.

- `Potability = 1` → Potable / Safe to drink
- `Potability = 0` → Not potable

## 📊 Dataset

The notebook uses a CSV file named:

```text
water_potability.csv
```

The dataset contains **3,276 records** and **10 columns**:

| Feature | Description |
|---|---|
| `ph` | Acidity/basicity level of water |
| `Hardness` | Calcium and magnesium content |
| `Solids` | Total dissolved solids |
| `Chloramines` | Chloramine concentration |
| `Sulfate` | Sulfate concentration |
| `Conductivity` | Electrical conductivity |
| `Organic_carbon` | Organic carbon content |
| `Trihalomethanes` | Trihalomethanes concentration |
| `Turbidity` | Water turbidity |
| `Potability` | Target variable |

### Missing Values

The notebook identifies missing values in:

- `ph` — approximately 14.99%
- `Sulfate` — approximately 23.84%
- `Trihalomethanes` — approximately 4.95%

No duplicate rows were found in the dataset.

## 🔎 Exploratory Data Analysis

The notebook includes:

- Dataset shape and descriptive statistics
- Missing-value analysis
- Duplicate-value checking
- Correlation analysis
- Correlation heatmap
- Univariate analysis using KDE plots
- Skewness analysis
- Bivariate analysis
- Potability class distribution
- Outlier visualization using box plots

## 🛠️ Data Preprocessing

The following preprocessing steps are implemented:

### 1. Train-Test Split

The dataset is divided into:

- **80% training data**
- **20% testing data**

with `random_state=42`.

### 2. Outlier Capping

IQR-based capping is applied to numerical features where possible.

### 3. Missing Value Imputation

Median imputation is applied to:

- `ph`
- `Sulfate`
- `Trihalomethanes`

The imputation is included inside a preprocessing pipeline so that imputed values are correctly passed to the scaling step.

### 4. Feature Scaling

`StandardScaler` is used to standardize the numerical features.

### 5. Handling Class Imbalance

The target variable is imbalanced, so **SMOTE (Synthetic Minority Over-sampling Technique)** is applied to the training data through an imbalanced-learn pipeline.

This helps increase representation of the minority class without applying SMOTE to the test set.

## 🤖 Machine Learning Models

The notebook compares the following classification algorithms:

1. Random Forest Classifier
2. Logistic Regression
3. Decision Tree Classifier
4. XGBoost Classifier
5. Gradient Boosting Classifier

Each model is evaluated using the same preprocessing and SMOTE pipeline.

## 📈 Evaluation Metrics

The following metrics are calculated:

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC Score
- Classification Report

A combined **ROC-AUC curve** is also plotted to compare model performance.

## 🏆 Model Results

The recorded results from the notebook are:

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Random Forest | 0.6524 | 0.5364 | 0.4836 | 0.5086 | **0.6936** |
| Logistic Regression | 0.4970 | 0.3639 | 0.4713 | 0.4107 | 0.5069 |
| Decision Tree | 0.5686 | 0.4296 | 0.4877 | 0.4568 | 0.5521 |
| XGBoost | 0.6250 | 0.4961 | 0.5205 | 0.5080 | 0.6654 |
| Gradient Boosting | 0.6098 | 0.4769 | 0.5082 | 0.4921 | 0.6634 |

### Best Performing Model

Based on the recorded results, **Random Forest** performs best overall, achieving:

- Accuracy: **65.24%**
- ROC-AUC: **69.36%**

The ROC-AUC score is useful here because the target classes are imbalanced.

## ⚙️ Installation

Clone the repository and move into the project directory:

```bash
git clone <your-repository-url>
cd Water-Potability-Prediction
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ How to Run

1. Make sure `water_potability.csv` is in the same directory as the notebook.
2. Install the dependencies from `requirements.txt`.
3. Open the notebook using Jupyter Notebook, JupyterLab, VS Code, or Google Colab.
4. Run the cells from top to bottom.

