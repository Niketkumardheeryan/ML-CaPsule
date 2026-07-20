# 🖐️ Hand Gesture Controlled Game

Control games using natural hand gestures through your webcam—no physical controller required. This project combines **Computer Vision**, **Machine Learning**, and **Human-Computer Interaction (HCI)** to recognize hand movements and convert them into keyboard inputs in real time.

---

# 📖 Overview

This project uses **Google MediaPipe Hands**, a pre-trained machine learning solution, to detect and track hand landmarks from a live webcam feed. The detected landmarks are analyzed to recognize directional hand movements, which are then translated into keyboard events using **PyAutoGUI**.

Instead of relying on traditional gaming controllers, users can interact with games using intuitive hand gestures, making the project an excellent demonstration of touchless human-computer interaction.

---

# ✨ Features

* Real-time webcam-based hand tracking
* Detection of 21 hand landmarks using MediaPipe
* Automatic neutral hand position calibration
* Gesture-based directional controls
* Keyboard event simulation using PyAutoGUI
* Lightweight and beginner-friendly implementation

---

# 🧠 Machine Learning & Computer Vision

This project uses **MediaPipe Hands**, Google's pre-trained hand tracking framework.

### Hand Detection

A palm detection model first locates the hand in the webcam frame.

### Hand Landmark Estimation

MediaPipe predicts **21 three-dimensional hand landmarks** representing finger joints and fingertips.

### Gesture Recognition

Rather than training a custom model, this project performs **rule-based gesture recognition** by comparing the wrist position with the calibrated neutral position.

### Human-Computer Interaction

Detected gestures are converted into keyboard arrow key presses using PyAutoGUI, allowing touch-free game control.

---

# ⚙️ How It Works

1. Capture video frames from the webcam.
2. Detect the user's hand using MediaPipe.
3. Extract the wrist landmark position.
4. Set the first detected position as the neutral reference.
5. Compare current wrist coordinates with the neutral position.
6. Trigger keyboard arrow keys when the movement exceeds the configured threshold.
7. Continue tracking in real time until the application exits.

---

# 🎮 Gesture Mapping

| Hand Movement | Keyboard Action |
| ------------- | --------------- |
| Move Right    | → Right Arrow   |
| Move Left     | ← Left Arrow    |
| Move Up       | ↑ Up Arrow      |
| Move Down     | ↓ Down Arrow    |

---

# 🛠️ Requirements

* Python 3.10 or later
* Webcam

Install dependencies:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

---

# 🚀 Running the Project

1. Install all required dependencies.
2. Open `hand_gesture_control.ipynb` in Jupyter Notebook or VS Code.
3. Run the notebook cells sequentially.
4. Allow webcam access.
5. Open any game that supports arrow key controls.
6. Control the game using hand gestures.

---

# ⚙️ Configuration

| Variable            | Description                                    |
| ------------------- | ---------------------------------------------- |
| `gesture_delay`     | Minimum time between gesture detections        |
| `dead_zone`         | Minimum movement required to trigger an action |
| `VideoCapture(0/1)` | Select the webcam index                        |

---

# 📂 Project Structure

```
hand_gesture_controlled_game/
├── hand_gesture_control.ipynb
└── README.md
```

---

# 📚 Technologies Used

| Technology | Purpose                                |
| ---------- | -------------------------------------- |
| Python     | Programming language                   |
| OpenCV     | Webcam capture and image processing    |
| MediaPipe  | Hand detection and landmark estimation |
| NumPy      | Numerical operations                   |
| PyAutoGUI  | Keyboard event automation              |

---

# 🚀 Future Improvements

* Support multiple hand gestures
* Custom gesture mapping
* Dynamic sensitivity adjustment
* Multi-player gesture control
* Deep learning-based custom gesture classification

---

Made with ❤️ using Python, OpenCV, MediaPipe, and Computer Vision.
