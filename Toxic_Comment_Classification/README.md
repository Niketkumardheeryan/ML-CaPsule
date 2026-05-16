# 🚫 Toxic Comment Classification

A Machine Learning project to detect and classify toxic comments using Natural Language Processing (NLP) techniques.

---

## 📌 Problem Statement

Online platforms face the challenge of filtering harmful content. This project builds a **multi-label classifier** that detects 6 types of toxic content in comments automatically.

---

## 🎯 Categories Detected

| Category | Description |
|----------|-------------|
| `toxic` | General toxic content |
| `severe_toxic` | Extremely toxic content |
| `obscene` | Obscene language |
| `threat` | Threatening language |
| `insult` | Insulting content |
| `identity_hate` | Hate based on identity |

---

## 📂 Dataset

- **Source:** [Kaggle - Jigsaw Toxic Comment Classification Challenge](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data)
- **Size:** ~160,000 comments
- **Labels:** Multi-label (a comment can belong to multiple categories)

---

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **Libraries:**
  - `pandas`, `numpy` — Data manipulation
  - `scikit-learn` — ML models & evaluation
  - `nltk` — Text preprocessing
  - `matplotlib`, `seaborn` — Visualization
  - `wordcloud` — Word cloud generation

---

## 🔄 Project Workflow

```
Data Loading → EDA → Text Preprocessing → 
Train-Test Split → TF-IDF Vectorization → 
Model Training → Evaluation → Prediction
```

---

## 📊 Model Used

- **TF-IDF Vectorizer** (bigrams, 50k features)
- **Logistic Regression** with `OneVsRestClassifier` for multi-label classification

---

## 📈 Results

| Label | Accuracy |
|-------|----------|
| Toxic | ~95% |
| Severe Toxic | ~99% |
| Obscene | ~97% |
| Threat | ~99% |
| Insult | ~96% |
| Identity Hate | ~99% |

---

## 🚀 How to Run

1. Clone the repository:
```bash
git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
cd ML-CaPsule/Toxic_Comment_Classification
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download dataset from [Kaggle](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data) and place `train.csv` in this folder.

4. Open the notebook:
```bash
jupyter notebook toxic_comment_classification.ipynb
```

---

## 📁 Folder Structure

```
Toxic_Comment_Classification/
├── toxic_comment_classification.ipynb  ← Main notebook
├── requirements.txt                    ← Dependencies
└── README.md                           ← Project documentation
```

---

## 🔮 Future Improvements

- Use **BERT / RoBERTa** for better accuracy
- Build a **Streamlit web app** for live predictions
- Handle **class imbalance** with SMOTE or class weights
- Deploy as a **REST API**

---

## 👨‍💻 Author

Contributed as part of **GSSoC (GirlScript Summer of Code)**

---

## 📄 License

This project is licensed under the MIT License.
