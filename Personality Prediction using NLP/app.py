import os
import re
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

AXES = [
    ('IE', 'I', 'E', 'Mind'),
    ('NS', 'N', 'S', 'Information'),
    ('TF', 'T', 'F', 'Decision'),
    ('JP', 'J', 'P', 'Lifestyle'),
]

MBTI_TYPES = [
    'infj', 'infp', 'intj', 'intp', 'isfj', 'isfp', 'istj', 'istp',
    'enfj', 'enfp', 'entj', 'entp', 'esfj', 'esfp', 'estj', 'estp',
]

TRAIT_DESCRIPTIONS = {
    'I': ('Introversion', 'Gains energy from solitude and inner reflection'),
    'E': ('Extroversion', 'Gains energy from social interaction and external stimulation'),
    'N': ('Intuition', 'Focuses on patterns, abstract ideas, and future possibilities'),
    'S': ('Sensing', 'Focuses on concrete facts, present reality, and practical details'),
    'T': ('Thinking', 'Makes decisions through logic and objective analysis'),
    'F': ('Feeling', 'Makes decisions through personal values and empathy'),
    'J': ('Judging', 'Prefers structure, planning, and decisive closure'),
    'P': ('Perceiving', 'Prefers flexibility, spontaneity, and keeping options open'),
}


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\|+', ' ', text)
    text = re.sub(r'[^a-z\s]', '', text)
    for t in MBTI_TYPES:
        text = text.replace(t, '')
    return re.sub(r'\s+', ' ', text).strip()


@st.cache_resource(show_spinner="Training models on MBTI dataset (one-time setup)...")
def load_models():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mbti_1.csv')
    if not os.path.exists(data_path):
        return None, None, None, f"Dataset not found at {data_path}. Download mbti_1.csv from Kaggle and place it in this folder."

    df = pd.read_csv(data_path)
    df['IE'] = df['type'].apply(lambda x: 0 if x[0] == 'I' else 1)
    df['NS'] = df['type'].apply(lambda x: 0 if x[1] == 'N' else 1)
    df['TF'] = df['type'].apply(lambda x: 0 if x[2] == 'T' else 1)
    df['JP'] = df['type'].apply(lambda x: 0 if x[3] == 'J' else 1)
    df['clean_posts'] = df['posts'].apply(clean_text)

    tfidf = TfidfVectorizer(
        max_features=10000, stop_words='english', ngram_range=(1, 2), min_df=3
    )
    X = tfidf.fit_transform(df['clean_posts'])

    models = {}
    metrics = {}
    for col, label0, label1, axis_name in AXES:
        y = df[col].values
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=42
        )
        model = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        models[col] = model
        metrics[col] = {
            'axis': axis_name,
            'task': f'{label0} vs {label1}',
            'accuracy': accuracy_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred, average='weighted'),
            'roc_auc': roc_auc_score(y_test, y_prob),
        }

    return tfidf, models, metrics, None


def predict_mbti(text: str, tfidf, models):
    vec = tfidf.transform([clean_text(text)])
    mbti = ''
    per_axis = {}
    for col, label0, label1, axis_name in AXES:
        model = models[col]
        pred = model.predict(vec)[0]
        prob = model.predict_proba(vec)[0]
        letter = label0 if pred == 0 else label1
        mbti += letter
        per_axis[col] = {
            'axis': axis_name,
            'label0': label0,
            'label1': label1,
            'prob0': float(prob[0]),
            'prob1': float(prob[1]),
            'letter': letter,
        }
    return mbti, per_axis


def main():
    st.set_page_config(
        page_title="MBTI Personality Predictor",
        page_icon="🧠",
        layout="centered",
    )

    st.title("MBTI Personality Predictor")
    st.markdown(
        "Paste any text below to get a predicted MBTI personality type. "
        "Each of the 4 axes is classified independently using TF-IDF + Logistic Regression."
    )

    tfidf, models, metrics, error = load_models()

    if error:
        st.error(error)
        st.stop()

    with st.expander("Model performance on test set"):
        rows = []
        for col, m in metrics.items():
            rows.append({
                'Axis': m['axis'],
                'Task': m['task'],
                'Accuracy': f"{m['accuracy']:.1%}",
                'F1': f"{m['f1']:.3f}",
                'ROC-AUC': f"{m['roc_auc']:.3f}",
            })
        st.table(pd.DataFrame(rows))

    st.divider()

    text_input = st.text_area(
        "Enter text to analyse:",
        height=200,
        placeholder=(
            "Write anything here: a journal entry, social media posts, "
            "a self-description, or any free-form text..."
        ),
    )

    predict_btn = st.button("Predict Personality", type="primary")

    if predict_btn:
        if not text_input.strip():
            st.warning("Please enter some text first.")
            st.stop()
        if len(text_input.split()) < 10:
            st.warning("Please enter at least a few sentences for a reliable prediction.")
            st.stop()

        mbti, per_axis = predict_mbti(text_input, tfidf, models)

        st.markdown(f"## Predicted Type: **{mbti}**")

        cols = st.columns(4)
        for i, (col_name, label0, label1, axis_name) in enumerate(AXES):
            r = per_axis[col_name]
            confidence = r['prob0'] if r['letter'] == label0 else r['prob1']
            with cols[i]:
                st.metric(label=axis_name, value=r['letter'])
                st.progress(confidence)
                st.caption(
                    f"{label0}: {r['prob0']:.0%}   {label1}: {r['prob1']:.0%}"
                )

        st.markdown("### What this means")
        for letter in mbti:
            name, desc = TRAIT_DESCRIPTIONS[letter]
            st.markdown(f"- **{letter} - {name}:** {desc}")

        st.divider()
        st.caption(
            "Results are based on patterns in social media text from the MBTI Personality Type Dataset. "
            "Longer, more expressive input produces more reliable predictions."
        )


if __name__ == '__main__':
    main()
