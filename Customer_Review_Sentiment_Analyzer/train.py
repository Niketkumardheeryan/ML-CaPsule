import pandas as pd
import re
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("dataset/reviews.csv")

# Keep required columns
df = df[["review_body", "star_rating"]]

# Remove missing values
df.dropna(inplace=True)

# Convert ratings to sentiment
def get_sentiment(rating):
    if rating >= 4:
        return "Positive"
    elif rating == 3:
        return "Neutral"
    else:
        return "Negative"

df["sentiment"] = df["star_rating"].apply(get_sentiment)

# Clean text
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\\S+", "", text)
    text = re.sub(r"[^a-zA-Z ]", "", text)
    return text

df["review_body"] = df["review_body"].apply(clean_text)

# Features and labels
X = df["review_body"]
y = df["sentiment"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Model
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train_vec, y_train)

# Predictions
predictions = model.predict(X_test_vec)

# Metrics
print("Accuracy:", accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))

# Save files
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model saved successfully.")