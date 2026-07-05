# Monthly Electricity Bill Prediction System

## Overview

The **Monthly Electricity Bill Prediction System** is a Machine Learning project that predicts a household's monthly electricity bill (INR) using residential energy consumption, electrical characteristics, household information, appliance usage, and billing-related features.

The project demonstrates a complete end-to-end machine learning workflow, including data preprocessing, exploratory data analysis (EDA), feature engineering, model training, evaluation, and prediction using an XGBoost regression model.

This implementation is designed to serve as both a practical ML example and an educational reference for building regression models on structured tabular datasets.

---

## Features

* Comprehensive data preprocessing pipeline
* Exploratory Data Analysis (EDA)
* Missing value handling
* Outlier detection and removal
* Categorical feature encoding
* Feature scaling (where required)
* Correlation analysis
* XGBoost Regression model implementation
* Model evaluation using Scikit-learn metrics
* Feature importance analysis
* User input prediction example
* Well-commented notebook with section-wise implementation

---

## Dataset

The repository includes a synthetic Indian household electricity dataset containing residential energy consumption information.

### Target Variable

* **Total_Bill_INR**

### Example Features

* State
* Region
* Household Size
* Home Type
* Season
* Ambient Temperature
* Connection Type
* Sanctioned Load
* Power Factor
* BEE Star Rating
* Wiring Condition
* Wiring Age
* Monthly Billed Units
* Base Monthly kWh
* Energy Charges
* Fixed Charges
* PPAC Charges
* Electricity Duty
* Appliance-related features
* Electrical quality indicators (THD, Phase Imbalance)

---

## Project Structure

```
├── Monthly_Electricity_Bill_Prediction_System.ipynb
├── indian_household_electricity_bill_dataset.csv
└── README.md
```

---

## Machine Learning Workflow

### 1. Data Loading

* Imported the dataset
* Performed initial inspection
* Verified feature types

### 2. Data Preprocessing

* Checked missing values
* Removed duplicate records
* Encoded categorical variables
* Treated outliers
* Prepared features and target variable

### 3. Exploratory Data Analysis

* Summary statistics
* Distribution plots
* Correlation heatmap
* Feature relationship analysis

### 4. Model Training

The project uses **XGBoost Regressor** for prediction.

### 5. Model Evaluation

Performance was evaluated using:

* Mean Absolute Error (MAE)
* Mean Squared Error (MSE)
* Root Mean Squared Error (RMSE)
* R² Score

### 6. Feature Importance

The notebook includes feature importance visualization to identify the variables contributing most to electricity bill prediction.

### 7. User Prediction

A sample section demonstrates how users can provide custom household information to obtain a predicted monthly electricity bill.

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* XGBoost

---

## Model Pipeline

```
Dataset
     │
     ▼
Data Cleaning
     │
     ▼
EDA
     │
     ▼
Feature Engineering
     │
     ▼
Train-Test Split
     │
     ▼
XGBoost Regression
     │
     ▼
Model Evaluation
     │
     ▼
Feature Importance
```

---

## Learning Outcomes

This project demonstrates practical implementation of:

* Regression modeling
* Data preprocessing
* Feature engineering
* Exploratory Data Analysis
* Model evaluation
* XGBoost
* End-to-end machine learning workflow
