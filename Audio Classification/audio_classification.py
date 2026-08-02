import os
import sys
import pickle
import numpy as np
import scipy.io.wavfile as wav
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Emotion dictionary corresponding to RAVDASS dataset emotion codes
EMOTIONS = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

EMOTION_NAMES = list(set(EMOTIONS.values()))
EMOTION_NAMES.sort()

def extract_audio_features(signal, sr, n_mfcc=13):
    """
    Extract MFCC and spectral summary features from raw audio signal.
    Uses numpy and scipy FFT for robust, fallback-safe extraction.
    """
    if signal.ndim > 1:
        signal = np.mean(signal, axis=1)
    
    # Normalize signal
    max_val = np.max(np.abs(signal))
    if max_val > 0:
        signal = signal / max_val
    
    # Frame division
    frame_len = int(sr * 0.025)  # 25ms
    frame_step = int(sr * 0.010) # 10ms
    signal_len = len(signal)
    
    if signal_len < frame_len:
        signal = np.pad(signal, (0, frame_len - signal_len), 'constant')
        signal_len = len(signal)
        
    num_frames = 1 + int(np.floor((signal_len - frame_len) / frame_step))
    
    # Simple spectral energy & zero crossing feature calculation
    zc_rate = np.sum(np.abs(np.diff(np.sign(signal)))) / (2.0 * signal_len)
    rms_energy = np.sqrt(np.mean(signal ** 2))
    
    # Compute FFT magnitude spectra across frames
    frames = []
    window = np.hanning(frame_len)
    for i in range(num_frames):
        start = i * frame_step
        end = start + frame_len
        if end > signal_len:
            break
        frame = signal[start:end] * window
        frames.append(frame)
        
    if len(frames) == 0:
        frames = [signal[:frame_len] * window]
        
    frames = np.array(frames)
    mag_frames = np.abs(np.fft.rfft(frames, n=512))
    
    # Log mel filterbank simulation / band energies (13 features)
    n_bands = n_mfcc
    freq_bins = mag_frames.shape[1]
    band_size = max(1, freq_bins // n_bands)
    
    mfcc_feats = []
    for b in range(n_bands):
        start_bin = b * band_size
        end_bin = (b + 1) * band_size if b < n_bands - 1 else freq_bins
        band_energy = np.mean(mag_frames[:, start_bin:end_bin], axis=1)
        log_band_energy = np.log(band_energy + 1e-10)
        mfcc_feats.append(np.mean(log_band_energy))
        mfcc_feats.append(np.std(log_band_energy))
        
    # Additional global features
    extra_feats = [
        zc_rate,
        rms_energy,
        np.mean(mag_frames),
        np.std(mag_frames),
        np.max(mag_frames)
    ]
    
    features = np.array(mfcc_feats + extra_feats)
    return features


def generate_synthetic_dataset(num_samples=400, sr=16000, duration=1.0):
    """
    Generate synthetic audio dataset mimicking 8 emotional acoustic patterns.
    Ensures tests and demonstrations execute without external dataset dependency.
    """
    np.random.seed(42)
    X = []
    y = []
    t = np.linspace(0, duration, int(sr * duration))
    
    emotions = EMOTION_NAMES
    
    for i in range(num_samples):
        emotion = emotions[i % len(emotions)]
        # Acoustic properties per emotion: modulation frequency, noise, and tone
        if emotion == 'happy':
            signal = 0.5 * np.sin(2 * np.pi * 440 * t) + 0.3 * np.sin(2 * np.pi * 880 * t)
            signal += 0.05 * np.random.randn(len(t))
        elif emotion == 'angry':
            signal = 0.8 * np.sin(2 * np.pi * 150 * t) + 0.5 * np.sin(2 * np.pi * 300 * t)
            signal += 0.2 * np.random.randn(len(t))
        elif emotion == 'sad':
            signal = 0.2 * np.sin(2 * np.pi * 200 * t) + 0.02 * np.random.randn(len(t))
        elif emotion == 'fearful':
            signal = 0.4 * np.sin(2 * np.pi * (600 + 100 * np.sin(2 * np.pi * 5 * t)) * t)
            signal += 0.1 * np.random.randn(len(t))
        elif emotion == 'disgust':
            signal = 0.3 * np.sin(2 * np.pi * 180 * t) + 0.2 * np.sin(2 * np.pi * 220 * t)
            signal += 0.08 * np.random.randn(len(t))
        elif emotion == 'surprised':
            signal = 0.6 * np.sin(2 * np.pi * (300 + 300 * t) * t)
            signal += 0.04 * np.random.randn(len(t))
        elif emotion == 'calm':
            signal = 0.25 * np.sin(2 * np.pi * 260 * t)
            signal += 0.01 * np.random.randn(len(t))
        else: # neutral
            signal = 0.3 * np.sin(2 * np.pi * 330 * t)
            signal += 0.03 * np.random.randn(len(t))
            
        feats = extract_audio_features(signal, sr)
        X.append(feats)
        y.append(emotion)
        
    return np.array(X), np.array(y)


class AudioEmotionClassifier:
    """
    Audio Emotion Classifier model pipeline using KNN and Random Forest.
    """
    def __init__(self, k_neighbors=5):
        self.k_neighbors = k_neighbors
        self.scaler = StandardScaler()
        self.knn_model = KNeighborsClassifier(n_neighbors=k_neighbors)
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False

    def train(self, X_train, y_train):
        X_scaled = self.scaler.fit_transform(X_train)
        self.knn_model.fit(X_scaled, y_train)
        self.rf_model.fit(X_scaled, y_train)
        self.is_trained = True

    def evaluate(self, X_test, y_test):
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation.")
            
        X_scaled = self.scaler.transform(X_test)
        
        knn_preds = self.knn_model.predict(X_scaled)
        rf_preds = self.rf_model.predict(X_scaled)
        
        knn_acc = accuracy_score(y_test, knn_preds)
        rf_acc = accuracy_score(y_test, rf_preds)
        
        metrics = {
            'knn_accuracy': knn_acc,
            'rf_accuracy': rf_acc,
            'knn_report': classification_report(y_test, knn_preds, output_dict=True),
            'knn_cm': confusion_matrix(y_test, knn_preds, labels=EMOTION_NAMES),
            'rf_cm': confusion_matrix(y_test, rf_preds, labels=EMOTION_NAMES)
        }
        return metrics

    def predict(self, features):
        if not self.is_trained:
            raise ValueError("Model must be trained before inference.")
        
        if features.ndim == 1:
            features = features.reshape(1, -1)
            
        feats_scaled = self.scaler.transform(features)
        pred_emotion = self.knn_model.predict(feats_scaled)[0]
        probs = self.knn_model.predict_proba(feats_scaled)[0]
        
        confidence = np.max(probs)
        return pred_emotion, confidence, dict(zip(self.knn_model.classes_, probs))

    def save(self, model_path='model.pkl', scaler_path='scaler.pkl'):
        with open(model_path, 'wb') as f:
            pickle.dump(self.knn_model, f)
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)

    def load(self, model_path='model.pkl', scaler_path='scaler.pkl'):
        with open(model_path, 'rb') as f:
            self.knn_model = pickle.load(f)
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        self.is_trained = True


if __name__ == '__main__':
    print("=" * 60)
    print("      AUDIO EMOTION CLASSIFICATION SYSTEM (KNN & RF)      ")
    print("=" * 60)
    
    print("\n[1/3] Generating synthetic RAVDASS-style audio feature dataset...")
    X, y = generate_synthetic_dataset(num_samples=400)
    print(f"Dataset shapes -> Features: {X.shape}, Target labels: {y.shape}")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    print("\n[2/3] Training K-Nearest Neighbors (KNN) and Random Forest classifiers...")
    clf = AudioEmotionClassifier(k_neighbors=5)
    clf.train(X_train, y_train)
    
    metrics = clf.evaluate(X_test, y_test)
    print(f" -> KNN Model Accuracy:           {metrics['knn_accuracy'] * 100:.2f}%")
    print(f" -> Random Forest Model Accuracy: {metrics['rf_accuracy'] * 100:.2f}%")
    
    print("\n[3/3] Testing inference on sample audio features...")
    sample_feat = X_test[0]
    expected = y_test[0]
    predicted, conf, prob_dict = clf.predict(sample_feat)
    
    print(f" -> Ground Truth Emotion: {expected}")
    print(f" -> Predicted Emotion:    {predicted} (Confidence: {conf * 100:.1f}%)")
    
    # Save model artifacts
    script_dir = os.path.dirname(os.path.abspath(__file__))
    clf.save(
        model_path=os.path.join(script_dir, 'model.pkl'),
        scaler_path=os.path.join(script_dir, 'scaler.pkl')
    )
    print(f"\nModel artifacts successfully saved to '{script_dir}'.")
