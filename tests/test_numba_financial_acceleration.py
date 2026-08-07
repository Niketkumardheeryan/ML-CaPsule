import json
import time
import unittest
import numpy as np
import pandas as pd
from pathlib import Path
from numba import njit, prange

REPO_ROOT = Path(__file__).resolve().parents[1]

# Dividend Capture Numba functions
@njit(fastmath=True)
def div_fitness_numba(individual, dividends, stock_prices):
    buy_signal = individual[0]
    sell_signal = individual[1]
    capital = 100000.0
    position = 0.0
    returns = 0.0
    n = len(dividends)

    for i in range(n):
        if dividends[i] > buy_signal and position == 0.0:
            position = capital / stock_prices[i]
            capital = 0.0

        if dividends[i] < sell_signal and position > 0.0:
            capital = position * stock_prices[i]
            returns += capital - 100000.0
            position = 0.0

    return returns

@njit(fastmath=True, parallel=True)
def div_eval_pop_numba(population, dividends, stock_prices):
    pop_size = population.shape[0]
    scores = np.empty(pop_size, dtype=np.float64)
    for p in prange(pop_size):
        scores[p] = div_fitness_numba(population[p], dividends, stock_prices)
    return scores

def div_fitness_py(individual, data):
    buy_signal = individual[0]
    sell_signal = individual[1]
    capital = 100000.0
    position = 0.0
    returns = 0.0
    for i in range(len(data)):
        if data['Dividend'][i] > buy_signal and position == 0:
            position = capital / data['Stock_Price'][i]
            capital = 0.0
        if data['Dividend'][i] < sell_signal and position > 0:
            capital = position * data['Stock_Price'][i]
            returns += capital - 100000.0
            position = 0.0
    return returns

# Algorithmic Trading Numba functions
@njit(fastmath=True)
def trade_backtest_numba(chromosome_vec, prices, sma_20, sma_50, rsi, macd_diff):
    rsi_oversold = chromosome_vec[0]
    rsi_overbought = chromosome_vec[1]
    sma_ratio_buy = chromosome_vec[2]
    sma_ratio_sell = chromosome_vec[3]
    macd_diff_buy = chromosome_vec[4]
    macd_diff_sell = chromosome_vec[5]

    n = len(prices)
    position = 0
    equity = 1.0
    equity_curve = np.empty(n)
    daily_returns = np.zeros(n - 1)
    num_trades = 0
    equity_curve[0] = equity

    for i in range(1, n):
        prev = i - 1
        sma_ratio = sma_20[prev] / sma_50[prev] if sma_50[prev] > 1e-12 else 1.0

        buy_votes = (
            (1 if rsi[prev] < rsi_oversold else 0) +
            (1 if sma_ratio > sma_ratio_buy else 0) +
            (1 if macd_diff[prev] > macd_diff_buy else 0)
        )
        sell_votes = (
            (1 if rsi[prev] > rsi_overbought else 0) +
            (1 if sma_ratio < sma_ratio_sell else 0) +
            (1 if macd_diff[prev] < macd_diff_sell else 0)
        )

        day_ret = (prices[i] - prices[prev]) / prices[prev]

        if position == 0 and buy_votes >= 2:
            position = 1
            num_trades += 1
            strat_ret = 0.0
        elif position == 1 and sell_votes >= 2:
            position = 0
            strat_ret = day_ret
        elif position == 1:
            strat_ret = day_ret
        else:
            strat_ret = 0.0

        equity *= (1.0 + strat_ret)
        equity_curve[i] = equity
        daily_returns[i-1] = strat_ret

    peak_val = equity_curve[0]
    max_drawdown = 0.0
    for i in range(n):
        if equity_curve[i] > peak_val:
            peak_val = equity_curve[i]
        dd = (peak_val - equity_curve[i]) / (peak_val if peak_val > 1e-12 else 1.0)
        if dd > max_drawdown:
            max_drawdown = dd

    return num_trades, max_drawdown, equity_curve[n-1] - 1.0, daily_returns

@njit(fastmath=True)
def trade_fitness_numba(chromosome_vec, prices, sma_20, sma_50, rsi, macd_diff):
    num_trades, max_drawdown, total_return, returns = trade_backtest_numba(
        chromosome_vec, prices, sma_20, sma_50, rsi, macd_diff
    )
    if num_trades == 0:
        return -10.0
    if num_trades < 3:
        return -5.0 + num_trades * 0.5

    n_ret = len(returns)
    sum_r = 0.0
    for i in range(n_ret):
        sum_r += returns[i]
    mean_r = sum_r / n_ret

    var_r = 0.0
    for i in range(n_ret):
        diff = returns[i] - mean_r
        var_r += diff * diff
    std_r = np.sqrt(var_r / (n_ret - 1)) if n_ret > 1 else 0.0

    if std_r < 1e-12:
        return -5.0

    sharpe = (mean_r / std_r) * np.sqrt(252.0)
    dd_penalty = (max_drawdown - 0.30) * 3.0 if max_drawdown > 0.30 else 0.0
    return sharpe - dd_penalty

@njit(fastmath=True, parallel=True)
def trade_eval_pop_numba(pop_matrix, prices, sma_20, sma_50, rsi, macd_diff):
    pop_size = pop_matrix.shape[0]
    scores = np.empty(pop_size, dtype=np.float64)
    for i in prange(pop_size):
        scores[i] = trade_fitness_numba(
            pop_matrix[i], prices, sma_20, sma_50, rsi, macd_diff
        )
    return scores

class TestNumbaFinancialAcceleration(unittest.TestCase):

    def test_dividend_capture_numba_parity_and_speedup(self):
        np.random.seed(42)
        dates = pd.date_range(start='2020-01-01', end='2021-12-31', freq='D')
        prices = np.random.uniform(50, 150, len(dates))
        dividends = np.zeros(len(dates))
        div_idx = np.random.choice(len(dates), size=15, replace=False)
        dividends[div_idx] = np.random.uniform(0.5, 2.0, 15)

        data = pd.DataFrame({'Stock_Price': prices, 'Dividend': dividends})
        pop_list = [np.random.uniform(0.01, 2.0, 2) for _ in range(50)]
        pop_mat = np.array(pop_list)

        dividends_arr = dividends.astype(np.float64)
        prices_arr = prices.astype(np.float64)

        # Warmup Numba
        _ = div_eval_pop_numba(pop_mat, dividends_arr, prices_arr)

        # Evaluate Parity
        py_scores = [div_fitness_py(ind, data) for ind in pop_list]
        nb_scores = div_eval_pop_numba(pop_mat, dividends_arr, prices_arr)
        np.testing.assert_allclose(py_scores, nb_scores, rtol=1e-5, atol=1e-5)

        # Benchmark Speedup
        t0 = time.perf_counter()
        for _ in range(20):
            _ = [div_fitness_py(ind, data) for ind in pop_list]
        t_py = time.perf_counter() - t0

        t0 = time.perf_counter()
        for _ in range(20):
            _ = div_eval_pop_numba(pop_mat, dividends_arr, prices_arr)
        t_nb = time.perf_counter() - t0

        speedup = t_py / t_nb if t_nb > 0 else 100.0
        self.assertGreater(speedup, 5.0, f"Expected speedup > 5x, got {speedup:.1f}x")

    def test_algorithmic_trading_numba_parity_and_speedup(self):
        np.random.seed(42)
        n = 200
        prices = np.random.uniform(10, 100, n)
        sma_20 = np.random.uniform(10, 100, n)
        sma_50 = np.random.uniform(10, 100, n)
        rsi = np.random.uniform(10, 90, n)
        macd_diff = np.random.uniform(-5, 5, n)

        pop_mat = np.random.uniform(0.1, 1.0, (50, 6))

        # Warmup
        _ = trade_eval_pop_numba(pop_mat, prices, sma_20, sma_50, rsi, macd_diff)
        scores = trade_eval_pop_numba(pop_mat, prices, sma_20, sma_50, rsi, macd_diff)

        self.assertEqual(len(scores), 50)
        self.assertFalse(np.isnan(scores).any())

    def test_notebooks_contain_numba_acceleration(self):
        div_nb = REPO_ROOT / "Optimizing_Dividend_Capture_Strategies_Using_Genetics_Algorithms" / "Optimizing_Dividend_Capture_Strategies_Using_Genetics_Algorithms.ipynb"
        trade_nb = REPO_ROOT / "Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms" / "Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms (1).ipynb"

        for nb_path in [div_nb, trade_nb]:
            self.assertTrue(nb_path.exists(), f"Notebook {nb_path} does not exist")
            with open(nb_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("numba", content.lower())
            self.assertIn("@njit", content)

if __name__ == "__main__":
    unittest.main()
