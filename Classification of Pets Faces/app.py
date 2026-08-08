"""
🐱🐶 Cat vs Dog Classifier - Streamlit Web App
A clean, modern interface for classifying pet images using MobileNetV2
"""
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import json
import os

from design import page_css
page_css()

# Page config
st.set_page_config(
    page_title="Cat vs Dog Classifier",
    layout="centered",
    initial_sidebar_state="collapsed"
)
MODEL_PATH = "pet_classifier.keras"
CLASS_NAMES_PATH = "class_names.json"
IMG_SIZE = (160, 160)


# ──────> Helpers 
@st.cache_resource
def load_model():
    """Load the trained model and class names"""
    if not os.path.exists(MODEL_PATH):
        return None, None
    model = tf.keras.models.load_model(MODEL_PATH)
    with open(CLASS_NAMES_PATH, "r") as f:
        class_names = json.load(f)
    return model, class_names

def preprocess_image(image: Image.Image) -> np.ndarray:
    """Preprocess image for MobileNetV2"""
    image = image.resize(IMG_SIZE)
    if image.mode != "RGB":
        image = image.convert("RGB")
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return img_array

def predict(model, image_array: np.ndarray, class_names: list) -> tuple:
    """Run prediction and return label, confidence, and all probabilities"""
    preds = model.predict(image_array, verbose=0)
    pred_idx = np.argmax(preds[0])
    confidence = float(preds[0][pred_idx])
    label = class_names[pred_idx]
    return label, confidence, preds[0]

def render_result(label: str, confidence: float, all_probs: np.ndarray, class_names: list):
    """Unified result rendering for both upload and sample images"""
    is_cat = label == "Cat"
    emoji = "🐱" if is_cat else "🐶"
    card_class = "cat" if is_cat else "dog"
    fill_class = "cat" if is_cat else "dog"

    st.markdown(f"""
    <div class="result-card {card_class}">
        <div class="result-emoji">{emoji}</div>
        <div class="result-label">{label}</div>
        <div class="result-confidence">Confidence: {confidence:.1%}</div>
        <div class="confidence-bar">
            <div class="confidence-fill {fill_class}" style="width: {confidence*100}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Probability breakdown
    st.markdown('<div class="prob-section"><h3>Class Probabilities</h3>', unsafe_allow_html=True)
    for name, prob in zip(class_names, all_probs):
        pct = float(prob) * 100
        fill_class = "cat" if name == "Cat" else "dog"
        prob_emoji = "🐱" if name == "Cat" else "🐶"
        st.markdown(f"""
        <div class="prob-row">
            <span class="prob-label">{prob_emoji} {name}</span>
            <div class="prob-bar"><div class="prob-fill {fill_class}" style="width: {pct}%;"></div></div>
            <span class="prob-value">{pct:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ──────> Load model
model, class_names = load_model()

# ──────> Header 
st.markdown("<h1>Cat vs Dog Classifier</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Upload a photo of a cat or dog and let the MobileNetV2 model classify it!</p>", unsafe_allow_html=True)

# Model status
if model is None:
    st.error("⚠️ Model not found! Please run `python train_model.py` first to train and save the model.")
    st.stop()
else:
    st.success(f"✅ Model loaded: MobileNetV2 (Classes: {', '.join(class_names)})")

# ──────> File uploader
uploaded_file = st.file_uploader(
    "Choose an image...",
    type=["jpg", "jpeg", "png", "webp"],
    help="Upload a clear photo of a cat or dog",
    label_visibility="collapsed",
    max_upload_size=5,
)

# ──────> Prediction for uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.image(image, caption="📷 Your Image", use_container_width=True)

    with col2:
        with st.spinner("Analyzing..."):
            img_array = preprocess_image(image)
            label, confidence, all_probs = predict(model, img_array, class_names)

        render_result(label, confidence, all_probs, class_names)

# ──────> Info card
st.markdown("""
<div class="info-card">
    <h4>About this model</h4>
    <ul>
        <li>Built with <strong>MobileNetV2</strong> (pre-trained on ImageNet)</li>
        <li>Transfer learning on 10,000+ cat/dog images from Kaggle</li>
        <li>Input size: 160×160 pixels</li>
        <li>Best results with clear, well-lit photos of cats or dogs</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ──────> Sample images 
st.markdown('<div class="samples-section"><h3>Try with sample images</h3>', unsafe_allow_html=True)

sample_cols = st.columns(3)
sample_paths = [
    ("kagglecatsanddogs/PetImages/Cat/0.jpg", "🐱 Sample Cat"),
    ("kagglecatsanddogs/PetImages/Dog/0.jpg", "🐶 Sample Dog"),
]

for col, (path, label) in zip(sample_cols, sample_paths):
    with col:
        disabled = not os.path.exists(path)
        if st.button(label, use_container_width=True, disabled=disabled, key=f"sample_{path}"):
            st.session_state.sample_image = path
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ──────> Handle sample image selection 
if "sample_image" in st.session_state:
    sample_path = st.session_state.sample_image
    if os.path.exists(sample_path):
        image = Image.open(sample_path)

        st.markdown('<div class="sample-result">', unsafe_allow_html=True)
        st.image(image, caption=f"Sample: {os.path.basename(sample_path)}", use_container_width=True)

        img_array = preprocess_image(image)
        label, confidence, all_probs = predict(model, img_array, class_names)

        render_result(label, confidence, all_probs, class_names)

        if st.button("← Upload another image", use_container_width=True):
            del st.session_state.sample_image
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

