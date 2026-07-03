

# 💳 Anomaly Detection in Financial Transactions using Deep Learning

## 📌 Overview

Financial fraud has become one of the biggest challenges in digital banking and online payment systems. This project focuses on detecting fraudulent transactions using Deep Learning models. Three different neural network architectures—Multi-Layer Perceptron (MLP), Recurrent Neural Network (RNN), and Convolutional Neural Network (CNN)—are implemented, trained, and compared to identify anomalous financial transactions.

The project demonstrates the complete machine learning workflow, including data generation, preprocessing, exploratory data analysis (EDA), model development, evaluation, and performance comparison.

---

## 🎯 Project Objectives

- Generate a synthetic financial transaction dataset.
- Perform Exploratory Data Analysis (EDA) to understand transaction behavior.
- Build and train three Deep Learning models:
  - Multi-Layer Perceptron (MLP)
  - Recurrent Neural Network (RNN - LSTM)
  - Convolutional Neural Network (CNN - 1D)
- Detect fraudulent transactions accurately.
- Compare the performance of all models.

---

## 📂 Dataset

The project uses a synthetic dataset named **`transactions.csv`** containing transaction details.

### Features

| Feature | Description |
|----------|-------------|
| Transaction Amount | Amount involved in the transaction |
| Transaction Type | Type of transaction (Transfer, Payment, Cash Out, etc.) |
| Account Age | Age of the customer's account |
| Transaction Location | Location where the transaction occurred |
| Fraud Label | Binary target variable (0 = Genuine, 1 = Fraudulent) |

---

## 📊 Exploratory Data Analysis (EDA)

The following analyses were performed:

- Dataset overview
- Missing value analysis
- Summary statistics
- Distribution of transaction amounts
- Transaction type distribution
- Account age distribution
- Transaction location analysis
- Fraud vs Non-Fraud transaction visualization
- Correlation heatmap
- Feature relationship analysis

---

## 🧠 Deep Learning Models

### 1. Multi-Layer Perceptron (MLP)

A fully connected feed-forward neural network used as the baseline model for fraud detection.

**Architecture**
- Input Layer
- Dense Layer (ReLU)
- Dropout Layer
- Dense Layer (ReLU)
- Output Layer (Sigmoid)

---

### 2. Recurrent Neural Network (RNN)

An LSTM-based model capable of learning sequential dependencies within transaction data.

**Architecture**
- Input Layer
- LSTM Layer
- Dropout Layer
- Dense Layer
- Output Layer

---

### 3. Convolutional Neural Network (CNN)

A 1D Convolutional Neural Network designed to extract local feature patterns from transaction sequences.

**Architecture**
- Conv1D Layer
- MaxPooling Layer
- Flatten Layer
- Dense Layer
- Output Layer

---

## ⚙️ Technologies Used

- Python
- TensorFlow / Keras
- NumPy
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn

---

## 📦 Required Libraries

Install all dependencies using:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn tensorflow
```

---

## 📁 Project Structure

```
Anomaly-Detection/
│
├── transactions.csv
├── anomaly_detection.ipynb
├── README.md
├── models/
│   ├── mlp_model.h5
│   ├── rnn_model.h5
│   └── cnn_model.h5
│
├── images/
│   ├── fraud_distribution.png
│   ├── correlation_heatmap.png
│   └── transaction_distribution.png
│
└── requirements.txt
```

---

## 🚀 How to Run

### Clone the repository

```bash
git clone https://github.com/your-username/Anomaly-Detection.git
```

### Navigate to the project

```bash
cd Anomaly-Detection
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Launch Jupyter Notebook

```bash
jupyter notebook
```

Open:

```
anomaly_detection.ipynb
```

Run all cells.

---

## 📈 Model Evaluation

The models are evaluated using standard classification metrics:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

Performance comparison is carried out to determine which architecture performs best for fraud detection.

---

## 📊 Workflow

```
Synthetic Dataset
        │
        ▼
Data Cleaning
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Feature Preprocessing
        │
        ▼
Train-Test Split
        │
        ▼
─────────────────────────────────
│       MLP Model               │
│       RNN Model               │
│       CNN Model               │
─────────────────────────────────
        │
        ▼
Model Evaluation
        │
        ▼
Performance Comparison
```

---

## 💡 Key Learning Outcomes

- Data preprocessing for financial transaction datasets
- Exploratory Data Analysis (EDA)
- Building Deep Learning models using TensorFlow/Keras
- Fraud detection using neural networks
- Performance comparison of different architectures
- Binary classification using Deep Learning

---

## 🔮 Future Improvements

- Use real-world financial transaction datasets.
- Address class imbalance using SMOTE or class weighting.
- Implement Autoencoders for unsupervised anomaly detection.
- Experiment with Transformer-based architectures.
- Deploy the best-performing model using Flask, FastAPI, or Streamlit.
- Enable real-time fraud detection via REST APIs.

---

## 👩‍💻 Author

**Nitika Singh**

AI & Machine Learning Undergraduate

- Python
- Deep Learning
- Machine Learning
- Data Analytics
- TensorFlow
- Scikit-learn

---

## 📄 License

This project is intended for educational and research purposes.
