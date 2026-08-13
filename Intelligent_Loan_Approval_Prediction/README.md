# Loan Approval Prediction

A beginner-friendly Machine Learning project that predicts whether a loan application will be **approved or rejected** based on applicant information such as income, education, credit history, loan amount, and property area.

## Project Overview

Loan approval is a classification problem where the model learns from previous loan applications and predicts the outcome for a new applicant.

### Prediction

* `1` → Loan Approved
* `0` → Loan Rejected

The project compares multiple classification algorithms and uses preprocessing, feature engineering, SMOTE, and hyperparameter optimization to improve the prediction model.

---

## Dataset

The project uses `loan-train.csv`.
link: https://www.kaggle.com/datasets/dingxinlong/loan-data-setcsv

### Dataset Size

* **614 rows**
* **13 original columns**

### Important Features

| Feature             | Description                            |
| ------------------- | -------------------------------------- |
| `Loan_ID`           | Unique ID of the loan application      |
| `Gender`            | Gender of the applicant                |
| `Married`           | Marital status                         |
| `Dependents`        | Number of dependents                   |
| `Education`         | Education level                        |
| `Self_Employed`     | Whether the applicant is self-employed |
| `ApplicantIncome`   | Income of the applicant                |
| `CoapplicantIncome` | Income of the co-applicant             |
| `LoanAmount`        | Requested loan amount                  |
| `Loan_Amount_Term`  | Loan repayment term                    |
| `Credit_History`    | Credit history indicator               |
| `Property_Area`     | Location type of the property          |
| `Loan_Status`       | Target variable                        |

---

## Machine Learning Workflow

The project follows these main steps:

```text
Load Dataset
     ↓
Exploratory Data Analysis
     ↓
Check Missing Values & Duplicates
     ↓
Feature Engineering
     ↓
Train-Test Split
     ↓
Data Preprocessing
     ↓
Handle Class Imbalance using SMOTE
     ↓
Train Multiple ML Models
     ↓
Evaluate Models
     ↓
Hyperparameter Optimization
     ↓
Final Random Forest Model
```

---

## 1. Data Loading

The dataset is loaded using Pandas:

```python
data = pd.read_csv('loan-train.csv')
```

The dataset contains **614 loan applications and 13 columns**.

---

## 2. Exploratory Data Analysis

The notebook performs basic data analysis using:

* `data.shape`
* `data.info()`
* `data.describe()`
* Missing-value percentage
* Duplicate checking
* Correlation analysis
* Distribution/count plots
* Feature vs. target visualizations

### Missing Values

Some columns contain missing values.

The highest missing-value percentage is in:

* `Credit_History` → approximately **8.14%**
* `Self_Employed` → approximately **5.21%**
* `LoanAmount` → approximately **3.58%**

No duplicate rows were found in the dataset.

---

## 3. Feature Engineering

Two new features are created.

### Total Income

Applicant and co-applicant income are combined:

```python
data['Total_Income'] = data['ApplicantIncome'] + data['CoapplicantIncome']
```

### Income-to-Loan Ratio

A ratio between total income and loan amount is calculated:

```python
data['Income_Loan_Ratio'] = data['Total_Income'] / data['LoanAmount']
```

These features provide additional information about the applicant's financial situation.

---

## 4. Dependents Transformation

The original `Dependents` column contains values such as:

```text
0
1
2
3+
```

Missing values are replaced with `0`, and `3+` is converted to `3`.

The values are then grouped into three categories:

| Dependents | Category       |
| ---------- | -------------- |
| 0          | Single         |
| 1 or 2     | Nuclear family |
| 3 or more  | Large family   |

This makes the feature easier to process as an ordinal categorical variable.

---

## 5. Target Encoding

The original target column contains:

```text
Y → Approved
N → Rejected
```

It is converted into numerical values:

```text
Y → 1
N → 0
```

This allows classification algorithms to work with the target variable.

---

## 6. Train-Test Split

The dataset is divided into training and testing sets:

```python
x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    random_state=42,
    test_size=0.2
)
```

### Split

* **80%** → Training data
* **20%** → Testing data
* `random_state = 42`

The test set contains **123 records**.

---

## 7. Data Preprocessing

A `ColumnTransformer` is used to apply different preprocessing techniques to different types of features.

### Categorical Features

One-hot encoding is applied to:

```text
Gender
Married
Self_Employed
Education
Property_Area
```

Missing categorical values are filled using the **most frequent value**.

```python
SimpleImputer(strategy='most_frequent')
```

Then:

```python
OneHotEncoder(handle_unknown='ignore')
```

is used.

### Ordinal Feature

`Dependents` is processed using:

```python
OrdinalEncoder()
```

with the categories:

```text
Single
Nuclear family
Large family
```

### Numerical Features

Missing numerical values are handled using:

* Mean imputation for `LoanAmount`
* Most-frequent imputation for `Loan_Amount_Term`, `Credit_History`, and `Income_Loan_Ratio`

`PowerTransformer` with the **Yeo-Johnson transformation** is also used for several numerical features.

`StandardScaler` is used for selected income-related features.

---

## 8. Handling Class Imbalance

The project uses **SMOTE (Synthetic Minority Over-sampling Technique)** with the Logistic Regression pipeline and during Random Forest hyperparameter optimization.

SMOTE creates synthetic samples for the minority class so that the model gets a more balanced training dataset.

```python
SMOTE(random_state=42)
```

This is especially useful when one loan-status class has fewer examples than the other.

---

## 9. Machine Learning Models

The project evaluates multiple classification algorithms.

### Models Used

1. Logistic Regression
2. Random Forest
3. Gradient Boosting
4. XGBoost
5. Decision Tree
6. Optimized Random Forest

---

## 10. Model Performance

The models were evaluated using **accuracy** and **classification reports**.

| Model                       |   Accuracy |
| --------------------------- | ---------: |
| Logistic Regression + SMOTE |     75.61% |
| Random Forest               |     80.49% |
| Gradient Boosting           |     78.86% |
| XGBoost                     |     75.61% |
| Decision Tree               |     78.05% |
| Optimized Random Forest     | **80.49%** |

The best test accuracy obtained in the notebook is **80.49%**.

---

## 11. Hyperparameter Optimization

The Random Forest model is further optimized using **Optuna**.

The following parameters are searched:

* `n_estimators`
* `max_depth`
* `min_samples_split`
* `min_samples_leaf`
* `max_features`

The optimization runs for:

```python
50 trials
```

The best parameters found were:

```python
{
    'n_estimators': 409,
    'max_depth': 13,
    'min_samples_split': 6,
    'min_samples_leaf': 4,
    'max_features': None
}
```

These parameters are used to create the final Random Forest model.

---

## 12. Final Model

The final model is an optimized Random Forest classifier:

```python
RandomForestClassifier(
    n_estimators=409,
    max_depth=13,
    min_samples_split=6,
    min_samples_leaf=4,
    max_features=None,
    random_state=42
)
```

The final model achieved:

```text
Test Accuracy: 80.49%
```

---

## 13. Evaluation Metrics

The project uses:

### Accuracy

Measures the percentage of total predictions that are correct.

```text
Accuracy = Correct Predictions / Total Predictions
```

### Precision

Measures how many predicted positive cases were actually positive.

### Recall

Measures how many actual positive cases were correctly identified.

### F1-Score

Combines precision and recall into a single metric.

The notebook uses:

```python
accuracy_score()
classification_report()
```

---

## 14. Technologies Used

### Programming Language

* Python

### Libraries

* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Imbalanced-learn
* XGBoost
* Optuna

### Machine Learning Techniques

* Classification
* Feature Engineering
* One-Hot Encoding
* Ordinal Encoding
* Missing Value Imputation
* Standardization
* Yeo-Johnson Power Transformation
* SMOTE
* Random Forest
* Hyperparameter Optimization

---

## 15. Project Structure

```text
Loan-Approval-Prediction/
│
├── Loan_Approval_Prediction.ipynb
├── loan-train.csv
└── README.md
```

---

## 16. How to Run the Project

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
```

### Step 2: Open the Project

```bash
cd Loan-Approval-Prediction
```

### Step 3: Install Required Libraries

```bash
pip install pandas numpy matplotlib seaborn scikit-learn imbalanced-learn xgboost optuna
```

### Step 4: Make Sure the Dataset Exists

Place:

```text
loan-train.csv
```

in the same directory as the notebook.

### Step 5: Open the Notebook

You can use:

* Jupyter Notebook
* JupyterLab
* Google Colab
* VS Code

### Step 6: Run the Notebook

Run the cells from top to bottom.

---

## 17. What a Beginner Can Learn

This project demonstrates a complete beginner-to-intermediate Machine Learning workflow.

You can learn:

* How to load a CSV dataset
* How to inspect a dataset
* How to identify missing values
* How to check duplicate records
* How to perform basic EDA
* How to create new features
* How to encode categorical variables
* How to split data into training and testing sets
* How to build preprocessing pipelines
* How SMOTE handles class imbalance
* How to train classification models
* How to compare different models
* How to evaluate classification results
* How to optimize model hyperparameters using Optuna
* How to build a final Random Forest model

---

## 18. Key Takeaway

The goal of this project is to use applicant information to predict whether a loan application is likely to be approved.

The project compares several machine learning algorithms and finds that the **optimized Random Forest model** provides the best test accuracy among the models evaluated in the notebook, achieving approximately **80.49% accuracy**.

> **Note:** This project is intended for educational and machine-learning practice purposes. Loan approval decisions in real-world financial systems require additional validation, fairness checks, regulatory considerations, and domain-specific risk assessment.
