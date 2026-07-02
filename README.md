# Concept Drift Detection and Adaptive Retraining Pipeline

## Overview
This project demonstrates concept drift detection using a real machine learning dataset and an adaptive retraining pipeline.

## Dataset Used
The project uses the Breast Cancer Wisconsin Dataset from Scikit-learn.

The dataset contains numerical medical features computed from digitized images of breast mass samples. The task is to classify whether a tumor is malignant or benign.

## Model Used
The project uses a Random Forest Classifier as the baseline machine learning model.

## How to Use This Project

1. Open `concept_drift_detection_and_retraining.ipynb` in Google Colab or Jupyter Notebook.
2. Run all cells from top to bottom.
3. The notebook will:
   - Load the Breast Cancer Wisconsin dataset.
   - Train a Random Forest classification model.
   - Evaluate baseline model performance.
   - Simulate feature drift in selected features.
   - Detect drift using the Kolmogorov-Smirnov test.
   - Retrain the model after drift is detected.
   - Compare model accuracy before and after retraining.

## Features
- Real dataset usage
- Random Forest model training
- Data drift simulation
- KS-test based drift detection
- Adaptive retraining
- Accuracy comparison
- Visualization of drift and performance changes

## Requirements
```bash
pip install pandas numpy scikit-learn matplotlib seaborn scipy joblib
