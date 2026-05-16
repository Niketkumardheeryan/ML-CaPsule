# Email Intent Classification using DistilBERT

## Overview

This project implements an Email Intent Classification system using DistilBERT and Natural Language Processing (NLP).

The model classifies emails into multiple intent categories such as:
- Complaint
- Support
- Billing
- Inquiry
- Feedback
- Spam

The project demonstrates transformer-based text classification using HuggingFace Transformers and PyTorch.

---

## Features

- DistilBERT-based NLP classification
- Email preprocessing pipeline
- Train-test split with stratification
- Automated tokenization
- Model evaluation metrics
- Prediction utility for inference
- Modular project structure

---

## Tech Stack

- Python
- PyTorch
- HuggingFace Transformers
- Scikit-learn
- Pandas
- NumPy

---

## Project Structure

```text
Email_Intent_Classification_DistilBERT/
│
├── README.md
├── requirements.txt
├── preprocess.py
├── train.py
├── predict.py
├── config.py
└── sample_dataset.csv
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Run Training

```bash
python train.py
```

---

## Run Prediction

```bash
python predict.py
```

---

## Sample Output

```text
Predicted Intent: support
```

---

## Future Improvements

- Larger dataset integration
- Streamlit deployment
- Multi-language email classification
- Real-time inference API
- Confidence score visualization

---

## Author

Developed as part of GSSOC'26 open source contribution.