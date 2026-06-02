# Explainable Loan Default Risk Prediction System

This project predicts whether a loan applicant is likely to default and explains the prediction with SHAP values. It includes a complete tabular machine learning workflow and an interactive Streamlit dashboard for risk scoring.

## Features

- Synthetic loan applicant dataset generation for reproducible demos
- Data loading and preprocessing with missing-value handling
- Categorical encoding and numeric scaling through scikit-learn pipelines
- Logistic Regression, Random Forest, and Gradient Boosting model comparison
- Accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrix reporting
- SHAP-based global feature importance and local prediction explanations
- Streamlit dashboard for applicant input, risk category, and feature contributions

## Project Structure

```text
Explainable Loan Default Risk Prediction/
├── app.py
├── requirements.txt
├── README.md
└── src/
    └── loan_default_pipeline.py
```

## Dataset

The project generates a realistic synthetic loan dataset when no CSV is provided. The generated data contains borrower and loan attributes such as age, income, employment length, loan amount, interest rate, debt-to-income ratio, credit history, missed payments, employment status, education level, loan purpose, and property area.

Target column:

- `default`: `1` for likely default, `0` for non-default

You can replace the synthetic data with a real CSV by updating `DATA_PATH` in `app.py` or importing the helpers from `src/loan_default_pipeline.py`.

## Setup

```bash
pip install -r requirements.txt
```

## Run The Dashboard

```bash
streamlit run app.py
```

## Train And Evaluate From Python

```python
from src.loan_default_pipeline import build_dataset, train_models

data = build_dataset()
result = train_models(data)

print(result.metrics)
print(result.best_model_name)
```

## Workflow

1. Generate or load loan applicant data.
2. Split the dataset into train and test sets.
3. Impute missing values, scale numeric columns, and one-hot encode categorical columns.
4. Train Logistic Regression, Random Forest, and Gradient Boosting models.
5. Select the best model using ROC-AUC.
6. Explain global model behavior and individual predictions with SHAP.
7. Serve the selected model through a Streamlit dashboard.

## Model Evaluation

The training pipeline reports:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion matrix

These metrics are suitable for a binary financial risk classification problem where false negatives and false positives both matter.

## SHAP Explainability

The dashboard shows:

- Top global drivers of default risk
- Applicant-specific feature contribution chart
- Default probability and risk tier

For tree-based models, SHAP values are calculated using `shap.TreeExplainer`. For Logistic Regression, the project uses `shap.Explainer` over the transformed feature matrix.

## Risk Tiers

- Low Risk: default probability below `0.35`
- Medium Risk: default probability from `0.35` to `0.65`
- High Risk: default probability above `0.65`

## Notes

This project is intended for education and experimentation. It should not be used for real credit decisions without validated real-world data, fairness checks, compliance review, and monitoring.
