# Internet Speed Prediction Using Machine Learning

##  Project Overview

This project uses **Machine Learning regression algorithms** to predict internet speed based on the available features in the dataset.
https://gist.githubusercontent.com/anu-006/7ebeb25da6ff1a352f483ef00a617f15/raw/3a673ef537946ba81b9b91238670ab02b5977e86/Internet%2520Speed.csv

The project performs:

* Data loading and inspection
* Data quality checking
* Exploratory Data Analysis (EDA)
* Correlation analysis
* Data visualization
* Training multiple regression models
* Comparing model performance
* Selecting the best-performing model

The best-performing model in this project is **XGBoost Regressor**, which achieved an **R² score of 0.9995** on the test data.

---

##  Objective

The main objective of this project is to build a machine learning model that can predict:

> **Internet Speed**

The target variable used in the project is: Internet_speed


This is a **supervised machine learning regression problem** because the target is a continuous numerical value.

---



### Files Description

| File                              | Description                                               |
| --------------------------------- | --------------------------------------------------------- |
| `Internet_Speed_Prediction.ipynb` | Main Jupyter Notebook containing the complete ML workflow |
| `Internet Speed.csv`              | Dataset used for training and testing                     |
| `README.md`                       | Project documentation                                     |
| `requirements.txt`                | Python libraries required to run the project              |

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* XGBoost
* Jupyter Notebook

---

## 🤖 Machine Learning Models Used

Four regression algorithms were trained and compared:

### 1. Linear Regression

### 2. Decision Tree Regressor

### 3. Gradient Boosting Regressor

### 4. XGBoost Regressor

XGBoost is an optimized gradient boosting algorithm that is widely used for machine learning problems involving structured/tabular data.


##  Model Evaluation

The models are evaluated using three metrics.

### R² Score

R² measures how well the model explains the variation in the target variable.

**Higher R² is better.**

An R² score closer to `1` generally indicates better performance.

### Mean Absolute Error (MAE)

MAE measures the average absolute difference between actual and predicted values.

**Lower MAE is better.**

### Mean Squared Error (MSE)

MSE calculates the average squared difference between actual and predicted values.

**Lower MSE is better.**

---

## 🏆 Results


### Best Model

**XGBoost Regressor**

R² Score = 0.9995

According to the notebook, XGBoost gives the best performance among the models tested.

