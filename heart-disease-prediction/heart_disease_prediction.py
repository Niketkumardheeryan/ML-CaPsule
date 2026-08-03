from utils.error_handler import error_handler, DataValidationError, ModelError
import pandas as pd
import numpy as np

@error_handler
def validate_heart_data(df):
    required_columns = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 
        'ca', 'thal', 'target'
    ]
    
    # Check required columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise DataValidationError(f"Missing required columns: {missing_cols}")
    
    # Validate value ranges
    if not (df['age'] >= 0).all():
        raise DataValidationError("Age cannot be negative")
    if not df['sex'].isin([0, 1]).all():
        raise DataValidationError("Sex must be binary (0 or 1)")
    if not (df['trestbps'] > 0).all():
        raise DataValidationError("Blood pressure must be positive")
    
    return True

@error_handler
def prepare_heart_data(df):
    try:
        validate_heart_data(df)
        
        # Handle missing values
        if df.isnull().sum().any():
            logging.warning("Missing values found - applying mean imputation")
            df = df.fillna(df.mean())
        
        # Feature scaling
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
        
        return df
    except Exception as e:
        raise DataValidationError(f"Data preparation failed: {str(e)}") 