"""
metrics_utils.py
────────────────
Shared utility functions for the benchmarking framework.
Covers data splitting, timing, memory profiling, and pretty-printing.
"""

from __future__ import annotations

import time
import tracemalloc
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


# ──────────────────────────────────────────────────────────────────────────────
# Data structures
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class BenchmarkResult:
    """Container for a single model's benchmark output."""

    model_name: str
    task: str                        # "classification" | "regression"
    metrics: dict[str, float] = field(default_factory=dict)
    train_time_s: float = 0.0
    predict_time_s: float = 0.0
    peak_memory_kb: float = 0.0
    extra: dict[str, Any] = field(default_factory=dict)   # confusion matrix, etc.

    def to_series(self) -> pd.Series:
        row = {
            "model": self.model_name,
            "train_time_s": round(self.train_time_s, 4),
            "predict_time_s": round(self.predict_time_s, 6),
            "peak_memory_kb": round(self.peak_memory_kb, 1),
        }
        row.update({k: round(v, 4) for k, v in self.metrics.items()})
        return pd.Series(row)


# ──────────────────────────────────────────────────────────────────────────────
# Context managers
# ──────────────────────────────────────────────────────────────────────────────

@contextmanager
def timer():
    """Yields a mutable dict so elapsed seconds can be read after the block."""
    state = {"elapsed": 0.0}
    start = time.perf_counter()
    try:
        yield state
    finally:
        state["elapsed"] = time.perf_counter() - start


@contextmanager
def memory_tracker():
    """Yields peak memory usage in KiB after the block completes."""
    state = {"peak_kb": 0.0}
    tracemalloc.start()
    try:
        yield state
    finally:
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        state["peak_kb"] = peak / 1024


# ──────────────────────────────────────────────────────────────────────────────
# Data helpers
# ──────────────────────────────────────────────────────────────────────────────

def prepare_split(
    X: np.ndarray,
    y: np.ndarray,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Stratified split for classification; regular split for regression."""
    try:
        return train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
    except ValueError:
        return train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )


# ──────────────────────────────────────────────────────────────────────────────
# Reporting helpers
# ──────────────────────────────────────────────────────────────────────────────

def results_to_dataframe(results: list[BenchmarkResult]) -> pd.DataFrame:
    rows = [r.to_series() for r in results]
    df = pd.DataFrame(rows).set_index("model")
    return df


def print_summary_table(df: pd.DataFrame, title: str = "Benchmark Summary") -> None:
    sep = "─" * 80
    print(f"\n{sep}")
    print(f"  {title}")
    print(sep)
    print(df.to_string())
    print(sep + "\n")


def highlight_best(df: pd.DataFrame, higher_is_better: list[str], lower_is_better: list[str]) -> pd.DataFrame:
    """
    Return a copy of *df* with a '★' appended to the best value in each column.
    Useful for quick human-readable output.
    """
    out = df.copy().astype(str)
    for col in higher_is_better:
        if col in df.columns:
            best_idx = df[col].idxmax()
            out.loc[best_idx, col] += " ★"
    for col in lower_is_better:
        if col in df.columns:
            best_idx = df[col].idxmin()
            out.loc[best_idx, col] += " ★"
    return out
