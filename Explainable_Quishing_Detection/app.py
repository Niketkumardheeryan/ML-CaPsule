import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import shap
import matplotlib.pyplot as plt

# Streamlit title
st.title("Explainable AI for Quishing Detection")

st.write("Detect whether a QR code URL is safe or malicious.")

# User input
url = st.text_input("Enter URL from QR Code")

# Simple feature extraction
def extract_features(url):
    return [
        len(url),
        url.count('.'),
        url.count('-'),
        int("https" in url),
        url.count('/'),
        url.count('@')
    ]

# Dummy training data
X = np.array([
    [20,1,0,1,2,0],
    [80,5,4,0,8,1],
    [30,2,1,1,3,0],
    [100,7,5,0,10,1]
])

y = np.array([0,1,0,1])

# Train model
model = RandomForestClassifier()
model.fit(X, y)

if st.button("Detect"):
    
    features = np.array([extract_features(url)])
    
    prediction = model.predict(features)[0]
    
    if prediction == 1:
        st.error("Malicious QR Code Detected!")
    else:
        st.success("Safe QR Code")

    # SHAP Explainability
    explainer = shap.Explainer(model, X)
    shap_values = explainer(features)

    st.subheader("Why this prediction?")

    feature_names = [
        "URL Length",
        "Dots Count",
        "Hyphen Count",
        "HTTPS Present",
        "Slash Count",
        "@ Symbol Count"
    ]

    feature_df = pd.DataFrame({
        "Feature": feature_names,
        "Value": features[0]
    })

    st.write(feature_df)

    fig, ax = plt.subplots()
    shap.plots.waterfall(shap_values[0, :, 1], show=False)
    st.pyplot(fig)
