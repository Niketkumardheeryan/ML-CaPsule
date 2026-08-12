from pathlib import Path

import pandas as pd
import streamlit as st
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "financial_data.csv"
MODEL_PATH = PROJECT_DIR / "financial_model.keras"
FEATURE_COLUMNS = ["Revenue", "Expenses", "Profit", "Assets", "Liabilities"]
TARGET_COLUMN = "Equity"


@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    data["Date"] = pd.to_datetime(data["Date"])
    return data


@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)


st.set_page_config(page_title="Automated Financial Reporting", layout="wide")
st.title("Automated Financial Reporting with Deep Learning")

if not MODEL_PATH.is_file():
    st.error("The trained financial model has not been generated.")
    st.code("python train_model.py", language="bash")
    st.info("Run this command from the project directory, then restart the app.")
    st.stop()

try:
    model = load_model()
except (OSError, ValueError) as error:
    st.error("The financial model is invalid or incompatible.")
    st.code(f"{type(error).__name__}: {error}")
    st.info("Delete the generated model and run `python train_model.py` again.")
    st.stop()

df = load_data()
X = df[FEATURE_COLUMNS]
y = df[TARGET_COLUMN]
X_train, X_test, _, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = MinMaxScaler()
scaler.fit(X_train)
X_test_scaled = scaler.transform(X_test)

test_loss, test_mae = model.evaluate(X_test_scaled, y_test, verbose=0)
predictions = model.predict(X_test_scaled, verbose=0).reshape(-1)

# Preserve test indices so predictions remain paired with their source rows.
comparison = df.loc[X_test.index, ["Date", TARGET_COLUMN]].copy()
comparison = comparison.rename(columns={TARGET_COLUMN: "Actual"})
comparison["Predicted"] = predictions
comparison = comparison.sort_values("Date").set_index("Date")

st.subheader("Actual vs Predicted Equity Values")
st.dataframe(comparison, use_container_width=True)
st.line_chart(comparison[["Actual", "Predicted"]])

metric_col1, metric_col2 = st.columns(2)
metric_col1.metric("Test loss (MSE)", f"{test_loss:,.2f}")
metric_col2.metric("Test MAE", f"{test_mae:,.2f}")

st.subheader("Dataset Summary Statistics")
summary = df.describe(include="number")
st.dataframe(summary, use_container_width=True)

st.download_button(
    "Download prediction report",
    comparison.reset_index().to_csv(index=False),
    file_name="financial_report.csv",
    mime="text/csv",
)
st.download_button(
    "Download summary statistics",
    summary.to_csv(),
    file_name="financial_summary.csv",
    mime="text/csv",
)
