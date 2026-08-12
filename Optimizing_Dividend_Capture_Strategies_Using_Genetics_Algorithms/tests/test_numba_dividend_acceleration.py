import time
import unittest
import numpy as np
import pandas as pd
from pathlib import Path
from numba import njit, prange

PROJECT_ROOT = Path(__file__).resolve().parents[1]

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

class TestDividendCaptureNumbaAcceleration(unittest.TestCase):

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

    def test_notebook_contains_numba_acceleration(self):
        nb_path = list(PROJECT_ROOT.glob("*.ipynb"))[0]
        self.assertTrue(nb_path.exists(), f"Notebook {nb_path} does not exist")
        with open(nb_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("numba", content.lower())
        self.assertIn("@njit", content)

if __name__ == "__main__":
    unittest.main()
