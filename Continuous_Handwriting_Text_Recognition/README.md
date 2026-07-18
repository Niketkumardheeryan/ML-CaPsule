# Continuous Handwriting Text Recognition Pipeline

## Overview

The goal of this project is to read handwritten text from images as accurately as possible. This is a combined Deep Learning and Natural Language Processing (NLP) task. We use a smart neural network model to read the handwriting from the image, and then use NLP (language rules and spelling tools) to clean up the text so it forms a readable, grammatically correct English sentence.

The deep learning model was trained on Teklia/IAM-line dataset.

Dataset link : https://huggingface.co/datasets/Teklia/IAM-line

## Models

The project uses bidirectional Convolutional Recurrent Neural Network (bi-CRNN) to process the sequential text in the image. It uses a visual part (CNN) to look at the image, and a text part (RNN) to read the letters in order. To find the best results, we trained and tested two different types of text-reading networks:

- BiLSTM (Bidirectional Long Short-Term Memory): Excellent at remembering the context of a sentence over long distances.

- BiGRU (Bidirectional Gated Recurrent Unit): A faster, lighter model that uses fewer computer resources.

To make sure the models didn't just memorize the training data (overfitting), we used protective training techniques like Dropout and Early Stopping.

The Character Error Rate and Word Error Rate of the bi-LSTM model are 8.71% and 29.88% respectively.

The Character Error rate and Word Error Rate of the bi-GRU model are 8.61% and 30.41% respectively.

## Working

- Image Input: You give the pipeline an image containing a handwritten line of text.
- Image Cleanup (Preprocessing): The code cleans up the image. It flips the colors so the text is white on a black background, brightens it, and sharpens the edges. This makes the letters stand out clearly for the models.
- Prediction: Both the BiLSTM and BiGRU models look at the cleaned image and make their best guesses as to what letters are written there.
- Combining the Best Guesses (Ensembling): The code dynamically aligns the outputs of both models and merges them, canceling out random mistakes made by just one network.
- Language Cleanup (NLP): The text from the AI might still have mashed-together words or small spelling mistakes (like reading tomnmander instead of commander). This is where our NLP steps in:

1. Predictive Word Splitting: It automatically adds spaces to separate squished words (like changing thefrwers into the frwers).

2. Word Recombination & Correction (Grid-Scan Recombination): It automatically looks at broken pieces of words, scans a dictionary, and glues them back together into the correct words (like fixing the frwers into the flowers).

## Outputs
<img width="1134" height="388" alt="image" src="https://github.com/user-attachments/assets/bfe2334a-0179-4ad8-8330-ea385f14a7f5" />

Here, the models process the given image containing the sentence: The commander is a nice person.

As is visible, the models produce nearby but illegible text. NLP is then used to produce the most meaningful sentence out of those predictions.
