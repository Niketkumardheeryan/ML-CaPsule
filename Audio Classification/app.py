import os
import tempfile
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from audio_classification import (
    AudioEmotionClassifier,
    extract_audio_features,
    generate_synthetic_dataset,
    EMOTION_NAMES
)

st.set_page_config(
    page_title="Audio Emotion Classification System",
    page_icon="🎙️",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4F46E5;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #4F46E5;
    }
</style>
""", unsafe_allow_dict_scheme=True)

st.markdown('<div class="main-header">🎙️ Emotion Audio Classification System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Classifying Speech Emotions using Acoustic Feature Extraction & K-Nearest Neighbors (KNN)</div>', unsafe_allow_html=True)

@st.cache_resource
def load_trained_model():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'model.pkl')
    scaler_path = os.path.join(script_dir, 'scaler.pkl')
    
    clf = AudioEmotionClassifier(k_neighbors=5)
    if os.path.exists(model_path) and os.path.exists(scaler_path):
        clf.load(model_path, scaler_path)
    else:
        # Train on synthetic dataset if models don't exist
        X, y = generate_synthetic_dataset(num_samples=400)
        clf.train(X, y)
        clf.save(model_path, scaler_path)
    return clf

model = load_trained_model()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Audio Source Selection")
    input_type = st.radio("Choose Input Method:", ("Upload WAV File", "Generate Sample Emotional Audio"))
    
    sr = 16000
    signal = None
    sample_name = ""
    
    if input_type == "Upload WAV File":
        uploaded_file = st.file_uploader("Upload an Audio file (.wav)", type=["wav"])
        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            sr, signal = wav.read(tmp_path)
            st.audio(uploaded_file, format='audio/wav')
            sample_name = uploaded_file.name
    else:
        selected_emotion = st.selectbox("Select Emotion Preset to Generate:", EMOTION_NAMES)
        duration = 1.0
        t = np.linspace(0, duration, int(sr * duration))
        
        # Synthetic signal generation matching preset
        if selected_emotion == 'happy':
            signal = 0.5 * np.sin(2 * np.pi * 440 * t) + 0.3 * np.sin(2 * np.pi * 880 * t) + 0.05 * np.random.randn(len(t))
        elif selected_emotion == 'angry':
            signal = 0.8 * np.sin(2 * np.pi * 150 * t) + 0.5 * np.sin(2 * np.pi * 300 * t) + 0.2 * np.random.randn(len(t))
        elif selected_emotion == 'sad':
            signal = 0.2 * np.sin(2 * np.pi * 200 * t) + 0.02 * np.random.randn(len(t))
        elif selected_emotion == 'fearful':
            signal = 0.4 * np.sin(2 * np.pi * (600 + 100 * np.sin(2 * np.pi * 5 * t)) * t) + 0.1 * np.random.randn(len(t))
        elif selected_emotion == 'disgust':
            signal = 0.3 * np.sin(2 * np.pi * 180 * t) + 0.2 * np.sin(2 * np.pi * 220 * t) + 0.08 * np.random.randn(len(t))
        elif selected_emotion == 'surprised':
            signal = 0.6 * np.sin(2 * np.pi * (300 + 300 * t) * t) + 0.04 * np.random.randn(len(t))
        elif selected_emotion == 'calm':
            signal = 0.25 * np.sin(2 * np.pi * 260 * t) + 0.01 * np.random.randn(len(t))
        else: # neutral
            signal = 0.3 * np.sin(2 * np.pi * 330 * t) + 0.03 * np.random.randn(len(t))
            
        signal = (signal * 32767).astype(np.int16)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            wav.write(tmp_file.name, sr, signal)
            tmp_path = tmp_file.name
        st.audio(tmp_path, format='audio/wav')
        sample_name = f"Preset: {selected_emotion}"

with col2:
    st.subheader("2. Audio Signal Analysis")
    if signal is not None:
        fig, ax = plt.subplots(2, 1, figsize=(8, 4.5))
        
        # Plot Waveform
        time_axis = np.linspace(0, len(signal) / sr, len(signal))
        ax[0].plot(time_axis, signal, color='#4F46E5', alpha=0.8)
        ax[0].set_title(f"Audio Waveform ({sample_name})")
        ax[0].set_xlabel("Time (s)")
        ax[0].set_ylabel("Amplitude")
        ax[0].grid(True, linestyle='--', alpha=0.5)
        
        # Plot Spectrogram / FFT Spectrum
        fft_spec = np.abs(np.fft.rfft(signal))
        freq_axis = np.fft.rfftfreq(len(signal), d=1.0/sr)
        ax[1].plot(freq_axis[:1000], fft_spec[:1000], color='#10B981')
        ax[1].set_title("Frequency Spectrum (Magnitude)")
        ax[1].set_xlabel("Frequency (Hz)")
        ax[1].set_ylabel("Magnitude")
        ax[1].grid(True, linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("Upload or generate an audio file to view waveform & frequency spectrum.")

st.markdown("---")

if signal is not None:
    st.subheader("3. Emotion Classification Results")
    
    # Feature extraction
    features = extract_audio_features(signal, sr)
    pred_emotion, conf, probs = model.predict(features)
    
    res_col1, res_col2 = st.columns([1, 1.5])
    
    with res_col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Predicted Emotion: <span style="color:#4F46E5; text-transform:capitalize;">{pred_emotion}</span></h3>
            <h4>Confidence: <b>{conf * 100:.1f}%</b></h4>
            <p><b>Model:</b> K-Nearest Neighbors (KNN)</p>
            <p><b>Features Extracted:</b> 31 (MFCC energy summaries, Zero Crossing Rate, RMS Energy, Spectral Stats)</p>
        </div>
        """, unsafe_allow_html=True)
        
    with res_col2:
        fig_bar, ax_bar = plt.subplots(figsize=(8, 3.5))
        emotions_list = list(probs.keys())
        prob_values = [probs[e] * 100 for e in emotions_list]
        
        colors = ['#4F46E5' if e == pred_emotion else '#9CA3AF' for e in emotions_list]
        bars = ax_bar.bar(emotions_list, prob_values, color=colors)
        ax_bar.set_ylabel("Probability (%)")
        ax_bar.set_title("Class Probability Distribution")
        ax_bar.set_ylim(0, 105)
        
        for bar in bars:
            yval = bar.get_height()
            ax_bar.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f'{yval:.0f}%', ha='center', va='bottom', fontsize=9)
            
        plt.xticks(rotation=30)
        plt.tight_layout()
        st.pyplot(fig_bar)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #9CA3AF;'>ML-CaPsule Audio Classification Project • RAVDASS Dataset Standard</p>", unsafe_allow_html=True)
