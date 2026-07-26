import streamlit as st
import numpy as np
import cv2
from PIL import Image
from tensorflow.keras.models import load_model

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Alzheimer's Disease Predictor",
    page_icon="🧠",
    layout="centered"
)

# ── Labels & descriptions ───────────────────────────────────────────────────────
LABELS = {
    0: "AD — Alzheimer's Disease",
    1: "CN — Cognitively Normal",
    2: "EMCI — Early Mild Cognitive Impairment",
    3: "LMCI — Late Mild Cognitive Impairment",
    4: "MCI — Mild Cognitive Impairment"
}

DESCRIPTIONS = {
    0: "The scan shows signs consistent with Alzheimer's Disease. Please consult a neurologist immediately.",
    1: "The scan appears cognitively normal. No signs of Alzheimer's detected.",
    2: "The scan shows early mild cognitive impairment. Early intervention is recommended.",
    3: "The scan shows late mild cognitive impairment. Medical consultation is advised.",
    4: "The scan shows mild cognitive impairment. Please follow up with a healthcare professional."
}

COLORS = {
    0: "🔴",
    1: "🟢",
    2: "🟡",
    3: "🟠",
    4: "🟡"
}

# ── Load model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_cnn_model():
    model = load_model("alzheimer_model.h5")
    return model

# ── UI ─────────────────────────────────────────────────────────────────────────
st.title("🧠 Alzheimer's Disease Predictor")
st.write("Upload a brain MRI scan image to predict the Alzheimer's disease stage.")

st.markdown("---")

# Info box
st.info("""
**How to use:**
1. Upload a brain MRI scan image (JPG or PNG)
2. The model will classify it into one of 5 categories
3. Results are shown instantly
""")

# Image upload
uploaded_file = st.file_uploader(
    "Upload Brain MRI Scan",
    type=["jpg", "jpeg", "png"],
    help="Upload a grayscale or color brain MRI scan image"
)

if uploaded_file is not None:
    # Show uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Brain Scan", use_column_width=True)

    st.markdown("---")

    # Predict button
    if st.button("🔍 Predict", use_container_width=True):
        with st.spinner("Analyzing brain scan..."):
            try:
                # Preprocess image (same as notebook)
                img_array = np.array(image)
                if len(img_array.shape) == 3:
                    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                else:
                    gray = img_array
                gray = gray / 255.0
                gray = cv2.resize(gray, (240, 240))
                gray = gray.reshape(1, 240, 240, 1)

                # Load model and predict
                model = load_cnn_model()
                prediction = model.predict(gray)
                predicted_class = int(np.argmax(prediction[0]))
                confidence = float(np.max(prediction[0])) * 100

                # Show result
                st.markdown("## 📊 Prediction Result")
                st.markdown(f"### {COLORS[predicted_class]} {LABELS[predicted_class]}")
                st.progress(confidence / 100)
                st.write(f"**Confidence:** {confidence:.2f}%")
                st.markdown(f"> {DESCRIPTIONS[predicted_class]}")

                # Show all class probabilities
                st.markdown("### 📈 Class Probabilities")
                for i, prob in enumerate(prediction[0]):
                    st.write(f"{LABELS[i]}: **{prob*100:.2f}%**")
                    st.progress(float(prob))

            except Exception as e:
                st.error(f"Error loading model: {e}")
                st.warning("Make sure `alzheimer_model.h5` is in the same folder as `app.py`")

st.markdown("---")
st.caption("⚠️ This tool is for educational purposes only and not a substitute for medical diagnosis.")