# Gold-Price-Analysis-with-Time--1950-to-2020-Time-Series-Forecasting-
Applied statistical and machine learning techniques including Linear Regression, Naive Model, and Exponential Smoothing. Visualized historical trends and seasonal patterns to generate accurate future predictions. Achieved robust forecasting performance with a comprehensive evaluation of model accuracy.


OVERVIEW:
-----------
This project involves a comprehensive analysis and forecasting of gold prices from January 1950 to August 2020. Using various statistical and machine learning techniques, we aim to understand historical trends and make future predictions.

Dataset
The dataset contains monthly gold prices spanning from January 1950 to August 2020. The data was processed and analyzed using Python libraries such as Pandas, NumPy, Matplotlib, Seaborn, and Statsmodels.

METHODOLOGY:
--------------
Data Preprocessing:

Loaded the dataset and inspected its structure.
Converted the 'Date' column to datetime format and set it as the index.
Conducted exploratory data analysis (EDA) to visualize trends and patterns.
Exploratory Data Analysis (EDA):

Visualized gold prices over time using line plots.
Created box plots to analyze price distribution across years and months.
Generated descriptive statistics to summarize the data.
Resampled the data to visualize yearly, quarterly, and decadal trends.
Time Series Decomposition:

Decomposed the time series data to identify trend, seasonal, and residual components.
Modeling and Forecasting:

Linear Regression: Built a linear regression model to forecast future prices.
Naive Model: Used the last observed value as the forecast for future periods.
Exponential Smoothing: Applied the Holt-Winters method to account for trends and seasonality in the data.
Evaluated models using Mean Absolute Percentage Error (MAPE) to compare accuracy.

KEY RESULTS:
---------------
Visualizations:

Line plots and box plots provided insights into price trends and distributions over the years.
Resampling revealed the long-term trends and seasonal patterns in gold prices.
Forecasting Models:

Linear Regression: Achieved a MAPE of 29.760%.
Naive Model: Achieved a MAPE of 19.380%.
Exponential Smoothing: Achieved a MAPE of 17.241%.


FINAL FORECAST:
-----------------

The final forecast model using Exponential Smoothing provided a robust prediction of future gold prices, considering both trend and seasonality.


CONCLUSION:
-----------------
This project demonstrates the use of statistical and machine learning techniques for time series analysis and forecasting. The visualizations and models developed provide valuable insights into historical gold price trends and offer reliable predictions for future prices.

Tools and Libraries:
---------------------
Programming Language: Python
Libraries: Pandas, NumPy, Matplotlib, Seaborn, Statsmodels, Scikit-learn

Future Work:
--------------
Incorporate external economic indicators to improve forecasting accuracy.
Explore more advanced models such as ARIMA, SARIMA, and machine learning approaches like LSTM for time series forecasting.


