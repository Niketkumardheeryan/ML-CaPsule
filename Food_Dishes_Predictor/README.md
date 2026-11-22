#  Food Dish Classification using Deep Learning (lightweight for cpu only machines)

This project implements a deep learning–based system that classifies food dishes from images.  
The system supports **two modes of prediction**:

1. **Image Upload Mode** – classify a user-provided food image  
2. **Webcam Mode** – classify food dishes in real time using a webcam feed  

The model predicts the most likely dish along with a confidence score.

The system is trained using a convolutional neural network (MobileNetV2) and is designed to run efficiently on CPU-only machines, making it suitable for lightweight deployment and academic demonstrations.

---

## Project Overview

- **Input**:
  - Uploaded image of a food dish **OR**
  - Live webcam frame
- **Output**: Predicted food dish name + confidence score
- **Model**: MobileNetV2 (transfer learning)
- **Framework**: PyTorch
- **Training**: Google Colab (GPU)
- **Inference**: Local machine (CPU)

---

## Key Features

- Multi-class food classification (80+ dishes)
- Supports both **image-based** and **webcam-based** prediction
- Uses pretrained MobileNetV2 for efficient learning
- Proper dataset handling with train/validation split
- Confidence score using softmax probabilities
- Modular and clean project structure

---

##  Project Structure

mlproj/
├── dataset/
│ ├── raw/ # Original dataset (not used directly)
│ ├── train/ # Training images (80%)
│ └── val/ # Validation images (20%)
│
├── models/
│ ├── food_classifier.pth # Trained model weights
│ └── classes.txt # Class labels
│
├── scripts/
│ ├── split_random.py # Splits raw → train/val
│ ├── predict_image.py # Predict dish from an uploaded image
│ ├── run_single_image.py # Single-image test script
│ ├── run_webcam.py # Live webcam-based prediction
│ └── camera_test.py # Webcam sanity check
│
├── notebooks/
│ └── train_classifier.ipynb # Training notebook (Google Colab)
│
├── sample_images/
│ └── test$.jpg # Sample image for testing ($ - 1,2,3)
│
├── requirements.txt
└── README.md



---

##  Dataset Handling

- Images are organized by dish name (folder = class)
- Dataset is split into:
  - **80% training**
  - **20% validation**
- The `raw/` folder is preserved as the original dataset
- Training and validation subsets are generated programmatically to prevent data leakage

---

##  Model Architecture

- **Backbone**: MobileNetV2 (pretrained on ImageNet)
- **Classifier head**: Fully connected layer adapted to number of dishes
- **Loss function**: Cross-Entropy Loss
- **Optimizer**: Adam
- **Input size**: RGB images

MobileNetV2 was chosen for its balance between accuracy and computational efficiency, enabling real-time inference on CPU systems.

---

##  Training Details

- Training performed on **Google Colab with GPU acceleration**
- Validation accuracy achieved: ~**69%** across 20+ food classes
- Training stopped based on validation performance to avoid overfitting
- Final model exported for local inference

---

# How to Run the Project

Follow the steps below to run the food dish classification system on your local machine.

---

### Clone the Project and Navigate to Folder

#### 1. Image-Based Food Prediction
```bash
cd mlproj

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python scripts/predict_image.py sample_images/test1.jpg

```
##### Predicted Dish : dal_makhani
##### Confidence    : 91.25%

#### 2. Webcam-Based Food Prediction

```bash
cd mlproj

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python scripts/camera_test.py

```

# some images of working model - 

![alt text](<Screenshot 2026-02-08 174207.png>) ![alt text](<Screenshot 2026-02-08 174146.png>)![alt text](<Screenshot 2026-02-08 174126.png>) 
