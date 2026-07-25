# Driver Drowsiness Detection

This project contains two independently documented implementations of real-time driver drowsiness detection.

## Implementations

| Folder | Method | Description |
| --- | --- | --- |
| [Legacy_Haar_CNN](Legacy_Haar_CNN) | Haar Cascades + CNN | Original implementation using Haar Cascade classifiers with a CNN for eye state classification. |
| [MediaPipe_EAR](MediaPipe_EAR) | MediaPipe Face Landmarker + Eye Aspect Ratio (EAR) | Modern implementation using MediaPipe facial landmarks and the Eye Aspect Ratio for drowsiness detection. |

Each implementation contains:
- A dedicated Jupyter notebook
- A separate README
- A requirements.txt file
- Implementation-specific assets

## Codebase

### Legacy Haar + CNN
- **Folder:** [Legacy_Haar_CNN](Legacy_Haar_CNN)
- **Notebook:** [CNN_Model.ipynb](Legacy_Haar_CNN/CNN_Model.ipynb)
- **Detection Notebook:** [Driver_Drowsiness_Detection_Haar_CNN.ipynb](Legacy_Haar_CNN/Driver_Drowsiness_Detection_Haar_CNN.ipynb)

### MediaPipe + EAR
- **Folder:** [MediaPipe_EAR](MediaPipe_EAR)
- **Notebook:** [Driver_Drowsiness_Detection_MediaPipe.ipynb](MediaPipe_EAR/Driver_Drowsiness_Detection_MediaPipe.ipynb)

## Dataset

### Legacy Haar + CNN
The CNN model is trained using eye image directories (Open/Closed). The dataset is organized into training and testing folders and **does not use a CSV file**.

### MediaPipe + EAR
This implementation performs real-time webcam inference using MediaPipe Face Landmarker and **does not require any dataset or CSV file**.

## Running the Project

Each implementation can be executed independently by following the instructions provided in its respective README.

Before submitting:
- All notebook cells should be executed.
- Outputs should remain saved in the notebook.
- Follow the setup instructions inside the corresponding implementation folder.