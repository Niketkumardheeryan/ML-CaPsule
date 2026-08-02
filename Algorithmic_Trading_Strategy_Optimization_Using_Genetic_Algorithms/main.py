"""
Main Execution Script for Algorithmic Trading Strategy Optimization Using Genetic Algorithms.

Runs dataset validation, Train/Test splitting, GA optimization, backtesting performance evaluation,
and plot generation.
"""

from pathlib import Path
import sys

# Ensure module path imports work correctly
MODULE_DIR = Path(__file__).resolve().parent
if str(MODULE_DIR.parent) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR.parent))

from Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms.backtest import (
    run_backtest,
)
from Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms.data_loader import (
    load_and_validate_data,
)
from Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms.ga_optimizer import (
    GeneticAlgorithmOptimizer,
)
from Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms.visualizer import (
    plot_equity_curves,
    plot_fitness_progression,
    plot_performance_summary,
)


def run_optimization_pipeline(
    data_path: str = None,
    pop_size: int = 30,
    generations: int = 25,
    test_split_ratio: float = 0.3,
):
    """Run full optimization pipeline from dataset loading to out-of-sample evaluation and visualization."""
    if data_path is None:
        data_path = MODULE_DIR / "trading_data.csv"

    print("=" * 70)
    print(" GA ALGORITHMIC TRADING STRATEGY OPTIMIZER ")
    print("=" * 70)

    # 1. Load and Validate Dataset
    print(f"\n[1/5] Loading and validating market dataset from: {data_path}")
    df = load_and_validate_data(str(data_path))
    print(f"      Successfully loaded {len(df)} OHLCV rows.")

    # 2. Train / Test Split
    split_idx = int(len(df) * (1.0 - test_split_ratio))
    df_train = df.iloc[:split_idx].reset_index(drop=True)
    df_test = df.iloc[split_idx:].reset_index(drop=True)
    print(f"\n[2/5] Train/Test Split: Train = {len(df_train)} rows | Test = {len(df_test)} rows")

    # 3. GA Optimization
    print(f"\n[3/5] Starting Genetic Algorithm Optimization ({generations} Generations, Pop Size {pop_size})...")
    optimizer = GeneticAlgorithmOptimizer(
        population_size=pop_size,
        generations=generations,
        crossover_rate=0.8,
        mutation_rate=0.2,
        elitism_count=2,
        seed=42,
    )
    result = optimizer.run(df_train, verbose=True)

    best_chrom = result["best_chromosome"]
    best_fit = result["best_fitness"]
    history = result["history"]

    print("\n" + "=" * 70)
    print(" OPTIMIZATION COMPLETED")
    print(f" Best Training Fitness (Sharpe Score): {best_fit:+.4f}")
    print(" Best Evolved Strategy Genes:")
    for gene, val in best_chrom.items():
        if isinstance(val, float):
            print(f"   - {gene:20s}: {val:.4f}")
        else:
            print(f"   - {gene:20s}: {val}")
    print("=" * 70)

    # 4. Backtest Evaluation
    print("\n[4/5] Running Backtest Evaluation on Train and Test Splits...")
    train_results = run_backtest(df_train, best_chrom)
    test_results = run_backtest(df_test, best_chrom)

    print("\n" + "-" * 60)
    print(" PERFORMANCE METRICS SUMMARY ")
    print("-" * 60)
    print(" Metric                     | Train (In-Sample)  | Test (Out-of-Sample)")
    print("-" * 60)
    print(f" Total Return (%)          | {train_results['total_return_pct']:+16.2f}% | {test_results['total_return_pct']:+17.2f}%")
    print(f" Sharpe Ratio              | {train_results['sharpe_ratio']:17.4f}  | {test_results['sharpe_ratio']:18.4f}")
    print(f" Maximum Drawdown (%)      | {train_results['max_drawdown_pct']:16.2f}% | {test_results['max_drawdown_pct']:17.2f}%")
    print(f" Win Rate (%)              | {train_results['win_rate_pct']:16.2f}% | {test_results['win_rate_pct']:17.2f}%")
    print(f" Profit Factor             | {train_results['profit_factor']:17.2f}  | {test_results['profit_factor']:18.2f}")
    print(f" Total Trades Executed     | {train_results['num_trades']:17d}  | {test_results['num_trades']:18d}")
    print("-" * 60)

    # 5. Visualizations
    print("\n[5/5] Generating and Saving Performance Visualization Charts...")
    plot_fitness_progression(history, save_path=str(MODULE_DIR / "ga_fitness_progression.png"))
    plot_equity_curves(train_results, test_results, save_path=str(MODULE_DIR / "equity_curves.png"))
    plot_performance_summary(
        history, train_results, test_results, save_path=str(MODULE_DIR / "strategy_dashboard.png")
    )

    print("\n[+] All tasks completed successfully!")
    return {
        "best_chromosome": best_chrom,
        "train_results": train_results,
        "test_results": test_results,
        "history": history,
    }


if __name__ == "__main__":
    run_optimization_pipeline()
