import pandas as pd
import re
import joblib

import seaborn as sns
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from xgboost import plot_importance

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from xgboost import XGBClassifier


import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_loader import load_flood_data

try:
    df = load_flood_data(file_name='flood.csv', local_path='../../data/flood.csv')
except FileNotFoundError as e:
    print(f"\nError: {e}")
    exit()

new_columns = []

for col in df.columns:
    new_col = col.lower()
    new_col = re.sub(r'[^a-zA-Z0-9]+', '_', new_col)
    new_col = new_col.strip('_')
    new_columns.append(new_col)

df.columns = new_columns

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

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

xgb_model = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=4,
    random_state=42
)

xgb_model.fit(X_train_scaled, y_train)
y_pred = xgb_model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)

print(f"\nXGBoost Accuracy: {accuracy * 100:.2f}%")

print("\nConfusion Matrix:")


#print(confusion_matrix(y_test, y_pred))
cm = confusion_matrix(y_test, y_pred)

sns.heatmap(cm, annot=True, fmt='d')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("XGBoost Confusion Matrix")
plt.show()


# #class distribution report
# sns.countplot(x='flood_occurred', data=df)
# plt.show()

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# Feature Importance
plot_importance(xgb_model)
plt.title("XGBoost Feature Importance")
plt.savefig('../../outputs/xgboost/feature_imp.png')
plt.show()


#SAVES OF MODEL AND SCALER
joblib.dump(xgb_model, '../../models/xgboost_model.joblib')
joblib.dump(scaler, '../../models/xgboost_scaler.joblib')

print("Model and scaler have been trained and saved successfully!")
print("Files created: xgb_model.joblib, scaler.joblib")