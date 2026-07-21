# AI Powered Resume Skill Gap Analyzer

An end-to-end Streamlit application that helps job seekers compare their resume against a target job description, identify missing skills, estimate similarity, and score ATS-friendliness.

## Overview

This project takes an uploaded resume (.pdf or .docx) and a job description (pasted text or uploaded .txt), then runs a lightweight NLP pipeline to:

- extract raw text from the resume
- preprocess and normalize the text
- identify technical and soft skills
- compute resume-to-JD similarity
- estimate ATS-friendliness
- surface improvement suggestions

The result is a dashboard-style report that makes skill gaps and resume weaknesses easier to understand.

## Features

- Upload and parse resumes in PDF or DOCX format
- Accept a job description via pasted text or .txt upload
- Clean and preprocess text for downstream NLP
- Extract skills using a spaCy PhraseMatcher and curated taxonomy
- Measure similarity using TF-IDF cosine similarity
- Score ATS-friendliness based on formatting and keyword coverage
- Display dashboard metrics with Plotly charts
- Download the analysis as an HTML report

## Tech Stack

- Python 3.10+
- Streamlit
- spaCy
- NLTK
- scikit-learn
- Plotly
- PyPDF2 / pdfplumber
- python-docx

## Architecture

```text
+-------------------+       +----------------------+       +------------------------+
| User Uploads     |       | Resume Parser        |       | Preprocessing Pipeline |
| Resume + JD      | ----> | parser.py            | ----> | preprocessing.py      |
+-------------------+       +----------------------+       +------------------------+
                                       |                              |
                                       v                              v
                           +----------------------+       +------------------------+
                           | Skill Extraction      |       | Similarity / ATS      |
                           | skill_extractor.py    |       | similarity.py /       |
                           +----------------------+       | ats_score.py          |
                                       |                              |
                                       v                              v
                           +----------------------+       +------------------------+
                           | Streamlit Dashboard  | <---- | Results + Report      |
                           | app.py               |       | Download              |
                           +----------------------+       +------------------------+
```

## Setup and Run

### 1. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the spaCy English model

```bash
python -m spacy download en_core_web_sm
```

### 4. Run the app

```bash
streamlit run app.py
```

## How It Works

1. Upload a resume
   - The app accepts a resume in PDF or DOCX format.

2. Parse the resume
   - The parser extracts raw text from the uploaded file.

3. Preprocess the text
   - The preprocessing pipeline cleans and normalizes the document for NLP.

4. Extract skills
   - A skill taxonomy and PhraseMatcher identify technical and soft skills from the resume and job description.

5. Compute similarity
   - TF-IDF vectorization and cosine similarity estimate how closely the resume matches the job description.

6. Score ATS-friendliness
   - Section detection and keyword coverage produce an ATS score plus practical recommendations.

7. Show results
   - The dashboard displays match percentage, ATS score, matched/missing skills, top keywords, and improvement suggestions.

## Sample Screenshots

Placeholder screenshots can be added under the screenshots/ folder:

- [screenshots/dashboard.png](screenshots/dashboard.png)
- [screenshots/results.png](screenshots/results.png)

## Contributing

New contributors should keep the utilities module boundaries clear:

- utils/parser.py: file parsing and text extraction only
- utils/preprocessing.py: text cleaning and normalization
- utils/skill_extractor.py: skill taxonomy loading and matching
- utils/similarity.py: TF-IDF similarity and keyword ranking
- utils/ats_score.py: ATS formatting and keyword coverage scoring
- app.py: Streamlit UI orchestration and presentation

When adding new functionality:

- keep parsing logic in the parser module
- keep NLP/text transformation in preprocessing
- keep skill matching in skill_extractor
- keep scoring in similarity or ats_score
- keep UI work in app.py

If you add new utilities, prefer a focused module with a single responsibility and document it clearly.
