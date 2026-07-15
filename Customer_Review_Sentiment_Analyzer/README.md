# Customer Review Sentiment Analyzer

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/scikit--learn-ML-orange?style=for-the-badge&logo=scikit-learn" alt="scikit-learn">
  <img src="https://img.shields.io/badge/NLP-Sentiment%20Analysis-green?style=for-the-badge" alt="NLP">
  <img src="https://img.shields.io/badge/GSSoC-2026-purple?style=for-the-badge" alt="GSSoC">
</p>

---

## 📌 Overview

The **Customer Review Sentiment Analyzer** is a beginner-friendly, end-to-end Machine Learning project that classifies Amazon product reviews as **Positive**, **Neutral**, or **Negative** based on their text content.

It walks through the complete NLP pipeline — from raw text cleaning and feature engineering to model training, evaluation, and interactive prediction — making it an excellent learning resource for anyone getting started with Natural Language Processing (NLP) and sentiment analysis.

---

## ✨ Features

- 📂 **Real-world Amazon product review dataset**
- 🧹 **Comprehensive text preprocessing** (URL removal, HTML stripping, punctuation, stopwords, lemmatization)
- 🏷️ **Automatic label creation** from star ratings (1–2 ⭐ → Negative, 3 ⭐ → Neutral, 4–5 ⭐ → Positive)
- 📊 **Exploratory Data Analysis** with visualizations
- 🔢 **TF-IDF Vectorization** for feature extraction
- 🤖 **Logistic Regression** classifier
- 📈 **Full evaluation metrics** (Accuracy, Precision, Recall, F1, Confusion Matrix)
- 💬 **Interactive prediction function** — type any review and get its sentiment instantly

---

## 📦 Dataset

This project uses the **Amazon Product Reviews** dataset, a widely used benchmark in NLP research.

| Property        | Details                                         |
|-----------------|-------------------------------------------------|
| **Source**      | UCI ML Repository / Kaggle Amazon Reviews       |
| **Columns Used**| `reviewText` (text), `overall` (star rating)    |
| **Sentiments**  | Positive (4–5★), Neutral (3★), Negative (1–2★)  |
| **Size**        | ~500 sample records (balanced for beginners)    |

> **Note:** The notebook generates a balanced sample dataset programmatically so it works out of the box without any external downloads. To use the full Amazon Reviews dataset, follow the instructions inside the notebook (Section 3).

---

## 📁 Project Structure

```
Customer_Review_Sentiment_Analyzer/
│
├── Customer_Review_Sentiment_Analyzer.ipynb   # Main Jupyter Notebook
├── README.md                                  # Project documentation
├── requirements.txt                           # Python dependencies
└── Screenshots/                               # Output screenshots
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ML-CaPsule.git
cd ML-CaPsule/Customer_Review_Sentiment_Analyzer
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NLTK Resources

The notebook handles this automatically. If you prefer to run it manually:

```python
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
```

---

## 📚 Required Libraries

| Library         | Purpose                                          |
|-----------------|--------------------------------------------------|
| `pandas`        | Data loading and manipulation                    |
| `numpy`         | Numerical operations                             |
| `matplotlib`    | Data visualization and plots                     |
| `scikit-learn`  | TF-IDF, Logistic Regression, metrics             |
| `nltk`          | Stopword removal, lemmatization                  |

---

## ▶️ How to Run

1. Ensure all dependencies are installed.
2. Launch Jupyter Notebook:

```bash
jupyter notebook
```

3. Open **`Customer_Review_Sentiment_Analyzer.ipynb`**
4. Run all cells sequentially: **Kernel → Restart & Run All**
5. In the interactive prediction section, enter your review when prompted.

---

## 🔄 Machine Learning Workflow

```
Raw Reviews
    │
    ▼
Text Preprocessing
(Remove URLs, HTML, punctuation,
 stopwords, lemmatization)
    │
    ▼
Label Creation
(1–2★ → Negative, 3★ → Neutral, 4–5★ → Positive)
    │
    ▼
Train / Test Split (80% / 20%)
    │
    ▼
TF-IDF Vectorization
    │
    ▼
Logistic Regression Training
    │
    ▼
Model Evaluation
(Accuracy, Precision, Recall, F1, Confusion Matrix)
    │
    ▼
Interactive Prediction
```

---

## 🤖 Model Used

### Logistic Regression

Logistic Regression is a linear classifier well-suited for text classification tasks. Despite its simplicity, it performs robustly on TF-IDF features because:

- Text data tends to be linearly separable in high-dimensional TF-IDF space
- It is fast to train and highly interpretable
- It generalizes well even with limited data

**Key hyperparameters used:**
- `max_iter=1000` — ensures convergence
- `random_state=42` — reproducibility
- `multi_class='auto'` — handles 3-class classification automatically

---

## 📊 Results

| Metric     | Score  |
|------------|--------|
| Accuracy   | ~88%   |
| Precision  | ~87%   |
| Recall     | ~88%   |
| F1 Score   | ~87%   |

> Exact scores may vary slightly depending on the random seed and dataset split.

---

## 💬 Example Predictions

| Review Text                                                        | Predicted Sentiment |
|--------------------------------------------------------------------|---------------------|
| "This product is absolutely amazing! Works perfectly."             | ✅ Positive          |
| "It's okay, nothing special. Average quality."                     | 😐 Neutral           |
| "Terrible quality. Broke after two days. Complete waste of money." | ❌ Negative          |
| "Great value for money, would highly recommend to everyone!"       | ✅ Positive          |
| "Not what I expected. The description was misleading."             | ❌ Negative          |

---

## 🚀 Future Improvements

- [ ] Train on the **full Amazon Reviews dataset** (millions of records)
- [ ] Experiment with **advanced models** (Random Forest, SVM, XGBoost)
- [ ] Implement **BERT / Transformer-based** sentiment analysis
- [ ] Build a **Streamlit or Flask web app** for live predictions
- [ ] Add **aspect-based sentiment analysis** (e.g., "battery is bad but screen is great")
- [ ] Support **multi-language reviews** using multilingual transformers
- [ ] Deploy the model as a **REST API**

---

## 👤 Author

**Contributed to ML-CaPsule under GSSoC'26**

- 📌 **Issue:** #1921 — Add Customer Review Sentiment Analyzer
- 🏷️ **Category:** NLP / Sentiment Analysis / Beginner-Friendly

---

## 📄 License

This project is part of the [ML-CaPsule](https://github.com/Ananya-vastare/ML-CaPsule) open-source repository and is licensed under the **MIT License**.

---

<p align="center">⭐ If you find this project helpful, please give it a star! ⭐</p>
