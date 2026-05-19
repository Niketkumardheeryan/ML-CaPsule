# ML Benchmarking Framework

A standardized, reusable benchmarking utility for comparing sklearn-compatible
classification and regression models across datasets — with automated metric
tables, confusion matrices, and visualization dashboards.

---

## Structure

```
benchmarking/
├── classification_benchmark.py   # Classification pipeline & metrics
├── regression_benchmark.py       # Regression pipeline & metrics
├── metrics_utils.py              # Shared data structures & timing utilities
├── visualization.py              # Matplotlib / Seaborn plotting suite
└── sample_results/               # CSV exports & saved figures (auto-created)
```

---

## Installation

```bash
pip install scikit-learn numpy pandas matplotlib seaborn
```

---

## Quick Start

### Classification

```python
from classification_benchmark import ClassificationBenchmark
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

X, y = load_breast_cancer(return_X_y=True)

bench = ClassificationBenchmark(X, y, dataset_name="Breast Cancer")
bench.add_model("Logistic Regression", LogisticRegression(max_iter=1000))
bench.add_model("Random Forest",       RandomForestClassifier(n_estimators=100))
bench.add_model("SVM",                 SVC(probability=True))
bench.run()
bench.print_summary()
bench.save_results("sample_results/clf_results.csv")
```

#### Sample output

```
🔬  Benchmarking on 'Breast Cancer'  (455 train / 114 test samples)

  ✓  Logistic Regression              acc=0.9737  f1=0.9737  train=0.043s
  ✓  Random Forest                    acc=0.9649  f1=0.9646  train=0.412s
  ✓  SVM                              acc=0.9737  f1=0.9737  train=0.005s

────────────────────────────────────────────────────────────────────────────────
  Classification — Breast Cancer
────────────────────────────────────────────────────────────────────────────────
                     accuracy  precision    recall  f1_score  roc_auc  train_time_s  ...
model
Logistic Regression  0.9737 ★  0.9738 ★   0.9737  0.9737 ★  0.9948   0.0430
Random Forest        0.9649    0.9654      0.9649  0.9646    0.9956 ★ 0.4120
SVM                  0.9737 ★  0.9738 ★   0.9737  0.9737 ★  0.9962   0.0050 ★
────────────────────────────────────────────────────────────────────────────────
```

> ★ marks the best value in each column.

---

### Regression

```python
from regression_benchmark import RegressionBenchmark
from sklearn.datasets import load_diabetes
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge

X, y = load_diabetes(return_X_y=True)

bench = RegressionBenchmark(X, y, dataset_name="Diabetes")
bench.add_model("Ridge",             Ridge())
bench.add_model("Random Forest",     RandomForestRegressor(n_estimators=100))
bench.add_model("Gradient Boosting", GradientBoostingRegressor(n_estimators=100))
bench.run()
bench.print_summary()
bench.save_results("sample_results/reg_results.csv")
```

---

### Visualization

```python
from visualization import BenchmarkVisualizer

# Pass the .results list from any completed benchmark
viz = BenchmarkVisualizer(bench.results, dataset_name="Breast Cancer")

# Classification plots
viz.plot_classification_metrics()   # grouped bar chart
viz.plot_heatmap()                  # normalised rank heatmap
viz.plot_confusion_matrices()       # grid of confusion matrices
viz.plot_speed_vs_accuracy()        # scatter: train time × accuracy

# Regression plots
viz.plot_regression_metrics()       # grouped bar chart (MAE / RMSE / R²)
viz.plot_heatmap()                  # same heatmap, regression metrics
viz.plot_speed_vs_r2()              # scatter: train time × R²

# Shared
viz.plot_performance_overhead()     # training time, predict time, memory

viz.save("sample_results/")        # saves all figures as PNG
viz.show()                          # renders interactive windows
```

---

## API Reference

### `ClassificationBenchmark`

| Method | Description |
|---|---|
| `add_model(name, model)` | Register an sklearn estimator. Chainable. |
| `run()` | Fit + evaluate all registered models. Chainable. |
| `print_summary()` | Leaderboard table with ★ for best values. |
| `print_confusion_matrices()` | Text-format confusion matrix per model. |
| `save_results(path)` | Export to CSV. |
| `get_dataframe()` | Returns `pd.DataFrame` (index = model name). |

**Metrics**: `accuracy`, `precision`, `recall`, `f1_score`, `roc_auc`,
`train_time_s`, `predict_time_s`, `peak_memory_kb`

---

### `RegressionBenchmark`

| Method | Description |
|---|---|
| `add_model(name, model)` | Register an sklearn estimator. Chainable. |
| `run()` | Fit + evaluate all registered models. Chainable. |
| `print_summary()` | Leaderboard table with ★ for best values. |
| `save_results(path)` | Export to CSV. |
| `get_dataframe()` | Returns `pd.DataFrame` (index = model name). |

**Metrics**: `mae`, `mse`, `rmse`, `r2`,
`train_time_s`, `predict_time_s`, `peak_memory_kb`

---

### `BenchmarkVisualizer`

| Method | Task | Description |
|---|---|---|
| `plot_classification_metrics()` | clf | Grouped bar chart of all clf metrics |
| `plot_heatmap()` | both | Column-normalised rank heatmap |
| `plot_confusion_matrices()` | clf | Grid of seaborn heatmaps |
| `plot_speed_vs_accuracy()` | clf | Scatter: train time × accuracy |
| `plot_regression_metrics()` | reg | Grouped bar chart: MAE / RMSE / R² |
| `plot_speed_vs_r2()` | reg | Scatter: train time × R² |
| `plot_performance_overhead()` | both | Horizontal bars: time & memory |
| `save(directory, fmt, prefix)` | both | Save all figures to disk |
| `show()` | both | Render interactive matplotlib windows |

---

## Running the Demos

Each module contains a `__main__` block with a full multi-dataset demo:

```bash
cd benchmarking/

# Classification demo (Breast Cancer + Iris, 7 models each)
python classification_benchmark.py

# Regression demo (Diabetes + California Housing, 9 models each)
python regression_benchmark.py

# Visualization demo (saves PNG files to sample_results/)
python visualization.py
```

---

## Design Notes

- **Reproducible splits** — `train_test_split` with a fixed `random_state=42`
  and stratification for classification.
- **Memory tracking** — uses `tracemalloc` (stdlib, zero overhead when idle).
- **Timing** — `time.perf_counter()` for sub-millisecond precision.
- **ROC-AUC fallback** — tries `predict_proba`, then `decision_function`,
  then degrades gracefully so hard-probability models (e.g. vanilla `SVC`)
  don't crash the run.
- **Chaining** — `add_model()` and `run()` return `self`, enabling one-liner
  pipelines.
- **Extensible** — `BenchmarkResult.extra` is an open dict; subclass either
  benchmark to add custom metrics without touching shared code.

---

## Contributing

1. Fork the repository and create a feature branch.
2. Add your model or metric inside the relevant benchmark class.
3. Verify the demo runs end-to-end: `python classification_benchmark.py`.
4. Open a pull request with a brief description of what was added and why.
