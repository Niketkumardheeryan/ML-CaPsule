#  Spam Mail Detection

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-NLP-orange)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

A machine learning project that classifies SMS messages as **Spam** or **Ham** (not spam) using Natural Language Processing (NLP) techniques and multiple classification algorithms. The project achieves up to **97.84% accuracy** using Support Vector Classification (SVC).

---

##  Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [How to Run](#how-to-run)
- [NLP Pipeline](#nlp-pipeline)
- [Model Performance](#model-performance)
- [Technologies Used](#technologies-used)
- [Results & Conclusion](#results--conclusion)
- [Contributing](#contributing)
- [License](#license)

---

##  Overview

SMS spam is any junk message delivered to a mobile phone via the Short Message Service (SMS). This project builds a complete machine learning pipeline to automatically detect and classify spam messages. It includes:

- **Exploratory Data Analysis (EDA)** — Data cleaning, manipulation, preprocessing, and visualization
- **NLP Processing** — Text tokenization, stemming, and vectorization using NLTK
- **Model Training** — Comparison of 11 different classification algorithms
- **Evaluation** — Accuracy scores, classification reports, and confusion matrices for each model

---

##  Dataset

| Property | Details |
|----------|---------|
| **Name** | SMS Spam Collection Dataset |
| **Source** | [Kaggle — UCI SMS Spam Collection](https://www.kaggle.com/uciml/sms-spam-collection-dataset) |
| **Total Samples** | 5,572 messages |
| **Classes** | 2 — `ham` (4,825) and `spam` (747) |
| **Format** | CSV with columns: `v1` (label), `v2` (message text) |
| **Location** | `Dataset/dataset.zip` |

---

##  Project Structure

```
Spam Mail Detection/
├── README.md                  # This file — Project overview and documentation
├── requirements.txt           # Python dependencies
├── Dataset/
│   └── dataset.zip            # SMS Spam Collection Dataset (compressed)
└── Model/
    ├── README.md              # Model-specific documentation
    └── spam_mail_detection.ipynb  # Main Jupyter Notebook with full pipeline
```

---

##  Setup & Installation

### Prerequisites

- Python 3.x
- pip (Python package manager)
- Jupyter Notebook or JupyterLab

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
   cd "ML-CaPsule/Spam Mail Detection"
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data**

   ```python
   import nltk
   nltk.download('stopwords')
   nltk.download('punkt')
   ```

4. **Extract the dataset**

   Unzip `Dataset/dataset.zip` into the `Dataset/` directory.

---

##  How to Run

1. Launch Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

2. Navigate to `Model/spam_mail_detection.ipynb`

3. Run all cells sequentially (`Cell → Run All`)

> **Note:** The notebook reads the dataset from a Kaggle path. You may need to update the file path in the data loading cell to point to your local `Dataset/` directory:
> ```python
> data = pd.read_csv('../Dataset/spam.csv')
> ```

---

##  NLP Pipeline

The text preprocessing pipeline includes the following steps:

| Step | Technique | Description |
|------|-----------|-------------|
| 1 | **Text Cleaning** | Removal of special characters, punctuation, and noise |
| 2 | **Tokenization** | Splitting text into individual words using NLTK's `word_tokenize` |
| 3 | **Stop Words Removal** | Filtering out common English stop words using NLTK corpus |
| 4 | **Stemming** | Reducing words to root form using Porter Stemmer |
| 5 | **Vectorization** | Converting text to numerical features using CountVectorizer and TF-IDF |

---

##  Model Performance

The following classification algorithms were trained and evaluated:

| # | Model | Accuracy |
|---|-------|----------|
| 1 | Logistic Regression | 96.19% |
| 2 | K-Nearest Neighbors (KNN) | 90.45% |
| 3 | **Support Vector Classifier (SVC)** | **97.84%** |
| 4 | Naive Bayes (Multinomial) | 96.69% |
| 5 | Decision Tree Classifier | 94.90% |
| 6 | Random Forest Classifier | 97.83% |
| 7 | AdaBoost Classifier | 97.48% |
| 8 | Gradient Boosting Classifier | 97.70% |
| 9 | XGBoost Classifier | 97.68% |
| 10 | Extra Trees Classifier | 97.27% |
| 11 | Bagging Classifier | 95.59% |

Each model includes detailed **classification reports** and **confusion matrices** in the notebook.

---

## Technologies Used

| Category | Libraries |
|----------|-----------|
| **Data Manipulation** | NumPy, Pandas |
| **Visualization** | Matplotlib, Seaborn, Scikit-plot |
| **NLP** | NLTK (tokenization, stemming, stop words) |
| **Machine Learning** | Scikit-learn, XGBoost |
| **Scientific Computing** | SciPy |
| **Environment** | Jupyter Notebook, Python 3.x |

---

##  Results & Conclusion

- **Best performing model:** Support Vector Classifier (SVC) with **97.84% accuracy**
- **Top 3 models** (all above 97.5%): SVC, Random Forest, and Gradient Boosting
- The combination of **TF-IDF vectorization** with ensemble classifiers yields consistently high performance
- Model accuracies can be further improved through hyperparameter tuning
- The dataset exhibits class imbalance (86.6% ham vs 13.4% spam), which was handled during preprocessing

---

##  Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes and commit (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

For detailed guidelines, see the main repository's [CONTRIBUTING.md](../CONTRIBUTING.md).

---

##  License

This project is part of the [ML-CaPsule](https://github.com/Niketkumardheeryan/ML-CaPsule) repository and is licensed under the [MIT License](../LICENSE).
