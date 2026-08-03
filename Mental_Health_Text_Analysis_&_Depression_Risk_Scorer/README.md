# Mental Health Text Analysis & Depression Risk Scorer

A multi-dimensional mental health risk analysis project leveraging Natural Language Processing (NLP), Transformer models (DistilBERT), and explainable AI (LIME/SHAP) techniques.

## 🚀 Features
- **Multi-Label Risk Scoring**: Simultaneously computes individual risk scores (0-100%) and categorizes severity levels (Low / Moderate / High) for **Depression**, **Anxiety**, **Stress**, and **Burnout**.
- **Explainability Layer**: Uses a text-perturbation explainer (inspired by LIME) that dynamically highlights words in the input entry. Hovering over highlighted words displays their individual contribution weights to the selected category score.
- **Interactive Streamlit UI**: Sleek, glassmorphic layout tailored for both dark & light themes, featuring quick-load journal templates.
- **Complete Pipeline Notebook**: Comprehensive notebook displaying dataset extraction, tokenization, training loop logic, and evaluation metrics.

## 📁 File Structure
```text
Mental_Health_Text_Analysis_&_Depression_Risk_Scorer/
├── requirements.txt            # Project dependencies
├── app.py                      # Streamlit interactive application
├── model_utils.py              # Risk scoring and LIME explainer logic
├── Mental_Health_Analysis.ipynb # EDA, Model fine-tuning, and inference notebook
└── README.md                   # Setup and usage guide
```

## 🛠️ Setup Instructions

### 1. Install Dependencies
Navigate to the project folder and install the required Python packages:
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit Web Application
Launch the interactive dashboard:
```bash
streamlit run app.py
```

### 3. Open the Jupyter Notebook
To run the model training pipeline, launch Jupyter and open `Mental_Health_Analysis.ipynb`:
```bash
jupyter notebook
```
