# Food Delivery Time Prediction Using Machine Learning

## Overview
This project uses machine learning regression algorithms to predict food delivery time from factors such as distance, weather, traffic level, time of day, vehicle type, preparation time, and courier experience.

## Objectives
- Perform basic data cleaning and preprocessing.
- Explore important relationships with delivery time.
- Encode categorical variables.
- Train and compare multiple regression models.
- Evaluate models using MAE, RMSE, and R² Score.
- Visualize model performance.
- Analyze feature importance.

## Dataset
link: https://gist.githubusercontent.com/anu-006/95eea119d84814494da73947c8619421/raw/fec62bef1ecc5b468c87c282d6f54fd91bb35a1b/Food_Delivery_Times 

The dataset contains delivery-related features including:
- `Distance_km`
- `Weather`
- `Traffic_Level`
- `Time_of_Day`
- `Vehicle_Type`
- `Preparation_Time_min`
- `Courier_Experience_yrs`

**Target:** `Delivery_Time_min`

## Machine Learning Models
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- XGBoost Regressor

## Evaluation Metrics
- **MAE:** Mean Absolute Error — lower is better.
- **RMSE:** Root Mean Squared Error — lower is better.
- **R² Score:** Proportion of target variation explained by the model — higher is better.

## Visualizations
The notebook includes relevant EDA and model visualizations such as:
- Delivery-time distribution
- Feature vs. delivery-time plots
- Correlation analysis
- Model performance comparison
- Actual vs. predicted values
- Feature importance

## Workflow
```text
Data Loading
    ↓
Data Cleaning
    ↓
Basic EDA
    ↓
Categorical Encoding
    ↓
Train-Test Split
    ↓
Model Training
    ↓
MAE / RMSE / R² Evaluation
    ↓
Model Comparison
    ↓
Feature Importance
    ↓
Best Model
```

## Technologies
Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, XGBoost, Jupyter Notebook.

## Installation
```bash
pip install -r requirements.txt
```

Then open:
```bash
jupyter notebook Food_Delivery_Time_Prediction.ipynb
```

## Note on Outliers
Because `Delivery_Time_min` is the target variable, extreme values should be inspected before being removed or capped. Genuine long delivery times may be valid observations.

## Project Structure
```text
Food-Delivery-Time-Prediction/
├── Food_Delivery_Time_Prediction.ipynb
├── README.md
├── requirements.txt
└── dataset/
    └── food_delivery.csv
```

## Expected Outcome
The project provides an end-to-end, beginner-friendly regression workflow for predicting food delivery time and comparing different machine learning models.
