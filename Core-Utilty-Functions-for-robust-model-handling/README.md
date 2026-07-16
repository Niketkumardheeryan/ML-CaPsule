Core Utilities

This project includes a set of essential utilities for error handling and model evaluation.

`error_handler.py`

This module provides a centralized logging configuration and defines custom exceptions to ensure robust error management throughout the application. It features an @error_handler decorator that can wrap functions to catch, log, and re-raise errors consistently.
```python
import logging
import sys
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ml_capsule.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class MLCapsuleError(Exception):
    """Base exception class for ML-CaPsule"""
    pass

class DataValidationError(MLCapsuleError):
    """Raised when data validation fails"""
    pass

class ModelError(MLCapsuleError):
    """Raised when model operations fail"""
    pass

def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MLCapsuleError as e:
            logging.error(f"ML-CaPsule error in {func.__name__}: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in {func.__name__}: {str(e)}")
            raise MLCapsuleError(f"Function {func.__name__} failed: {str(e)}")
    return wrapper
```


`model_evaluation.py`

This script contains functions for evaluating the performance of classification models. It relies on the error_handler to gracefully handle issues like dimension mismatches during evaluation.
```python
from utils.error_handler import error_handler, ModelError
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np

@error_handler
def evaluate_classification_model(y_true, y_pred):
    if len(y_true) != len(y_pred):
        raise ModelError("Prediction and ground truth dimensions do not match")
    
    try:
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1': f1_score(y_true, y_pred, average='weighted')
        }
        
        return metrics
    except Exception as e:
        raise ModelError(f"Model evaluation failed: {str(e)}")

@error_handler
def cross_validate_model(model, X, y, cv=5):
    from sklearn.model_selection import cross_val_score
    
    try:
        scores = cross_val_score(model, X, y, cv=cv)
        return {
            'mean_score': np.mean(scores),
            'std_score': np.std(scores),
            'scores': scores
        }
    except Exception as e:
        raise ModelError(f"Cross-validation failed: {str(e)}")
```


`model_evaluation.ipynb`

An interactive Jupyter Notebook showcasing the use case of the evaluation script, useful for prototyping and data exploration. (Note: The raw JSON structure of the notebook is not displayed here for brevity).
