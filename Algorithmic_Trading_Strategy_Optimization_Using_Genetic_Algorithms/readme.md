# Genetic Algorithm Trading Strategy Optimization (Improved Version)

## Objective

Optimize algorithmic trading strategies using a fully corrected and enhanced Genetic Algorithm (GA) pipeline with proper parameter evolution, realistic backtesting, and risk-adjusted fitness evaluation.

---

## Description

This project improves the original trading strategy optimizer by fixing major architectural, statistical, and backtesting flaws in the Genetic Algorithm implementation.

The previous implementation suffered from multiple critical issues:

* No real evolvable genes
* Mutation producing identical individuals
* Self-pair crossover cloning
* Incorrect RSI implementation
* Look-ahead bias in strategy execution
* Incorrect trade counting
* Non-risk-adjusted fitness evaluation
* Lack of diversity preservation in GA selection

These problems caused the optimizer to converge to meaningless solutions with constant fitness values across generations.

The improved implementation introduces:

* Real-valued evolvable parameter genes
* Gaussian mutation
* Tournament selection
* Elitism preservation
* Annualized Sharpe-ratio fitness
* Correct Wilder RSI computation
* Proper backtesting alignment
* Bias-free signal execution

---

# Major Improvements

## 1. Genetic Representation

* Replaced static function-reference individuals with 6 real-valued numeric genes
* Added proper bounded parameter evolution
* Fixed overlapping RSI threshold ranges
* Expanded threshold search space for high-conviction strategies

## 2. Mutation & Crossover

* Implemented Gaussian mutation with bounded clipping
* Prevented self-pair crossover (`parent1 != parent2`)
* Added tournament selection for improved population diversity
* Added elitism to preserve top-performing individuals

## 3. Fitness Function

* Replaced raw cumulative returns with annualized Sharpe ratio
* Switched from arithmetic returns to log returns
* Added volatility and variance safeguards
* Added proper activity validation

## 4. RSI & Indicator Computation

* Implemented Wilder-style EMA RSI
* Added division-by-zero safeguards
* Fixed flat-market RSI handling (`RSI = 50`)
* Computed indicators directly from close prices instead of relying on CSV columns

## 5. Backtesting & Bias Fixes

* Removed look-ahead bias by shifting execution one bar forward
* Corrected trade counting logic
* Fixed equity curve initialization and alignment
* Corrected mislabeled output columns

## 6. GA Stability Improvements

* Added final-generation evaluation pass
* Added explicit failure diagnostics
* Removed dead global variables
* Improved numerical stability

---

## Steps

1. Load and preprocess historical market data
2. Compute technical indicators (RSI, SMA, MACD)
3. Initialize a population of parameterized trading strategies
4. Evaluate fitness using annualized Sharpe ratio
5. Select high-performing individuals using tournament selection
6. Apply crossover and Gaussian mutation
7. Preserve elite individuals across generations
8. Repeat evolution for multiple generations
9. Backtest the optimized strategy

---

## Requirements

* Python
* NumPy
* Pandas
* Matplotlib

---

## Usage

1. Load historical trading data
2. Configure GA hyperparameters
3. Run the notebook
4. Observe generation-wise fitness evolution
5. Analyze optimized strategy performance
6. Compare strategy equity curve against buy-and-hold benchmark

---

## Result

The optimizer now performs meaningful parameter evolution and produces realistic, risk-adjusted trading strategy evaluation instead of constant zero-fitness outputs.

The improved implementation provides:

* Stable GA convergence
* Proper exploration of parameter space
* Correct backtesting methodology
* More realistic quantitative trading evaluation
