## Web Application for Breast Cancer Detection using Ultrasound Imaging

### Goal 🎯
The primary objective of this web application is to provide a user-friendly platform for detecting breast cancer using ultrasound imaging. The application aims to assist healthcare professionals in accurately diagnosing breast cancer cases based on ultrasound images.

### Models Employed in the Web App 🧮
The web application integrates the following models for breast cancer detection:

1. **VGG16 Transfer Learning Model**: Utilizes transfer learning from a pre-trained VGG16 model, leveraging its deep architecture to extract high-level features from ultrasound images. Transfer learning helps improve model accuracy and generalization by transferring knowledge from a model trained on a large dataset to a specific task.

2. **Custom Multilayer Perceptron (MLP)**: A custom-designed MLP architecture tailored for breast cancer detection using ultrasound images. MLPs are versatile and effective for image classification tasks, employing multiple layers of neurons for feature learning and classification. The custom design allows for fine-tuning model parameters to suit the specific characteristics of ultrasound images.

3. **ResNet50 Transfer Learning Model**: Incorporates transfer learning from a pre-trained ResNet50 model, renowned for its deep residual learning architecture. ResNet50 can effectively capture intricate features in ultrasound images, thanks to its skip connections and residual blocks, which enable the model to learn from both shallow and deep layers simultaneously.

### Web Application Code Features 🖥️
The provided code snippet showcases the key features of the web application for breast cancer detection using ultrasound images:

- **Flask Framework**: Utilizes Flask, a lightweight and versatile web framework, for building the web application.
- **Model Loading**: Loads the trained breast cancer detection model (`best_breast_cancer_detection_model.h5`) using TensorFlow/Keras for inference.
- **Image Preparation**: Implements a function (`prepare_image`) to preprocess input images, including converting to grayscale, resizing, and scaling to match the model input requirements.
- **Prediction Endpoint**: Defines endpoints (`/predict`) for receiving POST requests with images, processing them through the model, and returning the predicted class (Benign, Malignant, or Normal) to the user interface.
- **User Interface**: Renders an HTML template (`index.html`) for user interaction, allowing users to upload an ultrasound image for prediction and displaying the predicted class.

This code structure enables seamless integration of deep learning models into a user-friendly web interface for breast cancer detection using ultrasound imaging.

### Video Demonstration 🎥

https://github.com/TheNaiveSamosa/ML-CaPsule/assets/112872086/e38a9bd4-fa0f-4e59-b5f6-d346350fd427


### Signature ✒️
Aditya Khamitkar (TheNaiveSamosa)
[![Twitter](https://img.shields.io/badge/Twitter-%40Couch_Potatoh_-blue?style=flat&logo=twitter)](https://twitter.com/Couch_Potatoh_)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Aditya_Khamitkar-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/adityakhamitkar/)
[![Instagram](https://img.shields.io/badge/Instagram-couch_potatoh_-blue?style=flat&logo=instagram)](https://www.instagram.com/couch_potatoh_/)
[![Reddit](https://img.shields.io/badge/Reddit-The_Cactus_Flower-blue?style=flat&logo=reddit)](https://www.reddit.com/user/The-Cactus-Flower/)
