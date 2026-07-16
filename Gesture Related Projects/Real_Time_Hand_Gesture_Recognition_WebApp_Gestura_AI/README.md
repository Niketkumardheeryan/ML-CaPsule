# 🤖 Gestura AI: Real-Time Hand Gesture Recognition Web App

A high-performance, real-time Hand Gesture Recognition Web Application built using **MediaPipe**, **OpenCV**, **Scikit-learn**, and **Streamlit**.

This system processes live webcam feeds through a specialized background processing thread, detects hand structures, instantly registers gestures inside the system terminal, and appends them to a continuous visual chronological stack log.

---

## ✨ Features

- **Multi-Threaded Video Streaming:** High-efficiency web camera stream powered by `streamlit-webrtc`.
- **Precision Landmark Tracking:** Extracts 21 precise 3D hand coordinates using Google MediaPipe.
- **Instant Inference Pipeline:** Real-time gesture prediction via a pre-trained Scikit-learn classifier.
- **Console Telemetry Logs:** Prints gesture updates immediately to the system terminal on sign modification.
- **Glassmorphism Premium UI:** High-contrast dark mode design with responsive live badges and glowing metrics.
- **Log Queue & System Flush:** A running history queue of all continuous inputs with a one-click workspace reset button.

---

## 📸 Live Application Preview

> Add screenshots or GIFs of your application here.

---

## 🛠️ Tech Stack

- **Core Engine:** Python 3.9+
- **Deep Learning Tracking:** MediaPipe Tasks (Vision)
- **Computer Vision Processing:** OpenCV-Python
- **Inference & Serialization:** Scikit-learn, Joblib, NumPy
- **Interactive Framework:** Streamlit, streamlit-webrtc

---

## 📂 Project Structure

```text
Real_Time_Hand_Gesture_Recognition_WebApp_Gestura_AI/
├── fresh_gesture_app.py              # Main multi-threaded frontend web dashboard
├── model/
│   └── keypoint_classifier/
│       ├── hand_landmarker.task      # MediaPipe asset file for tracking
│       └── gesture_classifier.pkl    # Pre-trained ML/DL classification model
├── requirements.txt                  # Python dependencies configuration
└── README.md                         # Project documentation
```

---

## 🚀 Installation & Rapid Deployment

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

---

## 📦 Install Dependencies

```bash
pip install streamlit streamlit-webrtc opencv-python numpy mediapipe joblib scikit-learn
```

---

## ▶️ Run the Application

```bash
streamlit run fresh_gesture_app.py
```

---

## 🧠 Neural Class Mapping Information

The gesture recognition model is trained using hand landmark coordinates extracted using MediaPipe.

Possible recognized gestures may include:

- 🖐️ **Open Palm (Class 0)** → Toggles background simulation media threads
- ✊ **Closed Fist (Class 1)** → Flushes logs and restores workspace view defaults
- 👍 **Thumbs Up (Class 2)** → Locks feature matrices and triggers live UI badges
- ✌️ **Peace Sign (Class 3)** → Swaps interactive panel dashboard navigation rows
- 👌 **OK Sign (Class 4)** → Appends continuous token signals to terminal logs safely