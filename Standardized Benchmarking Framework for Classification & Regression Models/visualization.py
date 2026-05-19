"""
visualization.py
─────────────────
Publication-ready plots for benchmark results.

Produces
────────
  Classification
    • Grouped bar chart  — accuracy / F1 / ROC-AUC per model
    • Heatmap            — all metrics across models
    • Confusion matrices — grid of subplots (one per model)
    • Speed vs accuracy  — scatter: train_time × accuracy, sized by F1

  Regression
    • Grouped bar chart  — MAE / RMSE / R² per model
    • Heatmap            — all metrics across models
    • Speed vs R²        — scatter: train_time × R², sized by RMSE

  Shared
    • Memory & timing    — horizontal bar charts

Usage
─────
    from visualization import BenchmarkVisualizer
    from classification_benchmark import ClassificationBenchmark

    bench = ClassificationBenchmark(X, y).add_model(...).run()
    viz = BenchmarkVisualizer(bench.results)
    viz.plot_classification_metrics()
    viz.plot_heatmap()
    viz.plot_speed_vs_accuracy()
    viz.plot_performance_overhead()
    viz.show()                          # or viz.save("sample_results/")
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

from metrics_utils import BenchmarkResult, results_to_dataframe

# ── Global aesthetics ─────────────────────────────────────────────────────────
PALETTE  = sns.color_palette("muted")
BAR_EDGE = 0.6
FIG_DPI  = 130

plt.rcParams.update(
    {
        "figure.facecolor":  "white",
        "axes.facecolor":    "#f8f9fb",
        "axes.grid":         True,
        "grid.color":        "white",
        "grid.linewidth":    1.2,
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "font.family":       "sans-serif",
        "axes.titlesize":    13,
        "axes.labelsize":    11,
        "xtick.labelsize":   9,
        "ytick.labelsize":   9,
        "legend.fontsize":   9,
    }
)

# ──────────────────────────────────────────────────────────────────────────────

class BenchmarkVisualizer:
    """
    Generate plots from a list of BenchmarkResult objects.

    Parameters
    ----------
    results : list[BenchmarkResult]
        Output of ClassificationBenchmark.results or RegressionBenchmark.results.
    dataset_name : str
        Used as a suffix in figure titles.
    """

    def __init__(self, results: list[BenchmarkResult], dataset_name: str = "") -> None:
        if not results:
            raise ValueError("results list is empty.")
        self.results     = results
        self.task        = results[0].task       # "classification" | "regression"
        self.dataset_name = dataset_name
        self.df          = results_to_dataframe(results)
        self._figures: list[plt.Figure] = []

    # ── Public helpers ─────────────────────────────────────────────────────────

    def show(self) -> None:
        """Render all created figures (blocks until windows are closed)."""
        plt.show()

    def save(
        self,
        directory: str | Path = "sample_results",
        fmt: str = "png",
        prefix: str = "",
    ) -> None:
        """Save every figure created so far to *directory*."""
        out = Path(directory)
        out.mkdir(parents=True, exist_ok=True)
        tag = self.dataset_name.lower().replace(" ", "_")
        for i, fig in enumerate(self._figures):
            fname = out / f"{prefix}{tag}_fig{i+1}.{fmt}"
            fig.savefig(fname, dpi=FIG_DPI, bbox_inches="tight")
            print(f"  🖼   Saved → {fname}")
        print()

    # ── Classification plots ───────────────────────────────────────────────────

    def plot_classification_metrics(
        self,
        metrics: Optional[list[str]] = None,
    ) -> plt.Figure:
        """Grouped bar chart of classification metrics per model."""
        self._assert_task("classification")
        metrics = metrics or ["accuracy", "precision", "recall", "f1_score", "roc_auc"]
        metrics = [m for m in metrics if m in self.df.columns]

        models  = self.df.index.tolist()
        n_m, n_models = len(metrics), len(models)
        x       = np.arange(n_models)
        width   = 0.8 / n_m

        fig, ax = plt.subplots(figsize=(max(10, n_models * 1.4), 5), dpi=FIG_DPI)
        for i, metric in enumerate(metrics):
            vals = self.df[metric].values
            bars = ax.bar(
                x + (i - n_m / 2 + 0.5) * width,
                vals,
                width * BAR_EDGE,
                label=metric.replace("_", " ").title(),
                color=PALETTE[i % len(PALETTE)],
                zorder=3,
            )
            for bar, val in zip(bars, vals):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.005,
                    f"{val:.3f}",
                    ha="center", va="bottom", fontsize=7, color="#444",
                )

        ax.set_xticks(x)
        ax.set_xticklabels(models, rotation=30, ha="right")
        ax.set_ylabel("Score")
        ax.set_ylim(0, 1.08)
        ax.set_title(f"Classification metrics — {self.dataset_name}")
        ax.legend(loc="lower right", ncol=n_m)
        fig.tight_layout()
        self._figures.append(fig)
        return fig

    def plot_confusion_matrices(
        self, max_cols: int = 4, cmap: str = "Blues"
    ) -> Optional[plt.Figure]:
        """Grid of confusion-matrix heatmaps, one per model."""
        self._assert_task("classification")
        results_with_cm = [r for r in self.results if "confusion_matrix" in r.extra]
        if not results_with_cm:
            print("No confusion matrices available.")
            return None

        n     = len(results_with_cm)
        ncols = min(n, max_cols)
        nrows = (n + ncols - 1) // ncols
        fig, axes = plt.subplots(
            nrows, ncols,
            figsize=(ncols * 4, nrows * 3.8),
            dpi=FIG_DPI,
        )
        axes = np.array(axes).flatten()

        for ax, result in zip(axes, results_with_cm):
            cm      = result.extra["confusion_matrix"]
            labels  = result.extra.get("classes", list(range(cm.shape[0])))
            df_cm   = pd.DataFrame(cm, index=labels, columns=labels)
            sns.heatmap(
                df_cm, annot=True, fmt="d", cmap=cmap, ax=ax,
                linewidths=0.5, cbar=False, annot_kws={"size": 9},
            )
            ax.set_title(result.model_name, fontsize=10)
            ax.set_xlabel("Predicted")
            ax.set_ylabel("True")

        for ax in axes[n:]:
            ax.set_visible(False)

        fig.suptitle(f"Confusion matrices — {self.dataset_name}", fontsize=13, y=1.02)
        fig.tight_layout()
        self._figures.append(fig)
        return fig

    def plot_speed_vs_accuracy(self) -> plt.Figure:
        """Scatter: training time (x) vs accuracy (y), marker size proportional to F1."""
        self._assert_task("classification")
        fig, ax = plt.subplots(figsize=(8, 5), dpi=FIG_DPI)

        acc_col  = "accuracy"
        size_col = "f1_score" if "f1_score" in self.df.columns else None
        sizes    = (self.df[size_col].values * 500 + 50) if size_col else 150

        scatter = ax.scatter(
            self.df["train_time_s"],
            self.df[acc_col],
            s=sizes,
            c=range(len(self.df)),
            cmap="tab10",
            alpha=0.85,
            edgecolors="white",
            linewidths=0.8,
            zorder=3,
        )
        for idx, (model, row) in enumerate(self.df.iterrows()):
            ax.annotate(
                model,
                (row["train_time_s"], row[acc_col]),
                textcoords="offset points", xytext=(8, 4),
                fontsize=8, color="#333",
            )

        ax.set_xlabel("Training time (s)")
        ax.set_ylabel("Accuracy")
        ax.set_title(f"Speed vs Accuracy — {self.dataset_name}")
        if size_col:
            ax.text(0.02, 0.02, "Marker size ∝ F1-score",
                    transform=ax.transAxes, fontsize=8, color="#666")
        fig.tight_layout()
        self._figures.append(fig)
        return fig

    # ── Regression plots ───────────────────────────────────────────────────────

    def plot_regression_metrics(
        self, metrics: Optional[list[str]] = None
    ) -> plt.Figure:
        """Grouped bar chart of regression metrics per model."""
        self._assert_task("regression")
        metrics = metrics or ["mae", "rmse", "r2"]
        metrics = [m for m in metrics if m in self.df.columns]

        models  = self.df.index.tolist()
        n_m, n_models = len(metrics), len(models)
        x       = np.arange(n_models)
        width   = 0.8 / n_m

        fig, ax = plt.subplots(figsize=(max(10, n_models * 1.5), 5), dpi=FIG_DPI)
        for i, metric in enumerate(metrics):
            vals = self.df[metric].values
            bars = ax.bar(
                x + (i - n_m / 2 + 0.5) * width,
                vals,
                width * BAR_EDGE,
                label=metric.upper() if metric != "r2" else "R²",
                color=PALETTE[i % len(PALETTE)],
                zorder=3,
            )
            for bar, val in zip(bars, vals):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.002 * ax.get_ylim()[1],
                    f"{val:.3f}",
                    ha="center", va="bottom", fontsize=7, color="#444",
                )

        ax.set_xticks(x)
        ax.set_xticklabels(models, rotation=30, ha="right")
        ax.set_title(f"Regression metrics — {self.dataset_name}")
        ax.legend(loc="upper right")
        fig.tight_layout()
        self._figures.append(fig)
        return fig

    def plot_speed_vs_r2(self) -> plt.Figure:
        """Scatter: training time (x) vs R² (y), marker size proportional to 1/RMSE."""
        self._assert_task("regression")
        fig, ax = plt.subplots(figsize=(8, 5), dpi=FIG_DPI)

        rmse_inv = 1 / (self.df["rmse"].values + 1e-6)
        sizes    = rmse_inv / rmse_inv.max() * 400 + 50

        ax.scatter(
            self.df["train_time_s"],
            self.df["r2"],
            s=sizes,
            c=range(len(self.df)),
            cmap="tab10",
            alpha=0.85,
            edgecolors="white",
            linewidths=0.8,
            zorder=3,
        )
        for model, row in self.df.iterrows():
            ax.annotate(
                model,
                (row["train_time_s"], row["r2"]),
                textcoords="offset points", xytext=(8, 4),
                fontsize=8, color="#333",
            )

        ax.set_xlabel("Training time (s)")
        ax.set_ylabel("R²")
        ax.set_title(f"Speed vs R² — {self.dataset_name}")
        ax.text(0.02, 0.02, "Marker size ∝ 1/RMSE  (larger = lower error)",
                transform=ax.transAxes, fontsize=8, color="#666")
        fig.tight_layout()
        self._figures.append(fig)
        return fig

    # ── Shared plots ───────────────────────────────────────────────────────────

    def plot_heatmap(
        self,
        metrics: Optional[list[str]] = None,
        cmap: str = "YlOrRd_r",
    ) -> plt.Figure:
        """
        Heatmap of all metrics, normalised column-wise so colours encode
        relative rank rather than raw magnitude (which can vary wildly between
        MAE and R², for example).
        """
        default_clf = ["accuracy", "precision", "recall", "f1_score", "roc_auc"]
        default_reg = ["mae", "mse", "rmse", "r2"]
        metrics = metrics or (default_clf if self.task == "classification" else default_reg)
        metrics = [m for m in metrics if m in self.df.columns]

        sub  = self.df[metrics].copy()
        norm = (sub - sub.min()) / (sub.max() - sub.min() + 1e-9)

        # For error metrics (lower = better) flip normalisation so red = bad
        lower_is_better = {"mae", "mse", "rmse", "train_time_s", "predict_time_s"}
        for col in norm.columns:
            if col in lower_is_better:
                norm[col] = 1 - norm[col]

        fig, ax = plt.subplots(
            figsize=(len(metrics) * 1.2 + 2, len(sub) * 0.55 + 2), dpi=FIG_DPI
        )
        sns.heatmap(
            norm,
            annot=sub.round(4),
            fmt=".4f",
            cmap=cmap,
            linewidths=0.4,
            linecolor="white",
            ax=ax,
            cbar_kws={"label": "Normalised rank (green = better)"},
            annot_kws={"size": 9},
        )
        ax.set_xticklabels(
            [m.replace("_", " ").upper() for m in metrics],
            rotation=30, ha="right",
        )
        ax.set_title(f"Metric heatmap — {self.dataset_name}", pad=12)
        fig.tight_layout()
        self._figures.append(fig)
        return fig

    def plot_performance_overhead(self) -> plt.Figure:
        """Horizontal bars: training time, prediction time, and memory per model."""
        cols = [c for c in ["train_time_s", "predict_time_s", "peak_memory_kb"]
                if c in self.df.columns]
        labels = {
            "train_time_s":    "Train time (s)",
            "predict_time_s":  "Predict time (s)",
            "peak_memory_kb":  "Peak memory (KB)",
        }

        n     = len(cols)
        fig, axes = plt.subplots(1, n, figsize=(n * 5, max(4, len(self.df) * 0.55 + 1.5)), dpi=FIG_DPI)
        if n == 1:
            axes = [axes]

        models = self.df.index.tolist()
        y      = np.arange(len(models))

        for ax, col in zip(axes, cols):
            vals = self.df[col].values
            bars = ax.barh(y, vals, color=PALETTE[cols.index(col)], alpha=0.85, zorder=3)
            ax.set_yticks(y)
            ax.set_yticklabels(models)
            ax.set_xlabel(labels[col])
            ax.set_title(labels[col])
            ax.invert_yaxis()
            # Value labels
            for bar, val in zip(bars, vals):
                ax.text(
                    val * 1.01, bar.get_y() + bar.get_height() / 2,
                    f"{val:.4f}", va="center", fontsize=8, color="#444",
                )

        fig.suptitle(f"Performance overhead — {self.dataset_name}", fontsize=13)
        fig.tight_layout()
        self._figures.append(fig)
        return fig

    # ── Internal ──────────────────────────────────────────────────────────────

    def _assert_task(self, expected: str) -> None:
        if self.task != expected:
            raise ValueError(
                f"This plot requires task='{expected}', but results are for task='{self.task}'."
            )


# ──────────────────────────────────────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from sklearn.datasets import load_breast_cancer, load_diabetes
    from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor, RandomForestClassifier, RandomForestRegressor
    from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
    from sklearn.svm import SVC, SVR
    from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

    # ── Classification ────────────────────────────────────────────────────────
    from classification_benchmark import ClassificationBenchmark

    X, y = load_breast_cancer(return_X_y=True)
    clf_bench = (
        ClassificationBenchmark(X, y, dataset_name="Breast Cancer")
        .add_model("Logistic Regression", LogisticRegression(max_iter=1000, random_state=42))
        .add_model("Random Forest",       RandomForestClassifier(n_estimators=100, random_state=42))
        .add_model("Decision Tree",       DecisionTreeClassifier(random_state=42))
        .add_model("SVM",                 SVC(probability=True, random_state=42))
        .add_model("Gradient Boosting",   GradientBoostingClassifier(random_state=42))
        .run()
    )

    clf_viz = BenchmarkVisualizer(clf_bench.results, dataset_name="Breast Cancer")
    clf_viz.plot_classification_metrics()
    clf_viz.plot_heatmap()
    clf_viz.plot_confusion_matrices()
    clf_viz.plot_speed_vs_accuracy()
    clf_viz.plot_performance_overhead()
    clf_viz.save("sample_results/", prefix="clf_")

    # ── Regression ────────────────────────────────────────────────────────────
    from regression_benchmark import RegressionBenchmark

    X, y = load_diabetes(return_X_y=True)
    reg_bench = (
        RegressionBenchmark(X, y, dataset_name="Diabetes")
        .add_model("Linear Regression",  LinearRegression())
        .add_model("Ridge",              Ridge())
        .add_model("Random Forest",      RandomForestRegressor(n_estimators=100, random_state=42))
        .add_model("Decision Tree",      DecisionTreeRegressor(random_state=42))
        .add_model("Gradient Boosting",  GradientBoostingRegressor(random_state=42))
        .add_model("SVR",               SVR(kernel="rbf"))
        .run()
    )

    reg_viz = BenchmarkVisualizer(reg_bench.results, dataset_name="Diabetes")
    reg_viz.plot_regression_metrics()
    reg_viz.plot_heatmap()
    reg_viz.plot_speed_vs_r2()
    reg_viz.plot_performance_overhead()
    reg_viz.save("sample_results/", prefix="reg_")

    plt.show()
