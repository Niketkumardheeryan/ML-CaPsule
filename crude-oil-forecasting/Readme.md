# Crude Oil Price Prediction

## Overview

This project aims to predict crude oil prices using historical data and machine learning techniques. It involves data collection, preprocessing, model training, and evaluation to forecast future prices. The approach leverages time-series data and various visualization techniques to enhance understanding and accuracy of predictions.

## Objectives

1. **Data Collection**: Gather historical crude oil price data from reliable sources.
2. **Data Preprocessing**: Clean, normalize, and prepare the data for modeling.
3. **Feature Engineering**: Create relevant features that could impact crude oil prices.
4. **Model Selection**: Choose appropriate machine learning algorithms for prediction.
5. **Model Training**: Train the selected models on historical data.
6. **Evaluation**: Assess model performance using appropriate metrics.
7. **Prediction**: Use trained models to forecast future crude oil prices.

## Methodology

### Data Collection

- Utilized datasets (e.g., CSV files) containing historical crude oil prices.
- Handled missing data and outliers appropriately.

### Data Preprocessing

- Cleaned the data by removing duplicates and handling null values.
- Normalized the data using `MinMaxScaler` for better model performance.

### Feature Engineering

- Created time-based features (e.g., moving averages, lagged values).
- Included relevant external factors that could influence crude oil prices.

### Model Selection

- Selected a Recurrent Neural Network (RNN) model due to its effectiveness in time-series prediction.

### Model Training

- Split the data into training and testing sets.
- Trained the RNN model using historical data with a sequence length of 10 time steps.

### Evaluation

- Evaluated the model using metrics such as Mean Squared Error (MSE) and Root Mean Squared Error (RMSE).
- Analyzed residuals and conducted feature ablation studies to understand feature importance.

### Prediction

- Used the trained RNN model to forecast crude oil prices for future periods.
- Visualized predictions and provided insights into price trends.

## Tools and Technologies

- **Programming Languages**: Python
- **Libraries**: pandas, numpy, scikit-learn, TensorFlow/Keras (for deep learning models), matplotlib, seaborn

## Visualization and Plots

### Time-Series Plot

- **Purpose**: Visualize normalized feature values over time to identify trends and patterns.
- **Impact**: Helps in understanding the overall data distribution and seasonal variations.

### Actual vs Predicted Plot

- **Purpose**: Compare actual and predicted crude oil prices.
- **Impact**: Evaluates the model's prediction accuracy visually.

### Residual Analysis Plot

- **Purpose**: Plot residuals to identify any patterns or anomalies.
- **Impact**: Ensures that the model's errors are randomly distributed, indicating a good fit.

### Feature Ablation Study Plot

- **Purpose**: Show the impact of removing each feature on the model's performance.
- **Impact**: Identifies the most influential features, aiding in model interpretation and improvement.

### Feature Importance Plot

- **Purpose**: Display the importance of each feature based on the model's weights.
- **Impact**: Provides insights into which features contribute the most to the prediction.

## Conclusion

This project effectively predicts crude oil prices using a SimpleRNN model. Key steps included thorough data preparation through cleaning, normalization, and feature engineering, which significantly enhanced model performance. The SimpleRNN model was chosen for its ability to capture temporal patterns in the data. Model evaluation using metrics like MSE, RMSE, and R², along with residual analysis, validated its accuracy and reliability. A feature ablation study identified the most influential factors, providing valuable insights into price drivers. Visualizations, including time-series plots and feature importance charts, played a crucial role in interpreting the model's performance. Overall, the project highlights the importance of comprehensive data preparation, model selection, and evaluation in time-series forecasting.
