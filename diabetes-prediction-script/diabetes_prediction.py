from utils.error_handler import error_handler, DataValidationError, ModelError
import pandas as pd
import numpy as np

@error_handler
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            raise DataValidationError("Empty dataset loaded")
        return df
    except FileNotFoundError:
        raise DataValidationError(f"Dataset not found at {file_path}")

@error_handler
def preprocess_data(df):
    if not isinstance(df, pd.DataFrame):
        raise DataValidationError("Input must be a pandas DataFrame")
    
    # Check for missing values
    if df.isnull().sum().any():
        logging.warning("Missing values detected in the dataset")
        df = df.fillna(df.mean())
    
    # Check for invalid values
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if (df[col] < 0).any():
            raise DataValidationError(f"Negative values found in column {col}")
    
    return df

@error_handler
def train_model(X_train, y_train, model_type='random_forest'):
    if len(X_train) != len(y_train):
        raise DataValidationError("Feature and target dimensions do not match")
    
    try:
        if model_type == 'random_forest':
            from sklearn.ensemble import RandomForestClassifier
            model = RandomForestClassifier(random_state=42)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise ModelError(f"Model training failed: {str(e)}")