\# Customer Churn Prediction



A machine learning project for predicting customer churn using customer demographics, account information, services, contract details, and billing information.



\## Problem Statement



Customer churn is a major concern for subscription-based businesses. Identifying customers who are likely to leave can help businesses take preventive actions and improve customer retention.



This project analyzes customer behavior and builds machine learning models to predict whether a customer is likely to churn.



\## Dataset



The dataset contains 7,043 customer records and 21 columns.



The target variable is:



\- `Churn` — whether the customer has churned (`Yes`/`No`)



The dataset contains demographic, service, contract, and billing information.



\## Data Preprocessing



The following preprocessing steps were performed:



\- Inspected data types and missing values

\- Checked for duplicate records

\- Converted `TotalCharges` from string to numeric

\- Identified 11 blank/invalid `TotalCharges` values

\- Handled invalid `TotalCharges` values

\- Encoded the target variable

\- Applied preprocessing to numerical and categorical features

\- Split the data into training and testing sets



The final dataset contained:



\- 7,043 observations

\- 19 predictive features



The train-test split was:



\- Training: 5,634 samples

\- Testing: 1,409 samples



\## Exploratory Data Analysis



The dataset contains:



\- 5,174 customers who did not churn (73.46%)

\- 1,869 customers who churned (26.54%)



Important patterns observed during EDA:



\- Month-to-month contract customers had substantially higher churn.

\- Customers with one-year and two-year contracts had much lower churn.

\- Fiber optic customers showed higher churn than DSL customers.

\- Customers without online security or technical support showed higher churn.

\- Senior citizens had a higher churn rate than non-senior citizens.

\- Customers with shorter tenure were more likely to churn.

\- Customers with higher monthly charges showed higher churn tendency.



\## Models



Three machine learning models were evaluated:



1\. Logistic Regression

2\. Random Forest

3\. XGBoost



\### Model Comparison



| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |

|---|---:|---:|---:|---:|---:|

| Logistic Regression | 0.8055 | 0.6572 | 0.5588 | 0.6040 | 0.8421 |

| Random Forest | 0.7708 | 0.5606 | 0.6310 | 0.5937 | 0.8220 |

| XGBoost | 0.7544 | 0.5255 | 0.7727 | 0.6255 | 0.8445 |

| XGBoost (Tuned) | 0.7729 | 0.5529 | 0.7540 | 0.6380 | 0.8445 |



\## Threshold Optimization



The default classification threshold of 0.50 was evaluated using precision, recall, and F1-score across different thresholds.



The best threshold based on F1-score was:



\*\*0.54\*\*



At this threshold:



\- Precision: 0.5529

\- Recall: 0.7540

\- F1-Score: 0.6380

\- Accuracy: 0.7729



The tuned threshold provides a better balance between precision and recall for the churn prediction task.



\## Final Model



The final model selected for the project is:



\*\*XGBoost with a classification threshold of 0.54\*\*



The model was selected because of its strong churn recall, F1-score, and ROC-AUC performance.



\## Feature Importance



The most important features identified by XGBoost include:



1\. Contract — Month-to-month

2\. Internet Service — Fiber optic

3\. Online Security

4\. Tech Support

5\. Contract — Two year

6\. Internet Service — DSL

7\. Payment Method — Electronic check

8\. Streaming Movies

9\. Contract — One year

10\. Tenure



The strongest feature was the month-to-month contract category.



\## Project Structure



```text

Customer-Churn-Prediction/

│

├── data/

│   └── customer\_churn.csv

│

├── notebook/

│   └── Churn\_Prediction.ipynb

│

├── xgb\_churn\_model.pkl

├── model\_config.pkl

└── README.md

