from pathlib import Path

import joblib
import streamlit as st

from src.Predict import predict


PROJECT_DIR = Path(__file__).resolve().parent
MODEL_DIR = PROJECT_DIR / "models"
MODEL_PATH = MODEL_DIR / "Voting.pkl"
VECTORIZER_PATH = MODEL_DIR / "tfidf.pkl"


@st.cache_resource
def load_artifacts():
    missing = [path.name for path in (MODEL_PATH, VECTORIZER_PATH) if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing model artifacts: {', '.join(missing)}")
    return joblib.load(MODEL_PATH), joblib.load(VECTORIZER_PATH)


st.set_page_config(page_title="Cyberbullying Classifier", layout="wide")
st.header("Cyberbullying Classifier")

try:
    model, vectorizer = load_artifacts()
except FileNotFoundError as error:
    st.error("The trained cyberbullying model is not available yet.")
    st.info("Generate the required artifacts, then restart this dashboard.")
    st.code("python train_model.py", language="bash")
    st.code(str(error))
    st.stop()
except (EOFError, OSError, ValueError) as error:
    st.error("The saved model artifacts are invalid or incompatible.")
    st.info("Regenerate them by running `python train_model.py`.")
    st.code(f"{type(error).__name__}: {error}")
    st.stop()

text = st.text_area(
    "Enter text to classify",
    placeholder="Enter a tweet or sentence...",
)

if st.button("Classify", type="primary"):
    if not text.strip():
        st.warning("Enter some text before running classification.")
    else:
        result = predict(model, vectorizer, [text]).iloc[0]
        label = result["type"]
        if label == "not_cyberbullying":
            st.success(f"Predicted type: {label}")
        else:
            st.error(f"Predicted type: {label}")
