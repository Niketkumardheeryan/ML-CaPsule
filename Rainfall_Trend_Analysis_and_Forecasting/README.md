# Rainfall-Trends-India

## Dataset
- Source: Indian rainfall dataset (1901–2015)
- The notebook downloads the dataset as `data.csv` via `gdown`:
- Link :  https://drive.google.com/file/d/1LfTTYEYkDoD8wFEv-s_Ws-wj3LLHFdzI/view?usp=sharing

This project analyzes over a century of rainfall data in India to identify long-term trends, seasonal patterns, anomalies, and future forecasts. Using data science and machine learning techniques, the study explores rainfall variability, detects extreme events like droughts and floods, and predicts future rainfall patterns using time series forecasting.

## Key Features
1. Annual rainfall trend visualization
2. Monthly & seasonal rainfall analysis
3. Climate change impact using rolling averages
4. Detection of drought & extreme rainfall years
5. Anomaly detection using Isolation Forest
6. Correlation analysis between seasons
7. Clustering (Dry, Normal, Wet years)
8. Forecasting using Prophet model

 ## Tech Stack
 - Python
 - Pandas, NumPy
 - Plotly (visualization)
 - Scikit-learn (IsolationForest, KMeans)
 - SciPy (statistics)
 - Prophet (time-series forecasting)
 - gdown (dataset download)

## Usage
1. Open `Rainfall_Trends_in_India_Analysis_and Forecasting.ipynb` in Jupyter Notebook or Google Colab.
2. Run all cells (requires `gdown` to download `data.csv`).
3. Review the generated plots and Prophet forecasts.
