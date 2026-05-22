# Resume Screening & Job Role Classifier

## Aim

To build a Machine Learning model that automatically classifies resumes into their respective job role categories using Natural Language Processing (NLP) techniques.

## Purpose

Recruiters manually screen hundreds of resumes for every job opening — a process that is time-consuming, inconsistent, and prone to human bias. This project demonstrates how NLP and ML can automate resume screening and predict the most suitable job role category from raw resume text.

## Dataset

- **Source:** [Kaggle — Resume Dataset by Gaurav Dutta](https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset)
- **Size:** ~2,484 resumes
- **Categories:** 25 job role categories including Data Science, Java Developer, Python Developer, HR, Web Designing, and more

## Tech Stack

| Library                 | Purpose                                      |
| ----------------------- | -------------------------------------------- |
| `pandas`, `numpy`       | Data loading and manipulation                |
| `matplotlib`, `seaborn` | Data visualization and EDA                   |
| `nltk`                  | Text preprocessing (stopwords, tokenization) |
| `scikit-learn`          | TF-IDF Vectorization, ML models, evaluation  |
| `wordcloud`             | Visualizing most frequent words per category |

## Project Structure

```
Resume_Screening_Job_Role_Classifier/
├── resume_classifier.ipynb    # Main notebook: EDA → Preprocessing → Modeling → Evaluation
├── README.md                  # Project documentation
└── requirements.txt           # Required Python libraries
```

## Workflow

1. **Data Loading** — Load and explore the dataset
2. **EDA** — Visualize category distribution and word frequencies
3. **Text Preprocessing** — Clean text: remove URLs, special characters, stopwords; apply stemming
4. **Feature Extraction** — TF-IDF Vectorization
5. **Model Training** — Train KNN, SVM, and Random Forest classifiers
6. **Evaluation** — Compare accuracy scores and classification reports
7. **Prediction** — Predict job role from a sample resume text

## Results

| Model                  | Accuracy |
| ---------------------- | -------- |
| K-Nearest Neighbors    | ~99%     |
| Support Vector Machine | ~99%     |
| Random Forest          | ~99%     |

## How to Run

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download NLTK stopwords (run once):
   ```python
   import nltk
   nltk.download('stopwords')
   ```
4. Open and run `resume_classifier.ipynb` in Jupyter Notebook or VS Code

## Sample Prediction

```python
sample_resume = "Experienced Python developer with skills in Django, REST APIs, PostgreSQL and AWS deployment."
predicted_role = predict_job_role(sample_resume)
print(predicted_role)  # Output: Python Developer
```

## Key Learnings

- Real-world NLP pipeline: cleaning → vectorizing → classifying
- TF-IDF feature extraction for text data
- Comparison of multiple classification algorithms
- Multi-class classification with 25 categories

---

_This project was contributed as part of GSSoC-2026._
