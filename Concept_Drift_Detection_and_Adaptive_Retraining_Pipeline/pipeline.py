import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import StandardScaler

from generate_data import generate_synthetic_data
from drift_detector import check_feature_drift

# Set style for nice charts
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'figure.titlesize': 18
})

def run_drift_pipeline():
    # Create outputs directory if it doesn't exist
    os.makedirs("outputs", exist_ok=True)
    
    # 1. Generate Synthetic Data
    print("Generating synthetic temporal data...")
    df = generate_synthetic_data(n_samples_per_batch=1200, n_batches=10, random_seed=42)
    
    features = ['age', 'income', 'debt_to_income', 'credit_score']
    target = 'default'
    
    # Split each batch into train (800 samples) and test (400 samples)
    # This ensures evaluation is done on unseen test data for that period.
    train_size = 800
    
    # Batch 1 is our baseline reference
    batch_1 = df[df['batch_id'] == 1]
    batch_1_train = batch_1.iloc[:train_size]
    batch_1_test = batch_1.iloc[train_size:]
    
    X_train_baseline = batch_1_train[features]
    y_train_baseline = batch_1_train[target]
    
    X_test_baseline = batch_1_test[features]
    y_test_baseline = batch_1_test[target]
    
    # Train scaler
    scaler = StandardScaler()
    X_train_baseline_scaled = scaler.fit_transform(X_train_baseline)
    X_test_baseline_scaled = scaler.transform(X_test_baseline)
    
    # Train initial baseline model
    print("Training baseline model on Batch 1 (Train)...")
    model_no_retrain = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=6)
    model_no_retrain.fit(X_train_baseline_scaled, y_train_baseline)
    
    # Adaptive model starts as a copy of the baseline model
    model_adaptive = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=6)
    model_adaptive.fit(X_train_baseline_scaled, y_train_baseline)
    
    # We will track statistics for plotting
    history = []
    
    print("\nStarting batch monitoring pipeline...")
    print(f"{'Batch':<6} | {'PSI (DTI)':<10} | {'KS p-val (DTI)':<15} | {'F1 (Static)':<12} | {'F1 (Adapt)':<12} | {'Retrained?'}")
    print("-" * 80)
    
    # Reference data for drift checking is Batch 1 Train
    reference_df = batch_1_train
    
    for batch_id in range(2, 11):
        batch_df = df[df['batch_id'] == batch_id]
        batch_train = batch_df.iloc[:train_size]
        batch_test = batch_df.iloc[train_size:]
        
        X_train = batch_train[features]
        y_train = batch_train[target]
        X_test = batch_test[features]
        y_test = batch_test[target]
        
        # Standardize
        X_train_scaled = scaler.transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # 1. Detect Drift using train features
        drift_report = check_feature_drift(reference_df, batch_train, features)
        
        # Check if any feature has significant drift (PSI >= 0.2)
        drift_features = [f for f, report in drift_report.items() if report['psi_value'] >= 0.2]
        drift_detected = len(drift_features) > 0
        
        # Get stats for debt_to_income feature for logging/plotting
        dti_psi = drift_report['debt_to_income']['psi_value']
        dti_p_val = drift_report['debt_to_income']['ks_p_value']
        
        # 2. Evaluate Performance of Static Model (No Retraining) on unseen test split
        y_pred_static = model_no_retrain.predict(X_test_scaled)
        acc_static = accuracy_score(y_test, y_pred_static)
        f1_static = f1_score(y_test, y_pred_static)
        
        # 3. Evaluate Performance of Adaptive Model (Before retraining on this batch) on unseen test split
        y_pred_adaptive_pre = model_adaptive.predict(X_test_scaled)
        acc_adaptive_pre = accuracy_score(y_test, y_pred_adaptive_pre)
        f1_adaptive_pre = f1_score(y_test, y_pred_adaptive_pre)
        
        # 4. Adaptive Retraining Trigger
        retrained = False
        if drift_detected:
            # Trigger retraining using current batch train split
            model_adaptive = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=6)
            model_adaptive.fit(X_train_scaled, y_train)
            
            # Re-evaluate performance of the adaptive model post-retraining on test split
            y_pred_adaptive_post = model_adaptive.predict(X_test_scaled)
            acc_adaptive = accuracy_score(y_test, y_pred_adaptive_post)
            f1_adaptive = f1_score(y_test, y_pred_adaptive_post)
            retrained = True
        else:
            acc_adaptive = acc_adaptive_pre
            f1_adaptive = f1_adaptive_pre
            
        print(f"{batch_id:<6} | {dti_psi:<10.3f} | {dti_p_val:<15.3e} | {f1_static:<12.3f} | {f1_adaptive:<12.3f} | {str(retrained):<10}")
        
        history.append({
            'batch_id': batch_id,
            'dti_psi': dti_psi,
            'dti_p_val': dti_p_val,
            'acc_static': acc_static,
            'acc_adaptive': acc_adaptive,
            'f1_static': f1_static,
            'f1_adaptive': f1_adaptive,
            'drift_detected': drift_detected,
            'retrained': retrained
        })
        
    history_df = pd.DataFrame(history)
    
    # 5. Visualizations
    # Chart 1: Model F1-Score Over Batches
    plt.figure(figsize=(10, 6))
    plt.plot(history_df['batch_id'], history_df['f1_static'], marker='o', linewidth=2.5, label='Static Model (No Retrain)', color='#e74c3c')
    plt.plot(history_df['batch_id'], history_df['f1_adaptive'], marker='s', linewidth=2.5, label='Adaptive Model (With Retraining)', color='#2ecc71')
    
    # Highlight retraining points
    retrain_points = history_df[history_df['retrained'] == True]
    if not retrain_points.empty:
        plt.scatter(retrain_points['batch_id'], retrain_points['f1_adaptive'], color='blue', s=150, zorder=5, 
                    label='Retraining Triggered (Drift Detected)', marker='*')
        
    plt.title("Model F1-Score Over Time Under Concept/Data Drift", pad=15)
    plt.xlabel("Batch ID (Time Steps)")
    plt.ylabel("F1-Score")
    plt.xticks(range(2, 11))
    plt.ylim(0.4, 1.0)
    plt.legend(frameon=True, facecolor='white', edgecolor='none')
    plt.tight_layout()
    plt.savefig("outputs/f1_comparison.png", dpi=300)
    plt.close()
    
    # Chart 2: Feature distribution comparison before vs after drift
    plt.figure(figsize=(12, 5))
    
    # Reference (Batch 1) vs Covariate Shift (Batch 5) vs Concept Drift (Batch 9)
    plt.subplot(1, 2, 1)
    sns.kdeplot(df[df['batch_id'] == 1]['debt_to_income'], label='Batch 1 (Baseline)', fill=True, color='#3498db')
    sns.kdeplot(df[df['batch_id'] == 5]['debt_to_income'], label='Batch 5 (Data Drift)', fill=True, color='#f1c40f')
    sns.kdeplot(df[df['batch_id'] == 9]['debt_to_income'], label='Batch 9 (Concept Drift)', fill=True, color='#e67e22')
    plt.title("Feature Distribution Shift (Debt-to-Income)")
    plt.xlabel("Debt-to-Income Ratio")
    plt.legend(frameon=True)
    
    # Drift metric over time
    plt.subplot(1, 2, 2)
    plt.plot(history_df['batch_id'], history_df['dti_psi'], marker='o', color='#8e44ad', linewidth=2)
    plt.axhline(y=0.25, color='r', linestyle='--', label='Action Limit (PSI = 0.25)')
    plt.axhline(y=0.1, color='g', linestyle='--', label='Warning Limit (PSI = 0.1)')
    plt.title("Population Stability Index (PSI) Over Time")
    plt.xlabel("Batch ID")
    plt.ylabel("PSI Value")
    plt.xticks(range(2, 11))
    plt.legend(frameon=True)
    
    plt.tight_layout()
    plt.savefig("outputs/drift_analysis.png", dpi=300)
    plt.close()
    
    print("\nPipeline execution complete! Visualizations saved to the 'outputs' directory.")

if __name__ == "__main__":
    run_drift_pipeline()
