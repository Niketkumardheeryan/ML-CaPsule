# Emotion-based Music Recommendations

## Features

- **Mood Detection**: Enter your feelings or describe your day, and the app detects your emotions.
- **Language Preference**: Choose your preferred language for music recommendations.
- **Emotion-based Music**: Get song recommendations that match your current mood or help uplift your spirits.
- **Interactive UI**: Select and play recommended YouTube videos directly within the app.

## How to Use

1. **Enter Your Mood**: In the text box, type how you are feeling today.
2. **Select Language (Optional)**: Enter your preferred language for the song recommendations (or "I am feeling lucky").
3. **Get Recommendations**: Click the "Get Recommendations" button to see song recommendations based on your detected emotion.
4. **Choose Your Music**: If you are feeling sad, you can choose between "Sad songs" or "Joyful/uplifting songs" from the dropdown menu.
5. **Play Music**: Select a video from the recommendations and play it directly within the app.

## YouTube API Setup

    YOUTUBE_API_KEY=your_actual_key_here

This app requires a YouTube Data API key to fetch video recommendations.

### Step 1: Set Up a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click the **Select a project** dropdown, then **New Project**, fill in the details, and click **Create**.
3. Select your project, then navigate to **APIs & Services > Library**.
4. Search for **YouTube Data API v3** and click **Enable**.

### Step 2: Obtain API Credentials

1. Go to **APIs & Services > Credentials**.
2. Click **Create Credentials > API key**. Copy the generated key.
3. *(Optional, recommended)* Restrict the key under **Key restrictions > HTTP referrers**, adding the URLs that will use it.

### Step 3: Configure Your Environment

1. Copy `.env.example` to `.env` in this folder:
```bash
   cp .env.example .env
```
2. Open `.env` and paste your API key:
## Installation

1. Clone the repository:
```bash
   git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
```
2. Navigate to this project's folder:
```bash
   cd "ML-CaPsule/Emotion-based music recommendation"
```
3. Install the required dependencies:
```bash
   pip install -r requirements.txt
```
4. Set up your `.env` file as described above.
5. Run the app:
```bash
   streamlit run front.py
```

## Additional Resources

- [Google Cloud Console](https://console.cloud.google.com/)
- [YouTube Data API v3 Documentation](https://developers.google.com/youtube/v3/docs)
- [Google API Python Client Documentation](https://github.com/googleapis/google-api-python-client)
