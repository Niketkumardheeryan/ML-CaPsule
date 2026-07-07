# Human Activity Recognition
Identify human activity and posture recognition using a Convolutional Neural Network (CNN) and Recurrent Neural Network (RNN).

## library used :
- OpenCV (cv2)
- NumPy
- Matplotlib (plt)
- Google Colab Patches (cv2_imshow)
  
## Neural network used :
  1. pose_deploy_linevec_faster_4_stages.prototxt
  2. pose_iter_160000.caffemodel

## Features
- Gesture and Action Recognition: The project identifies and classifies human gestures and actions. For example, it can 
  recognize activities like walking, running, sitting, or waving.
- Deep Learning Models: It employs Convolutional Neural Networks (CNNs) and Recurrent Neural Networks (RNNs) to learn 
  patterns from input data (such as video frames or sensor readings).
- Real-Time Processing: The system can process data in real time, making it suitable for applications like surveillance, 
  fitness tracking, or interactive games.

 ### How It Works:
  - Data Collection: Gather labeled data (videos, sensor data, etc.) showing various human activities.
  - Preprocessing: Clean and preprocess the data (e.g., resizing images, normalizing values).
  - Model Architecture:
     1. CNN: Extract spatial features from images or video frames.
     2. RNN: Capture temporal dependencies (e.g., recognizing a sequence of actions).
  - Training: Train the combined CNN-RNN model on the labeled dataset.
  - Inference: Apply the trained model to new data for prediction.

## Usage:
- Automated Monitoring: Detect abnormal behavior (e.g., falls, sudden movements) for safety applications.
- Health and Fitness: Track exercises, analyze posture, and provide feedback.
- User Interfaces: Enable gesture-based interaction in applications (e.g., controlling devices with hand gestures).



<img width="341" alt="Screenshot 2024-05-21 130046" src="https://github.com/Pranshu-jais/Human-Activity-Recognition/assets/150207373/219e511f-c887-41a9-ba55-7637f7cf2784">


<img width="333" alt="Screenshot 2024-05-21 130316" src="https://github.com/Pranshu-jais/Human-Activity-Recognition/assets/150207373/268aae28-4541-438a-9165-7ae8d69a7281">
