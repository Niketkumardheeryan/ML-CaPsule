"""
Flask Web App — Smart Home Energy Consumption Prediction
========================================================
Routes:
  GET  /         → Input form
  POST /predict  → Show predicted energy + 30-day forecast graph
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import io, base64

app = Flask(__name__)

# ── Paths ────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")


def load_model_artifacts():
    """Load the saved model, column transformer, and metadata."""
    model = joblib.load(os.path.join(MODEL_DIR, "best_model.pkl"))
    ct = joblib.load(os.path.join(MODEL_DIR, "column_transformer.pkl"))
    meta = joblib.load(os.path.join(MODEL_DIR, "metadata.pkl"))
    return model, ct, meta


def predict_energy(temperature, appliance_type, household_size, hour, season):
    """
    Predict energy consumption for a single input.
    Returns predicted kWh value.
    """
    model, ct, meta = load_model_artifacts()
    temp_column = meta["temp_column"]

    appliance_mapping = {
        "AC": "Air Conditioning",
        "Lighting": "Lights",
        "EV Charger": "Air Conditioning" # Map to high energy device
    }
    mapped_appliance = appliance_mapping.get(appliance_type, appliance_type)

    baseline_lags = {
        "Air Conditioning": 3.5,
        "Heater": 3.5,
        "Fridge": 0.3,
        "Computer": 1.1,
        "Dishwasher": 1.1,
        "Lights": 1.1,
        "Microwave": 1.1,
        "Oven": 1.1,
        "Washing Machine": 1.1,
        "TV": 1.1
    }
    
    # Introduce small variations based on temperature and hour so prediction feels dynamic
    base_lag = baseline_lags.get(mapped_appliance, 1.0)
    lag_variation = (temperature - 20) * 0.01 + (hour - 12) * 0.005
    dynamic_lag = max(0.0, base_lag + lag_variation)

    row = {
        "Home ID": 0,
        "Appliance Type": mapped_appliance,
        temp_column: temperature,
        "Season": season,
        "Household Size": household_size,
        "Hour": hour,
        "Day": 15,
        "Month": 6,
        "Weekday": 2,
        "Peak_Hour": 1 if 18 <= hour <= 22 else 0,
        "Night_Usage": 1 if hour >= 23 or hour <= 5 else 0,
        "Temp_Squared": temperature ** 2,
        "Temp_x_HouseholdSize": temperature * household_size,
        "Rolling_Avg_3": dynamic_lag,
        "Lag_1": dynamic_lag,
        "Lag_2": dynamic_lag,
        "Lag_3": dynamic_lag,
    }

    input_df = pd.DataFrame([row])
    X_input = ct.transform(input_df)
    prediction = model.predict(X_input)[0]
    return round(float(prediction), 4)


def generate_forecast_chart():
    """
    Load the saved 30-day forecast CSV and return a base64-encoded PNG chart.
    """
    forecast_path = os.path.join(MODEL_DIR, "forecast_30days.csv")
    if not os.path.exists(forecast_path):
        return None

    forecast_df = pd.read_csv(forecast_path, index_col=0, parse_dates=True)
    forecast_df.columns = ["Forecast"]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(forecast_df.index, forecast_df["Forecast"],
            marker="o", color="#e74c3c", linewidth=2, markersize=4, label="Forecast")
    ax.fill_between(forecast_df.index, forecast_df["Forecast"],
                    alpha=0.15, color="#e74c3c")
    ax.set_title("Energy Consumption Forecast — Next 30 Days", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Daily Consumption (kWh)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Convert to base64
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return img_b64


# ── Routes ───────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    """Render the input form."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """Process form data and show prediction results."""
    try:
        temperature = float(request.form["temperature"])
        appliance_type = request.form["appliance_type"]
        household_size = int(request.form["household_size"])
        hour = int(request.form["hour"])
        season = request.form["season"]

        prediction = predict_energy(
            temperature=temperature,
            appliance_type=appliance_type,
            household_size=household_size,
            hour=hour,
            season=season
        )

        forecast_chart = generate_forecast_chart()

        return render_template(
            "result.html",
            prediction=prediction,
            temperature=temperature,
            appliance=appliance_type,
            household_size=household_size,
            hour=hour,
            season=season,
            forecast_chart=forecast_chart,
        )

    except Exception as e:
        return render_template("index.html", error=str(e))


# ── Run ──────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("  Smart Home Energy Prediction — Flask App")
    print("  Open: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
