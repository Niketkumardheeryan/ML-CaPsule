"""
classification_benchmark.py
────────────────────────────
Unified benchmarking pipeline for sklearn-compatible classification models.

Metrics collected
─────────────────
  • Accuracy
  • Precision  (weighted)
  • Recall     (weighted)
  • F1-Score   (weighted)
  • ROC-AUC    (one-vs-rest, weighted; binary datasets use standard AUC)
  • Confusion Matrix  (stored in result.extra)

Performance
───────────
  • Training time (seconds)
  • Inference time (seconds)
  • Peak memory   (KiB, tracemalloc)

Usage
─────
    from classification_benchmark import ClassificationBenchmark
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.datasets import load_breast_cancer

    X, y = load_breast_cancer(return_X_y=True)

    bench = ClassificationBenchmark(X, y, dataset_name="Breast Cancer")
    bench.add_model("Logistic Regression", LogisticRegression(max_iter=1000))
    bench.add_model("Random Forest",       RandomForestClassifier(n_estimators=100))
    bench.run()
    bench.print_summary()
    bench.save_results("sample_results/classification_results.csv")
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.preprocessing import LabelBinarizer

from metrics_utils import (
    BenchmarkResult,
    highlight_best,
    memory_tracker,
    prepare_split,
    print_summary_table,
    results_to_dataframe,
    timer,
)


class ClassificationBenchmark:
    """
    Run, record, and display classification metrics for multiple models.

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
    y : array-like of shape (n_samples,)
    dataset_name : str
        Human-readable label for console output.
    test_size : float
        Fraction of data held out for evaluation (default 0.2).
    random_state : int
        Seed for reproducible splits (default 42).
    """

    def __init__(
        self,
        X: np.ndarray,
        y: np.ndarray,
        dataset_name: str = "Dataset",
        test_size: float = 0.2,
        random_state: int = 42,
    ) -> None:
        self.dataset_name = dataset_name
        self.X_train, self.X_test, self.y_train, self.y_test = prepare_split(
            np.asarray(X), np.asarray(y), test_size=test_size, random_state=random_state
        )
        self._n_classes = len(np.unique(y))
        self._models: list[tuple[str, BaseEstimator]] = []
        self.results: list[BenchmarkResult] = []

    # ── Public API ────────────────────────────────────────────────────────────

    def add_model(self, name: str, model: BaseEstimator) -> "ClassificationBenchmark":
        """Register a model for benchmarking. Returns self for chaining."""
        self._models.append((name, model))
        return self

    def run(self) -> "ClassificationBenchmark":
        """Train and evaluate all registered models."""
        self.results.clear()
        print(f"\n🔬  Benchmarking on '{self.dataset_name}'  "
              f"({self.X_train.shape[0]} train / {self.X_test.shape[0]} test samples)\n")

        for name, model in self._models:
            result = self._evaluate(name, model)
            self.results.append(result)
            print(f"  ✓  {name:<35}  acc={result.metrics['accuracy']:.4f}  "
                  f"f1={result.metrics['f1_score']:.4f}  "
                  f"train={result.train_time_s:.3f}s")

        return self

    def print_summary(self) -> None:
        """Print a formatted leaderboard to stdout."""
        if not self.results:
            print("No results yet — call .run() first.")
            return
        df = results_to_dataframe(self.results)
        higher = ["accuracy", "precision", "recall", "f1_score", "roc_auc"]
        lower  = ["train_time_s", "predict_time_s", "peak_memory_kb"]
        highlighted = highlight_best(df, higher, lower)
        print_summary_table(highlighted, title=f"Classification — {self.dataset_name}")

    def print_confusion_matrices(self) -> None:
        """Pretty-print confusion matrices for every model."""
        for r in self.results:
            cm = r.extra.get("confusion_matrix")
            if cm is None:
                continue
            labels = r.extra.get("classes", list(range(cm.shape[0])))
            df_cm = pd.DataFrame(cm, index=[f"True {l}" for l in labels],
                                    columns=[f"Pred {l}" for l in labels])
            print(f"\n  {r.model_name}")
            print(df_cm.to_string())

    def save_results(self, path: str | Path = "classification_results.csv") -> None:
        """Export the summary table to a CSV file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df = results_to_dataframe(self.results)
        df.to_csv(path)
        print(f"\n  📄  Results saved → {path}")

    def get_dataframe(self) -> pd.DataFrame:
        """Return results as a tidy DataFrame (index = model name)."""
        return results_to_dataframe(self.results)

    # ── Internal ──────────────────────────────────────────────────────────────

    def _evaluate(self, name: str, model: BaseEstimator) -> BenchmarkResult:
        result = BenchmarkResult(model_name=name, task="classification")

        # ── Train ─────────────────────────────────────────────────────────────
        with memory_tracker() as mem, timer() as t:
            model.fit(self.X_train, self.y_train)
        result.train_time_s  = t["elapsed"]
        result.peak_memory_kb = mem["peak_kb"]

        # ── Predict ───────────────────────────────────────────────────────────
        with timer() as t:
            y_pred = model.predict(self.X_test)
        result.predict_time_s = t["elapsed"]

        # ── Metrics ───────────────────────────────────────────────────────────
        avg = "binary" if self._n_classes == 2 else "weighted"

        result.metrics["accuracy"]  = accuracy_score(self.y_test, y_pred)
        result.metrics["precision"] = precision_score(
            self.y_test, y_pred, average=avg, zero_division=0)
        result.metrics["recall"]    = recall_score(
            self.y_test, y_pred, average=avg, zero_division=0)
        result.metrics["f1_score"]  = f1_score(
            self.y_test, y_pred, average=avg, zero_division=0)

        # ROC-AUC — needs probability estimates
        result.metrics["roc_auc"] = self._roc_auc(model, y_pred)

        # Confusion matrix
        classes = np.unique(self.y_test)
        result.extra["confusion_matrix"] = confusion_matrix(self.y_test, y_pred, labels=classes)
        result.extra["classes"] = classes.tolist()

        return result

    def _roc_auc(self, model: BaseEstimator, y_pred: np.ndarray) -> float:
        """Compute ROC-AUC, gracefully falling back if the model lacks predict_proba."""
        try:
            if hasattr(model, "predict_proba"):
                y_score = model.predict_proba(self.X_test)
                if self._n_classes == 2:
                    return roc_auc_score(self.y_test, y_score[:, 1])
                return roc_auc_score(
                    self.y_test, y_score, multi_class="ovr", average="weighted"
                )
            elif hasattr(model, "decision_function"):
                y_score = model.decision_function(self.X_test)
                if self._n_classes == 2:
                    return roc_auc_score(self.y_test, y_score)
                lb = LabelBinarizer()
                y_bin = lb.fit_transform(self.y_test)
                return roc_auc_score(y_bin, y_score, average="weighted")
        except Exception:
            pass
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                return roc_auc_score(self.y_test, y_pred, average="weighted")
            except Exception:
                return float("nan")


# ──────────────────────────────────────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from sklearn.datasets import load_breast_cancer, load_iris
    from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import GaussianNB
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.tree import DecisionTreeClassifier

    MODELS = [
        ("Logistic Regression",      LogisticRegression(max_iter=1000, random_state=42)),
        ("Decision Tree",            DecisionTreeClassifier(random_state=42)),
        ("Random Forest",            RandomForestClassifier(n_estimators=100, random_state=42)),
        ("Gradient Boosting",        GradientBoostingClassifier(n_estimators=100, random_state=42)),
        ("K-Nearest Neighbours",     KNeighborsClassifier(n_neighbors=5)),
        ("Support Vector Machine",   SVC(kernel="rbf", probability=True, random_state=42)),
        ("Gaussian Naive Bayes",     GaussianNB()),
    ]

    for loader, dname in [(load_breast_cancer, "Breast Cancer"), (load_iris, "Iris")]:
        X, y = loader(return_X_y=True)
        bench = ClassificationBenchmark(X, y, dataset_name=dname)
        for mname, model in MODELS:
            bench.add_model(mname, model)
        bench.run()
        bench.print_summary()
        bench.save_results(f"sample_results/classification_{dname.lower().replace(' ', '_')}.csv")
