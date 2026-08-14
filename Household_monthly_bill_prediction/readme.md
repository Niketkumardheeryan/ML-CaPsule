# Electricity Bill Prediction — EDA & Machine Learning Pipeline

##  Overview
This project focuses on analyzing and predicting electricity bills using appliance usage, monthly hours, tariff rates, and company/city data. It integrates Exploratory Data Analysis (EDA), data preprocessing, and machine learning pipelines built with scikit-learn and XGBoost.

## Objectives
- Explore relationships between household appliances and electricity consumption.
- Handle skewness and outliers using statistical transformations.
- Build regression models to predict electricity bills.
- Compare performance across Linear Regression, Random Forest, and XGBoost models.

## Dataset Summary
- File: electricity_bill_dataset.csv
- Shape: 45,345 rows × 12 columns

## Key Features:

- Appliance usage (Fan, Refrigerator, AirConditioner, Television, Monitor, MotorPump)
- MonthlyHours and TariffRate
- City and Company (categorical)
- ElectricityBill (target variable)

## Exploratory Data Analysis
- Verified data types, nulls, and duplicates — dataset is clean.
- Converted numeric columns to integer types for efficiency.
- Generated descriptive statistics and correlation matrix.
- Visualized distributions using countplots, KDE plots, scatterplots, and heatmaps.
- Identified strong correlation between MonthlyHours and ElectricityBill (~0.96).

## Data Preprocessing
- Checked skewness for all numeric columns.
- Applied log transformation for negatively skewed data.
- Used Yeo-Johnson PowerTransformer for normalization.
- Handled outliers using IQR capping to limit extreme values.

## Model Building
- Created a ColumnTransformer combining OneHotEncoder, PowerTransformer, and StandardScaler.
- Built pipelines for three regression models:
         - Linear Regression → R² ≈ 0.9956

         - Random Forest Regressor → R² ≈ 0.9999

         - XGBoost Regressor → R² ≈ 0.9996

XGBoost achieved the best performance overall.

## How to Run the Project

### Clone the Repository:

    bash
    git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
    cd ML-CaPsule

### Install Dependencies:
    pip install -r requirements.txt

### Run the Model:
    jupyter lab ./household_monthly_bill_prediction.ipynb


## Insights
- MonthlyHours and TariffRate are the most influential predictors.
- City and Company add minor variations.
- The model demonstrates near-perfect predictive accuracy, suitable for billing automation.