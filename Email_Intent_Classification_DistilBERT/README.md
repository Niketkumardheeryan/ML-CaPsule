# 📧 Email Intent Classification using DistilBERT

A transformer-based NLP pipeline that classifies emails into 7 intent categories using a fine-tuned DistilBERT model — achieving semantic understanding beyond traditional keyword-based filtering.

---

## 📌 Problem Statement

Most email filtering systems rely on keyword matching and rule-based approaches that fail to capture the actual **intent** behind an email. This project uses contextual language understanding via DistilBERT to accurately classify emails into meaningful intent categories in real time.

---

## 🎯 Intent Categories

| Label | Description |
|-------|-------------|
| `meeting` | Meeting requests, calls, sync-ups, reviews |
| `deadline` | Submission reminders, due dates, urgent tasks |
| `support` | Technical issues, login problems, system failures |
| `finance` | Payments, invoices, billing, transactions |
| `promotion` | Marketing emails, discounts, offers |
| `personal` | Informal or personal communication |
| `spam` | Suspicious or phishing-like emails |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Model | DistilBERT (`distilbert-base-uncased`) |
| Framework | PyTorch |
| NLP Library | HuggingFace Transformers |
| Data Processing | Pandas, NumPy, Scikit-learn |
| Visualization | Matplotlib, Seaborn |
| Language | Python 3.10+ |

---

## 📁 Folder Structure

```
Email_Intent_Classification_DistilBERT/
├── Email_Intent_Classification_DistilBERT.ipynb   ← Main notebook
├── README.md                                       ← This file
├── requirements.txt                                ← Dependencies
└── data/
    └── emails.csv                                  ← Dataset (text, label)
```

---

## 📊 Dataset

- **Format:** CSV with two columns — `text` (email body) and `label` (intent category)
- **Classes:** 7 balanced intent categories
- **Preprocessing:** Label encoding, stratified train/test split (80/20), DistilBERT tokenization with `max_length=128`

---

## 🚀 How to Run

### 1. Clone ML-CaPsule and navigate to the folder
```bash
git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
cd ML-CaPsule/Email_Intent_Classification_DistilBERT
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Open the notebook
```bash
jupyter notebook Email_Intent_Classification_DistilBERT.ipynb
```

### 4. Run all cells in order
The notebook is fully self-contained — just run top to bottom.

---

## 📈 Results

- **Training:** Loss decreased consistently across 5 epochs indicating stable convergence
- **Inference:** Sub-300ms latency per email on CPU
- **Reliability:** Significantly improved after dataset balancing across all 7 classes

### Example Predictions

| Email | Predicted Intent | Confidence |
|-------|-----------------|------------|
| "Please submit the assignment before tonight." | `deadline` | High |
| "The app crashes every time I login." | `support` | High |
| "Can we schedule a sync tomorrow at 3 PM?" | `meeting` | High |
| "Your invoice #1042 is due." | `finance` | High |
| "Claim your 50% cashback rewards!" | `promotion` | High |
| "Hey! Hope you're doing well." | `personal` | High |
| "You've been selected as a winner. Click here." | `spam` | High |

---

## 🔑 Key Concepts Covered

- Transformer-based text classification
- HuggingFace `DistilBertForSequenceClassification`
- Custom PyTorch `Dataset` and `DataLoader`
- Fine-tuning pretrained language models
- Multi-class classification evaluation (accuracy, F1, confusion matrix)
- Confidence score visualization
- Model saving and loading with `save_pretrained()`

---

## 💡 Why DistilBERT?

- **40% smaller** and **60% faster** than BERT
- Retains **97% of BERT's performance**
- Ideal for CPU deployment in real-world applications
- Understands semantic context — not just keywords

---

## 🚀 Future Improvements

- Gmail API integration for live inbox classification
- Top-k intent predictions with uncertainty scores
- Email summarization alongside intent detection
- Cloud deployment (AWS Lambda / Google Cloud Run)
- Experiment with RoBERTa for higher accuracy

---

## 🔗 Full Application

The complete IntelliMail app (FastAPI + Streamlit + SQLite) is available here:  
👉 [github.com/Sanvi09Kulkarni/IntelliMail](https://github.com/Sanvi09Kulkarni/IntelliMail)

---

## 👩‍💻 Author

**Sanvi Kulkarni**  
Integrated MTech — Computer Science (Data Science), VIT Bhopal  
GitHub: [@Sanvi09Kulkarni](https://github.com/Sanvi09Kulkarni)

---

*Contributed to [ML-CaPsule](https://github.com/Niketkumardheeryan/ML-CaPsule) as part of GSSoC '25*
