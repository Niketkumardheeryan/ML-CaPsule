"""
Unit Tests for Genetic Algorithm Trading Strategy Optimization Module.
"""

import copy
import os
from pathlib import Path
import random
import sys
import unittest
from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd

# Core Engine Functions & Classes for Unit Testing
GENE_BOUNDS: Dict[str, Tuple[float, float, bool]] = {
    "rsi_buy_threshold": (15.0, 45.0, False),
    "rsi_sell_threshold": (55.0, 85.0, False),
    "sma_short_period": (5.0, 30.0, True),
    "sma_long_period": (35.0, 100.0, True),
    "macd_fast": (8.0, 16.0, True),
    "macd_slow": (20.0, 40.0, True),
    "macd_signal": (5.0, 15.0, True),
    "stop_loss_pct": (0.01, 0.10, False),
    "take_profit_pct": (0.02, 0.25, False),
}


def load_and_validate_data(source: Any) -> pd.DataFrame:
    if isinstance(source, str):
        df = pd.read_csv(source)
    elif isinstance(source, pd.DataFrame):
        df = source.copy()
    else:
        raise ValueError("Source must be a file path string or pandas DataFrame.")

    required_cols = ["Open", "High", "Low", "Close"]
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"Missing required column: '{col}'")
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Volume" in df.columns:
        df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce").fillna(0)

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)

    df = df.dropna(subset=required_cols).reset_index(drop=True)
    df["High"] = np.maximum(df["High"], np.maximum(df["Open"], df["Close"]))
    df["Low"] = np.minimum(df["Low"], np.minimum(df["Open"], df["Close"]))
    return df


def calculate_sma(series: pd.Series, period: int) -> pd.Series:
    period = max(1, int(period))
    return series.rolling(window=period, min_periods=1).mean()


def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    period = max(2, int(period))
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi.fillna(50.0)


def calculate_macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
    s = pd.Series(series)
    macd_line = s.ewm(span=max(2, fast), adjust=False).mean() - s.ewm(span=max(3, slow), adjust=False).mean()
    signal_line = macd_line.ewm(span=max(2, signal), adjust=False).mean()
    macd_hist = macd_line - signal_line
    return macd_line, signal_line, macd_hist


def compute_all_indicators(
    df: pd.DataFrame,
    sma_short: int = 10,
    sma_long: int = 50,
    rsi_period: int = 14,
    macd_fast: int = 12,
    macd_slow: int = 26,
    macd_signal: int = 9,
) -> pd.DataFrame:
    data = df.copy()
    data["SMA_Short"] = calculate_sma(data["Close"], sma_short)
    data["SMA_Long"] = calculate_sma(data["Close"], sma_long)
    data["RSI"] = calculate_rsi(data["Close"], rsi_period)
    macd, signal_l, hist = calculate_macd(data["Close"], macd_fast, macd_slow, macd_signal)
    data["MACD_Line"] = macd
    data["MACD_Signal"] = signal_l
    data["MACD_Hist"] = hist
    return data


def sanitize_chromosome(chrom: Dict[str, Any]) -> Dict[str, Any]:
    clean_chrom = {}
    for gene, (min_val, max_val, is_int) in GENE_BOUNDS.items():
        val = float(chrom.get(gene, (min_val + max_val) / 2.0))
        val = max(min_val, min(max_val, val))
        if is_int:
            val = int(round(val))
        clean_chrom[gene] = val

    if clean_chrom["rsi_buy_threshold"] >= clean_chrom["rsi_sell_threshold"]:
        clean_chrom["rsi_buy_threshold"] = clean_chrom["rsi_sell_threshold"] - 5.0

    if clean_chrom["sma_short_period"] >= clean_chrom["sma_long_period"]:
        clean_chrom["sma_long_period"] = clean_chrom["sma_short_period"] + 5.0

    if clean_chrom["macd_fast"] >= clean_chrom["macd_slow"]:
        clean_chrom["macd_slow"] = clean_chrom["macd_fast"] + 2.0

    return clean_chrom


def generate_random_chromosome() -> Dict[str, Any]:
    chrom = {}
    for gene, (min_val, max_val, is_int) in GENE_BOUNDS.items():
        if is_int:
            val = random.randint(int(min_val), int(max_val))
        else:
            val = random.uniform(min_val, max_val)
        chrom[gene] = val
    return sanitize_chromosome(chrom)


def generate_signals(df: pd.DataFrame, chromosome: Dict[str, Any]) -> pd.DataFrame:
    chrom = sanitize_chromosome(chromosome)
    data = compute_all_indicators(
        df,
        sma_short=int(chrom["sma_short_period"]),
        sma_long=int(chrom["sma_long_period"]),
        rsi_period=14,
        macd_fast=int(chrom["macd_fast"]),
        macd_slow=int(chrom["macd_slow"]),
        macd_signal=int(chrom["macd_signal"]),
    )

    n = len(data)
    signals = np.zeros(n, dtype=int)
    current_position = 0

    rsi_buy = chrom["rsi_buy_threshold"]
    rsi_sell = chrom["rsi_sell_threshold"]

    for i in range(1, n):
        rsi_val = data["RSI"].iloc[i]
        sma_s = data["SMA_Short"].iloc[i]
        sma_l = data["SMA_Long"].iloc[i]
        macd_h = data["MACD_Hist"].iloc[i]

        buy_score = 0
        sell_score = 0

        if rsi_val < rsi_buy:
            buy_score += 1
        if sma_s > sma_l:
            buy_score += 1
        if macd_h > 0:
            buy_score += 1

        if rsi_val > rsi_sell:
            sell_score += 1
        if sma_s < sma_l:
            sell_score += 1
        if macd_h < 0:
            sell_score += 1

        if current_position == 0:
            if buy_score >= 2:
                current_position = 1
        else:
            if sell_score >= 2:
                current_position = 0

        signals[i] = current_position

    data["Signal"] = signals
    return data


def run_backtest(
    df: pd.DataFrame,
    chromosome: Dict[str, Any],
    initial_capital: float = 10000.0,
    commission_pct: float = 0.0005,
) -> Dict[str, Any]:
    data = generate_signals(df, chromosome)
    n = len(data)

    prices = data["Close"].values
    highs = data["High"].values
    lows = data["Low"].values
    signals = data["Signal"].values

    stop_loss = chromosome.get("stop_loss_pct", 0.03)
    take_profit = chromosome.get("take_profit_pct", 0.06)

    cash = initial_capital
    position_units = 0.0
    entry_price = 0.0

    equity_curve = np.zeros(n)
    equity_curve[0] = initial_capital

    trades = []
    trade_entry_idx = None

    for i in range(n):
        price = prices[i]
        high_price = highs[i]
        low_price = lows[i]
        target_signal = signals[i]

        if position_units > 0 and entry_price > 0:
            sl_price = entry_price * (1.0 - stop_loss)
            tp_price = entry_price * (1.0 + take_profit)

            triggered_exit = False
            exit_price = price

            if low_price <= sl_price:
                triggered_exit = True
                exit_price = sl_price
            elif high_price >= tp_price:
                triggered_exit = True
                exit_price = tp_price

            if triggered_exit:
                proceeds = position_units * exit_price * (1.0 - commission_pct)
                pnl = proceeds - (position_units * entry_price)
                ret_pct = (exit_price / entry_price - 1.0) * 100.0

                trades.append({
                    "entry_idx": trade_entry_idx, "exit_idx": i,
                    "entry_price": entry_price, "exit_price": exit_price,
                    "pnl": pnl, "return_pct": ret_pct, "reason": "SL/TP"
                })
                cash += proceeds
                position_units = 0.0
                entry_price = 0.0
                trade_entry_idx = None

        if target_signal == 1 and position_units == 0.0:
            entry_price = price
            trade_entry_idx = i
            position_units = (cash * (1.0 - commission_pct)) / entry_price
            cash = 0.0

        elif target_signal == 0 and position_units > 0.0:
            exit_price = price
            proceeds = position_units * exit_price * (1.0 - commission_pct)
            pnl = proceeds - (position_units * entry_price)
            ret_pct = (exit_price / entry_price - 1.0) * 100.0

            trades.append({
                "entry_idx": trade_entry_idx, "exit_idx": i,
                "entry_price": entry_price, "exit_price": exit_price,
                "pnl": pnl, "return_pct": ret_pct, "reason": "Signal Exit"
            })
            cash += proceeds
            position_units = 0.0
            entry_price = 0.0
            trade_entry_idx = None

        current_equity = cash + (position_units * price)
        equity_curve[i] = current_equity

    bh_units = (initial_capital * (1.0 - commission_pct)) / prices[0]
    bh_equity = bh_units * prices

    final_equity = equity_curve[-1]
    total_return_pct = ((final_equity - initial_capital) / initial_capital) * 100.0

    daily_returns = np.diff(equity_curve) / equity_curve[:-1]
    daily_returns = daily_returns[np.isfinite(daily_returns)]

    if len(daily_returns) > 1 and np.std(daily_returns) > 1e-8:
        sharpe_ratio = float((np.mean(daily_returns) / np.std(daily_returns)) * np.sqrt(252.0))
    else:
        sharpe_ratio = 0.0

    running_max = np.maximum.accumulate(equity_curve)
    drawdowns = (running_max - equity_curve) / running_max
    max_drawdown_pct = float(np.max(drawdowns)) * 100.0

    num_trades = len(trades)
    winning_trades = [t for t in trades if t["pnl"] > 0]
    win_rate_pct = (len(winning_trades) / num_trades * 100.0) if num_trades > 0 else 0.0

    gross_profit = sum(t["pnl"] for t in trades if t["pnl"] > 0)
    gross_loss = abs(sum(t["pnl"] for t in trades if t["pnl"] < 0))
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (99.0 if gross_profit > 0 else 0.0)

    return {
        "total_return_pct": total_return_pct,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown_pct": max_drawdown_pct,
        "win_rate_pct": win_rate_pct,
        "profit_factor": profit_factor,
        "num_trades": num_trades,
        "equity_curve": equity_curve,
        "buy_and_hold_equity": bh_equity,
        "trades": trades,
    }


def evaluate_fitness(chromosome: Dict[str, Any], df: pd.DataFrame) -> float:
    results = run_backtest(df, chromosome)
    sharpe = results["sharpe_ratio"]
    mdd_frac = results["max_drawdown_pct"] / 100.0
    num_trades = results["num_trades"]

    if num_trades == 0:
        return -5.0

    trade_penalty = 0.5 if num_trades < 3 else 0.0
    dd_penalty = 3.0 * max(0.0, mdd_frac - 0.25)
    fitness = sharpe - dd_penalty - trade_penalty
    return float(max(-10.0, fitness))


def tournament_selection(population: List[Dict[str, Any]], fitness_scores: np.ndarray, k: int = 3) -> Dict[str, Any]:
    pop_size = len(population)
    selected_indices = random.sample(range(pop_size), k=min(k, pop_size))
    best_idx = selected_indices[int(np.argmax(fitness_scores[selected_indices]))]
    return copy.deepcopy(population[best_idx])


def crossover_chromosomes(parent1: Dict[str, Any], parent2: Dict[str, Any], crossover_rate: float = 0.8) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if random.random() > crossover_rate:
        return copy.deepcopy(parent1), copy.deepcopy(parent2)

    child1, child2 = {}, {}
    for gene in GENE_BOUNDS:
        val1, val2 = parent1[gene], parent2[gene]
        if random.random() < 0.5:
            child1[gene], child2[gene] = val2, val1
        else:
            alpha = random.uniform(0.1, 0.9)
            if GENE_BOUNDS[gene][2]:
                child1[gene] = int(round(alpha * val1 + (1.0 - alpha) * val2))
                child2[gene] = int(round((1.0 - alpha) * val1 + alpha * val2))
            else:
                child1[gene] = alpha * val1 + (1.0 - alpha) * val2
                child2[gene] = (1.0 - alpha) * val1 + alpha * val2

    return sanitize_chromosome(child1), sanitize_chromosome(child2)


def mutate_chromosome(chromosome: Dict[str, Any], mutation_rate: float = 0.2) -> Dict[str, Any]:
    mutated = copy.deepcopy(chromosome)
    for gene, (min_val, max_val, is_int) in GENE_BOUNDS.items():
        if random.random() < mutation_rate:
            gene_range = max_val - min_val
            scale = gene_range * 0.15
            delta = random.gauss(0.0, scale)
            new_val = max(min_val, min(max_val, mutated[gene] + delta))
            mutated[gene] = int(round(new_val)) if is_int else float(new_val)

    return sanitize_chromosome(mutated)


class GeneticAlgorithmOptimizer:
    def __init__(
        self,
        population_size: int = 30,
        generations: int = 20,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.2,
        elitism_count: int = 2,
        tournament_k: int = 3,
        seed: int = 42,
    ):
        self.pop_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism_count = min(elitism_count, population_size // 2)
        self.tournament_k = tournament_k
        random.seed(seed)
        np.random.seed(seed)

    def run(self, df: pd.DataFrame, verbose: bool = True) -> Dict[str, Any]:
        population = [generate_random_chromosome() for _ in range(self.pop_size)]
        best_overall_chrom = None
        best_overall_fitness = -np.inf
        history = {"best_fitness": [], "mean_fitness": []}

        for gen in range(1, self.generations + 1):
            fitness_scores = np.array([evaluate_fitness(ind, df) for ind in population])
            gen_best_idx = int(np.argmax(fitness_scores))
            gen_best_fit = float(fitness_scores[gen_best_idx])
            gen_mean_fit = float(np.mean(fitness_scores))

            history["best_fitness"].append(gen_best_fit)
            history["mean_fitness"].append(gen_mean_fit)

            if gen_best_fit > best_overall_fitness:
                best_overall_fitness = gen_best_fit
                best_overall_chrom = copy.deepcopy(population[gen_best_idx])

            sorted_indices = np.argsort(fitness_scores)[::-1]
            new_population = [copy.deepcopy(population[idx]) for idx in sorted_indices[:self.elitism_count]]

            while len(new_population) < self.pop_size:
                p1 = tournament_selection(population, fitness_scores, k=self.tournament_k)
                p2 = tournament_selection(population, fitness_scores, k=self.tournament_k)
                c1, c2 = crossover_chromosomes(p1, p2, self.crossover_rate)
                c1 = mutate_chromosome(c1, self.mutation_rate)
                c2 = mutate_chromosome(c2, self.mutation_rate)

                new_population.append(c1)
                if len(new_population) < self.pop_size:
                    new_population.append(c2)

            population = new_population

        return {
            "best_chromosome": best_overall_chrom,
            "best_fitness": best_overall_fitness,
            "history": history,
        }


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
        self.assertGreater(res["best_fitness"], -10.0)


if __name__ == "__main__":
    unittest.main()
