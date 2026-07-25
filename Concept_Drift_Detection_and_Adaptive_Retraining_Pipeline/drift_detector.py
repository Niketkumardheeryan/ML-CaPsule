import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

def calculate_psi(reference, target, num_bins=10, epsilon=1e-4):
    """
    Calculates the Population Stability Index (PSI) between reference and target datasets.
    
    PSI = sum((target_pct - reference_pct) * ln(target_pct / reference_pct))
    
    Threshold guidelines:
    - PSI < 0.1: No significant change (stable)
    - 0.1 <= PSI < 0.25: Moderate change / shift
    - PSI >= 0.25: Significant change / shift (drift)
    """
    # Convert inputs to numpy arrays
    reference = np.array(reference)
    target = np.array(target)
    
    # Determine bin edges based on reference dataset quantiles
    percentiles = np.linspace(0, 100, num_bins + 1)
    bin_edges = np.percentile(reference, percentiles)
    
    # Adjust boundaries to handle edge cases/duplicates
    bin_edges[0] -= epsilon
    bin_edges[-1] += epsilon
    
    # Compute frequency of values in bins
    ref_counts, _ = np.histogram(reference, bins=bin_edges)
    target_counts, _ = np.histogram(target, bins=bin_edges)
    
    # Convert counts to percentages
    ref_pct = ref_counts / len(reference)
    target_pct = target_counts / len(target)
    
    # Apply epsilon correction to avoid division by zero or log(0)
    ref_pct = np.where(ref_pct == 0, epsilon, ref_pct)
    target_pct = np.where(target_pct == 0, epsilon, target_pct)
    
    # Normalize percentages again to sum to 1 after epsilon adjustment
    ref_pct = ref_pct / np.sum(ref_pct)
    target_pct = target_pct / np.sum(target_pct)
    
    # Calculate PSI
    psi_value = np.sum((target_pct - ref_pct) * np.log(target_pct / ref_pct))
    
    return psi_value

def calculate_ks_test(reference, target):
    """
    Performs the two-sample Kolmogorov-Smirnov test to detect distribution differences.
    
    Returns:
    - ks_stat: The KS statistic
    - p_value: The two-tailed p-value
    - drift_detected: True if p_value < 0.05 (reject null hypothesis of identical distributions)
    """
    ks_stat, p_value = ks_2samp(reference, target)
    drift_detected = p_value < 0.05
    return ks_stat, p_value, drift_detected

def check_feature_drift(reference_df, target_df, features, psi_threshold=0.25):
    """
    Evaluates drift across multiple features using PSI and KS Test.
    
    Returns a dictionary with detailed metrics per feature.
    """
    drift_report = {}
    
    for feature in features:
        ref_data = reference_df[feature].dropna()
        tgt_data = target_df[feature].dropna()
        
        # Calculate metrics
        psi_val = calculate_psi(ref_data, tgt_data)
        ks_stat, p_val, ks_drift = calculate_ks_test(ref_data, tgt_data)
        
        psi_drift = psi_val >= psi_threshold
        
        drift_report[feature] = {
            'psi_value': psi_val,
            'psi_drift_detected': bool(psi_drift),
            'ks_statistic': ks_stat,
            'ks_p_value': p_val,
            'ks_drift_detected': bool(ks_drift),
            'overall_drift_detected': bool(psi_drift or ks_drift)
        }
        
    return drift_report
