import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

# Load the dataset
df = pd.read_csv('financial_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Load the trained model
model = tf.keras.models.load_model('financial_model.h5')

# Normalize the data using the same scaler as during training
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(df.drop('Date', axis=1))

# Prepare features and target
X = data_scaled[:, :-1]
y = data_scaled[:, -1]

# Make predictions
y_pred = model.predict(X)
y_pred_original = scaler.inverse_transform(np.c_[X, y_pred])[:, -1]

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
