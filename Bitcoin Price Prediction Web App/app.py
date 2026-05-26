import streamlit as st
import sklearn
from sklearn import datasets
from sklearn import metrics
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split



r = st.sidebar.radio("Navigation Menu",["Home","Bitcoin Price"])

if r=="Home":
    
    st.write("""
    # Bitcoin Price Predictive 
    #    
    """)
    st.image("price.png")
    st.subheader(" Bitcoin Price ")
    st.write(" Bitcoin is widely used cryptocurrency for digital market. It is decentralised that means it is not own by government or any other company.Transactions are simple and easy as it doesn’t belong to any country.Records data are stored in Blockchain.Bitcoin price is variable and it is widely used so it is important to predict the price of it for making any investment")
    
    

        

# Biocoin Price Prediction
bitcoin=pd.read_csv('coin_Bitcoin.csv')
bitcoin.drop(["Name"],axis=1, inplace=True)
bitcoin.drop(["SNo"],axis=1, inplace=True)
bitcoin.drop(["Symbol"],axis=1, inplace=True)

# import datetime as dt
# bitcoin["Date"]=pd.to_datetime(bitcoin["Date"])
# bitcoin['Date_year'] = bitcoin["Date"].dt.year
# bitcoin['Date_month'] = bitcoin["Date"].dt.month
# bitcoin['Date_day'] = bitcoin["Date"].dt.day
# bitcoin['Date_hour'] = bitcoin["Date"].dt.hour
# bitcoin['Date_minute'] = bitcoin["Date"].dt.minute
# bitcoin['Date_seconde'] = bitcoin["Date"].dt.second
bitcoin.drop(["Date"], axis=1, inplace=True)


X=bitcoin.drop(["Marketcap"], axis=1)
Y=bitcoin["Marketcap"]

from sklearn.linear_model import Lasso
Ls=Lasso()
xtrain,xtest,ytrain,ytest=train_test_split(X,Y,test_size=0.2)
Ls.fit(xtrain,ytrain)

if r=='Bitcoin Price':
    st.markdown("<h2 style='text-align: center; color: #ff9900;'>Predict Bitcoin Marketcap</h2>", unsafe_allow_html=True)
    st.write("Enter the historical data below to predict the Marketcap of Bitcoin.")
    
    col1, col2 = st.columns(2)
    with col1:
        High = st.number_input("Highest Price")
        Low = st.number_input("Lowest Price")
    with col2:
        Open = st.number_input("Opening Price")
        Close = st.number_input("Closing Price")
        
    volume = st.number_input("Volume")
    
    ypred = Ls.predict([[High, Low, Open, Close, volume]])
    
    if st.button("Predict"):
        st.success(f"Predicted Marketcap: ${abs(ypred[0]):,.2f}")
        

    
    

        
        

   
    

    
    
    