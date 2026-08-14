# Customer Churn Prediction

A machine learning project that predicts whether a telecom customer is likely to churn based on their demographics, services, contract details, tenure, and billing information.

## Problem Statement

Customer churn is a major challenge for subscription-based businesses. Identifying customers who are likely to leave allows businesses to take preventive measures, improve customer retention, and potentially reduce revenue loss.

This project performs exploratory data analysis and builds multiple classification models to predict customer churn. The models are evaluated using metrics such as Precision, Recall, F1-Score, and ROC-AUC, with particular attention to identifying customers who are likely to churn.

## Dataset

The project uses the **Telco Customer Churn** dataset.

The dataset contains:

- **7,043 customer records**
- **21 columns**
- Demographic information
- Service information
- Contract details
- Billing information
- Customer tenure

The target variable is:

- `Churn` — whether the customer has churned (`Yes`/`No`)

## Data Preprocessing

The following preprocessing steps were performed:

- Inspected data types and missing values
- Checked for duplicate records
- Converted `TotalCharges` from string to numeric
- Identified 11 blank/invalid `TotalCharges` values
- Handled invalid `TotalCharges` values
- Encoded the target variable
- Applied preprocessing to numerical and categorical features
- Applied class/sample weighting to account for class imbalance
- Split the dataset into training and testing sets

After preprocessing:

- **7,043 observations**
- **19 predictive features**

### Train-Test Split

| Dataset | Samples |
|---|---:|
| Training | 5,634 |
| Testing | 1,409 |

The split was performed using stratification to preserve the churn distribution across the training and testing sets.

## Exploratory Data Analysis

The target distribution was:

| Churn | Customers | Percentage |
|---|---:|---:|
| No | 5,174 | 73.46% |
| Yes | 1,869 | 26.54% |

Several important patterns were observed during EDA:

- Month-to-month contract customers had substantially higher churn.
- Customers with one-year and two-year contracts had considerably lower churn.
- Fiber optic customers showed higher churn than DSL customers.
- Customers without Online Security or Tech Support showed higher churn rates.
- Senior citizens had a higher churn rate than non-senior citizens.
- Customers with shorter tenure were more likely to churn.
- Customers with higher monthly charges showed a higher tendency to churn.
- Electronic check users showed a notably higher churn rate than customers using other payment methods.

These patterns were used to better understand the factors associated with customer churn and guide the modelling process.

## Models

Three classification algorithms were evaluated:

1. Logistic Regression
2. Random Forest
3. XGBoost

### Model Comparison

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8055 | 0.6572 | 0.5588 | 0.6040 | 0.8421 |
| Random Forest | 0.7708 | 0.5606 | 0.6310 | 0.5937 | 0.8220 |
| XGBoost | 0.7544 | 0.5255 | 0.7727 | 0.6255 | **0.8445** |
| XGBoost (Tuned) | 0.7729 | 0.5529 | **0.7540** | **0.6380** | **0.8445** |

## Threshold Optimization

For churn prediction, the default probability threshold of `0.50` does not necessarily provide the best balance between identifying churners and avoiding false positives.

Therefore, the XGBoost prediction threshold was evaluated across different values using the F1-Score as the optimization criterion.

The best threshold was:

**0.54**

At this threshold:

- **Precision:** 0.5529
- **Recall:** 0.7540
- **F1-Score:** 0.6380
- **Accuracy:** 0.7729
- **ROC-AUC:** 0.8445

The tuned threshold improved the F1-Score from **0.6255 to 0.6380**, providing a better balance between precision and recall for churn prediction.

## Model Selection

The final model selected for the project is:

**XGBoost with a classification threshold of 0.54**

XGBoost achieved the highest ROC-AUC among the evaluated models and provided strong recall for the churn class.

For a customer churn problem, recall is particularly important because failing to identify a customer who is likely to churn can mean losing an opportunity to intervene and retain that customer.

## Feature Importance

XGBoost feature importance analysis identified several features that contributed strongly to the model's predictions.

The most important features included:

1. Contract — Month-to-month
2. Internet Service — Fiber optic
3. Online Security
4. Tech Support
5. Contract — Two year
6. Internet Service — DSL
7. Payment Method — Electronic check
8. Streaming Movies
9. Contract — One year
10. Tenure

The strongest feature was:

**Contract — Month-to-month**

This is also consistent with the EDA, where month-to-month customers showed substantially higher churn rates than customers on longer-term contracts.

## Saved Model

The trained XGBoost model and its configuration are saved for potential reuse:

- `xgb_churn_model.pkl`
- `model_config.pkl`

## Project Structure

```text
Customer-Churn-Prediction/
│
├── data/
│   └── customer_churn.csv
│
├── notebook/
│   └── Customer_Churn_Prediction.ipynb
│
├── xgb_churn_model.pkl
├── model_config.pkl
├── requirements.txt
└── README.md
