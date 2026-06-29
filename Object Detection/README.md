
# 🧠 Object Detection Pipeline using CNN (TensorFlow / Keras)

  

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)

![Keras](https://img.shields.io/badge/Keras-DeepLearning-red.svg)

![Status](https://img.shields.io/badge/Status-Active-success.svg)

![License](https://img.shields.io/badge/License-MIT-green.svg)

  

> A complete, production-style deep learning pipeline for image classification using Convolutional Neural Networks (CNNs), built with TensorFlow/Keras.

> Covers the full lifecycle: **data ingestion → preprocessing → model design → training → evaluation → visualization**

  

---

  

## 📌 Overview

  

This repository presents an end-to-end implementation of an **image classification system** (often loosely referred to as object detection in beginner contexts) using deep learning.

  

The project is designed not just as a model, but as a **structured machine learning pipeline**, demonstrating how raw image data is transformed into a trained predictive system.

  

Unlike minimal tutorials, this implementation emphasizes:

- Reproducibility
- Clear pipeline separation
- Model interpretability
- Training diagnostics
- Scalable design principles

---

  

## Objective

Given an input image:

$X \in R^{(150,150,3)}$ Learn a mapping function: $f(X : \theta)  \to y$

Where:

- $\theta$ = trainable parameters of the CNN
- $y$ = predicted class label (multi-class classification)
---
## 🧩 System Pipeline
The project follows a standard deep learning workflow:
```
Raw Dataset
↓
Data Loading (Directory-based)
↓
Preprocessing (Resizing, Normalization)
↓
CNN Feature Extraction
↓
Dense Classification Head
↓
Training (Backpropagation + Optimization)
↓
Evaluation (Metrics & Loss Analysis)
↓
Visualization (Graphs & Predictions)
```
---
## 📂 Project Structure
```
├── object_detection.ipynb # Core implementation notebook
├── model_plot.png # Visualized model architecture
├── dataset/
│ ├── train/ # Training images
│ └── validation/ # Validation images
├── assets/
│ ├── training_graph.png
│ └── sample_output.png
├── requirements.txt
└── README.md
```
---


## 📊 Dataset Description

- **Domain**: Furniture Image Classification
- **Type**: Multi-class supervised learning
- **Input Size**: 150 × 150 × 3 (RGB images)

  

### 📁 Organization

```

dataset/
├── train/
│ ├── class_1/
│ ├── class_2/
│ └── ...
├── validation/
│ ├── class_1/
│ ├── class_2/
│ └── ...

``
  

### 🔍 Key Characteristics
- Folder-based labeling (implicit labels)

- Balanced / semi-balanced classes

- Real-world variability (lighting, angle, background)
---

## ⚙️ Environment Setup
### 1. Clone Repository
```bash
git clone https://github.com/your-username/object-detection.git
cd object-detection
```
### 2. Install Dependencies
```
pip install -r requirements.txt
```
Or manually:
```
pip install tensorflow keras numpy matplotlib opencv-python
```
### 3. Run Notebook

```
jupyter notebook object_detection.ipynb
```

# Model Architecture

![alt text](Gemini_Generated_Image_g9r4hbg9r4hbg9r4.png)

The model is a Convolutional Neural Network (CNN) designed to extract hierarchical spatial features.

  

### 🔬 Architecture Design

```
Input Layer (150x150x3)
↓
Conv2D → ReLU
↓
MaxPooling
↓
Conv2D → ReLU
↓
MaxPooling
↓
Flatten
↓
Dense Layer
↓
Softmax Output Layer
```

  

### ⚙️ Mathematical Insight

  

- **Convolution Operation:**

$$FeatureMap(i,j) = \sum\sum (Input × Kernel)$$
- Activation Function
$$ReLU(x) = \max(0, x)$$

### Loss Function

Categorical Crossentropy:

$$L = - \sum y_{true} log(y_{pred})$$

  

### Architecture Visualization

📈 Training Configuration

```
Parameter, Value
Epochs: 5
Batch Size: 32
Optimizer: Adam
Loss Function: Categorical Crossentropy
Metrics: Accuracy
```
### ⚡ Training Dynamics
The model is trained using adam optimizer where gradients are computed and weights updated:
$$m_t = \beta_1m_{t-1} + (1-\beta_1)\nabla L$$
$$v_t = \beta_2v_{t-1} + (1 - \beta_2)(\nabla L)^2$$
$$ \hat{v_t} = \frac{v_t}{\sqrt{1 - \beta_2^{t}}} $$
$$ \hat{m_t} = \frac{m_t}{\sqrt{1 - \beta_1^{t}}}$$
$$\theta = \theta - \frac{\eta \hat{m_t}}{\sqrt{\hat{v_t}  + \epsilon}}$$
Where:
- $\eta$ = learning rate
- $\nabla L$ = gradient of loss
- $m_t$ = Momentum at time t
- $v_t$ = Variance at time t
---

### Results & Performance

The model demonstrates:
- Strong convergence behavior
- Increasing training accuracy
- Stable validation performance
---
### Training Curves

![alt text](image.png)

![alt text](image-1.png)

---

### Model Evaluation

Key observations:

- No severe overfitting observed
- Validation accuracy follows training trend
- Loss decreases consistently

  

### Visualization

The project includes visual diagnostics:

- Training samples inspection
- Class-wise distribution
- Prediction outputs

---

### Future Improvements
This baseline can be extended significantly:
- Model Enhancements
- Transfer Learning (VGG16, ResNet50)
- ~~Fine-tuning deeper layers~~
- Regularization (Dropout, BatchNorm)
- ~~Add YOLO Single Phase Architecture details~~
- Data Improvements
- Data Augmentation
- Class balancing
- Larger datasets
- Deployment
- REST API (Flask / FastAPI)
- ~~Web App (Streamlit)~~
- Model serving (TensorFlow Serving)

### Contribution Guidelines

We welcome contributions to improve:
- Code quality
- Documentation
- Model performance
- Feature additions

### Open Source Contribution (GSSoC)

This project is enhanced under GirlScript Summer of Code (GSSoC) with a focus on:

- Professional documentation
- Beginner accessibility
- Structured deep learning pipeline

---

## Author

Shubham Saini
⭐ Support
If you found this project useful:
- ⭐ Star the repository
- 🍴 Fork and contribute
- 📢 Share with others

Enhanced By 
Ashish Divvela