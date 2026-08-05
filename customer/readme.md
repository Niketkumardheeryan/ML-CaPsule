# Predictive Customer Purchase Analysis Using Decision Tree Classifier

## 📌 Project Overview

This project predicts whether an online visitor is likely to complete a purchase based on their browsing behavior and session activity. A Decision Tree Classifier is used to classify customer sessions into purchase and non-purchase categories.

The project demonstrates a complete Machine Learning workflow, including data preprocessing, exploratory data analysis (EDA), feature engineering, model training, hyperparameter tuning, pruning, and performance evaluation.

---

## 🎯 Problem Statement

E-commerce websites receive thousands of customer visits every day, but only a small percentage of visitors complete a purchase. Identifying potential buyers can help businesses:

- Improve marketing campaigns
- Provide personalized recommendations
- Increase conversion rates
- Optimize customer engagement

This project aims to predict purchase intention using customer session data.

---

## 📂 Dataset

**Dataset:** Online Shoppers Purchasing Intention Dataset

The dataset contains browsing session information collected from an e-commerce website.

### Target Variable

- **Revenue**
  - True → Customer made a purchase
  - False → Customer did not make a purchase

### Features

- Administrative
- Administrative_Duration
- Informational
- Informational_Duration
- ProductRelated
- ProductRelated_Duration
- BounceRates
- ExitRates
- PageValues
- SpecialDay
- Month
- OperatingSystems
- Browser
- Region
- TrafficType
- VisitorType
- Weekend

---

## 🛠 Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

---

## 📊 Exploratory Data Analysis (EDA)

The following analyses were performed:

- Dataset overview
- Missing value analysis
- Duplicate value analysis
- Statistical summary
- Revenue distribution
- Feature distribution
- Correlation heatmap
- Product-related analysis
- Visitor type analysis
- Monthly traffic analysis
- Weekend analysis
- Purchase behavior analysis

---

## ⚙ Data Preprocessing

The following preprocessing steps were performed:

- Removed duplicate records
- Encoded categorical variables
- Converted boolean features
- Separated features and target variable
- Applied Stratified Train-Test Split

---

## 🤖 Machine Learning Model

**Algorithm Used**

- Decision Tree Classifier

### Hyperparameter Tuning

GridSearchCV was used for optimization with the following parameters:

- criterion
- max_depth
- min_samples_split
- min_samples_leaf
- ccp_alpha (Cost Complexity Pruning)

---

## 📈 Model Performance

### Baseline Decision Tree

| Metric | Score |
|---------|-------|
| Accuracy | 85.28% |
| Precision | 52.37% |
| Recall | 54.97% |
| F1-Score | 53.64% |

### Optimized Decision Tree

| Metric | Score |
|---------|-------|
| Accuracy | 89.74% |
| Precision | 74.16% |
| Recall | 51.83% |
| F1-Score | **61.02%** |

The optimized model achieved a significant improvement in overall performance after hyperparameter tuning and pruning.

---

## 📁 Project Structure

```
Predictive Customer Purchase Analysis Using Decision Tree Classifier/
│
├── customer_purchase_prediction.ipynb
├── README.md
├── requirements.txt
├── dataset/
│   └── online_shoppers_intention.csv
└── images/
```

---

## 🚀 Installation

Clone the repository

```bash
git clone <repository-url>
```

Move to the project folder

```bash
cd Predictive-Customer-Purchase-Analysis-Using-Decision-Tree-Classifier
```

Install dependencies

```bash
pip install -r requirements.txt
```

Launch Jupyter Notebook

```bash
jupyter notebook
```

---

## 📌 Results

- Successfully predicted customer purchase intention using a Decision Tree Classifier.
- Improved model performance through hyperparameter tuning.
- Applied Cost Complexity Pruning to reduce overfitting.
- Increased F1-score from **53.64%** to **61.02%**.
- Achieved an optimized model accuracy of **89.74%**.

---

## 🔮 Future Improvements

- Random Forest Classifier
- XGBoost Classifier
- LightGBM
- SMOTE for handling class imbalance
- Feature selection techniques
- Deployment using Flask or Streamlit

---

## 📚 Learning Outcomes

Through this project, the following concepts were explored:

- Data Cleaning
- Exploratory Data Analysis
- Feature Engineering
- Label Encoding
- Stratified Train-Test Split
- Decision Tree Classification
- Hyperparameter Tuning
- Cost Complexity Pruning
- Model Evaluation
- Precision, Recall, and F1-Score Analysis

---


