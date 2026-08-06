# 📱 Scam SMS Detector using Machine Learning & NLP

An intelligent, machine-learning-powered web application that detects scam, phishing, and fraudulent SMS text messages in real time using Natural Language Processing (NLP) and Scikit-Learn.

---

## 🎯 Project Overview

SMS phishing (Smishing) and fraud messages are a major cybersecurity threat targeting millions of mobile users daily. This project provides an accessible, AI-backed security filter that inspects text messages for:
- 🚨 Urgent high-pressure language
- 🔗 Malicious domain links and URL shorteners
- 💸 Fake monetary rewards, lotteries, or gift card incentives
- 🔐 Unauthorized bank/account lock baiting

---

## ✨ Features

- **High Accuracy Classification**: Classifies SMS into **Scam / Spam** or **Safe / Legitimate**.
- **NLP Text Normalization**: Tokenizes URLs, phone numbers, and currency symbols for robust text analysis.
- **Explainable Trigger Detection**: Identifies specific threat factors present in suspicious messages.
- **Interactive Web Interface**: Modern glassmorphic web UI powered by Flask, HTML5, CSS3, and JavaScript.
- **Preset Test Samples**: Quick one-click testing chips for instant demonstration.

---

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **Machine Learning & NLP**: Scikit-learn, Pandas, NumPy, Joblib
- **Web Framework**: Flask
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphic Design), JavaScript (ES6 AJAX)

---

## 📁 Directory Structure

```text
Scam_SMS_Detector/
├── data/
│   └── sms_spam_collection.csv    # Labeled SMS dataset (Ham vs Spam)
├── models/
│   ├── model.pkl                  # Serialized trained classifier
│   └── vectorizer.pkl             # Serialized TF-IDF vectorizer
├── static/
│   ├── css/
│   │   └── style.css              # Glassmorphic UI stylesheet
│   └── js/
│       └── main.js                # Frontend AJAX & DOM interactions
├── templates/
│   └── index.html                 # Flask Jinja2 HTML layout
├── app.py                         # Flask web application & API endpoints
├── generate_dataset.py            # Dataset creation utility script
├── train_model.py                 # ML training & evaluation script
├── requirements.txt               # Project dependencies
└── README.md                      # Project documentation
```

---

## 📊 Model Architecture & Performance

The training pipeline evaluates multiple classification algorithms using **Term Frequency - Inverse Document Frequency (TF-IDF)** with unigram and bigram feature extraction:

| Model Candidate | Accuracy | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| **Multinomial Naive Bayes** | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| **Logistic Regression** | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| **Random Forest** | 0.9565 | 1.0000 | 0.9091 | 0.9524 |

*Multinomial Naive Bayes was selected as the primary production model due to fast inference time and top performance on textual dataset characteristics.*

---

## 🚀 Getting Started

### 1. Navigate to Project Directory
```bash
cd Scam_SMS_Detector
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Dataset & Train Model
```bash
python generate_dataset.py
python train_model.py
```
*This outputs `model.pkl` and `vectorizer.pkl` into the `models/` folder.*

### 4. Run Flask Web Application
```bash
python app.py
```

Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🔌 API Endpoint Specifications

### `POST /predict`

Accepts JSON payload or Form data containing an SMS message text.

#### **Request Body (JSON)**:
```json
{
  "message": "URGENT! Your bank account #9281 has been locked. Verify immediately at http://bit.ly/bank-verify-sec"
}
```

#### **Response Body (JSON)**:
```json
{
  "status": "success",
  "is_scam": true,
  "prediction": "SCAM",
  "confidence_score": 100.0,
  "risk_level": "High Scam Risk",
  "risk_badge": "critical",
  "triggers": [
    {
      "type": "Suspicious Link",
      "desc": "Contains an external link or shortened domain URL."
    },
    {
      "type": "Urgent Language",
      "desc": "Uses high-pressure words: urgent, immediately, locked."
    }
  ],
  "original_message": "URGENT! Your bank account #9281 has been locked. Verify immediately at http://bit.ly/bank-verify-sec"
}
```

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to check out the rest of the repository at [ML-CaPsule](https://github.com/Niketkumardheeryan/ML-CaPsule).
