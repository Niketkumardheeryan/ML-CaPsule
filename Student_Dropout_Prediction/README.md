# Student Dropout Prediction Using Machine Learning

##  Project Overview

This project predicts a student's academic outcome using machine learning classification algorithms.

The notebook performs:
- Data loading from a CSV dataset hosted on GitHub Gist
- Exploratory Data Analysis (EDA)
- Missing-value and duplicate checks
- Correlation analysis
- Distribution and outlier visualization
- Train-test splitting with stratification
- Outlier clipping using IQR
- Target-label encoding
- Yeo-Johnson Power Transformation
- SMOTE-based class balancing
- Training and comparison of multiple classification models
- Evaluation using Accuracy, Precision, Recall, F1-score, Confusion Matrix and ROC-AUC

##  Dataset

The notebook loads the dataset from:

`https://gist.githubusercontent.com/anu-006/93037638865ee28fdc89c6d6775aae45/raw/8c9691de6d214b5b7d88116b7575064c60f39d1f/dataset.csv`

Dataset shape used in the notebook:

- **Rows:** 4,424
- **Columns:** 35
- **Features:** 34
- **Target:** `Target`
- **Missing values:** 0%
- **Duplicate rows:** 0

The target contains three encoded classes: `0`, `1`, and `2`.

##  Exploratory Data Analysis

The notebook includes:

- Dataset shape and information
- Descriptive statistics
- Missing-value analysis
- Duplicate-value analysis
- Numeric correlation matrix
- Target-class distribution
- KDE plots for feature distributions
- Skewness calculation
- Box plots for outlier inspection

##  Preprocessing

The workflow is:

1. Separate features and target.
2. Split the data into training and testing sets using an 80:20 split.
3. Use stratification to preserve class proportions.
4. Calculate IQR-based outlier limits from the training set.
5. Clip both training and test values using the training-set limits.
6. Encode the target using `LabelEncoder`.
7. Apply a Yeo-Johnson `PowerTransformer`.
8. Apply SMOTE only inside the training pipeline.
9. Train the classifier.

Keeping SMOTE inside the `imblearn` pipeline is important because it prevents synthetic samples from being created from the test set.

##  Models Used

Five classification algorithms are compared:

1. Logistic Regression
2. Random Forest Classifier
3. Gradient Boosting Classifier
4. XGBoost Classifier
5. Decision Tree Classifier


## Results

Results already produced by the notebook:

| Model | Accuracy | Weighted F1 | Weighted Precision | Weighted Recall | Weighted ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.718 | 0.730 | 0.758 | 0.718 | 0.886 |
| Random Forest | 0.731 | 0.730 | 0.731 | 0.731 | **0.897** |
| Gradient Boosting | **0.747** | **0.749** | **0.752** | **0.747** | 0.894 |
| XGBoost | 0.746 | 0.742 | 0.739 | 0.746 | 0.890 |
| Decision Tree | 0.619 | 0.630 | 0.645 | 0.619 | 0.715 |

###  Best Model

Based on the notebook's test-set results:

**Gradient Boosting** gives the best overall classification performance by accuracy and weighted F1-score:

- Accuracy: **74.69%**
- Weighted F1-score: **74.90%**
- Weighted Precision: **75.21%**
- Weighted Recall: **74.69%**
- ROC-AUC: **89.42%**

Random Forest has the highest reported weighted ROC-AUC at **89.72%**.



##  Installation

Clone the repository and install the required packages:

```bash
git clone <your-repository-url>
cd <your-repository-folder>
pip install -r requirements.txt
```

Then launch Jupyter Notebook:

```bash
jupyter notebook
```

Open:

`Student_dropout_prediction.ipynb`

