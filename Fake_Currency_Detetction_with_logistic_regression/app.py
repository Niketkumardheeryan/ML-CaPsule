import streamlit as st
import kagglehub
import joblib
from PIL import Image
import numpy as np
import scipy.stats as stats
import os

st.set_page_config("Fake Currency Note Detection" , "https://emojiterra.com/money-with-wings/", layout = "wide")

@st.cache_resource
def load_model():

    path = kagglehub.model_download("divvelaashish/custom-logistic-regression-weights/other/default")
    print("Path to model files:", path)

    data = joblib.load(os.path.join(path , "weights.pkl"))

    return data["model"], data["scaler"]

import numpy as np
import scipy.stats as stats

def get_metrics_features(img_array: np.ndarray) -> np.ndarray:
    """Extracts variance, skewness, kurtosis, and entropy as a 1D NumPy feature vector."""
    # 1. Convert to 1D float array for calculations
    flat_arr = img_array.astype(float).flatten()
    
    # 2. Calculate statistical moments
    variance = float(np.var(flat_arr))
    skewness = float(stats.skew(flat_arr))
    kurtosis = float(stats.kurtosis(flat_arr))
    
    # 3. Calculate Shannon entropy
    counts, _ = np.histogram(flat_arr, bins=256, range=(0, 255))
    probabilities = counts / np.sum(counts)
    probabilities = probabilities[probabilities > 0]
    entropy = float(-np.sum(probabilities * np.log2(probabilities)))
    
    # 4. Return as a 1D NumPy array shape (4,)
    return np.array([variance, skewness, kurtosis, entropy])


model , scaler = load_model()

file = st.file_uploader(label="Upload an image to detect" , type = ["jpg" , "img" , "jpeg"])

if file is not None:
    # Display the uploaded image
    image = Image.open(file)
    st.image(image, caption="Uploaded Image")
    
    # Trigger prediction on button click
    if st.button("Run Prediction"):
        
        # 3. Wrap processing and inference inside the spinner
        with st.spinner("Extracting statistical metrics and running model..."):
            
            # Convert PIL image to NumPy array
            img_array = np.array(image)
            
            # Extract features (using your get_metrics_features function)
            features = get_metrics_features(img_array)
            
            # Prepare data for ML model: Reshape to 2D array (1, 4)
            features_2d = features.reshape(1, -1)
            
            # Apply your fitted scaler
            features_scaled = scaler.transform(features_2d)
            
            # Execute model prediction
            prediction = model.predict(features_scaled)
            probability = model.predict_proba(features_scaled)  # If classification
            
        # Spinner disappears automatically when the block finishes
        st.success("Analysis Complete!")
        st.write(f"**Predicted Class:** {prediction[0]}")
        st.write(f"**Confidence:** {np.max(probability) * 100:.2f}%")


    