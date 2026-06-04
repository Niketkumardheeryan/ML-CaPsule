```markdown
# Internship Scam Detection System

An end-to-end Machine Learning pipeline built to identify fraudulent internship postings using metadata signals, text features, and recruiter behavior analytics. This system processes data completely leak-free using automated Scikit-Learn pipelines and optimizes a classification tree to achieve an **overall baseline accuracy of 70%**.

---

## 📊 Dataset Attribution

This project utilizes a subset of the **Internship Scam Detection Dataset** hosted on Kaggle. 

* **Dataset Author / Credits:** Special thanks to **aiexplorer77** for compiling and sharing this valuable open-source security benchmark.
* **Original Link:** https://www.kaggle.com/datasets/aiexplorer77/internship-scam-detection-dataset
* **Note on Scope:** The data handled in this repository represents a balanced, optimized subset extracted from the larger master dataset to facilitate fast pipeline prototyping and hyperparameter tuning.

---

## 🛠️ System Architecture & Engineering Rigor

This project strictly adheres to robust machine learning practices to ensure the model remains reliable, robust, and capable of generalizing to new, real-world data.

* **Step 1: Raw Data Ingestion & Target Selection**
* **Step 2: Explicit Train-Test Split (80% Train / 20% Test)**
* **Step 3: Automated ColumnTransformer Pipelines**
* **Step 4: GridSearchCV Hyperparameter Tuning**
* **Step 5: Robust Final Assessment**

### 1. Data Isolation (Strict Anti-Leakage Guardrail)
Following strict machine learning discipline, the data is split into **80% training** and **20% testing** partitions *before* any statistical computations (like medians or category frequencies) occur. This keeps the test set completely pristine and ensures zero data leakage.

### 2. Specialized Multi-Path Preprocessing
Because missing data and text types require different mathematical treatments, an automated `ColumnTransformer` handles feature transformations dynamically on the fly:
* **Stipend Path:** Imputes missing stipends with a constant `0` (indicating an unpaid position) and normalizes using `StandardScaler`.
* **Categorical Path:** Automatically detects structural text properties (`company_size`, `work_mode`) and converts them into machine-readable numeric formats via `OneHotEncoder`.
* **High-Cardinality Drop-List:** Non-predictive string identifiers like `company_name`, `internship_title`, `location`, `employment_type`, and `industry` are explicitly excluded from training to keep the model focused entirely on behavior patterns.

### 3. Eliminating Non-User-Provided Columns
Some columns present in the original dataset were dropped because a user evaluating a job posting would not have access to these metrics. These include:
* `unrealistic_salary_flag`
* `vague_description_score`
* `grammatical_errors`
* `urgency_score`
* `keyword_spam_score`
* `recruiter_experience_years`

---

## Model Performance & Optimization

The baseline model was systematically optimized using **Grid Search (`GridSearchCV`)** with 3-fold cross-validation. The grid automatically optimized tree constraints to prevent overfitting.


### Final Optimized Evaluation Report:
```bash
--- Optimized Decision Tree Evaluation Report ---
              precision    recall  f1-score   support

           0       0.67      0.77      0.71       197
           1       0.74      0.63      0.68       203

    accuracy                           0.70       400
   macro avg       0.70      0.70      0.70       400
weighted avg       0.70      0.70      0.70       400

```

### Key Metrics:

* **Overall Accuracy: 70%**
* **Scam Precision: 74%**
* **Scam Recall: 63%**

---

## Key Libraries Used

* **Pandas & NumPy** — High-performance data manipulation and distribution analysis.
* **Matplotlib** — Exploratory visualizations (Histograms and Scatter Matrices).
* **Scikit-Learn** — Pipeline automation, `ColumnTransformer`, `GridSearchCV`, and tree classification architectures.
