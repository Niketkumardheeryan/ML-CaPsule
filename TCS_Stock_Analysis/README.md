# TCS Stock Price Prediction using LSTM, K-Means Clustering, and Logistic Regression

## Overview

This project aims to predict the stock prices of Tata Consultancy Services (TCS) using a combination of Long Short-Term Memory (LSTM) networks, K-Means Clustering, and Logistic Regression. The system integrates these techniques to analyze historical stock price data and forecast future trends, enabling better investment decisions.

## Objectives

- Data Processing: Clean and preprocess historical stock price data of TCS.
- Model Development: Develop and train LSTM, K-Means Clustering, and Logistic Regression models for stock price prediction.
- Evaluation: Assess model performance and prediction accuracy.
- Optimization: Recommend optimal trading strategies based on model predictions.

## Technologies Used

- Python: Programming language for development.
- TensorFlow/Keras: Deep learning frameworks for building and training the LSTM model.
- Pandas: Data manipulation and analysis.
- NumPy: Numerical computing.
- Scikit-Learn: Machine learning tools for K-Means Clustering and Logistic Regression.
- Matplotlib/Seaborn: Data visualization.

## Models

### Long Short-Term Memory (LSTM)
- *Purpose*: Predict future stock prices by capturing temporal dependencies in historical data.
- *Architecture*: LSTM layers to handle sequential data, followed by dense layers for output prediction.

### K-Means Clustering
- *Purpose*: Segment historical stock data into clusters to identify patterns and trends.
- *Architecture*: K-Means algorithm to cluster data points based on similarities, aiding in feature extraction for predictive modeling.

### Logistic Regression
- *Purpose*: Classify stock price movements (e.g., up or down) based on extracted features.
- *Architecture*: Logistic regression model to predict binary outcomes, using features derived from historical data and clustering results.
