# Concept Drift Detection and Adaptive Retraining Pipeline

## Overview
This project demonstrates how machine learning models can lose accuracy when data distribution changes over time. It shows how to detect concept drift and retrain the model automatically.

## How to Use This Project

1. Open `concept_drift_detection_and_retraining.ipynb` in Google Colab or Jupyter Notebook.
2. Run all cells from top to bottom.
3. The notebook will generate a synthetic dataset, train a baseline model, simulate drift, detect drift using KS Test, and retrain the model.
4. Check the accuracy comparison and graphs to understand how retraining improves performance after drift.

## Requirements

Install the required libraries:

```bash
pip install numpy pandas scikit-learn scipy matplotlib seaborn
