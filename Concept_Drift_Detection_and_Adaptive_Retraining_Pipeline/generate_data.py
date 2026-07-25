import numpy as np
import pandas as pd

def generate_synthetic_data(n_samples_per_batch=1000, n_batches=10, random_seed=42):
    """
    Generates synthetic temporal data simulating covariate shift and concept drift.
    
    Features:
    - age: numerical (20-70)
    - income: numerical (annual in USD)
    - debt_to_income: ratio (0.0 to 1.0)
    - credit_score: numerical (300-850)
    
    Target:
    - default: 1 if borrower defaults, 0 otherwise
    """
    np.random.seed(random_seed)
    batches = []
    
    # Baseline coefficients for the probability of default
    # P(default) = sigmoid(w0 + w1*debt_to_income - w2*credit_score/850 - w3*income/100000)
    w_intercept = -1.0
    w_dti = 5.0
    w_credit = -4.0
    w_income = -1.5
    
    for batch_id in range(1, n_batches + 1):
        # Age remains stable across all batches
        age = np.random.randint(20, 70, size=n_samples_per_batch)
        
        # 1. Baseline Period (Batches 1-3)
        if batch_id <= 3:
            income = np.random.normal(60000, 15000, size=n_samples_per_batch)
            credit_score = np.random.normal(680, 50, size=n_samples_per_batch)
            debt_to_income = np.random.beta(2, 5, size=n_samples_per_batch) # Skewed towards lower ratios
            
        # 2. Covariate Shift Period (Batches 4-6)
        # Average income drops, debt-to-income ratio increases (e.g., economic downturn)
        # But the underlying relationship (coefficients) remains the same.
        elif 4 <= batch_id <= 6:
            income = np.random.normal(50000, 12000, size=n_samples_per_batch) # Lower income
            credit_score = np.random.normal(640, 60, size=n_samples_per_batch) # Lower credit score
            debt_to_income = np.random.beta(3, 4, size=n_samples_per_batch) # Shifted towards higher debt ratios
            
        # 3. Concept Drift Period (Batches 7-10)
        # Features return to normal or remain shifted, but the relationship shifts.
        # e.g., lenders become stricter, or default rates increase for a given credit score.
        else:
            income = np.random.normal(52000, 12000, size=n_samples_per_batch)
            credit_score = np.random.normal(650, 55, size=n_samples_per_batch)
            debt_to_income = np.random.beta(3, 4, size=n_samples_per_batch)
            
            # Change in coefficients (Concept Drift): debt-to-income and credit_score impact defaults more severely
            w_intercept = 0.5  # Higher baseline defaults
            w_dti = 7.0        # Higher impact of debt
            w_credit = -5.0    # Credit score has different sensitivity
            w_income = -1.0
            
        # Ensure values stay in reasonable ranges
        income = np.clip(income, 10000, 150000)
        credit_score = np.clip(credit_score, 300, 850)
        debt_to_income = np.clip(debt_to_income, 0.0, 1.0)
        
        # Calculate probability of default using Logistic Sigmoid
        # Standardize features for logistic equation
        norm_income = (income - 60000) / 15000
        norm_credit = (credit_score - 680) / 50
        norm_dti = (debt_to_income - 0.25) / 0.15
        
        logits = w_intercept + (w_dti * norm_dti) + (w_credit * norm_credit) + (w_income * norm_income)
        probs = 1 / (1 + np.exp(-logits))
        
        # Binary target
        default = np.random.binomial(1, probs)
        
        # Construct DataFrame
        df = pd.DataFrame({
            'age': age,
            'income': income,
            'debt_to_income': debt_to_income,
            'credit_score': credit_score,
            'default': default,
            'batch_id': batch_id
        })
        
        batches.append(df)
        
    full_df = pd.concat(batches, ignore_index=True)
    return full_df

if __name__ == "__main__":
    df = generate_synthetic_data()
    print("Generated data summary:")
    print(df.groupby('batch_id').agg({
        'income': 'mean',
        'debt_to_income': 'mean',
        'credit_score': 'mean',
        'default': 'mean'
    }))
    df.to_csv("synthetic_loan_data.csv", index=False)
    print("Saved synthetic data to synthetic_loan_data.csv")
