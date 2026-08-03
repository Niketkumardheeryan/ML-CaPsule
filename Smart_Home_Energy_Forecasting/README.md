# Smart Home Energy Forecasting with Flask Deployment

An end-to-end Machine Learning project for smart home energy analytics, anomaly waste detection, and time-series daily forecasting.

## Features

1. **Smart Home Energy Consumption Prediction**: High-performance XGBoost regressor model trained to predict total hourly energy consumption.
2. **Wasteful Energy Usage Pattern Detection**: KMeans clustering classifies habits into efficient, normal, and wasteful. Supervised XGBoost classifier predicts these classes in real-time.
3. **Exploratory Data Analysis (EDA)**: Complete EDA producing 19 detailed analysis plots saved inside the Flask app analytics asset folder.
4. **ARIMA Time Series Forecasting**: Fits ARIMA(1, 1, 1) daily aggregated models to predict next 14-days consumption requirements.
5. **Interactive Flask Web Application**: Clean, modern dark-themed interactive UI to input metrics, predict hourly loads, view forecasts, and view EDA charts.

## Project Structure

```
Smart_Home_Energy_Forecasting/
├── data/
│   └── smart_home_energy_dataset.csv (100k records generated)
├── models/
│   ├── xgb_regressor.joblib
│   ├── xgb_classifier.joblib
│   ├── scaler.joblib
│   ├── pca.joblib
│   ├── kmeans.joblib
│   └── arima_model.joblib
├── static/
│   ├── style.css (Custom modern styling)
│   └── images/
│       └── plots/ (19 auto-generated analysis plots)
├── templates/
│   ├── index.html (Dashboard)
│   ├── predict.html (Predictor & calculator page)
│   ├── forecast.html (Time series visual chart & table)
│   └── analytics.html (EDA panel)
├── generate_data.py (Data generation pipeline)
├── run_pipeline.py (ML modeling pipeline script)
├── create_notebook.py (Programmatic notebook builder)
├── smart_home_energy_forecasting.ipynb (Jupyter Notebook with all 13 sections)
└── app.py (Flask Entrypoint)
```

## Setup & Execution Guide

### 1. Install Dependencies
```bash
pip install pandas numpy scikit-learn xgboost statsmodels flask joblib matplotlib seaborn
```

### 2. Generate Dataset and Assets
To re-generate the dataset, train the models, and output all 19 plots:
```bash
python generate_data.py
python run_pipeline.py
```

To programmatically build the Jupyter notebook file:
```bash
python create_notebook.py
```

### 3. Run the Flask Web Application
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000/`.
