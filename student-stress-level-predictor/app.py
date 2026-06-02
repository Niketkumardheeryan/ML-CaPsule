"""
Student Stress Intelligence — Streamlit UI
Run locally: streamlit run app.py
"""
import json
import pickle

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------- Page config ----------
st.set_page_config(
    page_title="Student Stress Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .metric-card {
        background-color: #1a1f2e;
        padding: 18px; border-radius: 10px;
        border: 1px solid #2a3147;
    }
    h1, h2, h3, h4 { color: #19c37d !important; }
    .prediction-low    { color: #4caf50; font-size: 42px; font-weight: 700; }
    .prediction-medium { color: #ffb300; font-size: 42px; font-weight: 700; }
    .prediction-high   { color: #e53935; font-size: 42px; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ---------- Load artifacts ----------
@st.cache_resource
def load_artifacts():
    with open("models/stress_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("models/feature_meta.json") as f:
        meta = json.load(f)
    df = pd.read_csv("data/StressLevelDataset.csv")
    return model, meta, df

model, meta, df = load_artifacts()
FEATURES = meta["features"]
RANGES = meta["ranges"]

# ---------- Sidebar nav ----------
st.sidebar.title("🧠 Student Stress Intel")
st.sidebar.caption("Multi-class Stress Predictor")
page = st.sidebar.radio(
    "Navigate",
    ["Executive Overview", "Stress Prediction Lab", "Feature Importance", "About"],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    f"**Model:** XGBoost  \n"
    f"**Test accuracy:** `{meta['test_accuracy']:.3f}`  \n"
    f"**Macro F1:** `{meta['test_macro_f1']:.3f}`"
)
st.sidebar.markdown("---")
st.sidebar.caption("Built by @kri1105 · GSSoC'26")

# ---------- Pages ----------
if page == "Executive Overview":
    st.title("📊 Executive Overview")
    st.caption("Real-time pulse of the student stress dataset")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Records", f"{len(df):,}")
    c2.metric("Features", f"{len(FEATURES)}")
    c3.metric("Stress Classes", "3")
    c4.metric("Model Accuracy", f"{meta['test_accuracy']*100:.1f}%")
    c5.metric("Macro F1", f"{meta['test_macro_f1']:.3f}")

    st.markdown("### Stress Level Distribution")
    counts = (
        df["stress_level"].value_counts().sort_index()
        .rename({0: "Low", 1: "Medium", 2: "High"})
        .reset_index()
    )
    counts.columns = ["Stress Level", "Count"]
    fig = px.bar(
        counts, x="Stress Level", y="Count",
        color="Stress Level",
        color_discrete_map={"Low": "#4caf50", "Medium": "#ffb300", "High": "#e53935"},
        template="plotly_dark",
    )
    fig.update_layout(showlegend=False, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Top Correlations with Stress Level")
    corr = df.corr(numeric_only=True)["stress_level"].drop("stress_level")
    corr_df = corr.abs().sort_values(ascending=False).head(10).reset_index()
    corr_df.columns = ["Feature", "|Correlation|"]
    corr_df["Direction"] = corr.loc[corr_df["Feature"]].apply(
        lambda v: "Positive ↑" if v > 0 else "Negative ↓"
    ).values
    fig = px.bar(
        corr_df.iloc[::-1], x="|Correlation|", y="Feature", orientation="h",
        color="Direction",
        color_discrete_map={"Positive ↑": "#e53935", "Negative ↓": "#4caf50"},
        template="plotly_dark",
    )
    fig.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Stress Prediction Lab":
    st.title("🔬 Stress Prediction Lab")
    st.caption("Adjust the inputs to predict a student's stress level")

    left, right = st.columns([1.3, 1])

    with left:
        st.markdown("### Student Profile")
        inputs = {}
        col1, col2 = st.columns(2)
        for i, feat in enumerate(FEATURES):
            r = RANGES[feat]
            target = col1 if i % 2 == 0 else col2
            label = feat.replace("_", " ").title()
            inputs[feat] = target.slider(
                label, min_value=r["min"], max_value=r["max"], value=r["default"]
            )

    with right:
        st.markdown("### AI Prediction")
        x = np.array([[inputs[f] for f in FEATURES]])
        probs = model.predict_proba(x)[0]
        pred = int(np.argmax(probs))
        label = ["Low", "Medium", "High"][pred]
        css = ["prediction-low", "prediction-medium", "prediction-high"][pred]
        emoji = ["🟢", "🟡", "🔴"][pred]

        st.markdown(
            f'<div class="metric-card" style="text-align:center;">'
            f'<div style="color:#aaa;">Predicted Stress Level</div>'
            f'<div class="{css}">{emoji} {label}</div>'
            f'<div style="color:#888;">Confidence: {probs[pred]*100:.1f}%</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(" ")
        st.markdown("**Probability breakdown**")
        prob_df = pd.DataFrame({
            "Class": ["Low", "Medium", "High"],
            "Probability": probs,
        })
        fig = px.bar(
            prob_df, x="Class", y="Probability",
            color="Class",
            color_discrete_map={"Low": "#4caf50", "Medium": "#ffb300", "High": "#e53935"},
            template="plotly_dark",
        )
        fig.update_layout(
            showlegend=False, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
            yaxis=dict(range=[0, 1]),
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "Feature Importance":
    st.title("📈 Feature Importance")
    st.caption("Which factors the XGBoost model relies on most")
    imp = pd.Series(meta["feature_importance"]).sort_values(ascending=True)
    fig = px.bar(
        x=imp.values, y=imp.index, orientation="h",
        labels={"x": "Importance", "y": ""},
        template="plotly_dark",
    )
    fig.update_traces(marker_color="#19c37d")
    fig.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", height=600)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.title("ℹ️ About")
    st.markdown("""
**Student Stress Intelligence** is a multi-class classifier that predicts a student's
stress level (Low / Medium / High) from 20 lifestyle, academic, and psychological factors.

- **Dataset:** [Student Stress Factors – Kaggle](https://www.kaggle.com/datasets/rxnach/student-stress-factors-a-comprehensive-analysis)
- **Model:** XGBoost (also benchmarked against Logistic Regression and Random Forest)
- **Test Accuracy:** ~88.6% &nbsp;·&nbsp; **Macro F1:** ~0.886

Built by **@kri1105** as a GSSoC'26 contribution to
[ML-CaPsule](https://github.com/Niketkumardheeryan/ML-CaPsule).
""")
