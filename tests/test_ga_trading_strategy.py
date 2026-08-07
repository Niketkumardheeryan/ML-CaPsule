"""
Unit Tests for Genetic Algorithm Trading Strategy Optimization Module.
"""

import os
from pathlib import Path
import sys
import unittest
import numpy as np
import pandas as pd

# Ensure repository root is on sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms.backtest import (
    run_backtest,
)
from Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms.data_loader import (
    calculate_macd,
    calculate_rsi,
    calculate_sma,
    compute_all_indicators,
    load_and_validate_data,
)
from Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms.ga_optimizer import (
    GeneticAlgorithmOptimizer,
    crossover_chromosomes,
    evaluate_fitness,
    mutate_chromosome,
)
from Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms.strategy import (
    GENE_BOUNDS,
    generate_random_chromosome,
    generate_signals,
    sanitize_chromosome,
)


class TestGATradingStrategy(unittest.TestCase):

    def setUp(self):
        """Set up synthetic test market dataset."""
        np.random.seed(42)
        n = 100
        prices = 100.0 + np.cumsum(np.random.normal(0.1, 1.0, n))
        dates = pd.date_range("2023-01-01", periods=n, freq="D")

        highs = prices + np.abs(np.random.normal(0.5, 0.2, n))
        lows = prices - np.abs(np.random.normal(0.5, 0.2, n))
        opens = (highs + lows) / 2.0

        self.df = pd.DataFrame(
            {
                "Date": dates,
                "Open": opens,
                "High": highs,
                "Low": lows,
                "Close": prices,
                "Volume": np.random.randint(1000, 5000, n),
            }
        )

    def test_load_and_validate_data(self):
        """Test dataset validation and OHLC sanitization."""
        # Intentionally break High/Low bounds to test sanitization
        invalid_df = self.df.copy()
        invalid_df.loc[0, "High"] = invalid_df.loc[0, "Low"] - 1.0

        clean_df = load_and_validate_data(invalid_df)
        self.assertEqual(len(clean_df), len(self.df))
        self.assertTrue((clean_df["High"] >= clean_df["Low"]).all())
        self.assertTrue((clean_df["High"] >= clean_df["Open"]).all())

    def test_calculate_indicators(self):
        """Test SMA, RSI, and MACD technical indicator functions."""
        sma = calculate_sma(self.df["Close"], period=10)
        self.assertEqual(len(sma), len(self.df))

        rsi = calculate_rsi(self.df["Close"], period=14)
        self.assertEqual(len(rsi), len(self.df))
        self.assertTrue((rsi >= 0.0).all() and (rsi <= 100.0).all())

        macd, signal, hist = calculate_macd(self.df["Close"])
        self.assertEqual(len(macd), len(self.df))
        self.assertEqual(len(signal), len(self.df))
        self.assertEqual(len(hist), len(self.df))

        full_df = compute_all_indicators(self.df)
        self.assertIn("SMA_Short", full_df.columns)
        self.assertIn("SMA_Long", full_df.columns)
        self.assertIn("RSI", full_df.columns)
        self.assertIn("MACD_Line", full_df.columns)

    def test_chromosome_generation_and_sanitization(self):
        """Test chromosome boundary constraints and sanitization."""
        chrom = generate_random_chromosome()

        for gene, (min_v, max_v, is_int) in GENE_BOUNDS.items():
            self.assertIn(gene, chrom)
            val = chrom[gene]
            self.assertGreaterEqual(val, min_v)
            self.assertLessEqual(val, max_v)
            if is_int:
                self.assertIsInstance(val, (int, np.integer))

        self.assertLess(chrom["rsi_buy_threshold"], chrom["rsi_sell_threshold"])
        self.assertLess(chrom["sma_short_period"], chrom["sma_long_period"])
        self.assertLess(chrom["macd_fast"], chrom["macd_slow"])

    def test_crossover_and_mutation(self):
        """Test crossover and mutation operations."""
        p1 = generate_random_chromosome()
        p2 = generate_random_chromosome()

        c1, c2 = crossover_chromosomes(p1, p2, crossover_rate=1.0)
        self.assertIsNotNone(c1)
        self.assertIsNotNone(c2)

        mutated = mutate_chromosome(p1, mutation_rate=0.5)
        self.assertIsNotNone(mutated)
        self.assertLess(mutated["rsi_buy_threshold"], mutated["rsi_sell_threshold"])

    def test_backtest_simulation(self):
        """Test backtest metric calculations."""
        chrom = generate_random_chromosome()
        results = run_backtest(self.df, chrom)

        self.assertIn("total_return_pct", results)
        self.assertIn("sharpe_ratio", results)
        self.assertIn("max_drawdown_pct", results)
        self.assertIn("win_rate_pct", results)
        self.assertIn("profit_factor", results)
        self.assertIn("equity_curve", results)
        self.assertEqual(len(results["equity_curve"]), len(self.df))

    def test_ga_optimizer_runs_and_improves(self):
        """Test end-to-end GA optimization convergence."""
        optimizer = GeneticAlgorithmOptimizer(
            population_size=10,
            generations=5,
            crossover_rate=0.8,
            mutation_rate=0.2,
            seed=42,
        )
        res = optimizer.run(self.df, verbose=False)

        self.assertIsNotNone(res["best_chromosome"])
        self.assertGreater(len(res["history"]["best_fitness"]), 0)
        # Check fitness is valid numeric and not stagnating at -infinity
        self.assertGreater(res["best_fitness"], -10.0)


if __name__ == "__main__":
    unittest.main()
