import os

import pandas as pd
import streamlit as st
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Bitcoin Price Predictor",
    layout="centered",
)

r = st.sidebar.radio(
    "Navigation Menu",
    ["Home", "Bitcoin Price Prediction"],
)

if r == "Home":
    st.title("Bitcoin Price Prediction Web App")

    image_path = os.path.join(BASE_DIR, "price.png")
    st.image(image_path, use_column_width=True)

    st.markdown("## About Bitcoin")

    st.write(
        """
        Bitcoin is one of the most widely used cryptocurrencies in the digital market.
        It is decentralized, meaning it is not controlled by any government or company.

        Transactions are simple, secure, and recorded on blockchain technology.
        Since Bitcoin prices are highly volatile, predicting its market value can help users make better investment decisions.
        """
    )

    st.info(
        "This web application uses Machine Learning with Lasso Regression "
        "to predict Bitcoin market trends."
    )

csv_path = os.path.join(BASE_DIR, "coin_Bitcoin.csv")
bitcoin = pd.read_csv(csv_path)

bitcoin.drop(["Name", "SNo", "Symbol", "Date"], axis=1, inplace=True)

X = bitcoin.drop(["Marketcap"], axis=1)
Y = bitcoin["Marketcap"]

xtrain, xtest, ytrain, ytest = train_test_split(
    X,
    Y,
    test_size=0.2,
    random_state=42,
)

model = Lasso()
model.fit(xtrain, ytrain)

if r == "Bitcoin Price Prediction":
    st.title("Bitcoin Marketcap Prediction")

    st.markdown("### Enter Bitcoin Market Details")

    col1, col2 = st.columns(2)

    with col1:
        high = st.number_input("Highest Price of Bitcoin", min_value=0.0)
        open_price = st.number_input("Opening Price of Bitcoin", min_value=0.0)
        volume = st.number_input("Volume of Bitcoin", min_value=0.0)

    with col2:
        low = st.number_input("Lowest Price of Bitcoin", min_value=0.0)
        close = st.number_input("Closing Price of Bitcoin", min_value=0.0)

    if st.button("Predict Marketcap"):
        prediction = model.predict([[high, low, open_price, close, volume]])
        st.success(f"Predicted Bitcoin Marketcap: ${abs(prediction[0]):,.2f}")
        st.balloons()