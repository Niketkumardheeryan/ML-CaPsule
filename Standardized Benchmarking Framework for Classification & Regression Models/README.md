# ML Benchmarking Framework

A standardized, reproducible benchmarking framework for comparing sklearn-compatible
classification and regression models across datasets — with automated metric tables,
confusion matrices, and visualization dashboards.

---

## Repository Structure

```
benchmarking/
├── metrics_utils.ipynb            # Shared utilities (timers, memory, dataclasses)
├── classification_benchmark.ipynb # Classification pipeline, metrics & plots
├── regression_benchmark.ipynb     # Regression pipeline, metrics & plots
└── sample_results/                # Auto-generated CSVs and figures
    ├── classification_breast_cancer.csv
    ├── classification_iris.csv
    ├── regression_diabetes.csv
    ├── regression_synthetic.csv
    └── *.png  (11 figures)
```

---

## Installation

```bash
pip install scikit-learn numpy pandas matplotlib seaborn jupyter
```

---

## Running the Notebooks

Open each notebook in Jupyter Lab / Notebook and run all cells, or execute headlessly:

```bash
jupyter nbconvert --to notebook --execute --inplace metrics_utils.ipynb
jupyter nbconvert --to notebook --execute --inplace classification_benchmark.ipynb
jupyter nbconvert --to notebook --execute --inplace regression_benchmark.ipynb
```

> **Note:** Run `metrics_utils.ipynb` first — it writes `metrics_utils.py` to disk,
> which the other two notebooks import.

---

## Metrics Reference

### Classification

| Metric | Description |
|---|---|
| Accuracy | Fraction of correctly classified samples |
| Precision | Weighted-average positive predictive value |
| Recall | Weighted-average true positive rate |
| F1-Score | Harmonic mean of precision & recall |
| ROC-AUC | Area under ROC curve (one-vs-rest, weighted avg) |
| Train time | Wall-clock `fit()` duration (seconds) |
| Predict time | Wall-clock `predict()` duration (seconds) |
| Peak memory | `tracemalloc` peak during training (KiB) |

### Regression

| Metric | Description |
|---|---|
| MAE | Mean Absolute Error |
| MSE | Mean Squared Error |
| RMSE | Root Mean Squared Error |
| R² | Coefficient of Determination (higher = better) |
| Train time | Wall-clock `fit()` duration (seconds) |
| Predict time | Wall-clock `predict()` duration (seconds) |
| Peak memory | `tracemalloc` peak during training (KiB) |

---

## Results

> All experiments use an 80/20 stratified train-test split with `random_state=42`.
> ★ marks the best value in each column.

---

### Classification — Breast Cancer (binary, 569 samples, 30 features)

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Train (s) | Predict (s) | Memory (KB) |
|---|---|---|---|---|---|---|---|---|
| Logistic Regression | **0.9649** ★ | 0.9595 | **0.9861** ★ | **0.9726** ★ | **0.9954** ★ | 1.2560 | 0.0004 | 64.5 |
| Decision Tree | 0.9123 | 0.9559 | 0.9028 | 0.9286 | 0.9157 | 0.0131 | 0.0004 | 86.1 |
| Random Forest | 0.9561 | **0.9589** ★ | 0.9722 | 0.9655 | 0.9937 | 1.1534 | 0.0096 | 188.6 |
| Gradient Boosting | 0.9561 | 0.9467 | **0.9861** ★ | 0.9660 | 0.9907 | 0.6654 | 0.0010 | 154.4 |
| K-Nearest Neighbours | 0.9123 | 0.9429 | 0.9167 | 0.9296 | 0.9559 | **0.0019** ★ | 0.0333 | **30.0** ★ |
| Support Vector Machine | 0.9298 | 0.9211 | 0.9722 | 0.9459 | 0.9696 | 0.0266 | 0.0016 | 117.3 |
| Gaussian Naive Bayes | 0.9386 | 0.9452 | 0.9583 | 0.9517 | 0.9878 | 0.0038 | **0.0003** ★ | 206.8 |

**Key findings:**
- Logistic Regression achieves the best F1 (0.9726) and ROC-AUC (0.9954) with moderate training time.
- KNN is the fastest to train (0.002s) and uses the least memory (30 KB).
- Decision Tree and KNN tie for lowest accuracy (0.9123), indicating underfitting on this dataset.
- Gaussian Naive Bayes has the fastest inference (0.0003s) — ideal for latency-sensitive deployments.

---

### Classification — Iris (multiclass, 150 samples, 4 features)

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Train (s) | Predict (s) | Memory (KB) |
|---|---|---|---|---|---|---|---|---|
| Logistic Regression | 0.9667 | 0.9697 | 0.9667 | 0.9666 | **1.0000** ★ | 0.0508 | 0.0014 | 41.9 |
| Decision Tree | 0.9333 | 0.9333 | 0.9333 | 0.9333 | 0.9500 | 0.0064 | 0.0002 | 20.5 |
| Random Forest | 0.9000 | 0.9024 | 0.9000 | 0.8997 | 0.9867 | 1.1590 | 0.0080 | 119.3 |
| Gradient Boosting | 0.9667 | 0.9697 | 0.9667 | 0.9666 | 0.9900 | 0.9432 | 0.0017 | 172.6 |
| K-Nearest Neighbours | **1.0000** ★ | **1.0000** ★ | **1.0000** ★ | **1.0000** ★ | **1.0000** ★ | **0.0033** ★ | 0.0020 | **10.7** ★ |
| Support Vector Machine | 0.9667 | 0.9697 | 0.9667 | 0.9666 | 0.9967 | 0.0076 | **0.0003** ★ | 15.8 |
| Gaussian Naive Bayes | 0.9667 | 0.9697 | 0.9667 | 0.9666 | 0.9900 | 0.0035 | 0.0002 | 11.6 |

**Key findings:**
- KNN achieves perfect scores across all metrics on this small, well-separated dataset.
- Random Forest is the weakest performer here — ensemble overhead hurts on tiny datasets.
- Logistic Regression, Gradient Boosting, SVM, and GNB all converge to the same accuracy (0.9667).
- KNN also wins on speed (0.003s) and memory (10.7 KB), making it the clear winner on Iris.

---

### Regression — Diabetes (89 test samples, 10 features)

| Model | MAE | MSE | RMSE | R² | Train (s) | Predict (s) | Memory (KB) |
|---|---|---|---|---|---|---|---|
| Linear Regression | 42.7941 | 2900.19 | 53.8534 | 0.4526 | 0.0051 | 0.0002 | 76.9 |
| Ridge | 46.1389 | 3077.42 | 55.4745 | 0.4192 | 0.0039 | 0.0001 | 61.5 |
| Lasso | 42.8544 | **2798.19** ★ | **52.8980** ★ | **0.4719** ★ | 0.0034 | 0.0002 | 62.9 |
| ElasticNet | 63.7059 | 5311.21 | 72.8781 | -0.0025 | **0.0025** ★ | **0.0001** ★ | 61.7 |
| Decision Tree | 54.5281 | 4976.80 | 70.5464 | 0.0607 | 0.0102 | 0.0002 | 33.5 |
| Random Forest | 44.0530 | 2952.01 | 54.3324 | 0.4428 | 1.1125 | 0.0098 | 102.4 |
| Gradient Boosting | 44.6033 | 2898.44 | 53.8371 | 0.4529 | 0.2753 | 0.0006 | 96.4 |
| K-Nearest Neighbours | **42.7708** ★ | 3019.08 | 54.9461 | 0.4302 | 0.0023 | 0.0012 | **16.3** ★ |
| Support Vector Machine | 56.0237 | 4333.29 | 65.8277 | 0.1821 | 0.0076 | 0.0016 | 43.6 |

**Key findings:**
- Lasso achieves the best R² (0.4719), MSE, and RMSE — L1 regularization suits this sparse medical dataset.
- ElasticNet severely underfits (R² ≈ 0) despite fastest training; its default alpha is too aggressive here.
- KNN ties Lasso on MAE while using only 16.3 KB memory — a surprisingly competitive baseline.
- Gradient Boosting tracks closely with Lasso on R² (0.4529) with acceptable overhead.
- All R² values are moderate (≤ 0.47), which reflects the inherent difficulty of disease progression prediction.

---

### Regression — Synthetic (100 test samples, 20 features, noise=10)

| Model | MAE | MSE | RMSE | R² | Train (s) | Predict (s) | Memory (KB) |
|---|---|---|---|---|---|---|---|
| Linear Regression | 8.0437 | 96.86 | 9.8418 | 0.9948 | 0.0034 | 0.0003 | 153.5 |
| Ridge | 8.1279 | 98.57 | 9.9281 | 0.9947 | 0.0039 | **0.0001** ★ | 131.8 |
| Lasso | **8.0182** ★ | **95.39** ★ | **9.7667** ★ | **0.9949** ★ | 0.0026 | 0.0002 | 131.8 |
| ElasticNet | 41.4719 | 2845.32 | 53.3415 | 0.8476 | **0.0024** ★ | **0.0001** ★ | 131.9 |
| Decision Tree | 69.2163 | 8221.53 | 90.6727 | 0.5597 | 0.0100 | 0.0002 | 50.3 |
| Random Forest | 55.1397 | 4626.68 | 68.0197 | 0.7522 | 1.2648 | 0.0092 | 118.1 |
| Gradient Boosting | 36.9942 | 2229.97 | 47.2225 | 0.8806 | 0.3883 | 0.0007 | 109.6 |
| K-Nearest Neighbours | 72.6967 | 8344.55 | 91.3485 | 0.5531 | **0.0010** ★ | 0.0228 | **3.6** ★ |
| Support Vector Machine | 103.0090 | 17743.34 | 133.2041 | 0.0498 | 0.0091 | 0.0021 | 78.2 |

**Key findings:**
- Linear models (Linear Regression, Ridge, Lasso) dominate with R² > 0.99, confirming the data is truly linear.
- SVR fails completely (R² = 0.05) — the default RBF kernel struggles on high-dimensional linear data without tuning.
- KNN uses only 3.6 KB memory — the lightest model in the suite.
- Gradient Boosting is the best non-linear model (R² = 0.88), useful when the data-generating process is unknown.

---

## Visualizations

### Classification — Breast Cancer

**Metric comparison (grouped bar)**
![Classification metrics — Breast Cancer](sample_results/clf_bc_metrics.png)

**Normalised rank heatmap**
![Heatmap — Breast Cancer](sample_results/clf_bc_heatmap.png)

**Confusion matrices**
![Confusion matrices — Breast Cancer](sample_results/clf_bc_confusion.png)

**Speed vs Accuracy**
![Speed vs Accuracy — Breast Cancer](sample_results/clf_bc_speed.png)

**Performance overhead**
![Overhead — Breast Cancer](sample_results/clf_bc_overhead.png)

---

### Classification — Iris

**Metric comparison (grouped bar)**
![Classification metrics — Iris](sample_results/clf_iris_metrics.png)

**Normalised rank heatmap**
![Heatmap — Iris](sample_results/clf_iris_heatmap.png)

---

### Regression — Diabetes

**Metric comparison (grouped bar)**
![Regression metrics — Diabetes](sample_results/reg_diab_metrics.png)

**Normalised rank heatmap**
![Heatmap — Diabetes](sample_results/reg_diab_heatmap.png)

**Speed vs R²**
![Speed vs R² — Diabetes](sample_results/reg_diab_speed.png)

**Performance overhead**
![Overhead — Diabetes](sample_results/reg_diab_overhead.png)

---

### Regression — Synthetic

**Metric comparison (grouped bar)**
![Regression metrics — Synthetic](sample_results/reg_syn_metrics.png)

**Normalised rank heatmap**
![Heatmap — Synthetic](sample_results/reg_syn_heatmap.png)

---

## Design Notes

- **Reproducibility** — fixed `random_state=42` and stratified splits throughout.
- **Memory tracking** — `tracemalloc` (stdlib) with zero overhead when idle.
- **Timing** — `time.perf_counter()` for sub-millisecond precision.
- **ROC-AUC fallback** — tries `predict_proba` → `decision_function` → soft label; models without probability outputs never crash the run.
- **Chaining API** — `add_model()` and `run()` return `self`, enabling one-liner pipelines.
- **Heatmap normalisation** — metrics are scaled column-wise so colour encodes relative rank, not raw magnitude (making MAE and R² visually comparable in the same figure).

---

## Contributing

1. Fork the repository and create a feature branch.
2. Add your model inside the relevant notebook's model list cell.
3. Re-execute the notebook end-to-end: `jupyter nbconvert --to notebook --execute --inplace <notebook>.ipynb`
4. Update the results tables in this README.
5. Open a pull request with a brief description of what was added and why.
