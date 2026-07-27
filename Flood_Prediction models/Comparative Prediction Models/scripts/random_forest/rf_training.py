import pandas as pd
import re
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from sklearn.ensemble import RandomForestClassifier

import matplotlib.pyplot as plt
import seaborn as sns


import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_loader import load_flood_data

# Load Dataset
try:
    df = load_flood_data(file_name='flood.csv', local_path='../../data/flood.csv')

except FileNotFoundError as e:
    print(f"\nError: {e}")
    exit()


# Clean Column Names
new_columns = []

for col in df.columns:

    new_col = col.lower()
    new_col = re.sub(r'[^a-zA-Z0-9]+', '_', new_col)
    new_col = new_col.strip('_')

    new_columns.append(new_col)

df.columns = new_columns


# Features and Target
feature_names = [
    'rainfall',
    'temperature_c',
    'humidity',
    'water_level_m',
    'elevation_m'
]

target_name = 'flood_occurred'


X = df[feature_names]
y = df[target_name]


# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Feature Scaling
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Train Random Forest Model
rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train_scaled, y_train)


# Predictions
y_pred = rf_model.predict(X_test_scaled)


# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")


# Confusion Matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# Confusion Matrix Heatmap
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6,5))

sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues'
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Random Forest Confusion Matrix")

plt.savefig('../../outputs/random_forest/confusion_matrix.png')

plt.show()


# Feature Importance
importance = rf_model.feature_importances_

feature_importance = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importance
})

feature_importance = feature_importance.sort_values(
    by='Importance',
    ascending=False
)

#print("\nFeature Importance:")
#print(feature_importance)

plt.figure(figsize=(8,5))

sns.barplot(
    x='Importance',
    y='Feature',
    data=feature_importance
)

plt.title("Random Forest Feature Importance")

plt.savefig('../../outputs/random_forest/feature_imp.png')

plt.show()


#SAVES OF MODEL AND SCALER
joblib.dump(
    rf_model,
    '../../models/random_forest_model.joblib'
)

joblib.dump(
    scaler,
    '../../models/random_forest_scaler.joblib'
)


print("\nModel and scaler have been trained andsaved successfully!")
print("Files created: random_forest_model.joblib, random_forest_scaler.joblib")