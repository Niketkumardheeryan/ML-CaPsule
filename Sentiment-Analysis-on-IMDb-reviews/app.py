import streamlit as st
import pandas as pd
import plotly.express as px

from api import get_movies, get_reviews
from sentiment import textblob_sentiment, vader_sentiment

st.set_page_config(
    page_title="IMDb Sentiment Analysis",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 IMDb Sentiment Analysis")

movie_name = st.text_input("Enter Movie Name")

model = st.selectbox(
    "Select Sentiment Model",
    ["TextBlob", "VADER"]
)

if st.button("Analyze"):

    if movie_name:

        with st.spinner("Fetching movies..."):
            movies = get_movies(movie_name)

        if len(movies) == 0:
            st.error("No movies found")

        else:

            movie = movies[0]

            if movie["image"]:
                st.image(movie["image"], width=200)
            st.subheader(movie["title"])
            st.write(movie["description"])

            reviews = get_reviews(movie["id"])

            if len(reviews) == 0:
                st.warning("No reviews found")

            else:

                sentiments = []

                for review in reviews:

                    if model == "TextBlob":
                        sentiment = textblob_sentiment(review)
                    else:
                        sentiment = vader_sentiment(review)

                    sentiments.append(sentiment)

                df = pd.DataFrame({
                    "Review": reviews,
                    "Sentiment": sentiments
                })

                counts = df["Sentiment"].value_counts()

                st.subheader("Sentiment Distribution")

                fig = px.pie(
                    values=counts.values,
                    names=counts.index
                )

                st.plotly_chart(fig)

                st.subheader("Reviews")

                st.dataframe(df)