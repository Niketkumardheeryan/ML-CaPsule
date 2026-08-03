# Mobile Price Prediction using Machine Learning

## Overview

This project aims to predict mobile phone prices using various machine learning models. By analyzing features such as brand, RAM, storage, and battery capacity, the models will help consumers decide the best time to buy a phone and assist retailers in setting prices and managing stock.

## Objectives

- Data Processing: Clean and preprocess the synthetic mobile price data.
- Model Development: Develop and train Linear Regression, Random Forest Regressor, and Support Vector Regressor models for mobile price      prediction.
- Evaluation: Assess model performance and prediction accuracy.
- Optimization: Recommend the best model based on evaluation metrics.

## Technologies Used

- Python: Programming language for development.
- Pandas: Data manipulation and analysis.
- NumPy: Numerical computing.
- Scikit-Learn: Machine learning tools for building and evaluating models.
- Matplotlib/Seaborn: Data visualization.

## Models

### Linear Regression
- *Purpose*: Predict mobile prices based on input features.
- *Architecture*: Linear model that fits a line to minimize the error between predicted and actual prices.

### Random Forest Regressor
- *Purpose*: Improve prediction accuracy by using an ensemble of decision trees.
- *Architecture*: Multiple decision trees are built on subsets of the dataset, and their predictions are averaged for final output.

### Support Vector Regressor (SVR)
- *Purpose*: Predict mobile prices by finding the best-fit hyperplane that maximizes the margin.
- *Architecture*: Uses kernel functions to handle non-linear relationships in the data.