# Cervical Cancer Risk Prediction

This project aims to build a machine learning model to predict cervical cancer risk based on patient data. Various classification models are trained and evaluated, including Logistic Regression, Decision Tree, Random Forest, Support Vector Machine (SVM), and AdaBoost.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Dependencies](#dependencies)
3. [Dataset](#dataset)
4. [Data Preprocessing](#data-preprocessing)
5. [Model Training](#model-training)
6. [Evaluation](#evaluation)
7. [Usage](#usage)

## Project Overview
This project uses a dataset of risk factors associated with cervical cancer. The goal is to classify individuals based on these factors to estimate their likelihood of having cervical cancer. The project includes data preprocessing, visualization, model training, testing, and evaluation.

## Dependencies
To set up this project, install the following libraries:
```python
pandas
numpy
scikit-learn
matplotlib
seaborn
pickle
```

Install the dependencies with:
```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

## Dataset
The dataset used for this project can be downloaded from Kaggle: [Cervical Cancer Risk Factors Dataset](https://www.kaggle.com/). Save it as `kag_risk_factors_cervical_cancer.csv` and place it in the project directory.

## Data Preprocessing
1. **Load the Dataset**:
    - Load the dataset using pandas.
2. **Handle Missing Values**:
    - Replace all `'?'` values with `NaN`.
    - Convert all columns to numeric where possible and drop rows with missing values.
3. **Feature Scaling**:
    - Scale features using `StandardScaler`.
4. **Train-Test Split**:
    - Split the dataset into training and testing sets (80%-20%).

## Model Training
Five different models are used in this project:
- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier
- Support Vector Machine (SVM)
- AdaBoost Classifier

Each model is trained on the training dataset and evaluated on the test set.

## Evaluation
The models are evaluated using the following metrics:
- **Accuracy Score**
- **Classification Report**
- **Confusion Matrix**

A bar chart is generated to compare model accuracy.

## Usage
1. **Training the Model**:
    Run the code to preprocess the data, train models, and evaluate their performance.

2. **Saving the Model**:
    After training, the model and scaler are saved in the `saved_models` directory.

3. **Loading and Using the Model**:
    Use the saved model to make predictions on new data:
    ```python
    import pickle
    with open('../saved_models/model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('../saved_models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    # Preprocess new data and make predictions
    X_new_scaled = scaler.transform(X_new)
    predictions = model.predict(X_new_scaled)
    ```

## Visualizations
- **Histograms** of numerical columns to show data distributions.
- **Correlation Heatmap** to display relationships between features.
- **Count Plot** for categorical features.
- **Pair Plot** to visualize relationships among selected features.
