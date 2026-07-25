# Driver Drowsiness Detection (MediaPipe + EAR)

A real-time driver drowsiness detection system built using OpenCV and MediaPipe Face Landmarker. The system monitors eye movements from a live webcam feed, calculates the Eye Aspect Ratio (EAR) using facial landmarks, and triggers an alert when the driver's eyes remain closed for a configurable number of consecutive frames.

## Features

- Real-time webcam monitoring
- Face detection and facial landmark tracking using MediaPipe Face Landmarker
- Eye Aspect Ratio (EAR) based eye-closure detection
- Configurable EAR and consecutive-frame thresholds
- Real-time visual and audio alert
- Lightweight implementation with no CNN training required
- No Haar Cascade XML files or pretrained CNN model required

## How It Works

The application captures frames from the webcam and uses MediaPipe Face Landmarker to detect facial landmarks.

For each frame:

1. Detect facial landmarks around both eyes.
2. Calculate the Eye Aspect Ratio (EAR).
3. Compare the average EAR with a predefined threshold.
4. If the EAR remains below the threshold for a specified number of consecutive frames, trigger a drowsiness alert.
5. Ignore normal eye blinks using the consecutive-frame threshold.

The Eye Aspect Ratio is calculated as:

```
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 × ||p1 - p4||)
```

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run:

```
Driver_Drowsiness_Detection_MediaPipe.ipynb
```

On the first execution, the notebook automatically downloads the official MediaPipe Face Landmarker model (`face_landmarker.task`). The model is downloaded only once and reused in subsequent runs.

While running:

- Allow webcam access when prompted.
- Press **Q** to exit.
- Adjust `EAR_THRESHOLD` if required.
- Adjust `CLOSED_FRAME_THRESHOLD` if required.

## Dataset

This implementation performs real-time webcam inference using MediaPipe Face Landmarker.

No external dataset or CSV file is required.

## Dependencies

- Python
- OpenCV
- MediaPipe
- NumPy

The audio alert uses Python's built-in `winsound` module on Windows.

## Project Structure

```
MediaPipe_EAR/
│
├── Driver_Drowsiness_Detection_MediaPipe.ipynb
├── requirements.txt
├── README.md
└── .gitignore
```

## Expected Behavior

- Eyes open → No alert
- Normal blink → No alert
- Prolonged eye closure → Visual and audio alert
- Press **Q** → Exit safely

## Note

This project is intended for educational purposes only and should not be used as the sole safety mechanism in real-world driving applications.