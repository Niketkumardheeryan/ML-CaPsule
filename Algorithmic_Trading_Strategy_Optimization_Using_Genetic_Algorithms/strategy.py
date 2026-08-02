"""
Strategy Gene Representation & Signal Generation Module.

Defines numerical strategy chromosomes, gene boundary specifications, validation/sanitization logic,
and trading signal generation based on RSI, SMA, MACD, and Risk Management parameters.
"""

import random
from typing import Any, Dict
import numpy as np
import pandas as pd
from .data_loader import compute_all_indicators

# Definition of numerical gene bounds: (min_val, max_val, is_integer)
GENE_BOUNDS: Dict[str, tuple[float, float, bool]] = {
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


def sanitize_chromosome(chrom: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize gene values by clamping to valid boundaries and enforcing structural rules.

    Parameters
    ----------
    chrom : Dict[str, Any]
        Raw strategy chromosome dictionary.

    Returns
    -------
    Dict[str, Any]
        Sanitized chromosome dictionary.
    """
    clean_chrom = {}
    for gene, (min_val, max_val, is_int) in GENE_BOUNDS.items():
        val = float(chrom.get(gene, (min_val + max_val) / 2.0))
        val = max(min_val, min(max_val, val))
        if is_int:
            val = int(round(val))
        clean_chrom[gene] = val

    # Structural constraints enforcement
    if clean_chrom["rsi_buy_threshold"] >= clean_chrom["rsi_sell_threshold"]:
        clean_chrom["rsi_buy_threshold"] = clean_chrom["rsi_sell_threshold"] - 5.0

    if clean_chrom["sma_short_period"] >= clean_chrom["sma_long_period"]:
        clean_chrom["sma_long_period"] = clean_chrom["sma_short_period"] + 5.0

    if clean_chrom["macd_fast"] >= clean_chrom["macd_slow"]:
        clean_chrom["macd_slow"] = clean_chrom["macd_fast"] + 2.0

    return clean_chrom


def generate_random_chromosome() -> Dict[str, Any]:
    """
    Generate a diverse individual strategy chromosome initialized within numerical gene bounds.

    Returns
    -------
    Dict[str, Any]
        Randomized valid strategy chromosome.
    """
    chrom = {}
    for gene, (min_val, max_val, is_int) in GENE_BOUNDS.items():
        if is_int:
            val = random.randint(int(min_val), int(max_val))
        else:
            val = random.uniform(min_val, max_val)
        chrom[gene] = val

    return sanitize_chromosome(chrom)


def generate_signals(df: pd.DataFrame, chromosome: Dict[str, Any]) -> pd.DataFrame:
    """
    Generate dynamic buy/sell/hold trading signals for a dataset using strategy parameters.

    Parameters
    ----------
    df : pd.DataFrame
        OHLCV market DataFrame.
    chromosome : Dict[str, Any]
        Strategy chromosome containing indicator and risk parameters.

    Returns
    -------
    pd.DataFrame
        DataFrame with computed indicators and 'Signal' column (1 for Long, 0 for Flat).
    """
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
        else:  # current_position == 1
            if sell_score >= 2:
                current_position = 0

        signals[i] = current_position

    data["Signal"] = signals
    return data
