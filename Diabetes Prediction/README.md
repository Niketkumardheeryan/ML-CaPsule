# Diabetes Prediction using Decision Tree and Random Forest

## Overview

This project demonstrates a complete machine learning workflow for predicting diabetes using the Pima Indians Diabetes Dataset. It includes data preprocessing, exploratory data analysis (EDA), model training, performance evaluation, and result visualization.

Two machine learning models are implemented and compared:

- Decision Tree Classifier
- Random Forest Classifier

The notebook is designed to help beginners understand how healthcare datasets can be analyzed using machine learning.

---

## Dataset

**Dataset Used:** Pima Indians Diabetes Dataset from Kaggle
**Original Dataset:**
https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database

The notebook automatically downloads the dataset using `kagglehub`.

The dataset contains several medical diagnostic measurements of female patients, including:

- Pregnancies
- Glucose
- Blood Pressure
- Skin Thickness
- Insulin
- BMI
- Diabetes Pedigree Function
- Age

The target variable is:

- **Outcome**
  - 0 → Non-Diabetic
  - 1 → Diabetic

---

## Project Structure

```
Diabetes_Prediction/
│
├── diabetes_prediction.ipynb
├── diabetes_graphs_visualization_and_analysis.pdf
├── README.md
```

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Google Colab / Jupyter Notebook
- Kagglehub

---

## Project Workflow

1. Import libraries
2. Load dataset
3. Data preprocessing
4. Exploratory Data Analysis (EDA)
5. Feature correlation analysis
6. Train-test split
7. Train Decision Tree model
8. Train Random Forest model
9. Model evaluation
10. Visualization and comparison of results

---

## Machine Learning Models

### Decision Tree Classifier

A simple tree-based classification model used as the baseline model.

### Random Forest Classifier

An ensemble learning model that combines multiple decision trees to improve prediction performance and reduce overfitting.

---

## Evaluation Metrics

The models are evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

Special attention is given to **Recall** for diabetic patients, as correctly identifying positive diabetes cases is particularly important in healthcare applications.

---

## Visualizations Included

- Target Class Distribution
- Feature Correlation Heatmap
- Decision Tree Confusion Matrix
- Random Forest Confusion Matrix
- Recall Comparison of Machine Learning Models

---

## Results

Both models successfully predict diabetes from medical features.

The Random Forest model achieved higher recall for diabetic patients compared to the Decision Tree model, making it a more suitable choice for this classification problem.

---

## How to Run

1. Open the notebook in Google Colab or Jupyter Notebook.
2. Run all cells sequentially.
3. The dataset will be downloaded automatically using **Kagglehub**.
4. The notebook will generate all visualizations and evaluation results.

---

## Output

The notebook generates:

- Cleaned dataset
- Exploratory Data Analysis
- Correlation Heatmap
- Classification Reports
- Confusion Matrices
- Recall Comparison Graph
