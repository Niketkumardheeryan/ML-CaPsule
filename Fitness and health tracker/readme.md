# Fitness and Health Tracker

## Overview

This project is a fitness and health tracking application that uses Streamlit for the web interface. It includes data analysis and visualization features, and implements machine learning algorithms to provide insights into users' health metrics.

## Features

- **Data Generation**: Synthetic dataset generation for user fitness and health metrics.
- **Calories Burned Prediction**: Linear regression model to predict calories burned based on steps, distance, and active minutes.
- **Heart Rate Analysis**: K-means clustering to analyze and group users based on their average heart rate.
- **Sleep Quality Analysis**: (Optional) Classification model to analyze sleep quality.

## Dataset

The dataset contains the following columns:
- `Date`: The date of the record.
- `User_ID`: Unique identifier for each user.
- `Steps`: Number of steps taken by the user.
- `Calories`: Calories burned by the user.
- `Distance`: Distance walked by the user (in km).
- `Active_Minutes`: Active minutes recorded for the user.
- `Heart_Rate`: Average heart rate of the user.
- `Sleep_Duration`: Sleep duration of the user (in hours).

### Running the Streamlit APP
1 . Run the Streamlit app:
streamlit run app.py
    

## Algorithms

### Calories Burned Prediction (Linear Regression)

The `calories_prediction.py` script trains a linear regression model to predict calories burned based on steps, distance, and active minutes. The model is evaluated using Mean Squared Error (MSE).

### Heart Rate Analysis (K-means Clustering)

The `heart_rate_analysis.py` script performs K-means clustering to group users based on their average heart rate. The results are visualized using a scatter plot.

