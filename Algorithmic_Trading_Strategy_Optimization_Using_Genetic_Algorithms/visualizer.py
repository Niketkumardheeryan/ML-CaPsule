"""
Visualization Module for GA Fitness Progression & Strategy Backtest Analysis.

Generates and saves plots for GA convergence (Best vs Mean Fitness), Strategy Equity Curves vs.
Buy-and-Hold Baseline, and Strategy Performance Metric Comparison charts.
"""

from pathlib import Path
from typing import Any, Dict, Optional
import matplotlib.pyplot as plt
import numpy as np


def plot_fitness_progression(
    history: Dict[str, Any], save_path: Optional[str] = None
) -> None:
    """Plot GA Best and Mean fitness progression across generations."""
    best = history["best_fitness"]
    mean = history["mean_fitness"]
    gens = range(1, len(best) + 1)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(gens, best, "b-o", linewidth=2, label="Best Fitness (Sharpe)")
    ax.plot(gens, mean, "r--s", linewidth=1.5, label="Mean Fitness")

    ax.set_title("Genetic Algorithm Fitness Progression", fontsize=14, fontweight="bold")
    ax.set_xlabel("Generation", fontsize=12)
    ax.set_ylabel("Fitness Score", fontsize=12)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(fontsize=11)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Saved fitness progression plot to {save_path}")
    plt.close()


def plot_equity_curves(
    train_results: Dict[str, Any],
    test_results: Dict[str, Any],
    save_path: Optional[str] = None,
) -> None:
    """Plot In-Sample (Train) and Out-of-Sample (Test) Equity Curves against Buy & Hold Baseline."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Train Split
    ax1.plot(train_results["equity_curve"], "g-", linewidth=2, label="GA Strategy Equity")
    ax1.plot(
        train_results["buy_and_hold_equity"],
        "k--",
        linewidth=1.5,
        alpha=0.7,
        label="Buy & Hold",
    )
    ax1.set_title(
        f"Train Set Equity Curve (Return: {train_results['total_return_pct']:+.2f}%)",
        fontsize=12,
        fontweight="bold",
    )
    ax1.set_xlabel("Trading Days")
    ax1.set_ylabel("Portfolio Value ($)")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend()

    # Test Split
    ax2.plot(test_results["equity_curve"], "b-", linewidth=2, label="GA Strategy Equity")
    ax2.plot(
        test_results["buy_and_hold_equity"],
        "k--",
        linewidth=1.5,
        alpha=0.7,
        label="Buy & Hold",
    )
    ax2.set_title(
        f"Test Set Equity Curve (Return: {test_results['total_return_pct']:+.2f}%)",
        fontsize=12,
        fontweight="bold",
    )
    ax2.set_xlabel("Trading Days")
    ax2.set_ylabel("Portfolio Value ($)")
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend()

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Saved equity curve plot to {save_path}")
    plt.close()


def plot_performance_summary(
    history: Dict[str, Any],
    train_results: Dict[str, Any],
    test_results: Dict[str, Any],
    save_path: Optional[str] = None,
) -> None:
    """Generate a combined 3-panel visual dashboard summarizing GA convergence and Backtest performance."""
    fig = plt.figure(figsize=(15, 10))

    # Panel 1: Fitness Progression
    ax1 = fig.add_subplot(2, 2, 1)
    gens = range(1, len(history["best_fitness"]) + 1)
    ax1.plot(gens, history["best_fitness"], "b-o", linewidth=2, label="Best Fitness")
    ax1.plot(gens, history["mean_fitness"], "r--", linewidth=1.5, label="Mean Fitness")
    ax1.set_title("GA Fitness Progression Across Generations", fontweight="bold")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness Score (Sharpe)")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend()

    # Panel 2: Out-of-Sample Test Equity Curve
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.plot(test_results["equity_curve"], "b-", linewidth=2, label="GA Strategy")
    ax2.plot(test_results["buy_and_hold_equity"], "k--", linewidth=1.5, label="Buy & Hold")
    ax2.set_title("Out-of-Sample Test Equity Curve", fontweight="bold")
    ax2.set_xlabel("Trading Days")
    ax2.set_ylabel("Portfolio Equity ($)")
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend()

    # Panel 3: Performance Metrics Comparison
    ax3 = fig.add_subplot(2, 1, 2)
    metrics = ["Total Return (%)", "Sharpe Ratio", "Win Rate (%)", "Profit Factor"]
    strategy_vals = [
        test_results["total_return_pct"],
        test_results["sharpe_ratio"],
        test_results["win_rate_pct"],
        test_results["profit_factor"],
    ]

    x = np.arange(len(metrics))
    bars = ax3.bar(x, strategy_vals, color=["#2b5c8f", "#2ca02c", "#d62728", "#9467bd"], width=0.5)
    ax3.set_xticks(x)
    ax3.set_xticklabels(metrics, fontweight="bold")
    ax3.set_title("Test Set Optimized Strategy Key Metrics", fontweight="bold")
    ax3.grid(True, axis="y", linestyle="--", alpha=0.5)

    for bar in bars:
        height = bar.get_height()
        ax3.annotate(
            f"{height:.2f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Saved strategy dashboard to {save_path}")
    plt.close()
