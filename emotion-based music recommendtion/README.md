# Emotion-based Music Recommendations

## Features

- **Mood Detection**: Enter your feelings or describe your day, and the app detects your emotions.
- **Language Preference**: Choose your preferred language for music recommendations.
- **Emotion-based Music**: Get song recommendations that match your current mood or help uplift your spirits.
- **Interactive UI**: Select and play recommended YouTube videos directly within the app.

## How to Use

1. **Enter Your Mood**: In the text box, type how you are feeling today.
2. **Select Language (Optional)**: Enter your preferred language for the song recommendations (or I am feeling lucky).
3. **Get Recommendations**: Click the "Get Recommendations" button to see song recommendations based on your detected emotion.
4. **Choose Your Music**: If you are feeling sad, you can choose between "Sad songs" or "Joyful/uplifting songs" from the dropdown menu.
5. **Play Music**: Select a video from the recommendations and play it directly within the app.

# Youtube API guide:
This guide will help you set up and use the YouTube Data API to fetch YouTube video recommendations based on your queries.

## Step 1: Set Up Google Cloud Project

1. **Create a Google Cloud Project**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Click on the **Select a project** dropdown at the top of the page.
   - Click **New Project** and fill in the required details.
   - Click **Create**.

2. **Enable YouTube Data API v3**:
   - In the Google Cloud Console, select your project.
   - Navigate to **APIs & Services > Library**.
   - Search for **YouTube Data API v3** and click on it.
   - Click **Enable**.
## Additional Resources
- [Google Cloud Console](https://console.cloud.google.com/)
- [YouTube Data API v3 Documentation](https://developers.google.com/youtube/v3/docs)
- [Google API Python Client Documentation](https://github.com/googleapis/google-api-python-client)


By following these steps, you should be able to set up and use the YouTube Data API to get video recommendations based on user input in your Streamlit app.

## Step 2: Obtain API Credentials

1. **Create API Key**:
   - Go to **APIs & Services > Credentials**.
   - Click **Create Credentials** and select **API key**.
   - Your new API key will be created and displayed. Copy this key for use in your application.

2. **Restrict API Key (Optional but recommended)**:
   - In the **Credentials** page, click on the edit icon next to your API key.
   - Under **Key restrictions**, select **HTTP referrers (web sites)**.
   - Add the URLs that will use this API key.
   - Save your changes.

## Step 3: Install Required Python Libraries

To interact with the YouTube Data API using Python, install the necessary libraries.

```bash
pip install google-api-python-client

## Installation

To run the app locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/emotion-based-music-recommendations.git
   ```
2. Navigate to the app directory:
 ```
  cd emotion-based-music-recommendations
```

3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Run the app:
```
streamlit run front.py
```



