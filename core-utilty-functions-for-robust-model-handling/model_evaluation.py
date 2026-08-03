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