# Diabetes Prediction using Decision Tree and Random Forest

## Overview

This project demonstrates an end-to-end machine learning workflow for predicting diabetes using the **Pima Indians Diabetes Dataset**. It covers data preprocessing, exploratory data analysis (EDA), model training, performance evaluation, and visualization of results.

The project compares two popular machine learning algorithms:

* Decision Tree Classifier
* Random Forest Classifier

It is designed for beginners who want to understand the complete workflow of a supervised classification project using a real-world healthcare dataset.

---

# Features

* Automatic dataset download using **KaggleHub**
* Data preprocessing and cleaning
* Exploratory Data Analysis (EDA)
* Correlation analysis
* Decision Tree implementation
* Random Forest implementation
* Performance comparison of multiple models
* Confusion matrix visualization
* Recall-focused evaluation for healthcare prediction

---

# Dataset

**Dataset:** Pima Indians Diabetes Dataset

**Source:** Kaggle

**Link:** https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database

The notebook downloads the dataset automatically using **KaggleHub**, so no manual dataset download is required.

### Features

* Pregnancies
* Glucose
* Blood Pressure
* Skin Thickness
* Insulin
* BMI
* Diabetes Pedigree Function
* Age

### Target Variable

**Outcome**

* **0** → Non-Diabetic
* **1** → Diabetic

---

# Project Structure

```text
Diabetes Prediction/
│
├── diabetes_prediction.ipynb
├── diabetes_graphs_visualization_and_analysis.pdf
├── README.md
```

---

# Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* KaggleHub
* Jupyter Notebook / Google Colab

---

# Project Workflow

1. Import required libraries
2. Download and load the dataset
3. Perform data preprocessing
4. Conduct Exploratory Data Analysis (EDA)
5. Analyze feature correlations
6. Split the dataset into training and testing sets
7. Train the Decision Tree model
8. Train the Random Forest model
9. Evaluate both models
10. Compare model performance through visualizations

---

# Machine Learning Models

## Decision Tree Classifier

A tree-based supervised learning algorithm used as the baseline classification model.

## Random Forest Classifier

An ensemble learning algorithm that combines multiple decision trees to improve prediction accuracy and reduce overfitting.

---

# Evaluation Metrics

The models are evaluated using:

* Accuracy
* Precision
* Recall
* F1-Score
* Confusion Matrix

Since this is a healthcare classification problem, **Recall** is given special importance because correctly identifying diabetic patients helps minimize false negatives.

---

# Visualizations

The notebook includes the following visualizations:

* Target class distribution
* Correlation heatmap
* Decision Tree confusion matrix
* Random Forest confusion matrix
* Model recall comparison

---

# Results

Both models successfully classify diabetic and non-diabetic patients.

The **Random Forest Classifier** achieved better recall than the **Decision Tree Classifier**, making it the preferred model for this dataset.

---

# Prerequisites

Install the required libraries before running the notebook.

```bash
pip install kagglehub 
```
Also pandas numpy matplotlib seaborn scikit-learn

---

# How to Run

1. Clone this repository.
2. Open `diabetes_prediction.ipynb` in **Jupyter Notebook** or **Google Colab**.
3. Install the required Python libraries.
4. Run all notebook cells sequentially.
5. The dataset will be downloaded automatically using **KaggleHub**.
6. Review the generated evaluation metrics and visualizations.

---

# Output

Running the notebook generates:

* Processed dataset
* Exploratory Data Analysis
* Correlation Heatmap
* Classification Reports
* Confusion Matrices
* Performance Comparison
* Recall Comparison Graph

---

# Learning Outcomes

This project demonstrates:

* Data preprocessing
* Exploratory Data Analysis
* Feature engineering concepts
* Supervised machine learning
* Model evaluation
* Performance comparison between multiple classifiers
* Healthcare data prediction using machine learning
