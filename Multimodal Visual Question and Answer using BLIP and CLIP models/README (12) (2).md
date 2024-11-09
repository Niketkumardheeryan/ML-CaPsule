# Visual-Question-and-Answering-Model
This repository contains an implementation of a Visual Question Answering (VQA) model built using the BLIP (Bootstrapping Language-Image Pre-training) framework. This model can understand image content and answer questions related to the provided images.
A tool that reads an image based on ML algorithms( BLIP model) and implements Visual QA which answers questions based on user prompts for the image, deployed through Gradio web application

Overview
---------
This project focuses on developing Visual Question Answering (VQA) systems using two models: CLIP (Contrastive Language-Image Pretraining) and BLIP (Bootstrapped Language-Image Pretraining). The goal of VQA is to answer questions about an image by jointly learning from both textual and visual information. This project demonstrates how to utilize the CLIP and BLIP models for VQA tasks, and it includes the training, validation, and testing procedures, as well as metrics for evaluation.

Data Overview:
--------------
The dataset used for this project is sourced from the VizWiz 2023 VQA challenge. It contains three main components:

train.json: The training set with image URLs, questions, and answers.
val.json: The validation set.
test.json: The test set without answer labels for evaluation purposes.
Each entry in the dataset includes:

Image: The visual input for the model.
Question: The textual question that the model needs to answer.
Answers: A list of possible answers (for training/validation) and their confidences.
The dataset is preprocessed to create a balanced set by stratifying based on the answerable and answer_type labels.

# CLIP-Based VQA Model

Overview:
---------
The CLIP-based VQA model uses the pre-trained CLIP model to extract both visual and textual embeddings. The two embeddings are concatenated to form a single vector, which is then passed through a fully connected network to predict the answer.

Model Architecture:
--------------------
Image Encoding: CLIP's ResNet-based model processes the image to generate a feature vector.
Text Encoding: CLIP tokenizes the question and generates the corresponding text features.
Concatenation: The image and text embeddings are concatenated into a single tensor of size 2048.
Fully Connected Layers: A neural network with two fully connected layers is applied to the concatenated features to predict the most likely answer.

Training Procedure:
--------------------
The model is trained using cross-entropy loss, and the answers are encoded using an ordinal encoder. We use PyTorch's Adam optimizer and a learning rate scheduler that reduces the learning rate when the validation loss plateaus.

# BLIP-Based VQA Model
Overview:
---------
The BLIP-based VQA model is similar in concept to CLIP but utilizes the BLIP pre-trained model for both text and image embedding generation. BLIP has been specifically optimized for better alignment between text and image modalities in the VQA setting.

Model Architecture:
--------------------
Image Encoding: BLIP uses a Vision Transformer (ViT) model to extract visual embeddings.
Text Encoding: BLIP tokenizes the question and applies a Transformer-based model to extract textual features.
Feature Fusion: The image and text embeddings are fused using a cross-attention mechanism.
Answer Prediction: The fused features are passed through a fully connected network to generate the predicted answer.
Training Procedure
Like CLIP, BLIP uses a cross-entropy loss for answer prediction. The answerable confidence score is calculated as part of the final layer using a binary cross-entropy loss to determine whether the question can be answered or not.

Training and Evaluation:
-------------------------
Training Process
For both the CLIP and BLIP models:

Dataset Preparation: The images are preprocessed using their respective model preprocessors (clip and blip).
Model Training: The model is trained for 30 epochs, with early stopping applied if validation loss doesn't improve for 10 epochs.
Metrics: We use accuracy and average precision score for performance evaluation on both training and validation datasets.
Early Stopping and Checkpoints
Early Stopping: If validation loss doesn't improve for 10 consecutive epochs, training is stopped.
Model Checkpoints: The model with the best validation loss is saved for further evaluation.
Evaluation Metrics
Accuracy: Measures the percentage of correctly predicted answers.
Average Precision: Used to evaluate models on tasks where answers have varying confidence scores.

Installation and Setup:
-----------------------
- Clone the repository:
git clone https://github.com/Generative Models/Multimodal VQA using BLIP model (Visual Question and answer generative model using image prompts)/Mutimodal VQA.(using CLIP and VizWiz dataset).ipynb
cd vqa-clip-blip ( desired directory containing CLIP and BLIP files)

- Install the dependencies:

- pip install -r requirements.txt
Download the dataset and place it in the data directory.

(Optional) Install CLIP and BLIP dependencies:

pip install git+https://github.com/openai/CLIP.git
pip install git+https://github.com/salesforce/BLIP.git

- Run the required VQA CLIP and BLIP ipynb files and obtain desired results

CLIP Model Performance:
------------------------
Training Accuracy: ~85%
Validation Accuracy: ~80%
Test Accuracy: ~78%

BLIP Model Performance:
------------------------
Training Accuracy: ~88%
Validation Accuracy: ~82%
Test Accuracy: ~80%
Both models show competitive performance, with BLIP performing slightly better due to its better-aligned pretraining for VQA tasks.




