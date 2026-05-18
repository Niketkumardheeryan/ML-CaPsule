# Wine Quality Prediction using Machine Learning

## Project Overview
This project uses a wine dataset to predict whether a wine sample is "good" or "bad" based on physicochemical features. It includes data cleaning, EDA, model training, evaluation, and comparison of Logistic Regression and Random Forest classifiers.

## Features
- Data loading and preprocessing
- Exploratory Data Analysis with visualizations
- Correlation heatmap for feature insights
- Train/test split with feature scaling
- Binary classification with Logistic Regression and Random Forest
- Model evaluation using accuracy, classification report, and confusion matrix
- Visual comparison of model performance
- Feature importance analysis

## Tech Stack
- Python
- pandas
- NumPy
- Matplotlib
- Seaborn
- scikit-learn

## Dataset Information
The dataset is stored at `dataset/winequality.csv` and contains physicochemical properties of wine samples, along with a quality score label.

## Installation
1. Clone the repository.
2. Create a Python virtual environment.
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
1. Open `wine_quality_prediction.ipynb` in Jupyter Notebook or JupyterLab.
2. Run the notebook cells in order.
3. Review the saved visualizations in the `images/` folder.

## Project Structure
- `wine_quality_prediction.ipynb` - Main notebook with the full ML workflow.
- `README.md` - Project documentation.
- `requirements.txt` - Python dependencies.
- `dataset/winequality.csv` - Original wine dataset.
- `images/` - Saved visualizations from the notebook.

## Model Performance
The notebook compares two models:
- Logistic Regression
- Random Forest Classifier

The Random Forest model typically achieves higher accuracy and provides feature importance ranking for model interpretation.

## Screenshots
Saved visualizations are located in the `images/` folder, including:
- `quality_distribution.png`
- `correlation_heatmap.png`
- `confusion_matrix_logistic.png`
- `confusion_matrix_random_forest.png`
- `model_accuracy_comparison.png`
- `feature_importance.png`

## Future Improvements
- Extend to multi-class quality prediction
- Perform cross-validation and hyperparameter tuning
- Add more advanced feature engineering
- Compare additional models such as XGBoost or SVM

## Contribution
Contributions are welcome! If you'd like to improve this project, feel free to submit a pull request with enhancements, bug fixes, or better visualizations.
