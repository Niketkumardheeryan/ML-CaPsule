import streamlit as st
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline


model = joblib.load('news_category_prediction.pkl')

st.title("News Category Prediction")
st.write("""
## Predict the category of a news article based on its context.
""")

# user input
input_text = st.text_input("Enter your News Content: ", "")

# Prediction Button
if st.button("Classify"):
    if input_text:
        prediction = model.predict([input_text])[0]
        st.write(f"Predicted Category: {prediction}")
    else:
        st.write("Please Enter some text to classify.")