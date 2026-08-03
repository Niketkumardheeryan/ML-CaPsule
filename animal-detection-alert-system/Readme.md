# 🐾 Animal Detection & Alert System

Real-time dangerous animal detection using **YOLOv8** with a **Streamlit web interface**.  
Classifies detected animals into danger levels — HIGH / MEDIUM / LOW — and raises visual alerts.

## 🌐 Live Demo
👉 **[Try the App Here](https://ml-capsule-m7z2we9zxgjggq4s3wd2oq.streamlit.app/)**

---

## 🚀 Features

- **YOLOv8-powered detection** — nano / small model support
- **Image upload detection** with bounding boxes
- **Danger level classification** with color-coded alerts
  - 🔴 HIGH — Lion, Tiger, Bear, Elephant
  - 🟡 MEDIUM — Cow, Horse, Zebra
  - 🟢 LOW — Dog, Cat, Sheep, Bird
- **Adjustable confidence threshold** via sidebar
- **Hardware integration** (optional) — Arduino LED/buzzer + GPS + Twilio SMS alerts

---

## 🐉 Danger Level Map

| Animal | Danger Level |
|--------|-------------|
| Lion, Tiger, Bear, Elephant | 🔴 HIGH |
| Cow, Horse, Zebra | 🟡 MEDIUM |
| Dog, Cat, Sheep, Bird, Giraffe | 🟢 LOW |

---

## 🛠️ Local Setup

```bash
# Clone the repo
git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
cd ML-CaPsule/Animal_Detection_Alert_System

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open: [http://localhost:8501](http://localhost:8501)

---

## 📁 Project Structure

```
Animal_Detection_Alert_System/
├── app.py                      # Streamlit web UI
├── Detection.py                # Core YOLOv8 detection logic
├── requirements.txt            # Dependencies
├── Animal_Detection_Demo.ipynb # Demo notebook with results
└── README.md
```

---

## 🔧 Hardware Mode (Optional)

The original system also supports full hardware integration:
- **Arduino** — LED (green/orange/red) + buzzer alerts via serial
- **NEO-6M GPS module** — real-time location tracking
- **Twilio SMS** — alert messages with Google Maps link

---

## 📸 Tech Stack

- [Ultralytics YOLOv8](https://docs.ultralytics.com)
- [Streamlit](https://streamlit.io)
- Python 3.11+
