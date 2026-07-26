import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

# Base directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(BASE_DIR, exist_ok=True)

# Dataset Source URL (RAW link to GitHub branch)
DATASET_URL = "https://raw.githubusercontent.com/Rakshak05/ML-CaPsule/issue-%232028/E-Waste_Impact_Calculator_Recycling_Locator/dataset.csv"

# Define feature spaces
categories = ["Smartphone", "Laptop", "Desktop", "Tablet", "Television", "Smartwatch"]
brands = ["Apple", "Samsung", "Dell", "HP", "Lenovo", "LG", "Sony", "Asus", "Acer", "Generic"]
conditions = ["New", "Good", "Fair", "Poor", "Non-Functional"]

num_samples = 2500

# Try to load the dataset from remote URL
df = None
try:
    print(f"Attempting to download dataset from URL: {DATASET_URL}")
    df = pd.read_csv(DATASET_URL)
    print("Dataset successfully loaded from remote URL!")
except Exception as e:
    print(f"Could not load remote dataset: {e}")
    print("Falling back to local synthetic data generation...")

if df is None:
    # Set random seed for reproducibility
    np.random.seed(42)

    # Generate synthetic features
    data = {
        "category": np.random.choice(categories, num_samples),
        "brand": np.random.choice(brands, num_samples),
        "age_years": np.random.uniform(0.1, 12.0, num_samples),
        "condition": np.random.choice(conditions, num_samples),
    }

    df = pd.DataFrame(data)

    # Helper functions to determine target values realistically
    def calculate_metrics(row):
        cat = row["category"]
        brand = row["brand"]
        age = row["age_years"]
        cond = row["condition"]
        
        # 1. CO2 Footprint base values (kg CO2 eq)
        co2_base = {
            "Smartphone": 75,
            "Laptop": 300,
            "Desktop": 600,
            "Tablet": 150,
            "Television": 500,
            "Smartwatch": 35
        }
        
        brand_co2_factor = {
            "Apple": 1.15, "Samsung": 1.1, "Dell": 1.05, "HP": 1.05, 
            "Lenovo": 1.0, "LG": 1.0, "Sony": 1.1, "Asus": 0.95, 
            "Acer": 0.9, "Generic": 0.85
        }
        
        co2 = co2_base[cat] * brand_co2_factor[brand]
        # Add random noise
        co2 += np.random.normal(0, co2 * 0.05)
        co2 = max(10.0, co2)
        
        # 2. Toxic Material Score (0 - 100)
        toxic_base = {
            "Smartphone": 65,
            "Laptop": 75,
            "Desktop": 85,
            "Tablet": 60,
            "Television": 80,
            "Smartwatch": 45
        }
        # Older items have higher toxic component hazard (older manufacturing standards)
        age_toxic_factor = 1.0 + (age / 12.0) * 0.2
        
        toxic = toxic_base[cat] * age_toxic_factor
        # Add noise
        toxic += np.random.normal(0, 5)
        toxic = np.clip(toxic, 10, 100)
        
        # 3. Recyclability Score (0 - 100%)
        recyclability_base = {
            "Smartphone": 80,
            "Laptop": 70,
            "Desktop": 60,
            "Tablet": 75,
            "Television": 50,
            "Smartwatch": 85
        }
        
        cond_factor = {
            "New": 10,
            "Good": 5,
            "Fair": 0,
            "Poor": -15,
            "Non-Functional": -30
        }
        
        # Recyclability drops with age and worse condition
        recyclability = recyclability_base[cat] + cond_factor[cond] - (age * 2.5)
        recyclability += np.random.normal(0, 3)
        recyclability = np.clip(recyclability, 5, 98)
        
        return pd.Series([round(co2, 2), round(toxic, 1), round(recyclability, 1)])

    # Apply the metrics function to generate labels
    df[["co2_footprint", "toxic_score", "recyclability"]] = df.apply(calculate_metrics, axis=1)

    # Save generated dataset to CSV for reference
    df.to_csv(os.path.join(BASE_DIR, "dataset.csv"), index=False)
    print("Dataset generated successfully!")


# Apply the metrics function to generate labels
df[["co2_footprint", "toxic_score", "recyclability"]] = df.apply(calculate_metrics, axis=1)

# Save generated dataset to CSV for reference
df.to_csv(os.path.join(BASE_DIR, "dataset.csv"), index=False)
print("Dataset generated successfully!")

# Encoding categorical columns
encoders = {}
df_encoded = df.copy()

for col in ["category", "brand", "condition"]:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df[col])
    encoders[col] = le

# Prepare features and targets
X = df_encoded[["category", "brand", "age_years", "condition"]]
y = df_encoded[["co2_footprint", "toxic_score", "recyclability"]]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Regressor models for each target
models = {}
metrics = {}

for target in ["co2_footprint", "toxic_score", "recyclability"]:
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train[target])
    
    # Evaluate
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test[target], preds)
    r2 = r2_score(y_test[target], preds)
    
    models[target] = model
    metrics[target] = {"MAE": round(mae, 4), "R2": round(r2, 4)}
    print(f"Model for {target} - MAE: {round(mae, 4)}, R2: {round(r2, 4)}")

# Save everything using pickle
model_pack = {
    "models": models,
    "encoders": encoders,
    "categories": categories,
    "brands": brands,
    "conditions": conditions,
    "metrics": metrics
}

model_path = os.path.join(BASE_DIR, "e_waste_model.pkl")
with open(model_path, "wb") as f:
    pickle.dump(model_pack, f)

print(f"Model and assets saved to {model_path} successfully!")
