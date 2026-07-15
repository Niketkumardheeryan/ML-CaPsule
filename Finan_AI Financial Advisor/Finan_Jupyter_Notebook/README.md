# 📊 Finan AI Financial Advisor – Machine Learning Jupyter Notebook

## 📌 Overview

This notebook contains the complete machine learning workflow behind the Finan-AI Financial Advisor project. It provides a documented and reproducible pipeline for developing models that analyze financial behavior and generate personalized financial insights based on an Indian financial dataset.

The notebook includes data preprocessing, exploratory analysis, model training, evaluation, and prediction procedures for two complementary machine learning tasks:

* **Financial State Prediction** using a **Support Vector Classifier (SVC)**.
* **Suggested Monthly Budget Prediction** using a **Random Forest Regressor**.

The objective is to model real-world financial scenarios and provide data-driven recommendations that promote better budgeting and financial awareness.

---

# 🚀 Objectives

* 📈 Predict a user's overall financial state.
* 💰 Estimate an appropriate monthly budget.
* 🇮🇳 Model financial behavior based on Indian economic patterns.
* 📚 Provide a transparent and reproducible machine learning workflow.
* 🔬 Enable experimentation and future model improvements.

---

# 🧠 Machine Learning Models

## 📊 Financial State Prediction

### Model

* **Support Vector Classifier (SVC)**

### Task

Multi-class classification

### Purpose

Classify users into different financial categories based on their income and expenditure characteristics.

### Input Features

* Monthly Income
* Cost of Living Expenditure
* Investment Expenditure
* Consumerist Expenditure
* Crisis Shock Expenditure
* Debt Status

### Output

Financial state categories such as:

* 📈 High-Rate Saver
* 📉 Low-Rate Saver
* ⚖️ Balanced Financial State
* 💳 Debt-Driven Financial State

---

## 💵 Suggested Monthly Budget Prediction

### Model

* **Random Forest Regressor**

### Task

Regression

### Purpose

Estimate a recommended monthly budget based on financial attributes and spending behavior.

### Target Variable

* Suggested Monthly Budget

### Objective

Support users in maintaining sustainable expenditure patterns and improving financial planning.

---

# 🇮🇳 Dataset Characteristics

The models are trained on a custom dataset designed to reflect realistic Indian financial conditions.

### Features Included

* Monthly Income
* Cost of Living Expenses
* Investment Expenditure
* Consumer Spending
* Crisis-Related Expenses
* Debt Status
* Financial State Categories
* Current Monthly Income Enough or Not
* Current Expenditure Worth it or Not
* Suggested Monthly Budget

The dataset captures various spending behaviors and financial situations commonly observed in the Indian economic landscape.

---

# ⚙️ Workflow

## 📂 Data Preparation

* Data cleaning
* Feature selection
* Encoding categorical variables
* Dataset preprocessing

## 📈 Exploratory Data Analysis

* Understanding feature distributions
* Examining relationships between variables
* Identifying financial patterns

## 🤖 Model Training

### Financial State Prediction

* Support Vector Classifier (SVC)

### Suggested Budget Prediction

* Random Forest Regressor

## 📊 Model Evaluation

* Classification metrics for SVC
* Regression metrics for Random Forest
* Performance analysis and validation

## 🔍 Prediction Pipeline

* User input preprocessing
* Feature transformation
* Model inference
* Financial state and budget prediction

---

# 🛠️ Libraries and Technologies

### Programming Language

* Python

### Data Processing

* Pandas
* NumPy

### Machine Learning

* Scikit-learn

  * Support Vector Classifier (SVC)
  * Random Forest Regressor

### Model Evaluation

* Classification Report
* Confusion Matrix

### Notebook Environment

* Jupyter Notebook

---

# 📚 Documentation

The notebook is structured with detailed explanations and comments to improve readability and reproducibility. Each stage of the machine learning pipeline is documented to help contributors understand:

* Data preprocessing techniques
* Feature engineering steps
* Model selection rationale
* Training methodology
* Evaluation procedures
* Prediction mechanisms

---

# 🎯 Project Goal

To develop interpretable machine learning models that can classify financial conditions and estimate monthly budgets using an Indian finance-oriented dataset, while maintaining a transparent and well-documented workflow suitable for learning, experimentation, and future enhancements.
