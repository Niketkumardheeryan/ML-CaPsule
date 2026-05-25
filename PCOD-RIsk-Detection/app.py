"""
PCOS Detection System — AI-Powered Healthcare Dashboard
"""

import streamlit as st
import numpy as np
import joblib

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PCOS Detection System",
    page_icon="🌸",
    layout="wide"
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────
def inject_css():

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fff0f3 0%, #ffe4ec 100%);
    }

    .hero {
        background: linear-gradient(135deg, #ffe0e9 0%, #fff0f3 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid #f8c0d0;
        margin-bottom: 2rem;
    }

    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        color: #8b1a30;
        margin-bottom: 0.5rem;
    }

    .hero-sub {
        color: #a0536a;
        font-size: 1rem;
    }

    .result-high {
        background: #fff0f2;
        border: 2px solid #f48499;
        padding: 1.5rem;
        border-radius: 16px;
        margin-top: 1rem;
    }

    .result-low {
        background: #f0fff8;
        border: 2px solid #84c9a4;
        padding: 1.5rem;
        border-radius: 16px;
        margin-top: 1rem;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #e85c80, #c0395a);
        color: white;
        border-radius: 50px;
        border: none;
        font-size: 1rem;
        font-weight: 600;
        padding: 0.7rem 2rem;
    }

    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():

    model_path = "models/pcos_grid_model.pkl"

    try:
        model = joblib.load(model_path)
        return model

    except Exception as e:
        st.error(f"Model loading error: {e}")
        return None

# ─────────────────────────────────────────────────────────────
# FEATURES
# ─────────────────────────────────────────────────────────────
FEATURES = {
    'Follicle No. (R)': {
        "type": "number",
        "min": 0,
        "max": 50,
        "default": 10
    },

    'Follicle No. (L)': {
        "type": "number",
        "min": 0,
        "max": 50,
        "default": 10
    },

    'Skin darkening (Y/N)': {
        "type": "select",
        "options": [0, 1],
        "labels": ["No", "Yes"]
    },

    'Weight gain(Y/N)': {
        "type": "select",
        "options": [0, 1],
        "labels": ["No", "Yes"]
    },

    'hair growth(Y/N)': {
        "type": "select",
        "options": [0, 1],
        "labels": ["No", "Yes"]
    },

    'AMH(ng/mL)': {
        "type": "number",
        "min": 0.0,
        "max": 20.0,
        "default": 3.0
    },

    'Cycle(R/I)': {
        "type": "select",
        "options": [0, 1],
        "labels": ["Regular", "Irregular"]
    },

    'LH(mIU/mL)': {
        "type": "number",
        "min": 0.0,
        "max": 30.0,
        "default": 5.0
    },

    'FSH/LH': {
        "type": "number",
        "min": 0.0,
        "max": 10.0,
        "default": 1.0
    },

    'Cycle length(days)': {
        "type": "number",
        "min": 20,
        "max": 90,
        "default": 30
    }
}

# ─────────────────────────────────────────────────────────────
# SHAP
# ─────────────────────────────────────────────────────────────
def show_shap(model, input_array, feature_names):

    try:

        import shap
        import matplotlib.pyplot as plt

        explainer = shap.TreeExplainer(model)

        shap_values = explainer.shap_values(input_array)

        if isinstance(shap_values, list):
            values = shap_values[1][0]
        else:
            values = shap_values[0]

        indices = np.argsort(np.abs(values))[::-1]

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.barh(
            [feature_names[i] for i in indices],
            values[indices]
        )

        ax.set_title("SHAP Feature Impact")

        st.pyplot(fig)

    except Exception as e:
        st.warning(f"SHAP Error: {e}")

# ─────────────────────────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────────────────────────
def home_page():

    st.markdown("""
    <div class="hero">
        <div class="hero-title">
            🌸 PCOS Detection System
        </div>

        
    </div>
    """, unsafe_allow_html=True)

    model = load_model()

    if model is None:
        st.stop()

    st.subheader("📋 Patient Information")

    collected = {}

    cols = st.columns(2)

    feature_names = list(FEATURES.keys())

    for i, feature in enumerate(feature_names):

        with cols[i % 2]:

            cfg = FEATURES[feature]

            # NUMBER INPUTS
            if cfg["type"] == "number":

                collected[feature] = st.number_input(
                    feature,
                    min_value=float(cfg["min"]),
                    max_value=float(cfg["max"]),
                    value=float(cfg["default"])
                )

            # SELECT INPUTS
            elif cfg["type"] == "select":

                collected[feature] = st.selectbox(
                    feature,
                    options=cfg["options"],
                    format_func=lambda x: cfg["labels"][x]
                )

    st.markdown("")

    button_col = st.columns([1, 1, 1])

    with button_col[1]:

        predict_clicked = st.button(
            "🔍 Check PCOS Risk",
            use_container_width=True
        )

    # ─────────────────────────────────────────
    # PREDICTION
    # ─────────────────────────────────────────
    if predict_clicked:

        input_array = np.array([
            [collected[k] for k in feature_names]
        ])

        try:

            probability = model.predict_proba(input_array)[0][1]

            prediction = int(probability >= 0.5)

            st.session_state["prediction"] = prediction
            st.session_state["probability"] = probability
            st.session_state["input"] = input_array

        except Exception as e:
            st.error(f"Prediction Error: {e}")

    # ─────────────────────────────────────────
    # SHOW RESULTS
    # ─────────────────────────────────────────
    if "prediction" in st.session_state:

        prediction = st.session_state["prediction"]
        probability = st.session_state["probability"]

        if prediction == 1:

            st.markdown(f"""
            <div class="result-high">
                <h2>⚠️ High PCOS Risk</h2>
                <h4>Confidence: {probability * 100:.2f}%</h4>
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown(f"""
            <div class="result-low">
                <h2>✅ Low PCOS Risk</h2>
                <h4>Confidence: {(1 - probability) * 100:.2f}%</h4>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.subheader("🧠 SHAP Explainability")

        show_shap(
            model,
            st.session_state["input"],
            feature_names
        )

# ─────────────────────────────────────────────────────────────
# SECOND PAGE
# ─────────────────────────────────────────────────────────────
def second_page():

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ffe0e9 0%, #fff0f3 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid #f8c0d0;
        margin-bottom: 2rem;
    ">
    <h1 style="
        color:#8b1a30;
        font-family: 'Playfair Display', serif;
    ">
        📊 PCOS Health Dashboard
    </h1>

    <p style="
        color:#a0536a;
        font-size:1rem;
    ">
        Personalized health guidance based on AI prediction results.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # No prediction yet
    if "prediction" not in st.session_state:

        st.info("⚠️ Please complete prediction on the Home page first.")

        return

    prediction = st.session_state["prediction"]
    probability = st.session_state["probability"]

    # HIGH RISK
    if prediction == 1:

        st.markdown(f"""
        <div class="result-high">

        <h2>
            ⚠️ High PCOS Risk Detected
        </h2>

        <h4 style="color:#8b1a30;">
            Confidence Score: {probability * 100:.2f}%
        </h4>

        <p style="color:#6d4c57; font-size:1rem;">
            The AI model predicts a higher likelihood of PCOS.
            This does NOT confirm diagnosis. Clinical consultation
            and medical testing are strongly recommended.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.subheader("✅ Recommended Actions")

        st.markdown("""
        ### 🩺 Medical Steps
        - Consult a gynecologist or endocrinologist
        - Get ultrasound and hormonal tests done
        - Monitor menstrual cycle regularly
        - Check insulin resistance and thyroid profile

        ### 🥗 Lifestyle Improvements
        - Reduce processed and sugary foods
        - Maintain healthy body weight
        - Increase protein and fiber intake
        - Drink enough water daily

        ### 🏃 Physical Activity
        - Exercise at least 30 minutes daily
        - Include strength training and walking
        - Improve sleep quality

        ### 🧠 Mental Wellness
        - Reduce stress levels
        - Practice meditation or yoga
        - Avoid poor sleep cycles
        """)

        st.warning("""
        ⚠️ Important:
        This prediction is only an AI-assisted assessment and not a medical diagnosis.
        """)

    # LOW RISK
    else:

        st.markdown(f"""
        <div class="result-low">
        <h2>✅ Low PCOS Risk</h2>

        <h4 style="color:#1f7a4a;">
        Confidence Score: {(1 - probability) * 100:.2f}%
        </h4>

        <p style="color:#4f6b5b; font-size:1rem;">
        The AI model predicts a lower likelihood of PCOS
        based on the entered clinical features.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🌿 Healthy Practices To Continue")

        st.markdown("""
        ### 🥗 Nutrition
        - Continue balanced eating habits
        - Maintain healthy body weight
        - Eat fruits, vegetables, and protein-rich foods

        ### 🏃 Fitness
        - Stay physically active
        - Continue regular exercise
        - Maintain healthy sleep patterns

        ### 🩺 Preventive Care
        - Continue routine medical checkups
        - Track menstrual cycle health
        - Monitor hormonal health periodically

        ### 🧠 Wellness
        - Manage stress properly
        - Practice mindfulness and relaxation
        """)

        st.success("""
        ✅ Current assessment indicates lower PCOS risk.
        Continue maintaining a healthy lifestyle.
        """)
# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
def sidebar():

    with st.sidebar:

        st.markdown("## 🌸 PCOS AI System")

        page = st.radio(
            "Navigation",
            [
                "🏠 Home",
                "📊 Dashboard"
            ]
        )

    return page

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():

    inject_css()

    page = sidebar()

    if "Home" in page:
        home_page()
    else:
        second_page()

if __name__ == "__main__":
    main()