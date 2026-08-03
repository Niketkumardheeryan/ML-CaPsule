<img height="27" src="https://img.shields.io/badge/Audio_Deepfake_Detection-Advanced-darkred.svg?&style=for-the-badge&logo=tensorflow&logoColor=white"/>
<br>

![](https://img.shields.io/badge/Language-Python-blue.svg)
![](https://img.shields.io/badge/Framework-TensorFlow-orange.svg)
![](https://img.shields.io/badge/Status-Complete-brightgreen.svg)
![](https://img.shields.io/badge/Dataset-ASVspoof_2019-lightgrey.svg)

# Audio Deepfake Detection

## Why This Matters
Voice cloning and AI-generated speech are being weaponized for fraud, impersonation, and misinformation. Most deepfake detection work focuses on images and video audio is often overlooked. This project tackles that gap directly.

## What It Does
Classifies audio clips as **real (bonafide)** or **AI-generated (spoof)** using MFCC-based feature extraction and an LSTM deep learning model trained on the ASVspoof 2019 dataset.

## Pipeline
Raw Audio (.flac)
↓
MFCC Extraction (40 coefficients × 200 timesteps)
↓
LSTM Model (128 → 64 un

## Results

| Class | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| Bonafide | 0.85 | 0.92 | 0.88 |
| Spoof | 0.91 | 0.84 | 0.88 |

**Overall Accuracy: 88%**

## Tech Stack
- TensorFlow / Keras — model training
- librosa — audio feature extraction
- scikit-learn — evaluation metrics
- ASVspoof 2019 LA — dataset

## Run It
1. Download dataset from [Kaggle](https://www.kaggle.com/datasets/anishsarkar22/asvpoof-2019-dataset-la)
2. Open `Audio_Deepfake_Detection.ipynb` in Google Colab
3. Run all cells

[<img height="30" src="https://img.shields.io/badge/linkedin-blue.svg?&style=for-the-badge&logo=linkedin&logoColor=white" />][LinkedIn]
[<img height="30" src="https://img.shields.io/badge/github-black.svg?&style=for-the-badge&logo=github&logoColor=white" />][Github]

[linkedin]: https://www.linkedin.com/in/siddharthmac/
[github]: https://github.com/SiddharthRiot/