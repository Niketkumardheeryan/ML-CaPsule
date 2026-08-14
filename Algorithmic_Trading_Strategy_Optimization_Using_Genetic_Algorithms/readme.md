# Algorithmic Trading Strategy Optimization Using Genetic Algorithms (Numba-JIT Accelerated)

## Objective
Optimize algorithmic trading strategies using Genetic Algorithms (GA) with **Numba-JIT compiler acceleration**.

## Description
This project leverages Genetic Algorithms to discover optimal technical indicator decision thresholds (RSI, SMA ratios, MACD signal differentials) for long-only trading strategies. Core fitness evaluations and backtesting iterations are accelerated using **Numba JIT compilation** (`@njit(fastmath=True, parallel=True)`), converting heavy Python loops into C-level machine instructions for 300x-1000x computational speedup.

## Steps & Methodology
1. **Data Preprocessing**: Compute technical indicators (RSI, SMA-20, SMA-50, MACD) on historical asset data.
2. **Chromosome Encoding**: Represent trading strategies as 6 real-valued decision threshold genes.
3. **Numba-JIT Fitness Evaluation**: Compute Sharpe Ratios and drawdown penalties at C-level speeds using raw NumPy array passing and parallel CPU multithreading.
4. **GA Operators**: Apply Tournament Selection, BLX-α (Blend) Crossover, Gaussian Mutation, and 10% Elitism.
5. **Generational Optimization**: Evolve population over 60-100 generations.
6. **Out-of-Sample Backtesting**: Validate evolved strategies on a 70/30 train-test split against a Buy-and-Hold baseline.

## Requirements
- Python 3.8+
- NumPy
- Pandas
- Numba >= 0.58.0
- Matplotlib

## Usage
1. Open and execute `Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms (1).ipynb`.
2. Review technical indicator calculations, Chromosome gene mappings, and JIT-compiled backtest functions.
3. Run the **Numba-JIT Benchmark Cell** to observe 100-generation simulation speedups vs. native Python.
4. Train the GA model on the 70% historical split and evaluate test performance.

## Benchmark Results

Testing over a **100-generation simulation pass** (80 individuals = 8,000 backtests) on financial market data:

| Execution Engine | 100-Generation Time | Speedup Factor | Numerical Parity |
| :--- | :--- | :--- | :--- |
| Native Python Loops | ~4,170 - 16,890 ms | 1.0x (Baseline) | Exact |
| **Numba-JIT (Parallel)** | **~12 - 15 ms** | **>300x - 1,000x** | **Exact** |