# Algorithmic Trading Strategy Optimization Using Genetic Algorithms

A production-grade, extensible framework for evolving algorithmic trading strategies using **Real Parameter Evolution with Genetic Algorithms (GA)** embedded inside a self-contained Jupyter Notebook.

---

## Dataset Link
- **Raw Market Dataset**: [trading_data.csv](https://raw.githubusercontent.com/Rakshak05/ML-CaPsule/master/Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms/trading_data.csv)

---

## Project Structure
```text
Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms/
├── tests/
│   └── test_ga_trading_strategy.py                        # Unit tests suite
├── Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms.ipynb # Single executed codebase notebook
├── GA_Trading_Strategy_Report.pdf                         # Comprehensive technical report
└── readme.md                                              # Project documentation
```

---

## Core Pipeline Components (Notebook)

1. **Data Ingestion & Indicator Computation**: Direct URL loading, OHLC integrity validation (`High >= max(Open, Close)` and `Low <= min(Open, Close)`), and derivation of `SMA`, `RSI`, and `MACD` indicators.
2. **Strategy Chromosome Representation**: 9 numerical strategy parameters encoding indicator trigger thresholds (`RSI`, `SMA`, `MACD`) and risk management controls (`Stop-Loss` / `Take-Profit`).
3. **Event-Driven Backtester**: Simulates trades with intra-trade Stop-Loss and Take-Profit exits, computing Total Return, Sharpe Ratio, Maximum Drawdown, Win Rate, and Profit Factor.
4. **Genetic Algorithm Optimizer**: Evolves population parameters across generations using tournament selection, BLX-$\alpha$ crossover, bounded Gaussian mutation, and elitism.
5. **Visual Evaluation & Dashboard**: Renders inline Matplotlib charts for GA fitness convergence, In-Sample & Out-of-Sample equity curves against Buy & Hold benchmarks, and performance metric bar charts.

---

## Quick Start

### Installation
Ensure required libraries are installed:
```bash
pip install numpy pandas matplotlib jupyter
```

### Running the Notebook
Open and execute all cells in Jupyter Notebook or JupyterLab:
```bash
jupyter notebook Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms/Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms.ipynb
```

---

## Unit Tests

Run the test suite inside the project directory:
```bash
python -m unittest Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms/tests/test_ga_trading_strategy.py
```
