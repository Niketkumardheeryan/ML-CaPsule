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
AI mouse and gesture control/
├── Ai_virtual_mouse.ipynb    # Jupyter notebook — run this
└── README.md

## 🚀 Setup & Usage

1. Clone the repo and navigate into this project folder.
2. Create a virtual environment (recommended):
```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
```
3. Launch Jupyter and open the notebook:
```bash
   pip install notebook
   jupyter notebook
```
4. Run the application:
   - Open `Ai_virtual_mouse.ipynb`
   - Run the first cell to install dependencies (`opencv-python`, `mediapipe`, `pyautogui`, `numpy`)
   - Run all remaining cells in order (`Kernel → Restart & Run All`)
   - A window titled **"AI Virtual Mouse"** will open showing your webcam feed

   > **Note:** Must be run locally with webcam + display access. Will not
   > work on Google Colab or any headless/cloud environment.
5. Press **`q`** inside the video window at any time to quit.
   - If the kernel is interrupted before pressing `q`, run the final cleanup
     cell in the notebook to release the webcam and close the window.

## ⚙️ Configuration

Tunable constants are set in the notebook's configuration cell:

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