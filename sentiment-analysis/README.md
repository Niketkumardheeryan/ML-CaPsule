# Sentiment Analysis Major Project

A real-world Sentiment Analysis project that takes text input from the user and predicts whether the sentiment is **positive** or **negative**, using a trained Machine Learning model served through a Streamlit web app.

🔗 **Live Demo:** https://sentiment-analysis-2c3aepwbw6pucpse3zuea5.streamlit.app/
*(Note: hosted links may expire over time — see [Run Locally](#run-locally) below to run the app yourself.)*

---

## Project Workflow

### 1. Data Collection
The `amazonreviews.tsv` dataset from Kaggle was used for this project.

### 2. Data Preprocessing
- Lower casing the text
- Expanding contractions
- Removing punctuations and special characters
- Removing stopwords
- Tokenization
- Lemmatization

### 3. Sentiment Analysis Approach
- TF-IDF Vectorizer
- Support Vector Machine (SVM) model
- Model evaluation using Accuracy Score, Confusion Matrix, and Classification Report

### 4. Deployment
- Web application built using Streamlit
- Hosted on Streamlit Community Cloud

---

## Run Locally

<details>
<summary>Click to expand setup steps</summary>

### 1. Clone the repository
```bash
git clone https://github.com/UDAYAGIRICHARAN/ML-CaPsule.git
cd ML-CaPsule/Sentiment-Analysis
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app
```bash
streamlit run sent-analysis-app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

</details>

---

## Tech Stack
- Python
- scikit-learn
- NLTK
- Streamlit
- Pandas / NumPy

---

## Notes
- The original deployment used Heroku, but Heroku discontinued its free tier in November 2022, breaking the old link. The project has since been migrated to Streamlit Community Cloud.
- Hosted demo links can go down over time (inactivity, platform changes, etc.) — the **Run Locally** instructions above are the most reliable way to try the app.
