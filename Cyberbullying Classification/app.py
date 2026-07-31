import streamlit as st
import joblib
from src.Predict import predict


st.set_page_config("Text Classifier" , layout = "wide")

st.header("Cyber Bullying Classifier")

@st.cache_resource
def load_model():

    model = joblib.load("./models/Voting.pkl")

    return model

model = load_model()
with st.container():
    text = st.text_input("Enter a sentence to classify")


    if st.button("Submit"):

        if text is not None:
            ans_df = predict(model , [text])
            with st.container(border= True,horizontal_alignment="center"):
                if ans_df['type'][0] != "not_cyberbullying":
                    st.error(f"predicted type : {ans_df['type'][0]}")
                else:
                    st.success(f"predicted type : {ans_df['type'][0]}")


        