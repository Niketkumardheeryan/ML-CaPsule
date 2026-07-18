# 🛡️ Spam Mail Detection

A machine learning project that classifies SMS messages as **Spam** or **Ham (Not Spam)** using Natural Language Processing and multiple ML classifiers — now with an interactive **Streamlit web interface**.

---

## 📌 Project Overview

SMS spam is unsolicited bulk messaging sent to mobile phones. This project trains several ML classifiers on the [SMS Spam Collection Dataset](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset) and wraps the best model in a browser-based UI so anyone can test predictions without writing code.

| Metric | Value |
|--------|-------|
| Dataset size | 5,572 SMS messages |
| Spam ratio | ~13% spam, ~87% ham |
| Best accuracy | ~97–98% (SVC / Random Forest) |
| Deployed model | Multinomial Naïve Bayes + TF-IDF Pipeline |

---

## 🗂️ Folder Structure

```
spam detection/
├── dataset/
│   └── dataset.zip            ← Raw SMS Spam Collection CSV
├── model/
│   ├── readme.md
│   ├── save_model.py          ← Script to train & save the model
│   ├── spam_mail_detection.ipynb  ← Original notebook with EDA + 11 models
│   └── spam_model.pkl         ← Saved model (generated after running save_model.py)
├── app.py                     ← Streamlit web application ⭐
└── requirements.txt           ← All Python dependencies
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/ML-CaPsule.git
cd "ML-CaPsule/spam detection"
```

### 2. Create a virtual environment (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Prepare the dataset
Unzip `dataset/dataset.zip` so that `dataset/spam.csv` exists.

### 5. Train and save the model
```bash
python model/save_model.py
```
This creates `model/spam_model.pkl`.

### 6. Run the Streamlit app
```bash
streamlit run app.py
```
Open your browser at **http://localhost:8501** 🎉

---

## 🖥️ Web Interface Features

- **SMS input** — type or paste any message
- **Quick-fill sample buttons** — test with pre-loaded spam/ham examples  
- **Instant prediction** — Spam 🚫 or Not Spam ✅
- **Confidence scores** — probability breakdown for each class
- **Model stats** — algorithm, vectorizer, accuracy, training size

---

## 🤖 Models Explored (Notebook)

| Model | Accuracy |
|-------|----------|
| Logistic Regression | 96.19% |
| K-Nearest Neighbours | 90.16% |
| Support Vector Classifier | **97.84%** |
| Naïve Bayes (Bernoulli) | 96.69% |
| Decision Tree | 94.90% |
| **Random Forest** | **97.63%** |
| AdaBoost | 97.55% |
| Gradient Boosting | 97.70% |
| XGBoost | 97.70% |
| Extra Trees | 97.27% |
| Bagging Classifier | 96.26% |

---

## 🧹 Preprocessing Pipeline

1. Lowercase the text  
2. Remove punctuation  
3. Remove English stop words (NLTK)  
4. `CountVectorizer` — bag-of-words representation  
5. `TfidfTransformer` — TF-IDF weighting  
6. `MultinomialNB` — final classifier  

---

## 🧪 Sample Test Messages

| Message | Expected |
|---------|----------|
| "Congratulations! You've won a £1,000 gift card. Click now!" | 🚫 Spam |
| "Hey, are we still meeting at 6pm today?" | ✅ Ham |
| "URGENT: Your account is suspended. Verify immediately." | 🚫 Spam |
| "Can you pick up milk on your way home?" | ✅ Ham |

---

## 📦 Dependencies

See [`requirements.txt`](requirements.txt).  
Key packages: `streamlit`, `scikit-learn`, `nltk`, `pandas`, `numpy`.

---

## 🤝 Contributing

This project is part of [ML-CaPsule](https://github.com/Girlscript/ML-CaPsule) under **GirlScript Summer of Code (GSSoC)**.  
Contributions, issues, and feature requests are welcome!

---

## 📄 License

This project is open-source under the [MIT License](../../LICENSE).
