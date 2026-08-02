import os
import time
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score, confusion_matrix

# SMOTE
from imblearn.over_sampling import SMOTE

# Models
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.svm import SVC

# Explainability
import shap

def train_and_evaluate():
    print("Loading dataset...")
    data_path = os.path.join(os.path.dirname(__file__), 'cicids2017_sample.csv')
    df = pd.read_csv(data_path)
    
    # Feature & Label Separation
    X = df.drop(columns=['Label'])
    y = df['Label']
    
    # Encode target labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Train-test split (stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print("\nClass distribution before SMOTE (Train):")
    unique, counts = np.unique(y_train, return_counts=True)
    for u, c in zip(unique, counts):
        print(f"  {label_encoder.inverse_transform([u])[0]}: {c}")
        
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Handle Class Imbalance using SMOTE
    print("\nApplying SMOTE...")
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train_scaled, y_train)
    
    print("Class distribution after SMOTE (Train):")
    unique_res, counts_res = np.unique(y_train_res, return_counts=True)
    for u, c in zip(unique_res, counts_res):
        print(f"  {label_encoder.inverse_transform([u])[0]}: {c}")
        
    # Models initialization
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42, n_jobs=-1),
        'LightGBM': LGBMClassifier(random_state=42, n_jobs=-1, verbose=-1),
        'SVM': SVC(probability=True, random_state=42)
    }
    
    results = {}
    trained_models = {}
    
    # Training and evaluation loop
    for name, model in models.items():
        print(f"\nTraining {name}...")
        start_time = time.time()
        model.fit(X_train_res, y_train_res)
        training_time = time.time() - start_time
        
        # Inference speed test (predict on test set)
        start_inf = time.time()
        y_pred = model.predict(X_test_scaled)
        y_prob = model.predict_proba(X_test_scaled)
        inference_time = time.time() - start_inf
        
        # Metrics
        acc = accuracy_score(y_test, y_pred)
        prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
        
        # One-vs-rest ROC AUC for multi-class
        try:
            roc_auc = roc_auc_score(y_test, y_prob, multi_class='ovr', average='weighted')
        except Exception:
            roc_auc = 0.0
            
        cm = confusion_matrix(y_test, y_pred)
        
        # Calculate inference speed in microseconds per packet
        speed_per_packet_us = (inference_time / len(X_test_scaled)) * 1e6
        
        print(f"  Accuracy: {acc:.4f}")
        print(f"  F1-Score: {f1:.4f}")
        print(f"  Training Time: {training_time:.2f}s")
        print(f"  Inference Speed: {speed_per_packet_us:.2f} microseconds/packet")
        
        results[name] = {
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1-Score': f1,
            'ROC-AUC': roc_auc,
            'Training Time (s)': training_time,
            'Inference Speed (us/packet)': speed_per_packet_us,
            'Confusion Matrix': cm.tolist()
        }
        trained_models[name] = model

    # Feature correlation analysis (correlation matrix)
    corr_matrix = pd.DataFrame(X_train_scaled, columns=X.columns).corr()
    
    # Save objects to pickle for Streamlit
    print("\nSaving models and artifacts...")
    artifacts = {
        'scaler': scaler,
        'label_encoder': label_encoder,
        'models': trained_models,
        'results': results,
        'feature_names': list(X.columns),
        'corr_matrix': corr_matrix.to_dict()
    }
    
    artifacts_path = os.path.join(os.path.dirname(__file__), 'trained_artifacts.pkl')
    with open(artifacts_path, 'wb') as f:
        pickle.dump(artifacts, f)
    print(f"Saved artifacts to {artifacts_path}")

    # Generate SHAP values for RF model as a representative explainability model
    print("\nComputing SHAP values for Random Forest model on sample...")
    # Use a small background dataset for SHAP to make it fast
    background_summary = shap.kmeans(X_train_res, 10)
    explainer = shap.KernelExplainer(trained_models['Random Forest'].predict_proba, background_summary)
    
    # Sample a small test subset for visualization
    sample_indices = np.random.choice(len(X_test_scaled), size=30, replace=False)
    X_sample = X_test_scaled[sample_indices]
    
    shap_values = explainer.shap_values(X_sample)
    
    shap_artifacts = {
        'X_sample': X_sample,
        'shap_values': shap_values,
        'sample_labels': y_test[sample_indices]
    }
    
    shap_path = os.path.join(os.path.dirname(__file__), 'shap_artifacts.pkl')
    with open(shap_path, 'wb') as f:
        pickle.dump(shap_artifacts, f)
    print(f"Saved SHAP values to {shap_path}")

if __name__ == '__main__':
    train_and_evaluate()
