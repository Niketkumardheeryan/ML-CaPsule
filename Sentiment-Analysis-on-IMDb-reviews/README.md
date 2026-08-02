# Sentiment Analysis on IMDb Reviews 😊 😐 😔 😡

<br>
<div align="center">
  <img src="./image.PNG" width="200px" />
</div>

<br>

## Short Description 👇

This project demonstrates sentiment analysis on movie reviews using multiple NLP libraries.

The original implementation is provided as a **Jupyter Notebook**, which fetches movie reviews using the **IMDb API**. Additionally, a **Streamlit web application** has been added to provide an interactive interface. Since the original IMDb API is no longer available, the Streamlit application uses the **TMDB API** for fetching movie information and reviews.

<br>

## Process 🚀

### Jupyter Notebook

* Create an IMDb account and generate an API key.
* Fetch movie reviews using the IMDb API.
* Analyze sentiments using the selected NLP library.
* Visualize the results.

### Streamlit Application

* Search for a movie using the TMDB API.
* Retrieve movie details and available reviews.
* Analyze sentiments using the selected NLP model.
* Display results through an interactive web interface.

<br>

## Models/Libraries Implemented 📚

1. TextBlob
2. Vader
3. Flair
4. text2emotion

<br>

## Streamlit Web Application 🚀

A Streamlit interface has been added as an alternative way to interact with the project without running the notebook.

### Features

* Search movies through TMDB
* Interactive web interface
* Select a sentiment analysis model
* View movie details
* Analyze reviews
* Visualize sentiment distribution
* Display review predictions

### Environment Variables

Create a `.env` file in the project root and add your TMDB API key:

```env
TMDB_API_KEY=your_tmdb_api_key
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```

> **Note:** The Streamlit application requires a valid **TMDB API Key**. Please add your own API key before running the application. Do **not** commit your personal API key.

<br>

## Project Structure

```text
.
├── Sentiment_Analysis_on_IMDb_reviews.ipynb
├── app.py
├── api.py
├── sentiment.py
├── requirements.txt
├── image.PNG
└── README.md
```

<br>

## Notes 📌

* The **Jupyter Notebook** demonstrates the original workflow using the IMDb API.
* The **Streamlit application** uses the TMDB API because the original IMDb API used by the notebook is no longer actively available.
* Graphs may not be visible in GitHub's notebook preview.
* If you encounter dependency issues in Colab, restart the runtime and run the notebook again.

<br>


## Streamlit Version Output
<img width="1918" height="967" alt="Screenshot 2026-07-28 110630" src="https://github.com/user-attachments/assets/fb4f34e7-9275-4745-84a8-7daa731b7d39" />

<img width="1918" height="970" alt="Screenshot 2026-07-28 110645" src="https://github.com/user-attachments/assets/26a965c7-403b-45b4-a7fb-62f6e024e8ca" />

<br>

<h3 align="center">
Hope you like it
<img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="35px">
</h3>

## Author

<a href="https://github.com/GaganpreetKaurKalsi">Gaganpreet Kaur Kalsi</a>
