# 🏠 House Price Prediction using Machine Learning

Predict house prices using various Machine Learning regression algorithms. This project demonstrates a complete end-to-end regression workflow, including data preprocessing, exploratory data analysis (EDA), model training, evaluation, comparison, and prediction on unseen data.

---

## 📌 Project Overview

House Price Prediction is one of the most popular regression problems in Machine Learning. The objective is to estimate the selling price of a house based on its features such as area, number of bedrooms, bathrooms, parking availability, furnishing status, and other property characteristics.

This project covers the complete Machine Learning pipeline from raw data to model evaluation and prediction.

---

## 🎯 Objectives

- Understand a real-world regression problem.
- Perform Exploratory Data Analysis (EDA).
- Preprocess categorical and numerical data.
- Train multiple regression models.
- Compare model performance.
- Predict house prices for unseen data.

---

# 📂 Dataset

## 📥 Training Dataset

Load directly from GitHub Gist:

https://gist.githubusercontent.com/semicolonSimp/b48a667e01bce79e47ad7c784b9f2d9d/raw/297e45941d3caba4e10d1b2e7f6b99831f9a837a/houseprice-train.csv

---

## 📥 Testing Dataset

Load directly from GitHub Gist:

https://gist.githubusercontent.com/semicolonSimp/21a95e54961fe5babfc94c4531bb28ca/raw/8f542d3adf850e810a106addd4036afa26af3597/houseprice-test.csv

---

## 📖 Load Dataset using Pandas

```python
import pandas as pd

train_url = "https://gist.githubusercontent.com/semicolonSimp/b48a667e01bce79e47ad7c784b9f2d9d/raw/297e45941d3caba4e10d1b2e7f6b99831f9a837a/houseprice-train.csv"

test_url = "https://gist.githubusercontent.com/semicolonSimp/21a95e54961fe5babfc94c4531bb28ca/raw/8f542d3adf850e810a106addd4036afa26af3597/houseprice-test.csv"

train_df = pd.read_csv(train_url)
test_df = pd.read_csv(test_url)
```

---

# 📊 Dataset Features

## 📝 Feature Categories

### 🏡 General Property Information
- Id
- MSSubClass
- MSZoning
- LotFrontage
- LotArea
- Street
- Alley
- LotShape
- LandContour
- Utilities
- LotConfig
- LandSlope

### 📍 Location Features
- Neighborhood
- Condition1
- Condition2

### 🏠 Building Characteristics
- BldgType
- HouseStyle
- OverallQual
- OverallCond
- YearBuilt
- YearRemodAdd

### 🏚 Roof & Exterior
- RoofStyle
- RoofMatl
- Exterior1st
- Exterior2nd
- MasVnrType
- MasVnrArea
- ExterQual
- ExterCond

### 🧱 Basement Information
- Foundation
- BsmtQual
- BsmtCond
- BsmtExposure
- BsmtFinType1
- BsmtFinSF1
- BsmtFinType2
- BsmtFinSF2
- BsmtUnfSF
- TotalBsmtSF

### 🔥 Heating & Utilities
- Heating
- HeatingQC
- CentralAir
- Electrical

### 🏡 Living Area
- 1stFlrSF
- 2ndFlrSF
- LowQualFinSF
- GrLivArea

### 🚿 Bathrooms
- BsmtFullBath
- BsmtHalfBath
- FullBath
- HalfBath

### 🛏 Rooms
- BedroomAbvGr
- KitchenAbvGr
- KitchenQual
- TotRmsAbvGrd
- Functional
- Fireplaces
- FireplaceQu

### 🚗 Garage Details
- GarageType
- GarageYrBlt
- GarageFinish
- GarageCars
- GarageArea
- GarageQual
- GarageCond

### 🌳 Outdoor Features
- PavedDrive
- WoodDeckSF
- OpenPorchSF
- EnclosedPorch
- 3SsnPorch
- ScreenPorch
- PoolArea
- PoolQC
- Fence
- MiscFeature
- MiscVal

### 📅 Sale Information
- MoSold
- YrSold
- SaleType
- SaleCondition
### 🎯 Target Variable

```
Price
```

---

# 🤖 Machine Learning Algorithms Used

This project compares multiple regression algorithms to identify the best-performing model.

| Algorithm | Purpose |
|-----------|---------|
| **Linear Regression** | Baseline regression model for predicting house prices. |
| **Ridge Regression** | Linear Regression with L2 Regularization to reduce overfitting. |
| **Lasso Regression** | Linear Regression with L1 Regularization for feature selection. |
| **Decision Tree Regressor** | Captures non-linear relationships between features and target. |
| **Random Forest Regressor** | Ensemble of Decision Trees for improved accuracy and robustness. |
| **Gradient Boosting Regressor** | Sequential ensemble learning algorithm that improves prediction performance. |
| **XGBoost Regressor**  | Optimized Gradient Boosting model offering excellent predictive performance. |

---

# ⚙️ Project Workflow

## 1️⃣ Import Libraries

Import all required Python libraries.

Libraries used:

- NumPy
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn

---

## 2️⃣ Load Dataset

Read the training and testing datasets using Pandas.

---

## 3️⃣ Exploratory Data Analysis (EDA)

Performed various analyses including:

- Dataset Information
- Missing Value Detection
- Summary Statistics
- Correlation Analysis
- Feature Distribution

---

## 4️⃣ Data Preprocessing

Preprocessing steps include:

- Handling Missing Values
- Encoding Categorical Features
- Feature Selection
- Data Cleaning

---

## 5️⃣ Model Training

Each regression model is trained independently using the training dataset.

---

## 6️⃣ Model Evaluation

The trained models are evaluated using standard regression metrics.

### Evaluation Metrics

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score (Coefficient of Determination)

---

## 7️⃣ Model Comparison

The performance of all regression algorithms is compared to identify the most accurate model.

---

## 8️⃣ Prediction

The best-performing model is used to predict house prices on unseen test data.

Example:

```
Predicted Price : 4,250,000

Actual Price    : 4,180,000
```
---

# 📁 Project Structure

```
House-Price-Prediction
│
├── House_Price_Prediction.ipynb
├── README.md
```

---

# 💻 Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

---

# 📚 Learning Outcomes

After completing this project, you will understand:

- Regression Problems
- Data Cleaning
- Feature Engineering
- Categorical Encoding
- Model Training
- Model Evaluation
- Regression Metrics
- Model Comparison
- House Price Prediction

---

# 🚀 Future Improvements

Possible future enhancements include:

- Hyperparameter Tuning
- Cross Validation
- Feature Engineering
- Advanced Ensemble Models
- Model Deployment using Flask or Streamlit
- Interactive Web Application

---

