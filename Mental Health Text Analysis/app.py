"""
Gradio app for Mental Health Text Analysis.

This file loads the model artifacts created by mental_health_analysis.ipynb.
Run the notebook first so this app can use the trained TF-IDF + Logistic
Regression model instead of retraining every time the UI starts.
"""

from pathlib import Path
import re

import gradio as gr
import joblib


# The four categories used throughout the project.
CATEGORIES = ["Depression", "Anxiety", "Stress", "Burnout"]


# A compact stopword list keeps the app lightweight and avoids downloading data at launch time.
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
    "to", "was", "were", "will", "with", "i", "me", "my", "we", "our",
    "you", "your", "they", "them", "their", "this", "those", "these",
}


# These paths point to files saved by the notebook after training.
PROJECT_DIR = Path(__file__).resolve().parent
MODEL_DIR = PROJECT_DIR / "models"
PIPELINE_PATH = MODEL_DIR / "mental_health_tfidf_model.joblib"
THRESHOLDS_PATH = MODEL_DIR / "risk_thresholds.joblib"


def load_model_artifacts():
    """
    Load the trained model pipeline and thresholds from disk.

    The notebook saves a scikit-learn pipeline and a dictionary of severity
    thresholds. This function keeps loading logic in one place so the rest of
    the app can focus on prediction and display.
    """
    if not PIPELINE_PATH.exists() or not THRESHOLDS_PATH.exists():
        missing_files = [
            str(path)
            for path in [PIPELINE_PATH, THRESHOLDS_PATH]
            if not path.exists()
        ]
        raise FileNotFoundError(
            "Trained model files were not found. "
            "Please run mental_health_analysis.ipynb first. "
            f"Missing files: {missing_files}"
        )

    model_pipeline = joblib.load(PIPELINE_PATH)
    thresholds = joblib.load(THRESHOLDS_PATH)
    return model_pipeline, thresholds


MODEL_PIPELINE, RISK_THRESHOLDS = load_model_artifacts()


def clean_text(text):
    """
    Clean text using the same basic steps as the notebook.

    The model was trained on lowercase text with links, punctuation, and common
    stopwords removed, so applying the same cleaning here makes app predictions
    more consistent with notebook predictions.
    """
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = text.split()
    tokens = [token for token in tokens if token not in STOP_WORDS and len(token) > 2]
    return " ".join(tokens)


def severity_from_score(score, thresholds=None, category=None):
    """
    Convert a 0-100 risk score into a human-readable severity label.

    The default cutoffs are intentionally simple: under 40 is Low, 40-69 is
    Medium, and 70 or more is High. If the notebook saved category-specific
    thresholds, those values are used instead.
    """
    if thresholds and category in thresholds:
        medium_cutoff = thresholds[category]["medium"]
        high_cutoff = thresholds[category]["high"]
    else:
        medium_cutoff = 40
        high_cutoff = 70

    if score >= high_cutoff:
        return "High"
    if score >= medium_cutoff:
        return "Medium"
    return "Low"


def predict_risk_scores(text):
    """
    Predict risk scores for Depression, Anxiety, Stress, and Burnout.

    This function uses predicted probabilities from the trained TF-IDF +
    Logistic Regression pipeline. Each probability is scaled to a 0-100 risk
    score so the result is easier to understand in the UI.
    """
    if not text or not text.strip():
        return {category: "Please enter some text." for category in CATEGORIES}

    results = {}

    cleaned_text = clean_text(text)
    probabilities = MODEL_PIPELINE.predict_proba([cleaned_text])[0]

    for index, category in enumerate(CATEGORIES):
        score = round(probabilities[index] * 100, 2)
        severity = severity_from_score(score, RISK_THRESHOLDS, category)
        results[category] = f"{score}% risk - {severity} severity"

    return results


def build_interface():
    """
    Build and return the Gradio interface.

    Keeping the UI setup inside a function makes the file easier to understand,
    test, and modify later.
    """
    description = (
        "Enter a Reddit-style mental health text sample. "
        "The app returns estimated risk scores for four categories. "
        "This demo is for education only and is not a diagnosis tool."
    )

    interface = gr.Interface(
        fn=predict_risk_scores,
        inputs=gr.Textbox(
            lines=8,
            label="Input Text",
            placeholder="Example: I feel exhausted, anxious, and unable to keep up with everything.",
        ),
        outputs=gr.JSON(label="Risk Scores"),
        title="Mental Health Text Analysis",
        description=description,
        examples=[
            ["I feel hopeless and empty lately, and I do not enjoy anything anymore."],
            ["I am constantly worried and my thoughts keep racing every night."],
            ["I have too many deadlines and feel completely overwhelmed."],
        ],
    )

    return interface


if __name__ == "__main__":
    # Launch the Gradio app only when this file is run directly.
    demo = build_interface()
    demo.launch()
