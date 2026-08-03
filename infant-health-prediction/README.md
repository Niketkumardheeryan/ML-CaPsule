# Infant Health Prediction

## Overview
This repository contains code for predicting infant health based on synthetic infant health data. The prediction is made using various machine learning models, including logistic regression, decision trees, random forests, k-nearest neighbors (KNN), Gaussian Naive-Bayes, AdaBoostClassifier, GradientBoostingClassifier, and XGBoostClassifier.

## Dataset
This is a dataset of infant's health that has been synthetically generated. 
It includes various details about the infants, such as ChestXray, BodyO2, BodyCO2, Birth Diseases and Age (in days).

Link to the dataset: [Synthetic Infant Health Dataset](https://www.kaggle.com/datasets/bhavkaur/synthetic-infant-health-dataset)

## Prerequisites
- Python 3.6+
- numpy
- pandas
- matplotlib
- seaborn
- scipy
- statsmodels
- scikit-learn
- xgboost

## Models Used

**1. Logistic Regression:** A logistic regression model is trained and evaluated for both training and test sets. ROC curves are plotted to assess model performance.

**2. Decision Tree:** A decision tree classifier is trained and evaluated similarly to logistic regression.

**3. Random Forest:** A random forest classifier is trained and evaluated. Feature importances are visualized using bar plots.

**4. K-Nearest Neighbors (KNN):** The KNN classifier is trained and evaluated.

**5. Gaussian Naive-Bayes:** The Gaussian Naive-Bayes classifier is trained and evaluated.

**6. Boosting Algorithms:** AdaBoostClassifier and GradientBoostingClassifier are implemented using base estimators (Logistic Regression, Decision Tree, Random Forest, and Gaussian Naive-Bayes). Training and test scores are compared across models.

**7. XGBoostClassifier:** An XGBoostClassifier is trained and evaluated.

## Results
Model accuracies and ROC scores are reported for each model, highlighting their performance in predicting infant health based on the provided dataset.

## Contribution
Contributions are welcome! Feel free to submit issues, feature requests, or pull requests to improve the system.