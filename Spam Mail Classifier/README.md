# 📧 Spam Mail Detection using Machine Learning

A machine learning project that classifies emails as **Spam** or **Ham (Not Spam)** using **TF-IDF Vectorization** and **Logistic Regression**. This project demonstrates a complete text classification pipeline, including data preprocessing, feature extraction, model training, evaluation, and prediction.

> Developed as part of the **GirlScript Summer of Code (GSSoC) 2026** initiative.

---

## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Workflow](#project-workflow)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Dataset](#dataset)
- [Model Training](#model-training)
- [Evaluation](#evaluation)
- [Making Predictions](#making-predictions)
- [License](#license)

---

# Overview

Spam emails clutter inboxes, waste time, and may expose users to phishing attacks or malicious content. This project uses Natural Language Processing (NLP) and Machine Learning techniques to automatically classify incoming emails as:

- 📩 **Ham (Legitimate Email)**
- 🚫 **Spam (Unwanted Email)**

The project uses:

- TF-IDF Vectorization for text feature extraction
- Logistic Regression for classification
- Scikit-learn for model building and evaluation

---

# Features

- Email text preprocessing
- Missing value handling
- Label encoding
- TF-IDF feature extraction
- Logistic Regression classifier
- Model evaluation using accuracy
- Predict custom email messages
- Beginner-friendly implementation

---

# Project Workflow

The project follows the following machine learning pipeline:

```
Dataset
    │
    ▼
Data Cleaning
    │
    ▼
Label Encoding
    │
    ▼
Train-Test Split
    │
    ▼
TF-IDF Vectorization
    │
    ▼
Logistic Regression Training
    │
    ▼
Model Evaluation
    │
    ▼
Predict New Email
```

---

# Project Structure

```
Spam-Mail-Detection/
│
├── mail_data.csv
├── spam_mail_detection.py
├── requirements.txt
└── README.md
```

> **Note:** The current project contains a single Python script implementing the complete machine learning pipeline.

---

# Requirements

- Python 3.8+
- NumPy
- Pandas
- Scikit-learn

---

## Installation

1. Clone the ML-CaPsule repository:

```bash
git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
```

2. Navigate to the Spam Mail Detection project folder:

```bash
cd ML-CaPsule/Spam\ Mail\ Detection
```

3. (Optional) Create and activate a virtual environment.

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## How to Run

### Step 1: Ensure the dataset is available

Place the dataset file (`mail_data.csv`) inside the project directory.

The directory should look like:

```
Spam Mail Detection/
│── mail_data.csv
│── spam_mail_detection.py
│── requirements.txt
│── README.md
```

---

### Step 2: Update the dataset path (if required)

If you're running locally instead of Google Colab, replace:

```python
raw_mail_data = pd.read_csv('/content/mail_data.csv')
```

with

```python
raw_mail_data = pd.read_csv("mail_data.csv")
```

---

### Step 3: Run the project

Execute the Python script:

```bash
python spam_mail_detection.py
```

---

### Step 4: Model Workflow

Running the script performs the following operations automatically:

1. Load the email dataset
2. Replace missing values
3. Encode labels
   - Spam → 0
   - Ham → 1
4. Split the dataset into training and testing sets
5. Convert email text into TF-IDF feature vectors
6. Train a Logistic Regression classifier
7. Evaluate model performance on training and testing data
8. Predict whether a custom email is Spam or Ham

---

### Step 5: Predict Your Own Email

Modify the following section in the script:

```python
input_mail = [
    "Your email message here..."
]
```

Run the script again.

Example output:

```
Ham mail
```

or

```
Spam mail
```

The script performs the following steps automatically:

1. Loads the dataset
2. Cleans missing values
3. Encodes labels
4. Splits the dataset
5. Extracts TF-IDF features
6. Trains the Logistic Regression model
7. Evaluates model performance
8. Predicts whether a custom email is Spam or Ham

---

# Dataset

The dataset contains two columns:

| Column | Description |
|---------|-------------|
| Category | Spam or Ham |
| Message | Email text |

Example:

| Category | Message |
|-----------|----------|
| ham | Hey, are we meeting today? |
| spam | Congratulations! You won a free prize. |

---

# Model Training

The model training process consists of:

### 1. Data Loading

The dataset is loaded using Pandas.

### 2. Data Cleaning

- Replace missing values with empty strings.
- Prepare text for feature extraction.

### 3. Label Encoding

```
Spam → 0
Ham → 1
```

### 4. Train-Test Split

The dataset is divided into:

- 80% Training
- 20% Testing

using:

```python
train_test_split(test_size=0.2, random_state=3)
```

### 5. Feature Extraction

Email text is converted into numerical vectors using:

- TF-IDF Vectorizer
- English stop-word removal
- Lowercase conversion

### 6. Model Training

A Logistic Regression classifier is trained using the extracted TF-IDF features.

---

# Evaluation

The trained model is evaluated on both:

- Training Data
- Testing Data

Current evaluation metric:

- Accuracy Score

Example:

```
Training Accuracy:
0.97

Testing Accuracy:
0.96
```

---

# Making Predictions

To classify a new email, simply replace the text inside:

```python
input_mail = [
    "Congratulations! You've won a free vacation."
]
```

Run the script again.

Output:

```
Spam Mail
```

or

```
Ham Mail
```

---


# License

This project is licensed under the MIT License.

See the `LICENSE` file for more information.

---
