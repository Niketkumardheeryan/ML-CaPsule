import streamlit as st
import joblib

# Load model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

st.title("🛒 Customer Review Sentiment Analyzer")

st.write(
    "Enter a customer review and predict whether it is Positive, Neutral, or Negative."
)

review = st.text_area("Enter Review")

if st.button("Analyze Sentiment"):

    if review.strip() == "":
        st.warning("Please enter a review.")

    else:
        review_vec = vectorizer.transform([review])

        prediction = model.predict(review_vec)[0]

        if prediction == "Positive":
            st.success(f"🟢 Sentiment: {prediction}")

        elif prediction == "Neutral":
            st.info(f"🟡 Sentiment: {prediction}")

        else:
            st.error(f"🔴 Sentiment: {prediction}")