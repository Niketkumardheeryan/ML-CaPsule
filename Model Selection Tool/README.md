# Model Selection Tool

This Streamlit app helps users select features and a target column, visualize trends, choose test split size, and compare multiple ML models. It supports both classification and regression workflows.

## Features

- Upload a CSV file or use sample datasets.
- Pick X features and the y target column.
- View a trend plot before training.
- Select models: Linear, Multiple Linear, Polynomial, Random Forest, KNN, SVM, Decision Tree.
- Compare scores and highlight the best model.
- Show a confusion matrix (classification) or actual vs predicted plot (regression).

## How to Run

1. Create and activate a virtual environment.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```

## Notes

- For classification tasks, the linear models use logistic regression internally.
- For regression tasks, the comparison score is R2; for classification, it is accuracy.
