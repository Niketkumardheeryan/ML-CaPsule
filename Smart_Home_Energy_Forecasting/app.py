import os
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Security Configurations (GitHub Advanced Security / Security Analysis)
app.config['PREFERRED_URL_SCHEME'] = os.environ.get('PREFERRED_URL_SCHEME', 'https')
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', 'True').lower() in ('true', '1', 't')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Load models and scalers
MODELS_DIR = "models"
scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.joblib"))
pca = joblib.load(os.path.join(MODELS_DIR, "pca.joblib"))
kmeans = joblib.load(os.path.join(MODELS_DIR, "kmeans.joblib"))
scaler_cluster = joblib.load(os.path.join(MODELS_DIR, "scaler_cluster.joblib"))
xgb_reg = joblib.load(os.path.join(MODELS_DIR, "xgb_regressor.joblib"))
xgb_clf = joblib.load(os.path.join(MODELS_DIR, "xgb_classifier.joblib"))
arima_result = joblib.load(os.path.join(MODELS_DIR, "arima_model.joblib"))

# Load dataset for summary statistics
df_summary = pd.read_csv("data/smart_home_energy_dataset.csv")

@app.route('/')
def index():
    # Calculate some summary stats for the dashboard
    total_records = len(df_summary)
    avg_energy = round(df_summary['Total_Energy_kWh'].mean(), 2)
    max_energy = round(df_summary['Total_Energy_kWh'].max(), 2)
    avg_temp = round(df_summary['Temperature'].mean(), 1)
    
    # Get last 7 days of daily aggregated consumption for preview chart
    df_daily = df_summary.copy()
    df_daily['Timestamp'] = pd.to_datetime(df_daily['Timestamp'])
    df_daily = df_daily.set_index('Timestamp').resample('D')['Total_Energy_kWh'].mean().tail(10)
    
    recent_dates = [d.strftime('%b %d') for d in df_daily.index]
    recent_values = [round(v, 2) for v in df_daily.values]

    return render_template(
        'index.html',
        total_records=total_records,
        avg_energy=avg_energy,
        max_energy=max_energy,
        avg_temp=avg_temp,
        recent_dates=recent_dates,
        recent_values=recent_values
    )

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction = None
    waste_class = None
    features = {}
    
    if request.method == 'POST':
        try:
            # Parse form inputs
            temp = float(request.form.get('temperature', 20.0))
            humidity = float(request.form.get('humidity', 50.0))
            sqft = float(request.form.get('square_footage', 2000.0))
            occupants = float(request.form.get('occupants', 3.0))
            hour = int(request.form.get('hour', datetime.now().hour))
            month = int(request.form.get('month', datetime.now().month))
            day_of_week = int(request.form.get('day_of_week', 0))
            is_holiday = int(request.form.get('is_holiday', 0))
            
            lag1 = float(request.form.get('energy_lag1', 1.1))
            lag2 = float(request.form.get('energy_lag2', 1.0))
            lag3 = float(request.form.get('energy_lag3', 0.9))
            
            # Feature engineering
            hour_sin = np.sin(2 * np.pi * hour / 24.0)
            hour_cos = np.cos(2 * np.pi * hour / 24.0)
            month_sin = np.sin(2 * np.pi * month / 12.0)
            month_cos = np.cos(2 * np.pi * month / 12.0)
            
            temp_hum = temp * humidity
            density = sqft / (occupants + 1e-5)
            rolling_mean = (lag1 + lag2 + lag3) / 3.0
            
            # Form feature vector for scaling
            feature_vector = np.array([[
                temp, humidity, sqft, occupants,
                hour_sin, hour_cos, month_sin, month_cos,
                temp_hum, density, lag1, lag2, rolling_mean
            ]])
            
            # Scale
            scaled_vector = scaler.transform(feature_vector)
            
            # Predict total energy (Regression)
            predicted_val = xgb_reg.predict(scaled_vector)[0]
            prediction = round(float(predicted_val), 3)
            
            # Classify energy profile (0: Efficient, 1: Normal, 2: Wasteful)
            profile_val = xgb_clf.predict(scaled_vector)[0]
            
            profile_labels = {
                0: "Efficient (Low consumption for current conditions)",
                1: "Normal (Standard consumption pattern)",
                2: "Wasteful (High consumption / Potential Energy Waste)"
            }
            waste_class = profile_labels.get(int(profile_val), "Unknown")
            
            # Store features to pre-populate form fields
            features = {
                'temperature': temp,
                'humidity': humidity,
                'square_footage': sqft,
                'occupants': occupants,
                'hour': hour,
                'month': month,
                'day_of_week': day_of_week,
                'is_holiday': is_holiday,
                'energy_lag1': lag1,
                'energy_lag2': lag2,
                'energy_lag3': lag3
            }
            
        except Exception as e:
            return render_template('predict.html', error=str(e), features=features)
            
    return render_template('predict.html', prediction=prediction, waste_class=waste_class, features=features)

@app.route('/forecast')
def forecast():
    # Make a 14-day ARIMA forecast
    forecast_steps = 14
    forecast_res = arima_result.get_forecast(steps=forecast_steps)
    forecast_mean = [round(v, 2) for v in forecast_res.predicted_mean.tolist()]
    
    # Calculate forecast confidence intervals
    conf_int = forecast_res.conf_int()
    lower_bound = [round(v, 2) for v in conf_int.iloc[:, 0].tolist()]
    upper_bound = [round(v, 2) for v in conf_int.iloc[:, 1].tolist()]
    
    # Generate dates for forecast
    last_date = pd.to_datetime(df_summary['Timestamp']).max()
    forecast_dates = [(last_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, forecast_steps + 1)]
    
    # Historical data (last 30 days)
    df_daily = df_summary.copy()
    df_daily['Timestamp'] = pd.to_datetime(df_daily['Timestamp'])
    df_daily = df_daily.set_index('Timestamp').resample('D')['Total_Energy_kWh'].mean().tail(30)
    
    hist_dates = [d.strftime('%Y-%m-%d') for d in df_daily.index]
    hist_values = [round(v, 2) for v in df_daily.values]

    return render_template(
        'forecast.html',
        forecast_dates=forecast_dates,
        forecast_values=forecast_mean,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        hist_dates=hist_dates,
        hist_values=hist_values
    )

@app.route('/analytics')
def analytics():
    # We display the pre-generated plots saved in static/images/plots/
    plots = [
        {"id": 1, "title": "Total Energy Distribution", "filename": "plot1_dist_total_energy.png", "desc": "Histogram showing distribution of energy consumption logs."},
        {"id": 2, "title": "Energy by Home ID", "filename": "plot2_box_energy_by_home.png", "desc": "Boxplot comparing consumption ranges across different smart homes."},
        {"id": 3, "title": "Hourly Load Distribution", "filename": "plot3_box_energy_by_hour.png", "desc": "Hourly consumption showing peaks in evening and morning."},
        {"id": 4, "title": "Weekly Load Distribution", "filename": "plot4_box_energy_by_dayofweek.png", "desc": "Daily distribution over the week (0=Mon, 6=Sun)."},
        {"id": 5, "title": "Monthly Average Profile", "filename": "plot5_line_monthly_avg_energy.png", "desc": "Line plot showing monthly seasonality trends."},
        {"id": 6, "title": "Hourly Average Profile", "filename": "plot6_line_hourly_avg_energy.png", "desc": "The average daily demand pattern curve."},
        {"id": 7, "title": "Temperature vs. Energy", "filename": "plot7_scatter_temp_vs_energy.png", "desc": "Scatter plot showing relationship between external temperature and energy."},
        {"id": 8, "title": "Feature Correlation Heatmap", "filename": "plot8_heatmap_correlation.png", "desc": "Heatmap of Pearson correlation coefficients across numerical attributes."},
        {"id": 9, "title": "Appliance Energy Share", "filename": "plot9_bar_appliance_distribution.png", "desc": "Bar chart comparing average energy consumption of appliances."},
        {"id": 10, "title": "Key Feature Pairplot", "filename": "plot10_pairplot_key_features.png", "desc": "Pairwise relationships and distributions for major features."},
        {"id": 11, "title": "PCA Explained Variance", "filename": "plot11_pca_scree.png", "desc": "Scree plot detailing individual and cumulative explained variance ratio."},
        {"id": 12, "title": "PCA 2D Projection", "filename": "plot12_pca_2d.png", "desc": "Dataset projected on the first two principal components, colored by energy."},
        {"id": 13, "title": "KMeans Elbow Curve", "filename": "plot13_kmeans_elbow.png", "desc": "Finding optimal number of clusters using distortions metric."},
        {"id": 14, "title": "KMeans Clusters on PCA Space", "filename": "plot14_kmeans_pca_scatter.png", "desc": "KMeans clusters mapped to principal component coordinates."},
        {"id": 15, "title": "Clustered Consumption Comparison", "filename": "plot15_waste_profile_box.png", "desc": "Boxplot comparing total energy ranges across the classified profiles."},
        {"id": 16, "title": "Regression Error Rates", "filename": "plot16_reg_comparison.png", "desc": "Comparison of RMSE and MAE across Linear Regression, RF, and XGBoost."},
        {"id": 17, "title": "Classification Model Comparison", "filename": "plot17_clf_comparison.png", "desc": "Accuracy and F1-macro comparison across Logistic Regression, RF, and XGBoost."},
        {"id": 18, "title": "ARIMA In-Sample Fit", "filename": "plot18_arima_fitted.png", "desc": "ARIMA actual vs. fitted daily average load values."},
        {"id": 19, "title": "ARIMA Out-of-Sample Forecast", "filename": "plot19_arima_forecast.png", "desc": "ARIMA forecast against validation values with 95% confidence intervals."}
    ]
    return render_template('analytics.html', plots=plots)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
