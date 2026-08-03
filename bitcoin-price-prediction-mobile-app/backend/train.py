import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_percentage_error
import joblib
import os

def train_models():
    # Load dataset
    df = pd.read_csv('coin_Bitcoin.csv')
    
    # Preprocess
    df.drop(["SNo", "Name", "Symbol"], axis=1, inplace=True, errors='ignore')
    
    # Sort by Date
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')
    
    # Drop date for model inputs
    df_model = df.drop(["Date"], axis=1)
    
    # Prepare features and targets
    # 1. Model for Marketcap: Inputs [High, Low, Open, Close, Volume]
    X_mc = df_model[['High', 'Low', 'Open', 'Close', 'Volume']]
    y_mc = df_model['Marketcap']
    
    X_mc_train, X_mc_test, y_mc_train, y_mc_test = train_test_split(X_mc, y_mc, test_size=0.2, random_state=42)
    
    print("Training Marketcap Predictor Model...")
    mc_model = RandomForestRegressor(n_estimators=50, max_depth=12, random_state=42, n_jobs=-1)
    mc_model.fit(X_mc_train, y_mc_train)
    
    mc_pred = mc_model.predict(X_mc_test)
    mc_r2 = r2_score(y_mc_test, mc_pred)
    mc_mape = mean_absolute_percentage_error(y_mc_test, mc_pred)
    print(f"Marketcap Model - R2 Score: {mc_r2:.4f}, MAPE: {mc_mape*100:.2f}%")
    
    # 2. Model for Close Price: Inputs [High, Low, Open, Volume]
    X_close = df_model[['High', 'Low', 'Open', 'Volume']]
    y_close = df_model['Close']
    
    X_close_train, X_close_test, y_close_train, y_close_test = train_test_split(X_close, y_close, test_size=0.2, random_state=42)
    
    print("Training Close Price Predictor Model...")
    close_model = RandomForestRegressor(n_estimators=50, max_depth=12, random_state=42, n_jobs=-1)
    close_model.fit(X_close_train, y_close_train)
    
    close_pred = close_model.predict(X_close_test)
    close_r2 = r2_score(y_close_test, close_pred)
    close_mape = mean_absolute_percentage_error(y_close_test, close_pred)
    print(f"Close Price Model - R2 Score: {close_r2:.4f}, MAPE: {close_mape*100:.2f}%")
    
    # Save models
    os.makedirs('models', exist_ok=True)
    joblib.dump(mc_model, 'models/marketcap_model.pkl')
    joblib.dump(close_model, 'models/close_model.pkl')
    print("Models saved successfully in 'models/' directory!")

if __name__ == '__main__':
    train_models()
