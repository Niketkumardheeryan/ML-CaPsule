import streamlit as st
import pandas as pd
import plotly.express as px

from api import get_movies, get_reviews
from sentiment import ANALYSERS

st.set_page_config(
    page_title="IMDb Sentiment Analysis",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 IMDb Sentiment Analysis")

movie_name = st.text_input("Enter Movie Name")

model = st.selectbox(
    "Select Sentiment Model",
    list(ANALYSERS)
)

if model.startswith("Transformer"):
    st.caption(
        "The transformer downloads about 250 MB the first time it runs, "
        "then reads each review in full."
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
                analyse = ANALYSERS[model]

                with st.spinner(f"Analysing {len(reviews)} reviews with {model}..."):
                    for review in reviews:
                        sentiments.append(analyse(review))

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
