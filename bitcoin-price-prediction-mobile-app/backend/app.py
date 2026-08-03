from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import os

app = FastAPI(
    title="Bitcoin Price Prediction API",
    description="Backend API for predicting Bitcoin close prices and market cap based on High, Low, Open, and Volume features.",
    version="1.0.0"
)

# Load the models
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
mc_model_path = os.path.join(MODEL_DIR, "marketcap_model.pkl")
close_model_path = os.path.join(MODEL_DIR, "close_model.pkl")

try:
    mc_model = joblib.load(mc_model_path)
    close_model = joblib.load(close_model_path)
except Exception as e:
    mc_model = None
    close_model = None
    print(f"Error loading models: {e}")

# Load the historical dataset
csv_path = os.path.join(os.path.dirname(__file__), "coin_Bitcoin.csv")
try:
    df_history = pd.read_csv(csv_path)
    df_history['Date'] = pd.to_datetime(df_history['Date'])
    df_history = df_history.sort_values(by='Date')
except Exception as e:
    df_history = None
    print(f"Error loading history csv: {e}")


# Pydantic Schemas for requests and responses
class PredictionRequest(BaseModel):
    high: float
    low: float
    open_price: float
    volume: float

class PredictionResponse(BaseModel):
    predicted_close: float
    predicted_marketcap: float

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the Bitcoin Price Prediction API!",
        "endpoints": {
            "predict": "POST /predict",
            "history": "GET /history?limit=100",
            "market_overview": "GET /market-overview"
        }
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if not mc_model or not close_model:
        raise HTTPException(
            status_code=503,
            detail="Machine learning models are not loaded. Run train.py first."
        )
    
    try:
        # 1. Predict Close Price first based on High, Low, Open, Volume
        input_close = pd.DataFrame(
            [[request.high, request.low, request.open_price, request.volume]],
            columns=['High', 'Low', 'Open', 'Volume']
        )
        pred_close = float(close_model.predict(input_close)[0])
        
        # 2. Predict Marketcap based on High, Low, Open, Close, Volume
        input_mc = pd.DataFrame(
            [[request.high, request.low, request.open_price, pred_close, request.volume]],
            columns=['High', 'Low', 'Open', 'Close', 'Volume']
        )
        pred_mc = float(mc_model.predict(input_mc)[0])
        
        return PredictionResponse(
            predicted_close=round(pred_close, 2),
            predicted_marketcap=round(pred_mc, 2)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during prediction: {str(e)}"
        )

@app.get("/history")
def get_history(limit: int = 150):
    if df_history is None:
        raise HTTPException(
            status_code=503,
            detail="Historical data is not available."
        )
    
    # Return last 'limit' records formatted as simple list of dicts for charting
    df_sub = df_history.tail(limit)
    records = []
    for _, row in df_sub.iterrows():
        records.append({
            "date": row['Date'].strftime('%Y-%m-%d'),
            "open": float(row['Open']),
            "high": float(row['High']),
            "low": float(row['Low']),
            "close": float(row['Close']),
            "volume": float(row['Volume']),
            "marketcap": float(row['Marketcap'])
        })
    
    return {
        "count": len(records),
        "data": records
    }

@app.get("/market-overview")
def get_market_overview():
    if df_history is None:
        raise HTTPException(
            status_code=503,
            detail="Historical data is not available."
        )
    
    try:
        # Calculate overall and recent statistics
        all_time_high = float(df_history['High'].max())
        all_time_low = float(df_history['Low'].min())
        latest_row = df_history.iloc[-1]
        
        # Determine trend based on moving averages (e.g. 5-day vs 20-day)
        last_5 = df_history.tail(5)['Close'].mean()
        last_20 = df_history.tail(20)['Close'].mean()
        trend = "Bullish 📈" if last_5 >= last_20 else "Bearish 📉"
        
        return {
            "latest_price": float(latest_row['Close']),
            "latest_date": latest_row['Date'].strftime('%Y-%m-%d'),
            "all_time_high": round(all_time_high, 2),
            "all_time_low": round(all_time_low, 2),
            "market_trend": trend,
            "average_volume_20d": float(df_history.tail(20)['Volume'].mean()),
            "recommendation": "Hold/Buy" if trend == "Bullish 📈" else "Hold/Sell"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred calculating market overview: {str(e)}"
        )
