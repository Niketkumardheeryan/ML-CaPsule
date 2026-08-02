# Algorithmic Trading Strategy Optimization Using Genetic Algorithms

A production-grade, extensible framework for evolving algorithmic trading strategies using **Real Parameter Evolution with Genetic Algorithms (GA)**.

---

## Architecture & Features

This module replaces static demo functions with real numerical gene evolution across multi-indicator trading rules and risk management criteria.

### Real Parameter Evolution (Chromosome Genes)
Each individual in the population encodes numerical strategy parameters:
- **RSI Thresholds**: `rsi_buy_threshold` (15-45) and `rsi_sell_threshold` (55-85)
- **Moving Average Windows**: `sma_short_period` (5-30) and `sma_long_period` (35-100)
- **MACD Parameters**: `macd_fast` (8-16), `macd_slow` (20-40), `macd_signal` (5-15)
- **Risk Management**: `stop_loss_pct` (1%-10%) and `take_profit_pct` (2%-25%)

### Core Components
1. **Data Preprocessing & Validation (`data_loader.py`)**: Loads OHLCV datasets, validates price integrity (`High >= max(Open, Close)` and `Low <= min(Open, Close)`), handles missing values, and computes SMA, RSI, and MACD indicators.
2. **Strategy Gene & Signal Generator (`strategy.py`)**: Evaluates multi-condition indicator rules with strict boundary sanitization.
3. **Backtesting Simulator (`backtest.py`)**: Event-driven backtester supporting Stop-Loss / Take-Profit intra-trade exits and calculating:
   - Total Return (%)
   - Risk-Adjusted Sharpe Ratio
   - Maximum Drawdown (MDD %)
   - Win Rate (%)
   - Profit Factor
4. **Genetic Algorithm Optimizer (`ga_optimizer.py`)**: Diverse random population initialization, multi-component fitness function, tournament selection, uniform/blend crossover (BLX-$\alpha$), bounded Gaussian jitter mutation, and elitism preservation.
5. **Visualization Engine (`visualizer.py`)**: Automatically plots GA fitness convergence, In-Sample/Out-of-Sample Equity Curves against Buy & Hold baselines, and performance dashboard charts.

---

## Quick Start

### Installation
Ensure dependencies are installed:
```bash
pip install numpy pandas matplotlib
```

### Run Optimization Pipeline
To execute the full end-to-end GA optimization, backtesting, and visualization:
```bash
python Algorithmic_Trading_Strategy_Optimization_Using_Genetic_Algorithms/main.py
```

---

## Unit Tests

Run unit tests to verify data loading, indicator calculations, backtesting metrics, crossover/mutation, and GA convergence:
```bash
python -m unittest tests/test_ga_trading_strategy.py
```

---

## Sample Output Charts
Executing `main.py` generates the following visualizations:
- `ga_fitness_progression.png`: Convergence curve of Best & Mean fitness per generation.
- `equity_curves.png`: Strategy equity vs. Buy & Hold benchmark on Train & Test splits.
- `strategy_dashboard.png`: Summary metric dashboard.