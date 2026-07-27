# 🏠 House Price Prediction

## Overview

This project predicts California housing prices using supervised machine learning techniques. It demonstrates a complete end-to-end regression pipeline, including data loading, preprocessing, feature engineering, model training, hyperparameter tuning, evaluation, and model serialization.

The notebook compares multiple regression algorithms and selects the best-performing model for predicting median house values.

---

## Dataset

- **Dataset:** California Housing Dataset
- **Source:** Aurélien Géron's Hands-On Machine Learning repository
- **Training Samples:** ~16,512
- **Testing Samples:** ~4,128
- **Target Variable:** `median_house_value`

> The dataset is automatically downloaded during the first execution of the notebook. Future runs use the cached local copy.

---

## Model Performance

| Model | RMSE | Remarks |
|------|------:|------|
| Linear Regression | ~67,239 | Baseline model |
| Decision Tree Regressor | ~69,383 | Overfits the training data |
| **Random Forest Regressor** | **47,149.20** | Best-performing model after GridSearchCV |

### Final Metrics

- **RMSE:** **47,149.20**
- **R² Score:** **82.94%**

---

# Project Structure

```
Housing_Prediction/
│
├── Dataset/
│   └── housing.csv
│
├── Model/
│   ├── des_tree.pkl
│   └── lin_reg.pkl
│
├── 2-project-houseprediction/
│   ├── house-price-pridiction.ipynb
│   ├── readme.md
│   └── submission.csv
│
├── main_housing.ipynb
├── Readme.md
└── requirements.txt
```

---

# Requirements

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

Required packages:

- numpy
- pandas
- matplotlib
- scikit-learn
- six
- joblib

---

# Installation

### 1. Clone the repository

```bash
git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
```

### 2. Navigate to the project

```bash
cd ML-CaPsule/Housing_Prediction
```

### 3. (Optional) Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

# How to Run

### Step 1

Launch Jupyter Notebook or JupyterLab.

```bash
jupyter notebook
```

or

```bash
jupyter lab
```

### Step 2

Open

```
main_housing.ipynb
```

### Step 3

Run all notebook cells sequentially.

The notebook will automatically:

- Download the California Housing dataset (if not already present)
- Perform data preprocessing
- Create engineered features
- Train multiple regression models
- Tune the Random Forest model using GridSearchCV
- Evaluate the final model
- Save serialized models in the `Model/` directory where applicable

---

# Machine Learning Pipeline

## 1. Data Loading

The California Housing dataset is downloaded and loaded into a Pandas DataFrame.

---

## 2. Stratified Train-Test Split

The dataset is divided using **StratifiedShuffleSplit** based on categorized median income to preserve the income distribution across training and testing datasets.

---

## 3. Feature Engineering

Additional informative features are created:

- Rooms per Household
- Bedrooms per Room
- Population per Household

Correlation analysis is then performed to identify influential predictors.

---

## 4. Data Preprocessing

A preprocessing pipeline performs:

- Median imputation for missing values
- Standardization of numerical features
- One-Hot Encoding of `ocean_proximity`

using a `ColumnTransformer`.

---

## 5. Model Training

The notebook trains and compares:

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor

using cross-validation.

---

## 6. Hyperparameter Tuning

GridSearchCV searches for the best Random Forest hyperparameters, including:

- `n_estimators`
- `max_features`

to maximize predictive performance.

---

## 7. Final Evaluation

The optimized model is evaluated on the held-out test set using:

- Root Mean Squared Error (RMSE)
- R² Score

---

# Model Directory

The `Model/` directory stores serialized machine learning models for reuse without retraining.

| File | Description |
|------|-------------|
| `des_tree.pkl` | Serialized Decision Tree Regressor model. |
| `lin_reg.pkl` | Serialized Linear Regression model. |

These models can be loaded directly using Joblib for inference or experimentation.

---

# Loading a Saved Model

```python
import joblib

model = joblib.load("Model/lin_reg.pkl")

predictions = model.predict(sample_data)

print(predictions)
```

Similarly, the Decision Tree model can be loaded using:

```python
tree_model = joblib.load("Model/des_tree.pkl")
```

> **Note:** The Random Forest model is trained and evaluated within the notebook. If exported, it can also be serialized using Joblib following the same approach.

---

# Conclusion

The Random Forest Regressor achieves the best predictive performance for this dataset after hyperparameter tuning.

The project demonstrates an end-to-end machine learning workflow covering preprocessing, feature engineering, model comparison, hyperparameter optimization, evaluation, and model serialization.

**Best Results**

- **Model:** Random Forest Regressor
- **RMSE:** **47,149.20**
- **R² Score:** **82.94%**

---

## Author

**Chirag**

GitHub: https://github.com/chiragHimself