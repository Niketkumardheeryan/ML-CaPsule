from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download("vader_lexicon")

vader_analyzer = SentimentIntensityAnalyzer()


def textblob_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"


def vader_sentiment(text):
    score = vader_analyzer.polarity_scores(text)

    if score["compound"] >= 0.05:
        return "Positive"
    elif score["compound"] <= -0.05:
        return "Negative"
    else:
        return "Neutral"


TRANSFORMER_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
NEUTRAL_THRESHOLD = 0.6

_transformer_pipeline = None


def load_transformer(model_name=TRANSFORMER_MODEL):
    global _transformer_pipeline

    if _transformer_pipeline is None:
        from transformers import pipeline

        _transformer_pipeline = pipeline(
            "sentiment-analysis",
            model=model_name,
            truncation=True,
            max_length=512,
        )

    return _transformer_pipeline


def transformer_sentiment(text, threshold=NEUTRAL_THRESHOLD):
    result = load_transformer()(text)[0]

    # SST-2 is a binary model, so a low-confidence prediction is reported as
    # Neutral to match the labels the other analysers return.
    if result["score"] < threshold:
        return "Neutral"

    return "Positive" if result["label"].upper() == "POSITIVE" else "Negative"


def transformer_sentiment_score(text):
    result = load_transformer()(text)[0]
    return result["label"].upper(), float(result["score"])


ANALYSERS = {
    "TextBlob": textblob_sentiment,
    "VADER": vader_sentiment,
    "Transformer (DistilBERT)": transformer_sentiment,
}
