# Carnatic Raga Recognition using Hybrid ML/DL

## Overview
This project focuses on identifying Carnatic ragas using Machine Learning and Deep Learning techniques through audio feature analysis.

## Features
- Audio feature extraction
- Random Forest, SVM, KNN models
- Confusion matrix visualization
- Feature importance analysis
- Explainable AI integration (planned)
- Real-time/live audio support (planned)

## Dataset Features
- MFCCs
- Chroma STFT
- Spectral Centroid
- Spectral Bandwidth
- RMSE

## Models Used
- Random Forest
- SVM
- KNN
- Planned: CNN-BiLSTM

## Results
Random Forest achieved the best classification performance among baseline models.

## Future Enhancements
- Live microphone input
- Streamlit deployment
- Explainable AI
- Transformer-based audio modeling

## Tech Stack
Python, Scikit-learn, TensorFlow, Librosa, NumPy, Pandas

## Saved Models
The repository includes serialized trained models:
- Random Forest Classifier
- Label Encoder
- Feature Scaler

These can be directly loaded for inference and deployment.

This project was proposed and developed as part of GSSoC 2026 contributions under the ML-CaPsule repository.