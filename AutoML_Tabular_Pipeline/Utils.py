import joblib
from sklearn.metrics import classification_report

def save_model(model, filepath="best_automl_model.pkl"):
    """Saves the pipeline architecture and serialized weights."""
    joblib.dump(model, filepath)
    print(f"[Success] Saved functional pipeline state to: '{filepath}'")

def generate_report(model, X_test, y_test):
    """Outputs performance evaluation matrices to the terminal."""
    predictions = model.predict(X_test)
    print("\n================ AutoML Performance Report ================")
    print(classification_report(y_test, predictions))
    print("==========================================================")
