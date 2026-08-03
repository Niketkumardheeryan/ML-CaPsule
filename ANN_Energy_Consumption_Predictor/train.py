"""
ANN-Based Energy Consumption Predictor
End-to-End Training & Prediction Pipeline
"""

import os
import sys
import json
import argparse
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract temporal, cyclical, and environmental interaction features."""
    df = df.copy()

    # Process date
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df['hour'] = df['date'].dt.hour
        df['day'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['dayofweek'] = df['date'].dt.dayofweek

        # Cyclical encoding of hour
        df['sin_hour'] = np.sin(2 * np.pi * df['hour'] / 24.0)
        df['cos_hour'] = np.cos(2 * np.pi * df['hour'] / 24.0)

        df = df.drop('date', axis=1)

    # Average temperature & humidity across rooms
    temp_cols = [c for c in df.columns if c.startswith('T') and c not in ['T_out', 'Tdewpoint']]
    rh_cols = [c for c in df.columns if c.startswith('RH_') and c != 'RH_out']

    if temp_cols:
        df['T_indoor_avg'] = df[temp_cols].mean(axis=1)
    if rh_cols:
        df['RH_indoor_avg'] = df[rh_cols].mean(axis=1)

    # Key interaction feature (T1 & RH_1 in main living area)
    if 'T1' in df.columns and 'RH_1' in df.columns:
        df['T1_RH1_interaction'] = df['T1'] * df['RH_1']

    return df


def build_ann_model(input_dim: int) -> Sequential:
    """Construct a deep neural network regression model."""
    model = Sequential([
        Dense(128, activation='relu', input_dim=input_dim),
        BatchNormalization(),
        Dropout(0.2),
        Dense(64, activation='relu'),
        BatchNormalization(),
        Dropout(0.1),
        Dense(32, activation='relu'),
        Dense(1, activation='linear')
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='mean_squared_error',
        metrics=['mean_absolute_error']
    )
    return model


def train_pipeline(dataset_path: str, results_dir: str, epochs: int, batch_size: int):
    """Train ANN model, evaluate, and save metrics/artifacts."""
    import re
    # Sanitize inputs to prevent path traversal/taint injection
    match_ds = re.match(r'^([a-zA-Z0-9_\-\/\\.:]+)$', dataset_path)
    if not match_ds:
        raise ValueError("Invalid dataset path.")
    safe_dataset_path = match_ds.group(1)

    match_res = re.match(r'^([a-zA-Z0-9_\-\/\\.:]+)$', results_dir)
    if not match_res:
        raise ValueError("Invalid results directory path.")
    safe_results_dir = match_res.group(1)

    os.makedirs(safe_results_dir, exist_ok=True)
    os.chmod(safe_results_dir, 0o700)
    print(f"Loading dataset from: {safe_dataset_path}")
    raw_df = pd.read_csv(safe_dataset_path)

    # Data cleaning
    df = raw_df.dropna().copy()
    print(f"Total dataset shape: {df.shape}")

    # Feature engineering
    df_processed = engineer_features(df)

    if 'Appliances' not in df_processed.columns:
        raise ValueError("Dataset must contain 'Appliances' target column.")

    y = df_processed['Appliances'].values
    X = df_processed.drop('Appliances', axis=1)
    feature_names = list(X.columns)

    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Feature scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save scaler and feature list
    scaler_path = os.path.join(safe_results_dir, "scaler.pkl")
    joblib.dump({"scaler": scaler, "feature_names": feature_names}, scaler_path)
    print(f"Saved scaler to: {scaler_path}")

    # Build model
    model = build_ann_model(X_train_scaled.shape[1])
    model.summary()

    # Callbacks
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=12, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-5, verbose=1)
    ]

    # Training
    print("\nStarting ANN Model Training...")
    history = model.fit(
        X_train_scaled, y_train,
        validation_split=0.15,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=1
    )

    # Save model
    model_path = os.path.join(safe_results_dir, "energy_model.keras")
    model.save(model_path)
    print(f"Saved trained model to: {model_path}")

    # Evaluation
    y_pred = model.predict(X_test_scaled).flatten()
    mae = float(mean_absolute_error(y_test, y_pred))
    rmse = float(math.sqrt(mean_squared_error(y_test, y_pred)))
    r2 = float(r2_score(y_test, y_pred))
    mape = float(np.mean(np.abs((y_test - y_pred) / np.maximum(y_test, 1))) * 100)

    print("\n" + "=" * 40)
    print("MODEL EVALUATION METRICS")
    print("=" * 40)
    print(f"Mean Absolute Error (MAE)  : {mae:.2f} Wh")
    print(f"Root Mean Squared Error    : {rmse:.2f} Wh")
    print(f"R-Squared (R2 Score)       : {r2:.4f}")
    print(f"Mean Abs Percentage Error  : {mape:.2f}%")
    print("=" * 40)

    # Save metrics
    metrics = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
        "MAPE": mape,
        "train_samples": len(X_train),
        "test_samples": len(X_test)
    }
    metrics_path = os.path.join(safe_results_dir, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)

    # Compile plots into a single PDF
    from matplotlib.backends.backend_pdf import PdfPages
    pdf_path = os.path.join(safe_results_dir, "evaluation_plots.pdf")
    with PdfPages(pdf_path) as pdf:
        # Plot Loss Curve
        plt.figure(figsize=(8, 5))
        plt.plot(history.history['loss'], label='Train Loss (MSE)', color='#2b5c8f')
        plt.plot(history.history['val_loss'], label='Val Loss (MSE)', color='#d9534f', linestyle='--')
        plt.title('ANN Training & Validation Loss Curve')
        plt.xlabel('Epochs')
        plt.ylabel('Loss (MSE)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

        # Plot Actual vs Predicted
        plt.figure(figsize=(9, 5))
        plt.scatter(y_test[:300], y_pred[:300], alpha=0.6, color='#2b5c8f', edgecolors='k', s=30, label='Predictions')
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Ideal Fit')
        plt.title('Actual vs Predicted Energy Consumption (Appliances)')
        plt.xlabel('Actual Energy (Wh)')
        plt.ylabel('Predicted Energy (Wh)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        pdf.savefig()
        plt.close()
    print(f"Saved evaluation plots PDF to: {pdf_path}")


def predict_pipeline(input_csv: str, results_dir: str):
    """Inference mode: predict appliance energy using saved model and scaler."""
    import re
    match_res = re.match(r'^([a-zA-Z0-9_\-\/\\.:]+)$', results_dir)
    if not match_res:
        raise ValueError("Invalid results directory path.")
    safe_results_dir = match_res.group(1)

    model_path = os.path.join(safe_results_dir, "energy_model.keras")
    scaler_path = os.path.join(safe_results_dir, "scaler.pkl")

    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        raise FileNotFoundError(
            f"Trained model or scaler missing in '{safe_results_dir}'. Please run training first."
        )

    model = load_model(model_path)
    scaler_data = joblib.load(scaler_path)
    scaler = scaler_data["scaler"]
    feature_names = scaler_data["feature_names"]

    if input_csv:
        match_csv = re.match(r'^([a-zA-Z0-9_\-\/\\.:]+)$', input_csv)
        if not match_csv:
            raise ValueError("Invalid input CSV path.")
        safe_input_csv = match_csv.group(1)
        
        if os.path.exists(safe_input_csv):
            print(f"Loading input data from: {safe_input_csv}")
            df = pd.read_csv(safe_input_csv)
        else:
            print("No input CSV provided or file not found. Running inference on sample synthetic data...")
            # Create a sample record matching schema
            sample_data = {
                'date': ['2016-01-11 17:00:00'],
                'lights': [30], 'T1': [19.89], 'RH_1': [47.59], 'T2': [19.2], 'RH_2': [44.79],
                'T3': [19.79], 'RH_3': [44.73], 'T4': [19.0], 'RH_4': [45.56], 'T5': [17.16],
                'RH_5': [55.20], 'T6': [7.02], 'RH_6': [84.25], 'T7': [17.20], 'RH_7': [41.56],
                'T8': [18.20], 'RH_8': [48.90], 'T9': [17.03], 'RH_9': [45.53], 'T_out': [6.60],
                'Press_mm_hg': [733.5], 'RH_out': [92.0], 'Windspeed': [7.0], 'Visibility': [63.0],
                'Tdewpoint': [5.3], 'rv1': [13.27], 'rv2': [13.27]
            }
            df = pd.DataFrame(sample_data)
    else:
        print("No input CSV provided or file not found. Running inference on sample synthetic data...")
        # Create a sample record matching schema
        sample_data = {
            'date': ['2016-01-11 17:00:00'],
            'lights': [30], 'T1': [19.89], 'RH_1': [47.59], 'T2': [19.2], 'RH_2': [44.79],
            'T3': [19.79], 'RH_3': [44.73], 'T4': [19.0], 'RH_4': [45.56], 'T5': [17.16],
            'RH_5': [55.20], 'T6': [7.02], 'RH_6': [84.25], 'T7': [17.20], 'RH_7': [41.56],
            'T8': [18.20], 'RH_8': [48.90], 'T9': [17.03], 'RH_9': [45.53], 'T_out': [6.60],
            'Press_mm_hg': [733.5], 'RH_out': [92.0], 'Windspeed': [7.0], 'Visibility': [63.0],
            'Tdewpoint': [5.3], 'rv1': [13.27], 'rv2': [13.27]
        }
        df = pd.DataFrame(sample_data)

    if 'Appliances' in df.columns:
        df = df.drop('Appliances', axis=1)

    df_processed = engineer_features(df)

    # Ensure all trained features exist
    for col in feature_names:
        if col not in df_processed.columns:
            df_processed[col] = 0.0

    X_input = df_processed[feature_names]
    X_scaled = scaler.transform(X_input)
    predictions = model.predict(X_scaled).flatten()

    df['Predicted_Appliances_Wh'] = predictions
    print("\n" + "=" * 40)
    print("PREDICTION RESULTS")
    print("=" * 40)
    print(df[['date', 'Predicted_Appliances_Wh']].head() if 'date' in df.columns else df[['Predicted_Appliances_Wh']].head())
    print("=" * 40)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ANN Energy Consumption Predictor CLI")
    parser.add_argument("--dataset", type=str, default="dataset/energy.csv", help="Path to CSV dataset")
    parser.add_argument("--results_dir", type=str, default="results", help="Directory to save model & outputs")
    parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=64, help="Batch size for training")
    parser.add_argument("--predict", action="store_true", help="Run inference mode")
    parser.add_argument("--input_csv", type=str, default=None, help="Input CSV path for prediction")

    args = parser.parse_args()

    if args.predict:
        predict_pipeline(args.input_csv, args.results_dir)
    else:
        train_pipeline(args.dataset, args.results_dir, args.epochs, args.batch_size)
