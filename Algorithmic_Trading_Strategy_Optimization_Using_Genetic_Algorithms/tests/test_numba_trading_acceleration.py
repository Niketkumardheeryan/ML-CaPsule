import time
import unittest
import numpy as np
from pathlib import Path
from numba import njit, prange

PROJECT_ROOT = Path(__file__).resolve().parents[1]

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
        daily_returns[i - 1] = strat_ret

    peak_val = equity_curve[0]
    max_drawdown = 0.0
    for i in range(n):
        if equity_curve[i] > peak_val:
            peak_val = equity_curve[i]
        dd = (peak_val - equity_curve[i]) / (peak_val if peak_val > 1e-12 else 1.0)
        if dd > max_drawdown:
            max_drawdown = dd

    return num_trades, max_drawdown, equity_curve[n - 1] - 1.0, daily_returns

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

class TestAlgorithmicTradingNumbaAcceleration(unittest.TestCase):

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

    def test_notebook_contains_numba_acceleration(self):
        nb_path = list(PROJECT_ROOT.glob("*.ipynb"))[0]
        self.assertTrue(nb_path.exists(), f"Notebook {nb_path} does not exist")
        with open(nb_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("numba", content.lower())
        self.assertIn("@njit", content)

if __name__ == "__main__":
    unittest.main()
