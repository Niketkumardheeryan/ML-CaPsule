# 📄 AI Resume Analyzer

## 🚀 Overview

AI Resume Analyzer is an advanced AI-powered web application built using **Python, Streamlit, NLP, and Gemini AI**.

The application analyzes uploaded resumes, detects technical skills, calculates ATS scores, extracts important entities using NLP, and provides intelligent AI-generated resume improvement suggestions.

---

# ✨ Features

- 📂 Resume PDF Upload
- 🧠 AI-Powered Resume Analysis
- 📊 ATS Resume Score Calculation
- ✅ Skill Detection System
- ❌ Missing Skill Analysis
- 🤖 Gemini AI Resume Feedback
- 📌 NLP Entity Extraction
- 📈 Interactive Skill Analytics
- 💡 Resume Improvement Suggestions
- 🎯 Role-Based Skill Matching

---

# 🛠️ Technologies Used

- Python
- Streamlit
- spaCy NLP
- Google Gemini AI
- pdfplumber
- Matplotlib
- python-dotenv

---

# 📁 Project Structure

```bash
AI_Resume_Analyzer/
│
├── app.py
├── skills.py
├── nlp_utils.py
├── ai_suggestions.py
├── requirements.txt
├── README.md
├── .env
└── sample_resume.pdf
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Anant-06/ML-CaPsule.git
```

---

## 2️⃣ Navigate to Project Folder

```bash
cd ML-CaPsule/AI_Resume_Analyzer
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Install spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

---

## 5️⃣ Create `.env` File

Create a `.env` file inside the project folder and add:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

# 🔑 Generate Gemini API Key

Generate your API key from:

https://aistudio.google.com/app/apikey

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# 📊 Project Workflow

```text
Upload Resume
      ↓
PDF Text Extraction
      ↓
NLP Entity Extraction
      ↓
Skill Detection
      ↓
ATS Score Calculation
      ↓
Gemini AI Suggestions
      ↓
Analytics & Feedback
```

---

# 🤖 AI Features

The project uses **Google Gemini AI** to generate:

- Resume improvement suggestions
- ATS optimization tips
- Missing skill recommendations
- Career guidance
- Project recommendations

---

# 🧩 NLP Features

Using **spaCy Named Entity Recognition (NER)**:

- PERSON detection
- ORGANIZATION detection
- DATE extraction
- LOCATION extraction

---

# 📈 Future Improvements

- Resume Ranking System
- OCR-Based Resume Parsing
- Multi Resume Comparison
- Downloadable PDF Reports
- Authentication System
- Admin Dashboard
- Semantic Skill Matching
- Vector Embeddings

---

# 🖼️ Screenshots

_Add screenshots of the application here._

---

# 👨‍💻 Author

**Anant Gangwar**

GitHub:
https://github.com/Anant-06

---

# 🌟 Contribution

Contributions are welcome.

If you'd like to improve this project:
- Fork the repository
- Create a new branch
- Commit changes
- Open a Pull Request

---

# 📜 License

This project is open-source and available under the MIT License.