# Driver Drowsiness Detection (Legacy Haar + CNN)

This is the original implementation of the Driver Drowsiness Detection project. It detects whether the driver's eyes remain closed for multiple consecutive frames using Haar Cascade classifiers and a Convolutional Neural Network (CNN).

## Features

- Real-time webcam monitoring
- Face detection using Haar Cascade
- Eye detection using Haar Cascade classifiers
- CNN-based eye state classification
- Drowsiness detection using consecutive closed-eye frames
- Visual alert when prolonged eye closure is detected

## How It Works

The system performs the following steps:

1. Detects the driver's face using a Haar Cascade classifier.
2. Detects both eyes from the detected face.
3. Passes each detected eye to the trained CNN model.
4. Classifies each eye as Open or Closed.
5. If both eyes remain closed for 15 consecutive frames, the system displays a drowsiness alert.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Train the CNN model

Run:

```
CNN_Model.ipynb
```

This notebook:

- Loads the eye image dataset
- Trains the CNN model
- Saves:

```
model.json
model.h5
```

### Run Driver Drowsiness Detection

Run:

```
Driver_Drowsiness_Detection_Haar_CNN.ipynb
```

The notebook:

- Loads the trained CNN model
- Detects face and eyes using Haar Cascade
- Predicts eye state
- Displays an alert when prolonged eye closure is detected

## Dataset

The CNN model is trained using eye image directories organized into training and testing folders.

This implementation does **not** use a CSV file.

## Dependencies

- Python
- OpenCV
- TensorFlow
- Keras
- NumPy

## Project Structure

```
Legacy_Haar_CNN/
│
├── CNN_Model.ipynb
├── Driver_Drowsiness_Detection_Haar_CNN.ipynb
├── model.json
├── model.h5
├── haarcascade_frontalface_default.xml
├── haarcascade_lefteye_2splits.xml
├── haarcascade_righteye_2splits.xml
├── requirements.txt
└── README.md
```

## Demo

<img width="458" alt="Driver Drowsiness Detection Demo" src="https://user-images.githubusercontent.com/73430464/160766013-f7214357-ecf7-4463-b43f-077c45936da2.png">

## Note

This implementation is preserved as the original approach for reference and comparison purposes.