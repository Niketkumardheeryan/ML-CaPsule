import streamlit as st
import os
import librosa
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as f
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

#the model
class emotionCNN(nn.Module):
    def __init__(self, num_classes=4):
        super().__init__()
        self.layer1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=1, dilation=(1,2))
        self.bn1 = nn.BatchNorm2d(16)
        self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2, ceil_mode=True)
        self.drop1 = nn.Dropout2d(0.1)
       
        self.layer2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1, dilation=(1,4))
        self.bn2 = nn.BatchNorm2d(32)
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2, ceil_mode=True)
        self.drop2 = nn.Dropout2d(0.2)

        self.adaptive_pool = nn.AdaptiveAvgPool2d((4,4))
        self.fc = nn.Linear(32*4*4, num_classes)

    def forward(self, x):
        x = self.drop1(self.maxpool1(f.relu(self.bn1(self.layer1(x)))))
        x = self.drop2(self.maxpool2(f.relu(self.bn2(self.layer2(x)))))
        x = self.adaptive_pool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x

def extract_live_mfcc(file_path):
    target_sr = 16000
    n_mfc = 40
    max_frames = 128
    try:
        signal, sr = librosa.load(file_path, sr=target_sr)
        mfcc = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=n_mfc, norm='ortho', lifter=22)
        _, num_cols = mfcc.shape
        if num_cols > max_frames:
            mfcc_fixed = mfcc[:, :max_frames]
        else:
            pad_width = max_frames - num_cols
            mfcc_fixed = np.pad(mfcc, ((0,0), (0,pad_width)), mode='constant')
        return mfcc_fixed
    except Exception as e:
        st.error(f"Error processing audio: {e}")
        return None
st.title("🎙️ Speech Emotion Recognition App")
st.write("Upload an audio clip, choose the ground truth emotion, and view the confusion matrix output.")

# Define categories globally
emotion_labels = ["Happy", "Sad", "Angry", "Neutral"]

# Load the trained model into memory safely
@st.cache_resource
def load_trained_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = emotionCNN(num_classes=4).to(device)
    if os.path.exists('best_model.pth'):
        checkpoint = torch.load('best_model.pth', map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        return model, device
    else:
        st.error("Model weights file 'best_model.pth' not found in this folder!")
        return None, device

model, device = load_trained_model()

# User Inputs
uploaded_file = st.file_uploader("Choose a speech audio clip...", type=["wav", "mp3"])

# We must prompt the user for the true category to compute a proper Confusion Matrix
true_emotion_str = st.selectbox("What is the actual ground-truth emotion of this audio sample?", emotion_labels)

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    
    if st.button("Run Model Prediction"):
        # Save file locally temporarily to feed into Librosa
        temp_filename = "temp_input_audio.wav"
        with open(temp_filename, "wb") as f_out:
            f_out.write(uploaded_file.getbuffer())
            
        with st.spinner("Extracting features and running inference..."):
            mfcc_fea = extract_live_mfcc(temp_filename)
            
            if mfcc_fea is not None:
                # Convert matrix format to PyTorch shape matching (Batch=1, Channel=1, 40, 128)
                feat_tensor = torch.tensor(mfcc_fea, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)
                
                with torch.no_grad():
                    outputs = model(feat_tensor)
                    _, pred_idx = torch.max(outputs, 1)
                    predicted_class_idx = pred_idx.cpu().item()
                
                predicted_emotion_str = emotion_labels[predicted_class_idx]
                
                st.success(f"🎉 **Model Prediction Result:** The speaker sounds **{predicted_emotion_str}**!")
                
                # Clean up temp file
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
                
                # ==========================================
                # 4. PLOTTING THE CONFUSION MATRIX
                # ==========================================
                st.subheader("📊 Output Metrics (Confusion Matrix)")
                
                # Transform names into raw label index values 
                y_true = [emotion_labels.index(true_emotion_str)]
                y_pred = [predicted_class_idx]
                
                # Render standard matrix plot structure
                cm = confusion_matrix(y_true, y_pred, labels=[0, 1, 2, 3])
                
                fig, ax = plt.subplots(figsize=(6, 4.5))
                sns.heatmap(
                    cm, 
                    annot=True, 
                    fmt='d', 
                    cmap='Blues', 
                    xticklabels=emotion_labels, 
                    yticklabels=emotion_labels,
                    ax=ax
                )
                plt.xlabel('Predicted Emotion Labels')
                plt.ylabel('True Emotion Labels')
                plt.tight_layout()
                
                st.pyplot(fig)           