# 🧩 Autism Identification System

A Machine Learning project that identifies **Autism Spectrum Disorder (ASD)** from behavioural screening questionnaire data, using classification algorithms to support early diagnosis.

---

## 📌 Project Description


Autism Spectrum Disorder (ASD) is a neurodevelopmental condition affecting social interaction and communication. Traditional clinical diagnosis is expensive and time-consuming. This project uses ML classifiers trained on ASD screening questionnaire responses to predict whether an individual is likely to have ASD.

**Models used:**
- Logistic Regression
- Random Forest
- K-Nearest Neighbours (KNN)
- Support Vector Machine (SVM)

**Evaluation metrics:** Accuracy Score, Classification Report, MSE, R² Score

---

## 📂 Dataset

- **Name:** Autism Screening Dataset
- **Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/autism+screening+adult)
- **Created by:** Prof. Fadi Thabtah
- **License:** CC BY 4.0
- **File used in code:** `Data.csv` (included in the project folder)
- **Instances:** 704 records | **Features:** 20

### Key Features

| Feature | Description |
|---------|-------------|
| `A1_Score` – `A10_Score` | Responses to 10 ASD screening questions (0 or 1) |
| `age` | Age of the individual |
| `gender` | Male / Female |
| `ethnicity` | Ethnic background |
| `jaundice` | Whether born with jaundice (yes/no) |
| `austim` | Family member diagnosed with ASD (yes/no) |
| `result` | Total AQ screening score |
| `Class/ASD` | Target variable — ASD: Yes / No |

> ✅ `Data.csv` is already included in the project folder — no external download needed.
> 
> Alternatively, download from [Kaggle – Autism Screening Dataset](https://www.kaggle.com/datasets/faizunnabi/autism-screening)

---

## 🛠️ Dependencies

Install required libraries using:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### Library Versions (recommended)

| Library | Version |
|---------|---------|
| `pandas` | 1.5.3 |
| `numpy` | 1.23.5 |
| `matplotlib` | 3.6.3 |
| `seaborn` | 0.12.2 |
| `scikit-learn` | 1.2.2 |

> 💡 You can check your installed versions with `pip show <library-name>`

---

## 🚀 How to Run

> ✅ This project can be run on **Google Colab** or **locally with Jupyter Notebook**.

### Option A — Google Colab (easier)

1. Open [colab.research.google.com](https://colab.research.google.com/)
2. Upload the notebook file (`.ipynb`)
3. Upload `Data.csv` to the Colab session storage
4. Run all cells via `Runtime` → `Run all`

### Option B — Local Jupyter Notebook

1. Clone the repository:
   ```bash
   git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
   cd "ML-CaPsule/Autism Identification System"
   ```

2. Install dependencies:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn
   ```

3. Launch Jupyter:
   ```bash
   jupyter notebook
   ```

4. Open the `.ipynb` file and run all cells in order

> ⚠️ Make sure `Data.csv` is in the **same folder** as the notebook, since the code reads it as:
> ```python
> df = pd.read_csv("Data.csv", engine='python')
> ```

---

## 📊 Sample Output

### Dataset Preview

| age | gender | A1_Score | A2_Score | ... | Class/ASD |
|-----|--------|----------|----------|-----|-----------|
| 21 | Male | 1 | 1 | ... | YES |
| 17 | Female | 0 | 1 | ... | NO |

### Model Results

| Metric | Value |
|--------|-------|
| Accuracy Score | printed per model |
| Classification Report | Precision, Recall, F1-score |
| MSE | Mean Squared Error |
| R² Score | Coefficient of Determination |

---

## 📁 Project Structure

```
Autism Identification System/
├── Data.csv          ← ASD screening dataset
├── *.ipynb           ← Main notebook
└── README.md
```

---

## 👤 Contributor

- README added as part of [ML-CaPsule](https://github.com/Niketkumardheeryan/ML-CaPsule) open-source contribution
