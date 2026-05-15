# Store all ML models in one place.
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier



def get_models():
    """Returns a dictionary of ML models for autism identification"""
    
    return {
        "Logistic Regression": LogisticRegression(random_state=42),
        "Support Vector Machine": SVC(random_state=42),
        "Random Forest": RandomForestClassifier(random_state=42)
    }
    
