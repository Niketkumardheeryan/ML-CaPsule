# Financial Crisis Early Warning System

## Project Overview

This project aims to develop a Financial Crisis Early Warning System using deep learning techniques. We focus on predicting financial crises based on historical financial indicators. The dataset includes GDP growth, unemployment rate, inflation rate, interest rate, stock market return, credit growth, housing market index, and a binary indicator for financial crises.

## Dataset

The dataset is synthetic and contains the following columns:
- Date
- GDP_Growth
- Unemployment_Rate
- Inflation_Rate
- Interest_Rate
- Stock_Market_Return
- Credit_Growth
- Housing_Market_Index
- Financial_Crisis

## EDA (Exploratory Data Analysis)

The EDA process includes:
1. Loading and displaying the dataset.
2. Checking for missing values.
3. Statistical description of the dataset.
4. Visualizing the time series of each feature.
5. Plotting the correlation matrix.
6. Plotting histograms and pairplots to understand the distribution and relationships between variables.

## Deep Learning Models

We implemented three deep learning algorithms:
1. **LSTM (Long Short-Term Memory)**
2. **GRU (Gated Recurrent Unit)**
3. **Dense Neural Network (DNN)**

### LSTM Model

An LSTM model is built to capture long-term dependencies in the time series data.

### GRU Model

A GRU model is implemented as an alternative to the LSTM, focusing on reducing the computational cost.

### Dense Neural Network (DNN)

A simple DNN model is used as a baseline for comparison with the sequential models.

## Requirements

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- tensorflow

