# Student Marks Prediction with Machine Learning

This project demonstrates a regression model to predict student marks based on the number of courses taken and average daily study time.

## Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Model](#model)
- [Results](#results)
- [Contributing](#contributing)

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
