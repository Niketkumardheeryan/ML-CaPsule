# Mumbai_House_Price_Predictor

# Project Overview
This project builds a machine learning pipeline to predict house prices in Mumbai using structured property data. It demonstrates end‑to‑end workflow: data cleaning, feature engineering, encoding, model training, and evaluation.

The final model achieves an R² score of ~0.91 on test data, showing strong predictive performance.

# Dataset
Rows: 71,938
Columns: 15 (before dropping latitude/longitude)
https://www.kaggle.com/datasets/dravidvaishnav/mumbai-house-prices

# Key Notes:
The dataset contains a very large number of unique titles and localities (high cardinality).
→ We used Target Encoding instead of One‑Hot Encoding to avoid exploding the feature space.
The dataset had many outliers in features like area, price_per_sqft, and balcony_num.
→ We applied capping (winsorization) to limit extreme values while preserving the overall distribution, as seen in the boxplots and KDE graphs.

# Features include:
title, locality, city, property_type, furnished
area, price_per_sqft, bedroom_num, bathroom_num, balcony_num, age, total_floors
Target: price

# Preprocessing
Handled skewness in numerical features using np.log1p.
Dropped latitude/longitude due to extreme skewness.

# Encoding strategies:
StandardScaler for numerical features
OneHotEncoder for city, property_type
OrdinalEncoder for furnished (Unfurnished → Semi‑Furnished → Furnished)
TargetEncoder for title and locality (high cardinality)

Outlier treatment: Applied capping to ensure data distributions remain realistic without distortion.

#  Models Tried and their Results
Model	R² Score (Test)
Linear Regression	~0.78
SGD Regressor	~0.80
Decision Tree Regressor	~0.84
Random Forest Regressor	~0.87
Support Vector Regressor	~0.85
XGBoost Regressor	0.91 (Best)

Training vs. Test R² scores for XGBoost are close (0.9138 vs. 0.9127), showing no major overfitting.
XGBoost consistently outperformed other models by capturing complex feature interactions and handling skewness/outliers effectively.

# Visualizations
Scatter plots of Actual vs. Predicted Prices for train and test sets.
KDE plots and boxplots to analyze skewness and outliers.
Bar plots for top localities, property types, and furnishing categories.

