"""Train the XGBoost model and save artifacts the Streamlit app will load."""
import json
import os
import pickle

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report
from xgboost import XGBClassifier

RNG = 42
DATA = "data/StressLevelDataset.csv"
OUT = "models"
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(DATA)
X = df.drop(columns=["stress_level"])
y = df["stress_level"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RNG, stratify=y
)

model = XGBClassifier(
    n_estimators=300, max_depth=4, learning_rate=0.1,
    objective="multi:softprob", num_class=3,
    eval_metric="mlogloss", random_state=RNG, n_jobs=-1,
)
model.fit(X_train, y_train)
preds = model.predict(X_test)

acc = accuracy_score(y_test, preds)
mf1 = f1_score(y_test, preds, average="macro")
print(f"Test accuracy: {acc:.4f}")
print(f"Test macro-F1: {mf1:.4f}")
print(classification_report(y_test, preds, target_names=["low", "medium", "high"]))

# Save model
with open(f"{OUT}/stress_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save feature ranges (used by the Streamlit sliders)
feature_meta = {}
for col in X.columns:
    feature_meta[col] = {
        "min": int(X[col].min()),
        "max": int(X[col].max()),
        "default": int(X[col].median()),
    }

with open(f"{OUT}/feature_meta.json", "w") as f:
    json.dump({
        "features": list(X.columns),
        "ranges": feature_meta,
        "test_accuracy": round(acc, 4),
        "test_macro_f1": round(mf1, 4),
        "feature_importance": dict(zip(X.columns,
                                        [round(float(v), 4) for v in model.feature_importances_])),
    }, f, indent=2)

print(f"Saved {OUT}/stress_model.pkl + feature_meta.json")
