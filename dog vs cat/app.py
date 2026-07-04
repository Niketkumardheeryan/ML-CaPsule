import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dog vs Cat Classifier",
    page_icon="🐾",
    layout="centered"
)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🐶🐱 Dog vs Cat Classifier")
st.markdown("Upload any image of a **dog or cat** and the CNN model will predict what it is!")
st.markdown("---")

# ── Load Model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model_path = "dog_vs_cat_model.keras"
    if not os.path.exists(model_path):
        st.error("❌ Model file not found! Please train the model first by running the notebook.")
        return None
    return tf.keras.models.load_model(model_path)

model = load_model()

# ── Prediction function ───────────────────────────────────────────────────────
def predict(image: Image.Image):
    img = image.resize((150, 150))
    img_array = np.array(img) / 255.0
    if img_array.shape[-1] == 4:          # handle RGBA
        img_array = img_array[:, :, :3]
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array, verbose=0)[0][0]
    label      = "Dog 🐶" if prediction > 0.5 else "Cat 🐱"
    confidence = prediction if prediction > 0.5 else 1 - prediction
    return label, float(confidence)

# ── Upload Section ────────────────────────────────────────────────────────────
st.subheader("📤 Upload an Image")
uploaded_file = st.file_uploader(
    "Choose a JPG or PNG image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file and model:
    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(image, caption="Uploaded Image", use_column_width=True)

    with col2:
        st.subheader("🔍 Prediction")
        with st.spinner("Analyzing image..."):
            label, confidence = predict(image)

        # Result card
        if "Dog" in label:
            st.success(f"### {label}")
            color = "🟦"
        else:
            st.warning(f"### {label}")
            color = "🟧"

        # Confidence bar
        st.markdown(f"**Confidence: {confidence*100:.2f}%**")
        st.progress(confidence)

        # Confidence breakdown
        st.markdown("#### Confidence Breakdown")
        dog_conf = confidence   if "Dog" in label else 1 - confidence
        cat_conf = 1 - dog_conf

        st.markdown(f"🐶 **Dog:** {dog_conf*100:.2f}%")
        st.progress(float(dog_conf))
        st.markdown(f"🐱 **Cat:** {cat_conf*100:.2f}%")
        st.progress(float(cat_conf))

    st.markdown("---")

# ── Sample Predictions Section ────────────────────────────────────────────────
st.subheader("🖼️ Sample Predictions from Training")
sample_images_path = "sample_predictions.png"
if os.path.exists(sample_images_path):
    st.image(sample_images_path, caption="Model predictions on test images (Green = Correct, Red = Wrong)", use_column_width=True)
else:
    st.info("📌 Run the notebook first to generate sample prediction images.")

# ── Model Info ────────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("ℹ️ About the Model"):
    st.markdown("""
    **Architecture:** Custom CNN (3 Convolutional Blocks)
    
    | Layer Block | Filters | Operation |
    |---|---|---|
    | Block 1 | 32  | Conv2D → BatchNorm → MaxPool → Dropout |
    | Block 2 | 64  | Conv2D → BatchNorm → MaxPool → Dropout |
    | Block 3 | 128 | Conv2D → BatchNorm → MaxPool → Dropout |
    | Classifier | 512 | Dense → BatchNorm → Dropout → Sigmoid |
    
    - **Input size:** 150×150 RGB
    - **Optimizer:** Adam
    - **Loss:** Binary Crossentropy
    - **Dataset:** Kaggle Dogs vs Cats
    """)

st.markdown("---")
st.markdown("Built with ❤️ using TensorFlow & Streamlit | GSSoC 2026")
