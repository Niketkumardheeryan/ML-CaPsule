import pandas as pd
import re
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_loader import load_flood_data

# Load dataset
df = load_flood_data(file_name='flood.csv', local_path='../../data/flood.csv')

# Clean column names
new_columns = []

for col in df.columns:
    new_col = col.lower()
    new_col = re.sub(r'[^a-zA-Z0-9]+', '_', new_col)
    new_col = new_col.strip('_')
    new_columns.append(new_col)

df.columns = new_columns

# Features and target
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

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Scaling
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Logistic Regression model
lr_model = LogisticRegression(
    random_state=42,
    max_iter=1000
)

# Train model
lr_model.fit(X_train_scaled, y_train)

# Predictions
y_pred = lr_model.predict(X_test_scaled)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# Confusion Matrix Plot
plt.figure(figsize=(6,5))

sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=['No Flood', 'Flood'],
    yticklabels=['No Flood', 'Flood']
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Logistic Regression Confusion Matrix")

plt.savefig('../../outputs/logistic_regression/confusion_matrix.png')

plt.show()

importance = lr_model.coef_[0]

feature_importance = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importance
})

feature_importance = feature_importance.sort_values(
    by='Importance',
    ascending=False
)

# print("\nFeature Importance:")
# print(feature_importance)

plt.figure(figsize=(8,5))

sns.barplot(
    x='Importance',
    y='Feature',
    data=feature_importance
)

plt.title("Logistic Regression Feature Importance")

plt.savefig('../../outputs/logistic_regression/feature_importance.png')

plt.show()

# Save model and scaler
joblib.dump(
    lr_model,
    '../../models/logistic_regression_model.joblib'
)

joblib.dump(
    scaler,
    '../../models/logistic_regression_scaler.joblib'
)

print("\nModel and scaler saved successfully!")

print(
    "Files created: logistic_regression_model.joblib, logistic_regression_scaler.joblib"
)



# # Class Distribution Plot

# plt.figure(figsize=(6,5))

# sns.countplot(
#     x='flood_occurred',
#     data=df
# )

# plt.title("Class Distribution")

# plt.savefig('../../outputs/logistic_regression/class_distribution.png')

# plt.show()

