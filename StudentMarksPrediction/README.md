# Student Marks Prediction with Machine Learning

This project demonstrates a regression model to predict student marks based on the number of courses taken and average daily study time.

## Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Model](#model)
- [Results](#results)
- [Contributing](#contributing)
- [Deployment](#deployment)

## Overview

The project aims to predict student marks using a simple linear regression model. It uses Python and libraries such as NumPy, pandas, Plotly, and scikit-learn.

## Dataset

The dataset includes three columns:
- number_courses: Number of courses taken by the student.
- time_study: Average study time per day.
- Marks: Marks obtained (target variable).

Place the dataset file Student_Marks.csv in the data/ directory.

## Model

Steps involved:
1. *Data Preprocessing*: Checking for null values and understanding data distribution.
2. *Visualization*: Using Plotly to visualize relationships.
3. *Training*: Splitting data into training and test sets, then applying linear regression.
4. *Prediction*: Evaluating model performance with test data.

## Results

The model achieves a high accuracy with an R² score of approximately 0.946, indicating a strong correlation between the study time and marks obtained.

## Contributing

Contributions are welcome! Fork the repository, make your changes, and create a pull request.

---
---

## Installation

To get started, you need to install the required package modelbit.

bash
pip install modelbit


## Prediction Function

A function to predict student marks:

python
def StudentMarksPrediction(time_study, number_courses):
    features = np.array([[number_courses, time_study]])
    predicted_marks = model.predict(features)
    return predicted_marks

# Example usage
predicted_marks = StudentMarksPrediction(6.78, 2)
print(f"Predicted Marks: {predicted_marks}")


## Deploying the Model

To deploy the model using Modelbit, follow these steps:

1. *Login to Modelbit*:
    python
    import modelbit
    mb = modelbit.login()
    

2. *Deploy the function*:
    python
    mb.deploy(StudentMarksPrediction)
    

## Usage

After deploying the model, you can get predictions as follows:

1. *Define input data*:
    python
    time_study = 6.78
    number_courses = 2
    

2. *Get prediction from deployed model*:
    python
    prediction = modelbit.get_inference(
      region="ap-south-1",
      workspace="pondupondu",
      deployment="StudentMarksPrediction",
      data=[time_study, number_courses]
    )
    

3. *Display the prediction*:
    python
    print(f"The predicted score is: {prediction['data'][0]}")
    
