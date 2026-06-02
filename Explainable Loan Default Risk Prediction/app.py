from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import shap
import streamlit as st

from src.loan_default_pipeline import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    get_feature_names,
    load_or_build_dataset,
    predict_default,
    train_models,
)


st.set_page_config(
    page_title="Loan Default Risk",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    return load_or_build_dataset()


@st.cache_resource
def train_cached(data: pd.DataFrame):
    return train_models(data)


def build_applicant_form(data: pd.DataFrame) -> dict[str, object]:
    st.sidebar.header("Applicant Details")
    applicant: dict[str, object] = {}

    applicant["age"] = st.sidebar.slider("Age", 21, 70, 36)
    applicant["annual_income"] = st.sidebar.number_input("Annual income", 15000, 250000, 62000, step=1000)
    applicant["employment_length_years"] = st.sidebar.slider("Employment length", 0, 35, 6)
    applicant["loan_amount"] = st.sidebar.number_input("Loan amount", 1000, 100000, 18000, step=500)
    applicant["loan_term_months"] = st.sidebar.selectbox("Loan term", [36, 48, 60, 84], index=2)
    applicant["interest_rate"] = st.sidebar.slider("Interest rate", 0.04, 0.3, 0.13, step=0.005)
    applicant["debt_to_income_ratio"] = st.sidebar.slider("Debt-to-income ratio", 0.02, 0.8, 0.28, step=0.01)
    applicant["credit_score"] = st.sidebar.slider("Credit score", 300, 850, 690)
    applicant["credit_history_years"] = st.sidebar.slider("Credit history years", 1, 35, 9)
    applicant["previous_missed_payments"] = st.sidebar.slider("Previous missed payments", 0, 8, 0)

    for feature in CATEGORICAL_FEATURES:
        values = sorted(data[feature].dropna().unique().tolist())
        applicant[feature] = st.sidebar.selectbox(feature.replace("_", " ").title(), values)

    return applicant


def plot_confusion_matrix(matrix):
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.imshow(matrix, cmap="Blues")
    ax.set_xticks([0, 1], labels=["No Default", "Default"])
    ax.set_yticks([0, 1], labels=["No Default", "Default"])
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")

    for row in range(2):
        for col in range(2):
            ax.text(col, row, int(matrix[row, col]), ha="center", va="center", color="black")

    fig.tight_layout()
    return fig


def calculate_shap_values(result, applicant: dict[str, object]):
    model = result.model
    preprocessor = model.named_steps["preprocessor"]
    classifier = model.named_steps["classifier"]
    feature_names = get_feature_names(model)

    transformed_train = preprocessor.transform(result.x_train)
    transformed_applicant = preprocessor.transform(pd.DataFrame([applicant]))

    if hasattr(transformed_train, "toarray"):
        transformed_train = transformed_train.toarray()
    if hasattr(transformed_applicant, "toarray"):
        transformed_applicant = transformed_applicant.toarray()

    if result.best_model_name in {"Random Forest", "Gradient Boosting"}:
        explainer = shap.TreeExplainer(classifier)
        shap_values = explainer.shap_values(transformed_applicant)
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        elif getattr(shap_values, "ndim", 0) == 3:
            shap_values = shap_values[:, :, 1]
    else:
        background = transformed_train[:100]
        explainer = shap.Explainer(classifier, background)
        shap_values = explainer(transformed_applicant).values

    contributions = pd.DataFrame(
        {
            "feature": feature_names,
            "contribution": shap_values[0],
        }
    )
    contributions["absolute_contribution"] = contributions["contribution"].abs()
    return contributions.sort_values("absolute_contribution", ascending=False).head(12)


data = load_data()
result = train_cached(data)
applicant = build_applicant_form(data)
probability, risk = predict_default(result.model, applicant)

st.title("Explainable Loan Default Risk Prediction")

score_col, risk_col, model_col = st.columns(3)
score_col.metric("Default Probability", f"{probability:.1%}")
risk_col.metric("Risk Category", risk)
model_col.metric("Selected Model", result.best_model_name)

metrics_tab, prediction_tab, explain_tab, data_tab = st.tabs(
    ["Model Metrics", "Prediction", "SHAP Explainability", "Dataset"]
)

with metrics_tab:
    st.subheader("Model Comparison")
    st.dataframe(result.metrics, use_container_width=True)

    st.subheader("Confusion Matrix")
    st.pyplot(plot_confusion_matrix(result.confusion_matrices[result.best_model_name]))

with prediction_tab:
    st.subheader("Applicant Summary")
    applicant_frame = pd.DataFrame([applicant])[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    st.dataframe(applicant_frame, use_container_width=True)

    if risk == "High":
        st.error("This applicant has a high estimated default risk.")
    elif risk == "Medium":
        st.warning("This applicant has a medium estimated default risk.")
    else:
        st.success("This applicant has a low estimated default risk.")

with explain_tab:
    st.subheader("Top Local SHAP Contributions")
    contributions = calculate_shap_values(result, applicant)
    st.bar_chart(contributions.set_index("feature")["contribution"])
    st.dataframe(contributions[["feature", "contribution"]], use_container_width=True)

    st.subheader("Global Feature Importance")
    preprocessor = result.model.named_steps["preprocessor"]
    classifier = result.model.named_steps["classifier"]
    feature_names = get_feature_names(result.model)

    if hasattr(classifier, "feature_importances_"):
        global_importance = pd.DataFrame(
            {
                "feature": feature_names,
                "importance": classifier.feature_importances_,
            }
        ).sort_values("importance", ascending=False).head(12)
        st.bar_chart(global_importance.set_index("feature")["importance"])
    else:
        st.info("Global feature importance is shown for tree-based models. Local SHAP values are available above.")

with data_tab:
    st.subheader("Training Dataset Preview")
    st.dataframe(data.head(25), use_container_width=True)
    st.write(f"Rows: {len(data):,}")
