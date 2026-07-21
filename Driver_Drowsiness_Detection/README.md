# Driver Drowsiness Detection

A real-time driver drowsiness alert system built with OpenCV and MediaPipe Face Landmarker. It estimates eye closure from facial landmarks using the Eye Aspect Ratio (EAR) and plays an alarm when both eyes remain closed for a configurable number of consecutive frames.

## Features

- Real-time webcam monitoring
- MediaPipe Face Landmarker facial-landmark tracking
- Eye Aspect Ratio (EAR) calculation for both eyes
- Configurable EAR and consecutive-frame thresholds
- Built-in Windows audio alert
- No dataset, Haar Cascade XML files, or pretrained CNN model required

## How it works

MediaPipe provides landmark coordinates around each eye. The Eye Aspect Ratio compares the vertical eye distances with the horizontal eye distance:

    EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)

An open eye has a larger EAR than a closed eye. The notebook raises an alert only after the average EAR stays below the configured threshold for a configured number of consecutive frames, so normal blinks do not trigger the alarm.

## Installation

    pip install -r requirements.txt

## Run

Open and run Driver_Drowsiness_Detection.ipynb in Jupyter Notebook or VS Code. On the first run, the notebook downloads the official MediaPipe Face Landmarker model automatically; later runs reuse the downloaded file. Allow webcam access when prompted.

- Press q in the webcam window to exit.
- Adjust EAR_THRESHOLD for your camera and lighting conditions.
- Adjust CLOSED_FRAME_THRESHOLD to control how long eyes must remain closed before an alarm.

## Dependencies

- OpenCV
- MediaPipe
- NumPy

The alarm uses Python's built-in Windows audio module, so no audio package or sound file is needed.

## Note

This is an educational computer-vision project and must not be used as the sole safety system in a real vehicle.
