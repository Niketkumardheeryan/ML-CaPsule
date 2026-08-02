"""
Backtesting Simulator & Performance Evaluation Engine.

Provides event-driven position backtesting with Stop-Loss, Take-Profit execution,
equity curve generation, and realistic performance metric calculation (Total Return, Sharpe Ratio,
Max Drawdown, Win Rate, Profit Factor).
"""

from typing import Any, Dict
import numpy as np
import pandas as pd
from .strategy import generate_signals


def run_backtest(
    df: pd.DataFrame,
    chromosome: Dict[str, Any],
    initial_capital: float = 10000.0,
    commission_pct: float = 0.0005,
) -> Dict[str, Any]:
    """
    Backtest a strategy chromosome on an OHLCV dataset.

    Parameters
    ----------
    df : pd.DataFrame
        OHLCV DataFrame.
    chromosome : Dict[str, Any]
        Strategy chromosome containing stop_loss_pct and take_profit_pct.
    initial_capital : float
        Starting portfolio capital in USD.
    commission_pct : float
        Slippage/commission fee per trade as a fraction (e.g., 0.0005 = 0.05%).

    Returns
    -------
    Dict[str, Any]
        Dictionary containing backtest metrics, equity curve, buy-and-hold equity, and trade log.
    """
    data = generate_signals(df, chromosome)
    n = len(data)

    prices = data["Close"].values
    highs = data["High"].values
    lows = data["Low"].values
    signals = data["Signal"].values
    dates = data["Date"].dt.strftime("%Y-%m-%d").values if "Date" in data.columns else np.arange(n)

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

        # Intra-trade Stop-Loss / Take-Profit check if in position
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

                trades.append(
                    {
                        "entry_idx": trade_entry_idx,
                        "exit_idx": i,
                        "entry_date": dates[trade_entry_idx],
                        "exit_date": dates[i],
                        "entry_price": entry_price,
                        "exit_price": exit_price,
                        "pnl": pnl,
                        "return_pct": ret_pct,
                        "reason": "SL/TP",
                    }
                )

                cash += proceeds
                position_units = 0.0
                entry_price = 0.0
                trade_entry_idx = None

        # Execute signals if position state changed
        if target_signal == 1 and position_units == 0.0:
            # Enter Long Position
            entry_price = price
            trade_entry_idx = i
            position_units = (cash * (1.0 - commission_pct)) / entry_price
            cash = 0.0

        elif target_signal == 0 and position_units > 0.0:
            # Exit Long Position
            exit_price = price
            proceeds = position_units * exit_price * (1.0 - commission_pct)
            pnl = proceeds - (position_units * entry_price)
            ret_pct = (exit_price / entry_price - 1.0) * 100.0

            trades.append(
                {
                    "entry_idx": trade_entry_idx,
                    "exit_idx": i,
                    "entry_date": dates[trade_entry_idx],
                    "exit_date": dates[i],
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "pnl": pnl,
                    "return_pct": ret_pct,
                    "reason": "Signal Exit",
                }
            )

            cash += proceeds
            position_units = 0.0
            entry_price = 0.0
            trade_entry_idx = None

        # Record daily equity
        current_equity = cash + (position_units * price)
        equity_curve[i] = current_equity

    # Compute Buy & Hold Baseline Equity Curve
    bh_units = (initial_capital * (1.0 - commission_pct)) / prices[0]
    bh_equity = bh_units * prices

    # Calculate Performance Metrics
    final_equity = equity_curve[-1]
    total_return_pct = ((final_equity / initial_capital) - 1.0) * 100.0

    # Daily Returns & Sharpe Ratio
    daily_returns = np.diff(equity_curve) / equity_curve[:-1]
    daily_returns = daily_returns[~np.isnan(daily_returns)]

    if len(daily_returns) > 0 and np.std(daily_returns) > 1e-8:
        sharpe_ratio = float((np.mean(daily_returns) / np.std(daily_returns)) * np.sqrt(252))
    else:
        sharpe_ratio = 0.0

    # Maximum Drawdown
    running_max = np.maximum.accumulate(equity_curve)
    drawdowns = (running_max - equity_curve) / running_max
    max_drawdown_pct = float(np.max(drawdowns)) * 100.0

    # Win Rate & Profit Factor
    num_trades = len(trades)
    if num_trades > 0:
        winning_trades = [t for t in trades if t["pnl"] > 0]
        losing_trades = [t for t in trades if t["pnl"] < 0]
        win_rate_pct = (len(winning_trades) / num_trades) * 100.0

        gross_profit = sum(t["pnl"] for t in winning_trades)
        gross_loss = abs(sum(t["pnl"] for t in losing_trades))

        if gross_loss > 0:
            profit_factor = gross_profit / gross_loss
        else:
            profit_factor = float(gross_profit) if gross_profit > 0 else 0.0
    else:
        win_rate_pct = 0.0
        profit_factor = 0.0

    return {
        "initial_capital": initial_capital,
        "final_equity": final_equity,
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
