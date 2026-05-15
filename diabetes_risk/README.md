# Pima Indians Diabetes Prediction

This repository contains a machine learning pipeline to predict diabetes onset based on medical metrics.

## Project Overview
The goal is to classify patients as diabetic or non-diabetic using features like Insulin levels, BMI, and Age. We achieve ~80% accuracy using ensemble methods.

## Dataset Info
- **Source:** Pima Indians Diabetes Database (Kaggle/UCI).
- **Instances:** 768
- **Attributes:** 8 numerical features, 1 target (Outcome).

## Folder Structure
- `dataset/`: Contains `diabetes.csv`.
- `diabetes_prediction.ipynb`: Main analysis and modeling.
- `README.md`: Project documentation.
- `requirements.txt`: Libraries to be installed.

## Setup Steps
1. Clone the repo.
2. Install requirements: `pip install -r requirements.txt`.
3. Open `diabetes_prediction.ipynb` and run all cells.

## Model Results
| Model               | Accuracy | Precision | Recall | F1-Score |
| ------------------- | -------: | --------: | -----: | -------: |
| Random Forest       |   0.7792 |    0.7273 | 0.5926 |   0.6531 |
| XGBoost             |   0.7597 |    0.6735 | 0.6111 |   0.6408 |
| KNN                 |   0.7532 |    0.6600 | 0.6111 |   0.6346 |
| SVM                 |   0.7338 |    0.6444 | 0.5370 |   0.5859 |
| Logistic Regression |   0.7013 |    0.5870 | 0.5000 |   0.5400 |


## Visuals
The notebook includes Correlation Heatmaps, Feature Distributions, and ROC curves to compare model sensitivity.