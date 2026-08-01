# 🚀 Bike Price Prediction using Machine Learning

Predict the selling price of a bike using various Machine Learning regression algorithms based on bike specifications.

---

## 📌 Project Overview

This project develops a complete Machine Learning pipeline for predicting bike prices using regression techniques. It includes data preprocessing, exploratory data analysis (EDA), feature engineering, model training, evaluation, and comparison of multiple regression algorithms.

---

## 📂 Dataset

**Dataset Source:**

https://gist.githubusercontent.com/semicolonSimp/b379995207163d47dbc6c3adb8f5dac7/raw/f68a4cddfdbe72f11245d00476a85f1b6dc01a03/bike%2520price%2520prediction

### Dataset Features

| Feature | Description |
|----------|-------------|
| Bike_company | Manufacturer of the bike |
| Manufactured_year | Manufacturing year |
| Engine_warranty | Engine warranty (Years) |
| Engine_type | Type of engine |
| Fuel_type | Fuel used by the bike |
| CC(Cubic capacity) | Engine displacement (CC) |
| Fuel_Capacity | Fuel tank capacity (Litres) |
| Price | Target Variable |

---

## 📊 Exploratory Data Analysis (EDA)

- Dataset Overview
- Missing Value Analysis
- Duplicate Value Check
- Data Cleaning
- Distribution Analysis
- Correlation Analysis
- Outlier Detection

---

## ⚙️ Data Preprocessing

- Removed unnecessary columns
- Cleaned Engine Capacity (CC) values
- Cleaned Fuel Capacity values
- Handled missing values
- Encoded categorical features
- Feature Scaling
- Train-Test Split

---

## 🤖 Machine Learning Models Used

- Linear Regression
- Lasso Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor
- Support Vector Regressor (SVR)
- XGBoost Regressor

---

## 📈 Evaluation Metrics

The models were evaluated using:

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

---

## 🏆 Model Performance

| Model | Status |
|--------|--------|
| Linear Regression | Trained |
| Lasso Regression | Trained |
| Decision Tree Regressor | Trained |
| Random Forest Regressor | Trained |
| **Gradient Boosting Regressor** | ⭐ Best Model |
| Support Vector Regressor (SVR) | Trained |
| XGBoost Regressor | Trained |

---

## ⭐ Best Performing Model

| Model | R² Score |
|--------|---------:|
| **Gradient Boosting Regressor** | **78.16%** |

The Gradient Boosting Regressor achieved the highest **R² Score of 78.16%**, making it the best-performing model for predicting bike prices in this project.

---

## 🛠️ Libraries Used

- NumPy
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn
- XGBoost
- Joblib

---

## 📁 Project Structure

```
Bike-Price-Prediction
│── Bike_Price_Prediction.ipynb
│── README.md
```

---

