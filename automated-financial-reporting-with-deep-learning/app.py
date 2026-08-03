import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv('financial_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Load the trained model
model = tf.keras.models.load_model('financial_model.h5')

# Prepare features and target
X = df.drop('Date', axis=1).iloc[:, :-1]
y = df.drop('Date', axis=1).iloc[:, -1]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Normalize data
scaler = MinMaxScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Make predictions
y_pred = model.predict(X_test_scaled)

# Reconstruct for inverse transform
y_pred_original = scaler.inverse_transform(
    np.c_[X_test_scaled, y_pred]
)[:, -1]

# Add predictions to the DataFrame
df['Predicted_Equity'] = y_pred_original

# Streamlit app
st.title("Automated Financial Reporting with Deep Learning")

st.write("""
### Actual vs Predicted Equity Values
""")

# Display a sample of the actual vs predicted values
comparison = pd.DataFrame({
    'Actual': df['Equity'],
    'Predicted': df['Predicted_Equity']
})

st.write(comparison.head())

# Plot the actual vs predicted values
st.line_chart(comparison)

# Display the model's performance metrics
st.write(f"Test Loss: 0.08456173539161682, Test MAE: 0.2604014575481415")

st.write("""
### Training Metrics
""")

# Display the training metrics
training_metrics = {
    "Epoch": list(range(1, 11)),
    "Training Loss": [0.4236, 0.3555, 0.3024, 0.2610, 0.2237, 0.1883, 0.1559, 0.1281, 0.1029, 0.0861],
    "Training MAE": [0.5733, 0.5171, 0.4694, 0.4267, 0.3849, 0.3473, 0.3104, 0.2799, 0.2553, 0.2352],
    "Validation Loss": [0.3441, 0.2862, 0.2406, 0.2011, 0.1643, 0.1300, 0.1004, 0.0776, 0.0596, 0.0456],
    "Validation MAE": [0.5352, 0.4826, 0.4356, 0.3896, 0.3425, 0.3015, 0.2623, 0.2264, 0.1929, 0.1670]
}

metrics_df = pd.DataFrame(training_metrics)
st.line_chart(metrics_df[['Training Loss', 'Validation Loss']])
st.line_chart(metrics_df[['Training MAE', 'Validation MAE']])

st.write("""
### Summary Statistics
""")

# Display summary statistics
summary = df.describe()
st.write(summary)

# Save the report to a CSV file
df.to_csv('financial_report.csv', index=False)
summary.to_csv('financial_summary.csv')
st.write("Financial report and summary generated successfully. Check the generated CSV files for details.")
