"""
regression_benchmark.py
────────────────────────
Unified benchmarking pipeline for sklearn-compatible regression models.

Metrics collected
─────────────────
  • MAE   — Mean Absolute Error
  • MSE   — Mean Squared Error
  • RMSE  — Root Mean Squared Error
  • R²    — Coefficient of Determination

Performance
───────────
  • Training time (seconds)
  • Inference time (seconds)
  • Peak memory   (KiB, tracemalloc)

Usage
─────
    from regression_benchmark import RegressionBenchmark
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import Ridge
    from sklearn.datasets import fetch_california_housing

    X, y = fetch_california_housing(return_X_y=True)

    bench = RegressionBenchmark(X, y, dataset_name="California Housing")
    bench.add_model("Ridge",          Ridge())
    bench.add_model("Random Forest",  RandomForestRegressor(n_estimators=100))
    bench.run()
    bench.print_summary()
    bench.save_results("sample_results/regression_results.csv")
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from metrics_utils import (
    BenchmarkResult,
    highlight_best,
    memory_tracker,
    prepare_split,
    print_summary_table,
    results_to_dataframe,
    timer,
)


class RegressionBenchmark:
    """
    Run, record, and display regression metrics for multiple models.

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
            np.asarray(X, dtype=float),
            np.asarray(y, dtype=float),
            test_size=test_size,
            random_state=random_state,
        )
        self._models: list[tuple[str, BaseEstimator]] = []
        self.results: list[BenchmarkResult] = []

    # ── Public API ────────────────────────────────────────────────────────────

    def add_model(self, name: str, model: BaseEstimator) -> "RegressionBenchmark":
        """Register a model for benchmarking. Returns self for chaining."""
        self._models.append((name, model))
        return self

    def run(self) -> "RegressionBenchmark":
        """Train and evaluate all registered models."""
        self.results.clear()
        print(f"\n🔬  Benchmarking on '{self.dataset_name}'  "
              f"({self.X_train.shape[0]} train / {self.X_test.shape[0]} test samples)\n")

        for name, model in self._models:
            result = self._evaluate(name, model)
            self.results.append(result)
            print(f"  ✓  {name:<35}  R²={result.metrics['r2']:.4f}  "
                  f"RMSE={result.metrics['rmse']:.4f}  "
                  f"train={result.train_time_s:.3f}s")

        return self

    def print_summary(self) -> None:
        """Print a formatted leaderboard to stdout."""
        if not self.results:
            print("No results yet — call .run() first.")
            return
        df = results_to_dataframe(self.results)
        higher = ["r2"]
        lower  = ["mae", "mse", "rmse", "train_time_s", "predict_time_s", "peak_memory_kb"]
        highlighted = highlight_best(df, higher, lower)
        print_summary_table(highlighted, title=f"Regression — {self.dataset_name}")

    def save_results(self, path: str | Path = "regression_results.csv") -> None:
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
        result = BenchmarkResult(model_name=name, task="regression")

        # ── Train ─────────────────────────────────────────────────────────────
        with memory_tracker() as mem, timer() as t:
            model.fit(self.X_train, self.y_train)
        result.train_time_s   = t["elapsed"]
        result.peak_memory_kb = mem["peak_kb"]

        # ── Predict ───────────────────────────────────────────────────────────
        with timer() as t:
            y_pred = model.predict(self.X_test)
        result.predict_time_s = t["elapsed"]

        # ── Metrics ───────────────────────────────────────────────────────────
        mae  = mean_absolute_error(self.y_test, y_pred)
        mse  = mean_squared_error(self.y_test, y_pred)
        rmse = float(np.sqrt(mse))
        r2   = r2_score(self.y_test, y_pred)

        result.metrics.update({"mae": mae, "mse": mse, "rmse": rmse, "r2": r2})
        return result


# ──────────────────────────────────────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from sklearn.datasets import load_diabetes
    from sklearn.ensemble import (
        GradientBoostingRegressor,
        RandomForestRegressor,
    )
    from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.svm import SVR
    from sklearn.tree import DecisionTreeRegressor

    MODELS = [
        ("Linear Regression",      LinearRegression()),
        ("Ridge",                  Ridge(alpha=1.0)),
        ("Lasso",                  Lasso(alpha=0.1, max_iter=5000)),
        ("ElasticNet",             ElasticNet(max_iter=5000)),
        ("Decision Tree",          DecisionTreeRegressor(random_state=42)),
        ("Random Forest",          RandomForestRegressor(n_estimators=100, random_state=42)),
        ("Gradient Boosting",      GradientBoostingRegressor(n_estimators=100, random_state=42)),
        ("K-Nearest Neighbours",   KNeighborsRegressor(n_neighbors=5)),
        ("Support Vector Machine", SVR(kernel="rbf")),
    ]

    from sklearn.datasets import load_linnerud
    for loader, dname in [(load_diabetes, "Diabetes"), (load_linnerud, "Linnerud")]:
        X, y = loader(return_X_y=True)
        bench = RegressionBenchmark(X, y, dataset_name=dname)
        for mname, model in MODELS:
            bench.add_model(mname, model)
        bench.run()
        bench.print_summary()
        bench.save_results(f"sample_results/regression_{dname.lower().replace(' ', '_')}.csv")
