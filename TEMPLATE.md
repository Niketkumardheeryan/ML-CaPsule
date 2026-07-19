# Standardized Project Template

All project directories added to the **ML-CaPsule** repository should adhere to this standardized structure to ensure maintainability, readability, and programmatic index generation.

---

## Required Files Checklist

Every project folder should contain:
- [ ] **A Python Script or Jupyter Notebook**: The core model training/evaluation logic (`.py` or `.ipynb`).
- [ ] **`requirements.txt`**: A list of dependencies specific to this project.
- [ ] **`README.md`**: A project-specific README describing the goal, dataset, models used, and performance.

---

## README.md Template

Create a `README.md` inside your project directory matching the following template:

```markdown
# [Project Name]

## Goal
A clear description of the problem, what this project does, and the expected outcomes.

## Dataset
- **Source**: [Link to dataset on Kaggle/UCI/etc.]
- **Description**: Brief explanation of the dataset structure, features, and size.

## Models & Algorithms Used
List the machine learning models or deep learning architectures trained and evaluated:
- Model 1 (e.g., Logistic Regression)
- Model 2 (e.g., Random Forest)

## Libraries & Dependencies
List the primary packages used:
- `scikit-learn`
- `pandas`
- `numpy`

## Steps & Workflow
1. **Data Pre-processing**: Handled missing values, scaling, etc.
2. **Feature Engineering**: Feature selection, encoding.
3. **Model Training**: Trained models on train-test splits.
4. **Evaluation**: Compared models using accuracy, F1-score, etc.

## Performance & Results
Summary of model performance:
| Model | Accuracy / Metric |
|---|---|
| Model 1 | 92.4% |
| Model 2 | 89.1% |

## Conclusion
Key insights from model evaluation and recommended next steps.
```

---

## Code & Jupyter Notebook Standards

1. **Jupyter Notebook Structure**:
   - The first cell must be a **Markdown Cell** containing the `# Project Title` and a brief description.
   - Separate steps (Data loading, EDA, Pre-processing, Model training, Results) with descriptive headings.
   - Clean up intermediate or redundant outputs to keep the notebook readable.

2. **No Hardcoded Absolute Paths**:
   - Use relative paths for loading datasets (e.g., `pd.read_csv('data/dataset.csv')` instead of `pd.read_csv('C:/Users/.../dataset.csv')`).

3. **Requirements File**:
   - List only the dependencies required for this specific project.
   - Do not include standard libraries (like `math`, `os`, `sys`, `json`) in `requirements.txt`.
