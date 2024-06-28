# Wine Quality Prediction

## Overview

This project aims to predict the quality of wines based on various chemical features using machine learning techniques. It utilizes a dataset containing attributes such as fixed acidity, volatile acidity, citric acid, residual sugar, chlorides, free sulfur dioxide, total sulfur dioxide, density, pH, sulphates, and alcohol to train a predictive model.

## Dependencies

- NumPy
- Pandas
- Matplotlib
- Seaborn
- scikit-learn

## Data Collection

The dataset used in this project is sourced from "winequality-red.csv". It consists of 1599 rows and 12 columns.

## Data Analysis and Visualization

Statistical measures of the dataset and visualization of the data using seaborn and matplotlib are performed to understand the distribution of features and their relationship with the quality of wine.

## Data Preprocessing

Data preprocessing steps include checking for missing values, label binarization/encoding, and splitting the dataset into training and testing sets.

## Model Training

A Random Forest Classifier is trained on the training data to predict wine quality.

## Model Evaluation

The accuracy score of the trained model is calculated on the test data, which is found to be approximately 93.13%.

## Predictive System

A predictive system is built using the trained model to predict the quality of wine based on user-input features.

## Usage

1. Import the required dependencies.
2. Load the dataset.
3. Analyze and preprocess the data.
4. Train the model.
5. Evaluate the model.
6. Use the predictive system to predict wine quality for new instances.

## Example Usage

```python
# First Input case :
input_data = (7.8, 0.58, 0.02, 2.0, 0.073, 9.0, 18.0, 0.9968, 3.36, 0.57, 9.5)
prediction = model.predict(np.asarray(input_data).reshape(1, -1))
if prediction[0] == 1:
    print("Good Quality Wine")
else:
    print("Bad Quality Wine")
```
