# Water Potability Prediction using Machine Learning

## Dataset

- Source: [Water Potability Dataset](https://www.kaggle.com/code/imakash3011/water-quality-prediction-7-model)
- The dataset contains physicochemical properties of water samples used to predict whether water is safe for drinking.

### Features

- pH
- Hardness
- Solids
- Chloramines
- Sulfate
- Conductivity
- Organic Carbon
- Trihalomethanes
- Turbidity

### Target

- Potability
  - 0 → Not Safe to Drink
  - 1 → Safe to Drink

This project predicts the potability of water using supervised machine learning algorithms. It demonstrates a complete machine learning workflow including data preprocessing, exploratory data analysis, feature scaling, handling class imbalance using SMOTE, model training, evaluation, and comparison.

---

## Key Features

1. Missing value handling using Median Imputation
2. Exploratory Data Analysis (EDA)
3. Class imbalance handling using SMOTE
4. Feature scaling using StandardScaler
5. Model training using multiple classification algorithms
6. Performance evaluation using Accuracy, Precision, Recall, F1-score and ROC-AUC
7. Confusion Matrix visualization
8. Feature Importance analysis
9. ROC Curve comparison
10. Model comparison and best model selection

---

## Models Implemented

- Logistic Regression
- Decision Tree
- Random Forest
- K-Nearest Neighbors (KNN)
- Support Vector Machine (SVM)

---

## Best Result

| Model         | Accuracy   |
| ------------- | ---------- |
| Random Forest | **73.63%** |

---

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Imbalanced-learn (SMOTE)
- Joblib
- Jupyter Notebook

---

## Usage

1. Open `Water_Potability_Prediction.ipynb` in Jupyter Notebook or Google Colab.
2. Install the required libraries using `requirements.txt`.
3. Run all notebook cells sequentially.
4. Review the generated visualizations, model evaluation metrics, ROC curves, and feature importance analysis.
