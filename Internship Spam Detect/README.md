# Internship Scam Detection

A full-stack machine learning web application designed to detect fraudulent or spam internship postings using an optimized Decision Tree pipeline.

---

## Dataset
- **Source:** Kaggle Internship Scam Detection Dataset
- The notebook downloads the raw dataset as `internship_scam_data.csv` via `gdown`:
- **Link:** [Google Drive Dataset Link](https://drive.google.com/file/d/1JzvRWYKAjDbjhuVZSMJvIbGJryxyVKQo/view?usp=sharing)

---

## Key Features
1. Dynamic input form built with Vanilla JS and Tabler Icons.
2. Automated pipeline handling missing inputs (`SimpleImputer`) and category encoding (`OneHotEncoder`).
3. Model optimization via hyperparameter tuning with `GridSearchCV`.
4. Outputs live classification outcomes alongside real-time spam probability scores.
5. Built-in rule-based fallback mechanism for local runtime stability.

---

## Tech Stack
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)
- **Backend:** Python, Flask, Flask-CORS
- **Machine Learning:** scikit-learn, pandas, numpy, joblib
- **Utilities:** gdown

---

## Usage
1. Open `notebooks/internship_scam_detection.ipynb` in Jupyter/Colab.
2. Run all cells (downloads data via `gdown`, trains the model, and outputs `.pkl` saves).
3. Start the Flask backend server:
```bash
flask run
```
4. Open `http://127.0.0.1:5000` to test the application interface.

---

## Model Metrics

* **Overall Accuracy:** 70%
* **Scam Precision:** 74%
* **Scam Recall:** 63%

---

## Live Links & Contact

* **GitHub:** [spam-detect](https://github.com/naina-bhatnagar/spam-detect)
* **Live App:** [Render Link](https://spam-detect-saj2.onrender.com)
* **Created by:** [Naina Bhatnagar](https://github.com/naina-bhatnagar)
