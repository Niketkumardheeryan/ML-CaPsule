# ChurnScope — Telco Customer Churn Prediction

## Dataset
- Source: IBM Watson Telco Customer Churn dataset (7,043 customers, 21 attributes)
- The notebook downloads the dataset via the Kaggle API:
- Link: https://www.kaggle.com/datasets/blastchar/telco-customer-churn

This project predicts customer churn for a telecom company using classical machine learning techniques. It analyzes customer account details, subscription services, tenure, and billing information to identify which customers are most likely to cancel, and builds a model to predict churn probability with high recall so at-risk customers aren't missed.

## Key Features
1. Data cleaning and missing value handling (`TotalCharges`)
2. Exploratory data analysis of churn drivers
3. Custom engineered features (EasyLeaver, FiberNoAddons, SoloCustomer, NoProtection, HighRiskCombo)
4. Preprocessing pipeline with StandardScaler, OneHotEncoder, and ColumnTransformer
5. Class imbalance handling using SMOTE
6. Model comparison across Logistic Regression, Random Forest, Gradient Boosting, and XGBoost
7. Final model: Gradient Boosting Classifier (ROC-AUC 84.0%, churn recall 78%)
8. Feature importance analysis to identify top churn drivers

## Tech Stack
- Python
- Pandas, NumPy
- Matplotlib (visualization)
- Scikit-learn (Logistic Regression, Random Forest, Gradient Boosting, preprocessing)
- XGBoost
- imbalanced-learn (SMOTE)
- kaggle (dataset download)

## Usage
1. Open `Churn_Prediction.ipynb` in Jupyter Notebook.
2. Run all cells (requires the `kaggle` package and a `kaggle.json` API token to download `WA_Fn-UseC_-Telco-Customer-Churn.csv`).
3. Review the EDA plots, model comparison table, and churn probability outputs.