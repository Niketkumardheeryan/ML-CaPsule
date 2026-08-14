# Taxi Trip Price Prediction

## Project Overview

This project uses Machine Learning to predict taxi trip prices based on trip-related features such as distance, passenger count, fare rates, trip duration, time of day, traffic conditions, and weather.

The project includes data exploration, visualization, preprocessing, outlier handling, model training, and comparison of multiple regression algorithms.

## Features Used

### Numerical Features

- `Trip_Distance_km`
- `Passenger_Count`
- `Base_Fare`
- `Per_Km_Rate`
- `Per_Minute_Rate`
- `Trip_Duration_Minutes`

### Categorical Features

- `Time_of_Day`
- `Day_of_Week`
- `Traffic_Conditions`
- `Weather`

### Target Variable

- `Trip_Price`

## Machine Learning Models

The project compares:

1. Linear Regression
2. Decision Tree Regressor
3. Random Forest Regressor
4. XGBoost Regressor

## Evaluation Metrics

The models are evaluated using:

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- R-squared (R²)

The notebook identifies XGBoost as the best-performing model with an R² score of approximately 0.93.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- XGBoost
- Jupyter Notebook / Google Colab

## Project Structure

```text
Taxi-Price-Prediction/
│
├── Taxi_Price_Prediction.ipynb
├── README.md
└── requirements.txt
```

## Installation

Install all required dependencies using:

```bash
pip install -r requirements.txt
```

## Running the Project

Open the notebook using Jupyter:

```bash
jupyter notebook Taxi_Price_Prediction.ipynb
```

The notebook can also be executed in Google Colab.

