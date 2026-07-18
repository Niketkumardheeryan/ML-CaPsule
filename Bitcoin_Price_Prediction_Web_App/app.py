import streamlit as st
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Page Configuration
st.set_page_config(
    page_title="Bitcoin Price Predictor",
    page_icon="₿",
    layout="centered"
)

# Sidebar Navigation
r = st.sidebar.radio(
    "Navigation Menu",
    ["Home", "Bitcoin Price Prediction"]
)

# Home Page
if r == "Home":

    st.title("₿ Bitcoin Price Prediction Web App")

    image_path = os.path.join(BASE_DIR, "price.png")
    st.image(image_path, width="stretch")

    st.markdown("## About Bitcoin")

    st.write(
        """
        Bitcoin is one of the most widely used cryptocurrencies in the digital market.
        It is decentralized, meaning it is not controlled by any government or company.

        Transactions are simple, secure, and recorded on blockchain technology.
        Since Bitcoin prices are highly volatile, predicting its market value can help users make better investment decisions.
        """
    )

    st.info("This web application uses Machine Learning with Lasso Regression to predict Bitcoin market trends.")

# Load Dataset
csv_path = os.path.join(BASE_DIR, 'coin_Bitcoin.csv')
bitcoin = pd.read_csv(csv_path)

# Drop unnecessary columns
bitcoin.drop(["Name"], axis=1, inplace=True)
bitcoin.drop(["SNo"], axis=1, inplace=True)
bitcoin.drop(["Symbol"], axis=1, inplace=True)
bitcoin.drop(["Date"], axis=1, inplace=True)

# Features and Target
X = bitcoin.drop(["Marketcap"], axis=1)
Y = bitcoin["Marketcap"]

# Train Model
xtrain, xtest, ytrain, ytest = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

model = Lasso()
model.fit(xtrain, ytrain)

# Prediction Page
if r == "Bitcoin Price Prediction":

    st.title("📈 Bitcoin Marketcap Prediction")

    st.markdown("### Enter Bitcoin Market Details")

    col1, col2 = st.columns(2)

    with col1:
        High = st.number_input("Highest Price of Bitcoin", min_value=0.0)
        Open = st.number_input("Opening Price of Bitcoin", min_value=0.0)
        volume = st.number_input("Volume of Bitcoin", min_value=0.0)

    with col2:
        Low = st.number_input("Lowest Price of Bitcoin", min_value=0.0)
        Close = st.number_input("Closing Price of Bitcoin", min_value=0.0)

    prediction = model.predict([[High, Low, Open, Close, volume]])

    st.markdown("")

    if st.button("Predict Marketcap"):

        st.success(
            f"Predicted Bitcoin Marketcap: ${abs(prediction[0]):,.2f}"
        )

        st.balloons()
from sklearn.linear_model import Lasso
Ls=Lasso()
xtrain,xtest,ytrain,ytest=train_test_split(X,Y,test_size=0.2, random_state=42)
Ls.fit(xtrain,ytrain)

if r=='Bitcoin Price':
    st.header("Know the Price of Bitcoin")
    High=st.number_input("Highest Price of bitcoin")
    Low=st.number_input("Lowest Price of")
    Open=st.number_input("Opening Price of bitcoin")
    Close=st.number_input("Closing Price of Bitcoin")
    volume=st.number_input("Volume of the bitcoin")
    
    ypred=Ls.predict([[High,Low,Open,Close,volume]])
    if(st.button("Predict")):
        st.success(f"Your Predicted Bitcoin Marketcap Is ${abs(ypred[0]):,.2f}")
        

    
    

        
        

   
    

    
    
    
