"""
Utility module for Startup Profit Prediction project.
Contains data loading, preprocessing, and model saving/loading helper functions.
"""
from pathlib import Path
import pandas as pd
import joblib

# Constants mapping the exact feature structure from the notebook
CATEGORICAL_COLUMN = "State"
EXPECTED_DUMMY_COLUMNS = ["State_California", "State_Florida", "State_New York"]
FEATURE_COLUMNS = [
    "R&D Spend",
    "Administration",
    "Marketing Spend",
    "State_California",
    "State_Florida",
    "State_New York"
]


def load_dataset(file_path: Path) -> pd.DataFrame:
    """
    Loads dataset from a CSV file.

    Parameters:
    -----------
    file_path : Path
        Path to the CSV dataset file.

    Returns:
    --------
    pd.DataFrame
        Loaded pandas DataFrame.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found at {file_path}")
    return pd.read_csv(file_path)


def preprocess_data(df: pd.DataFrame, is_training: bool = True) -> tuple or pd.DataFrame:
    """
    Applies the encoding, feature selection, and datatype conversion pipeline
    exactly matching the original Jupyter Notebook.

    For training:
        - One-hot encodes 'State'
        - Drops the 'State' column
        - Concatenates dummy columns
        - Casts everything (features and target 'Profit') to int
        - Returns (X, y)

    For prediction/inference:
        - Handles encoding of 'State'
        - Aligns dummy column structure to match training columns
        - Casts features to int
        - Returns X

    Parameters:
    -----------
    df : pd.DataFrame
        Input data before preprocessing.
    is_training : bool
        True if preprocessing training data (returns X, y), False for inference (returns X).

    Returns:
    --------
    tuple (pd.DataFrame, pd.Series) or pd.DataFrame
        Preprocessed X (and y if is_training is True).
    """
    df_copy = df.copy()

    # Step 1: One-hot encode the categorical 'State' column
    if CATEGORICAL_COLUMN in df_copy.columns:
        df_encoded = pd.get_dummies(df_copy, columns=[CATEGORICAL_COLUMN])
    else:
        df_encoded = df_copy

    # Step 2: Align with the expected one-hot columns (e.g., California, Florida, New York)
    for col in EXPECTED_DUMMY_COLUMNS:
        if col not in df_encoded.columns:
            df_encoded[col] = 0

    # Ensure all required features are present (if any numeric feature is missing)
    for col in FEATURE_COLUMNS:
        if col not in df_encoded.columns:
            df_encoded[col] = 0

        # Step 3: Fast cast features to int as done in the notebook: prepareddata = newdata.astype(int)
        df_encoded[col] = df_encoded[col].fillna(0).astype(int)

    # Reorder columns to ensure exact matching sequence
    x = df_encoded[FEATURE_COLUMNS]

    if is_training:
        if "Profit" in df_encoded.columns:
            y = df_encoded["Profit"].astype(int)
        else:
            raise KeyError("Target column 'Profit' is missing from the training dataset.")
        return x, y
    
    return x


def save_model(model, file_path: Path) -> None:
    """
    Serializes and saves a model using joblib.

    Parameters:
    -----------
    model : scikit-learn model object
        The trained estimator to serialise.
    file_path : Path
        Where to save the joblib file.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, file_path)


def load_model(file_path: Path):
    """
    Loads a serialized model from a joblib file.

    Parameters:
    -----------
    file_path : Path
        Path to the joblib file.

    Returns:
    --------
    scikit-learn model object
        The deserialised model.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Serialized model file not found at {file_path}")
    return joblib.load(file_path)
