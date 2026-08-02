# Sleep Alarm Detector

## Overview

Sleep Alarm Detector is a computer vision project that detects drowsiness in real time using a webcam. It monitors the user's eye aspect ratio (EAR) with MediaPipe Face Mesh and triggers an alarm when the eyes remain closed for a specified duration.

This project is implemented as a Jupyter Notebook for easier understanding and execution.

---

## Features

- Real-time face detection
- Eye Aspect Ratio (EAR) based drowsiness detection
- MediaPipe Face Mesh tracking
- Webcam-based monitoring
- Alarm on prolonged eye closure
- Session timer
- Live status overlay

---

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- Pygame

---

## Project Structure

```
Sleep_Alarm_Detector/
│── Sleep_Alarm.ipynb
│── requirements.txt
│── README.md
│── dragon-studio-censor-beep-3-372460.mp3
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Sleep_Alarm_Detector
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Usage

1. Open `Sleep_Alarm.ipynb`.
2. Run all notebook cells in order.
3. Allow webcam access.
4. Press **Q** to stop the application.

---

## How It Works

- Detects facial landmarks using MediaPipe Face Mesh.
- Calculates the Eye Aspect Ratio (EAR).
- Determines whether the eyes are closed.
- Triggers an alarm if the eyes remain closed beyond the threshold.
- Displays EAR, alarm status, and session timer on the screen.

---

## Future Improvements

- Adjustable EAR threshold
- Blink statistics
- Fatigue detection analytics
- Email or notification alerts

---

## License

This project is intended for educational and learning purposes.
