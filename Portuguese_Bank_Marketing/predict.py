import os
import sys
import json
import argparse
import numpy as np
import pandas as pd
import joblib

def preprocess_input(data: dict) -> pd.DataFrame:
    """
    Applies the same feature engineering steps used during model training.
    """
    df = pd.DataFrame([data])
    
    # 1. previously_contacted (as coded in the notebook)
    if 'pdays' in df.columns:
        df['previously_contacted'] = (df['pdays'] != 999).astype(int)
        
    # 2. campaign_log
    if 'campaign' in df.columns:
        df['campaign_log'] = np.log1p(df['campaign'])
        
    # 3. campaign_level
    def bucket_campaign(c):
        if c <= 2: return 'low'
        elif c <= 5: return 'medium'
        else: return 'high'
    
    if 'campaign' in df.columns:
        df['campaign_level'] = df['campaign'].apply(bucket_campaign)
        
    # 4. previous_campaign_interaction
    if 'previous' in df.columns and 'previously_contacted' in df.columns:
        df['previous_campaign_interaction'] = df['previous'] * df['previously_contacted']
        
    # Drop the original 'campaign' feature as it was dropped in the training set
    if 'campaign' in df.columns:
        df = df.drop(columns=['campaign'])
        
    return df

def predict(data: dict, model_path: str):
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' not found.")
        print("Please ensure the model has been saved by running the Jupyter Notebook first.")
        sys.exit(1)
        
    try:
        model = joblib.load(model_path)
    except Exception as e:
        print(f"Error loading model from {model_path}: {e}")
        sys.exit(1)
        
    processed_df = preprocess_input(data)
    
    # Check if we have all the required features
    if hasattr(model, 'feature_names_in_'):
        expected_features = model.feature_names_in_
        missing = [col for col in expected_features if col not in processed_df.columns]
        if missing:
            print(f"Warning: Missing expected features: {missing}. Filling with default 0/Unknown.")
            for col in missing:
                processed_df[col] = 0
        
        # Ensure correct column order
        processed_df = processed_df[expected_features]
    
    try:
        prediction = model.predict(processed_df)
        prob = model.predict_proba(processed_df)[:, 1]
    except Exception as e:
        print(f"Error making prediction: {e}")
        sys.exit(1)
    
    result = "Subscribed (Yes)" if prediction[0] == 1 else "Not Subscribed (No)"
    print("\n" + "="*50)
    print("PORTUGUESE BANK MARKETING - PREDICTION RESULT")
    print("="*50)
    print(f"Prediction      : {result}")
    print(f"Probability     : {prob[0]:.2%}")
    print("="*50 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict term deposit subscription using the trained Gradient Boosting model.")
    parser.add_argument(
        "--data", 
        type=str, 
        required=True,
        help="JSON string of client data (e.g., '{\"age\": 30, \"job\": \"management\", \"marital\": \"married\", \"education\": \"tertiary\", \"default\": \"no\", \"balance\": 1500, \"housing\": \"yes\", \"loan\": \"no\", \"contact\": \"cellular\", \"day\": 5, \"month\": \"may\", \"duration\": 250, \"campaign\": 1, \"pdays\": -1, \"previous\": 0, \"poutcome\": \"unknown\"}')"
    )
    parser.add_argument(
        "--model", 
        type=str, 
        default="model/gradient_boosting_model.pkl", 
        help="Path to the saved pipeline model file"
    )
    
    args = parser.parse_args()
    
    try:
        client_data = json.loads(args.data)
        predict(client_data, args.model)
    except json.JSONDecodeError:
        print("Error: --data must be a valid JSON string.")
        sys.exit(1)
