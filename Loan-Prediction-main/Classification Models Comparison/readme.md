# 🏦 Loan Prediction using Machine Learning

## 📌 Overview

This project demonstrates **Loan Approval Prediction** using supervised machine learning algorithms. The goal is to predict whether a loan application will be **Approved** or **Rejected** based on an applicant's financial, personal, and credit-related information.

The notebook covers the complete machine learning pipeline, including data preprocessing, exploratory data analysis (EDA), feature engineering, model training, evaluation, and prediction using multiple classification algorithms.

---

## 📂 Dataset

The dataset is hosted on **GitHub Gist**.

### Dataset Link

https://gist.githubusercontent.com/semicolonSimp/c0c6d036efa489d9c896c8851c3b3de7/raw/c9446e0d053dd6c6fd0988eb9cb498f8814d3ad8/Filename:%2520loan_approval_data.csv

### Load Dataset

```python
import pandas as pd

url = "https://gist.githubusercontent.com/semicolonSimp/c0c6d036efa489d9c896c8851c3b3de7/raw/c9446e0d053dd6c6fd0988eb9cb498f8814d3ad8/Filename:%2520loan_approval_data.csv"

df = pd.read_csv(url)
```

---

## 🚀 Features

- Data Preprocessing
- Missing Value Handling
- Exploratory Data Analysis (EDA)
- Feature Encoding
- Feature Scaling
- Train-Test Split
- Model Training
- Model Evaluation
- Loan Approval Prediction
- Comparison of Multiple Machine Learning Models

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

---

## 🤖 Machine Learning Models

The following models are implemented and compared:

- Logistic Regression
- K-Nearest Neighbors (KNN)
- Naive Bayes

---

## 📊 Workflow

1. Load the dataset from GitHub Gist.
2. Explore the dataset.
3. Handle missing values.
4. Encode categorical features.
5. Scale numerical features.
6. Split the dataset into training and testing sets.
7. Train Logistic Regression, KNN, and Naive Bayes models.
8. Evaluate each model.
9. Compare model performance.
10. Predict loan approval for new applicants.

---

## 📈 Dataset Features

The dataset contains the following attributes:

- Applicant Income
- Co-applicant Income
- Employment Status
- Age
- Marital Status
- Dependents
- Credit Score
- Existing Loans
- Debt-to-Income Ratio (DTI Ratio)
- Savings
- Collateral Value
- Loan Amount
- Loan Term
- Loan Purpose
- Property Area
- Education Level
- Gender
- Employer Category
- **Loan Approved (Target Variable)**

---

## 📊 Output

The notebook produces:

- Cleaned Dataset
- Encoded Dataset
- Scaled Features
- Trained Models
- Accuracy Scores
- Confusion Matrix
- Classification Report
- Loan Approval Predictions

---

## 📌 Project Structure

```
Loan_prediction/
│── credit_wise.ipynb
│── README.md
```

> **Note:** The dataset is intentionally **not included** in this repository. It is loaded directly from the GitHub Gist link provided above.

---

## 🎯 Applications

- Loan Approval Prediction
- Credit Risk Assessment
- Banking Analytics
- Financial Decision Support
- Loan Eligibility Prediction
- Risk Management

---

## 📚 Learning Outcomes

By completing this project, you will learn:

- Data Cleaning
- Data Preprocessing
- Feature Engineering
- Feature Scaling
- Exploratory Data Analysis (EDA)
- Logistic Regression
- K-Nearest Neighbors (KNN)
- Naive Bayes
- Model Evaluation
- Confusion Matrix
- Classification Report

---

## ▶️ How to Run

1. Clone the repository.

```bash
git clone <repository-url>
```

2. Install the required libraries.

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

3. Open the notebook.

```bash
jupyter notebook credit_wise.ipynb
```

4. Run all cells.

