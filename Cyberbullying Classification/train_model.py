from pathlib import Path

import joblib
import kagglehub
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


PROJECT_DIR = Path(__file__).resolve().parent
MODEL_DIR = PROJECT_DIR / "models"
DATASET_HANDLE = "andrewmvd/cyberbullying-classification"
RANDOM_STATE = 42


def find_dataset(download_dir):
    candidates = list(Path(download_dir).rglob("*.csv"))
    if not candidates:
        raise FileNotFoundError("KaggleHub downloaded no CSV dataset file")
    return candidates[0]


def main():
    download_dir = kagglehub.dataset_download(DATASET_HANDLE)
    dataset_path = find_dataset(download_dir)
    data = pd.read_csv(dataset_path).dropna(
        subset=["tweet_text", "cyberbullying_type"]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        data["tweet_text"].astype(str),
        data["cyberbullying_type"].astype(str),
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=data["cyberbullying_type"],
    )

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2,
        max_features=20_000,
        sublinear_tf=True,
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    model = VotingClassifier(
        estimators=[
            ("logistic_regression", LogisticRegression(max_iter=1_000)),
            ("naive_bayes", MultinomialNB()),
            (
                "random_forest",
                RandomForestClassifier(
                    n_estimators=100,
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                ),
            ),
        ],
        voting="hard",
    )
    model.fit(X_train_tfidf, y_train)

    predictions = model.predict(X_test_tfidf)
    print(f"Validation accuracy: {accuracy_score(y_test, predictions):.3f}")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_DIR / "Voting.pkl")
    joblib.dump(vectorizer, MODEL_DIR / "tfidf.pkl")
    print(f"Saved model artifacts to {MODEL_DIR}")


if __name__ == "__main__":
    main()
