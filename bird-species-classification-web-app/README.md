# 🐦 Bird Species Classification using Deep Learning

A deep learning web application that classifies different **bird species** from uploaded images using the **Xception Transfer Learning** model. The application is built with **TensorFlow**, **Keras**, and **Streamlit**, providing an intuitive interface for image-based bird species prediction.

---

## 📌 Project Overview

Bird species classification is a challenging computer vision task due to the high visual similarity among many species. This project leverages **Transfer Learning** with the **Xception** architecture to accurately identify bird species from images.

The trained model is deployed as a **Streamlit** web application, allowing users to upload bird images and receive instant predictions.

---

## 🎯 Objectives

* Classify different bird species from images.
* Build a high-performance image classification model using Transfer Learning.
* Develop an interactive web application for real-time predictions.
* Deploy the model using Streamlit.
* Support reproducible deployment with Docker.

---

## 🧠 Deep Learning Model

This project uses the **Xception** architecture with Transfer Learning, which utilizes pretrained ImageNet weights to improve classification performance while reducing training time.

### Model Performance

| Model                          | Accuracy  |
| ------------------------------ | --------- |
| **Xception Transfer Learning** | **94.9%** |

---

## 🛠️ Technologies Used

* Python
* TensorFlow
* Keras
* Xception (Transfer Learning)
* NumPy
* Glob
* Streamlit

---

## 🌐 Live Web Application

Try the deployed application here:

https://share.streamlit.io/shreya024/bird-species-classification-web-app/app.py

---

## 📷 Application Preview

### Home Page

![bird1](https://user-images.githubusercontent.com/72400676/160309740-bf22a5e4-4887-4f08-a514-2deaf984d5e1.JPG)

### Prediction Page

![bird2](https://user-images.githubusercontent.com/72400676/160309748-b9cdc5e7-d2c1-466c-bbdd-7ad3cedeaa45.JPG)

---

## 📦 Model File

The trained model is available as an H5 file.

Download the model from:

https://drive.google.com/file/d/1MXPAFeg029S82cZywaRyRvY9twYq0pNF/view?usp=sharing

OR


https://www.kaggle.com/datasets/akash2907/bird-species-classification

Place the downloaded file:

```text
bird_classification_new_model.h5
```

inside the project directory before running the application.

---

## 🚀 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/bird-species-classification.git
cd bird-species-classification
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the trained model

Download **bird_classification_new_model.h5** from the link above and place it in the project root directory.

### 4. Run the Streamlit application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 🐳 Docker Deployment

This application can also be run inside a Docker container for consistent deployment across different environments.

### Step 1: Download the model

Download the trained model file and place it in the project directory before building the Docker image.

### Step 2: Build the Docker image

```bash
docker build -t bird-species-classification .
```

### Step 3: Run the Docker container

```bash
docker run -p 8501:8501 bird-species-classification
```

### Step 4: Open the application

```text
http://localhost:8501
```

---

## 📁 Project Structure

```text
bird-species-classification/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── bird_classification_new_model.h5
├── images/
├── notebooks/
├── dataset/
└── README.md
```

---

## 🔄 Workflow

1. Load the pretrained Xception model.
2. Upload an input bird image.
3. Preprocess the image for inference.
4. Generate predictions using the trained model.
5. Display the predicted bird species through the Streamlit interface.

---

## ✨ Features

* Image-based bird species classification
* Transfer Learning with Xception
* User-friendly Streamlit interface
* Fast and accurate predictions
* Docker support for portable deployment
* Easy local setup

---

## 🚀 Future Improvements

* Increase the number of supported bird species.
* Add prediction confidence scores.
* Display the top-5 predicted species.
* Integrate Grad-CAM visualizations for model explainability.
* Deploy on cloud platforms such as AWS, Azure, or Google Cloud.
* Support batch image predictions.

---

## 📝 Conclusion

This project demonstrates the application of **Transfer Learning** for image classification using the **Xception** architecture. With an accuracy of **94.9%**, the model effectively classifies bird species from images and provides an interactive prediction experience through a Streamlit web application.

---

## 👩‍💻 Contributor

**Shreya Ghosh**

GitHub: https://github.com/shreya024
