# Diabetes Risk Prediction

## Dataset

* Source: Pima Indians Diabetes Dataset
* The notebook downloads the dataset as `diabetes.csv` using `gdown`
* Link: https://drive.google.com/file/d/1cyB4B_s44Y9s6dfm9_tKbYdjkLTXfBlY/view?usp=sharing

This project uses machine learning techniques to predict whether a patient is likely to have diabetes based on diagnostic health measurements. The workflow includes data preprocessing, exploratory data analysis (EDA), feature scaling, model training, evaluation, and feature importance analysis.

## Key Features

1. Data cleaning and preprocessing
2. Missing value handling using median imputation
3. Duplicate record detection and removal
4. Exploratory Data Analysis (EDA)
5. Class distribution visualization
6. Feature distribution analysis
7. Correlation heatmap generation
8. Outlier detection using boxplots
9. Pairwise feature relationship analysis
10. Feature scaling using StandardScaler
11. Model training using multiple machine learning algorithms
12. Comparative model evaluation
13. ROC curve analysis
14. Feature importance visualization using Random Forest

## Models Used

* Logistic Regression
* Random Forest Classifier
* Support Vector Machine (SVM)
* K-Nearest Neighbors (KNN)
* XGBoost Classifier

## Evaluation Metrics

* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix
* ROC-AUC Score

## Tech Stack

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* XGBoost
* gdown

## Usage

1. Open `diabetes_prediction.ipynb` in Jupyter Notebook or Google Colab.
2. Install dependencies from `requirements.txt`.
3. Run all cells (requires `gdown` to download `diabetes.csv` automatically).
4. Review the generated visualizations, model comparison metrics, ROC curves, and feature importance analysis.

## Results

The models are evaluated using multiple classification metrics, and their performance is compared to identify the most effective approach for diabetes prediction. Random Forest Classifier achieved the best overall performance with:

- Accuracy: 77.9%
- Precision: 72.7%
- Recall: 59.3%
- F1-Score: 65.3%

## Feature Importance Analysis

The project includes feature importance visualization using Random Forest to identify the most influential medical indicators contributing to diabetes prediction.
