# Chatbot Song Recommender System 🎵

A powerful, conversational AI Song Recommender application built with Streamlit, Pandas, and Hugging Face Transformers. Instead of simple keyword matching, this chatbot utilizes a pre-trained Deep Learning Zero-Shot Classifier to accurately extract your mood or preferred genre from natural conversation, and recommends matching songs from a massive Spotify dataset containing over 230,000 tracks!

## Features
- **Deep Learning NLP**: Uses `cross-encoder/nli-distilroberta-base` to "understand" the context of your chat, diagnosing whether you are happy, sad, relaxed, motivated, or looking for a specific genre like rock, pop, or world music.
- **Massive Database**: Integrates an open-source Spotify features dataset, picking the absolute best songs by analyzing audio characteristics like `valence` (happiness vs sadness) and `energy`.
- **Short-Term Memory**: The bot remembers what it recommended to you! If you ask for *"different songs"*, it gives you entirely fresh recommendations without losing track of your current mood.
- **Dynamic Interactions**: No robotic or hardcoded responses. The chatbot randomly selects from a variety of natural templates.

## Screenshots & Results

Here is a preview of the Chatbot in action!
![Screenshot 1](Output%20SS/SS1.png)

![Screenshot 2](Output%20SS/SS2.png)

## Installation

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
2. Install the required packages (Note: Downloading PyTorch and Transformers may take a few minutes):
   ```bash
   pip install -r requirements.txt
   ```
3. Download the Dataset:
   ```bash
   python download_dataset.py
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).
3. Start chatting! Try saying something natural like *"I'm having a really tough day..."* or *"Can you give me some upbeat indian songs?"*.

## Project Structure
- `chatbot_song_recommender.ipynb`: A Jupyter Notebook demonstrating the core ML and dataset logic.
- `app.py`: The main Streamlit web application interface.
- `src/`: Contains the logic classes (`chatbot.py` and `recommender.py`) with full PEP8 compliance and docstrings.
- `data/`: The directory where the downloaded `SpotifyFeatures.csv` dataset resides.
