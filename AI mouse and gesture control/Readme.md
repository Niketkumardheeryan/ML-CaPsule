# 🖱️ AI Virtual Mouse & Gesture Controller

Control your computer's mouse cursor and clicks using real-time hand gestures
captured from a webcam — no physical mouse required.

## 📌 Overview

This project uses **MediaPipe** to detect 21 hand landmarks in real time,
**OpenCV** to capture and process webcam video, and **PyAutoGUI** to translate
finger positions into system-level cursor movement and click events.

## ✨ Features

- **Real-time hand tracking** — robust landmark detection via MediaPipe Hands
- **Cursor movement** — index fingertip position mapped to screen coordinates
- **Gesture-based clicking** — pinch (thumb + index distance) triggers a left click
- **Smoothening algorithm** — reduces cursor jitter for a usable experience
- **FPS counter** — on-screen performance readout

## 🎮 How It Works (Gesture Guide)

| Gesture | Action |
|---|---|
| ☝️ Index finger up, middle finger down | **Move mode** — cursor follows your index fingertip |
| ✌️ Index + middle fingers up, then pinch them together | **Click mode** — registers a left click when distance < threshold |

## 🛠️ Tech Stack

- Python 3.9+
- [OpenCV](https://opencv.org/) — video capture & image processing
- [MediaPipe](https://developers.google.com/mediapipe) — hand landmark detection
- [PyAutoGUI](https://pyautogui.readthedocs.io/) — system-level mouse control
- NumPy — coordinate interpolation

## 📂 Project Structure

```
ai-virtual-mouse/
├── hand_tracking_module.py   # Reusable MediaPipe hand-detection wrapper
├── virtual_mouse.py          # Main application loop (run this)
├── requirements.txt          # Python dependencies
└── README.md
```

## 🚀 Setup & Usage

1. Clone the repo and navigate into this project folder.
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python virtual_mouse.py
   ```
5. Press **`q`** at any time to quit.

## ⚙️ Configuration

Tunable constants are at the top of `virtual_mouse.py`:

- `FRAME_REDUCTION` — margin so the cursor can still reach screen edges
- `SMOOTHENING` — higher value = smoother movement but more input lag
- `CLICK_DISTANCE_THRESHOLD` — pixel distance between thumb & index to count as a pinch
- `CLICK_COOLDOWN` — minimum seconds between two clicks (prevents double-firing)

## ⚠️ Known Limitations

- Tuned for a right hand facing the camera; left-hand thumb detection may need
  the `fingers_up()` comparison flipped.
- Performance depends on webcam quality and lighting conditions.
- Single-hand tracking only (`max_hands=1`) by default for stability.

## 🙋 Author

Aditya Pandey ([@Tech4Aditya](https://github.com/Tech4Aditya)) — built as part of GSSoC 2026 contribution to [ML-CaPsule](https://github.com/Niketkumardheeryan/ML-CaPsule).
