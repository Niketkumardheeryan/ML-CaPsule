import streamlit as st
import cv2
import numpy as np
from PIL import Image
from mtcnn import MTCNN
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# ── Page setup
st.set_page_config(page_title="Mask Check", page_icon="🛡️", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #15171C; color: #E8E6E1; }
    h1 { font-family: 'Georgia', serif; font-weight: 700; letter-spacing: -0.5px; color: #F4F1EA; }
    .subtitle { color: #8A8D94; font-size: 0.95rem; margin-top: -10px; margin-bottom: 30px; }
    .result-card {
        background-color: #1C1F26; border: 1px solid #2C2F38;
        border-radius: 10px; padding: 20px 24px; margin-top: 16px;
    }
    .result-label {
        font-family: 'Courier New', monospace; font-size: 0.78rem;
        letter-spacing: 1.5px; color: #8A8D94; text-transform: uppercase;
    }
    .result-value { font-family: 'Courier New', monospace; font-size: 1.6rem; font-weight: 700; margin-top: 4px; }
    div[data-testid="stFileUploader"] { border: 1px dashed #3A3D47; border-radius: 10px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🛡️ Mask Check</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Upload a photo, or go live with your camera for real-time detection.</p>", unsafe_allow_html=True)

# ── Load model and detector once
@st.cache_resource
def load_assets():
    model = load_model('best_facemask_effnet.keras')
    detector = MTCNN()
    return model, detector

model, detector = load_assets()

label_map = {0: 'No Mask', 1: 'Incorrect Mask', 2: 'Mask Worn Correctly'}
color_map = {0: (220, 60, 60), 1: (230, 160, 50), 2: (70, 180, 110)}
status_color_hex = {0: '#E0524F', 1: '#E6A032', 2: '#46B46E'}

def run_detection(frame_rgb):
    faces = detector.detect_faces(frame_rgb)
    results = []
    for face in faces:
        x, y, w, h = face['box']
        x, y = max(0, x), max(0, y)
        face_crop = frame_rgb[y:y+h, x:x+w]
        if face_crop.size == 0:
            continue
        face_resized = cv2.resize(face_crop, (128, 128))
        face_array = preprocess_input(face_resized.astype('float32'))
        face_array = np.expand_dims(face_array, axis=0)

        pred = model.predict(face_array, verbose=0)
        pred_label = np.argmax(pred)
        confidence = float(pred[0][pred_label])

        label_text = f"{label_map[pred_label]} ({confidence*100:.1f}%)"
        color = color_map[pred_label]
        cv2.rectangle(frame_rgb, (x, y), (x+w, y+h), color, 3)
        cv2.putText(frame_rgb, label_text, (x, max(y-12, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        results.append((pred_label, confidence))
    return frame_rgb, results

# ── Video processor class - this is webrtc's required interface
class MaskDetectionProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="rgb24")
        processed, _ = run_detection(img)
        return av.VideoFrame.from_ndarray(processed, format="rgb24")

# ── Input mode toggle
mode = st.radio("Choose input method", ["Upload a photo", "Live webcam"], horizontal=True)

if mode == "Upload a photo":
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_array = np.array(Image.open(uploaded_file).convert('RGB'))
        with st.spinner("Scanning..."):
            result_image, results = run_detection(image_array.copy())
        st.image(result_image, use_container_width=True)

        if not results:
            st.warning("No face detected. Try a clearer, front-facing photo with good lighting.")
        for i, (label, conf) in enumerate(results):
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">Face {i+1} · Status</div>
                <div class="result-value" style="color:{status_color_hex[label]}">{label_map[label]}</div>
                <div class="result-label" style="margin-top:8px;">Confidence: {conf*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

else:
    st.write("Click **Start** below, then allow camera access.")
    webrtc_streamer(
    key="mask-detection",
    video_processor_factory=MaskDetectionProcessor,
    media_stream_constraints={"video": True, "audio": False},
    rtc_configuration=RTC_CONFIGURATION,
)