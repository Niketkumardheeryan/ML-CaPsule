"""
Data Loader & Preprocessing Module for Algorithmic Trading GA Optimization.

Provides robust dataset loading, OHLCV validation, and technical indicator computation
(SMA, RSI, MACD).
"""

from typing import Union
import numpy as np
import pandas as pd


def load_and_validate_data(source: Union[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Load OHLCV dataset from CSV file or DataFrame and perform validation.

    Parameters
    ----------
    source : str or pd.DataFrame
        File path to CSV or pre-loaded pandas DataFrame.

    Returns
    -------
    pd.DataFrame
        Cleaned, validated OHLCV DataFrame with Date index or column.
    """
    if isinstance(source, str):
        df = pd.read_csv(source)
    elif isinstance(source, pd.DataFrame):
        df = source.copy()
    else:
        raise ValueError("Source must be a file path string or pandas DataFrame.")

    required_cols = ["Open", "High", "Low", "Close"]
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"Missing required column in dataset: '{col}'")

    # Cast price columns to float
    for col in required_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Volume" in df.columns:
        df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce").fillna(0)

    # Date handling
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)

    # Drop NaNs in essential price columns
    df = df.dropna(subset=required_cols).reset_index(drop=True)

    if len(df) == 0:
        raise ValueError("Dataset is empty after dropping missing values.")

    # Validate and sanitize OHLC integrity
    # Ensure High is at least max(Open, Close) and Low is at most min(Open, Close)
    high_valid = df["High"] >= np.maximum(df["Open"], df["Close"])
    low_valid = df["Low"] <= np.minimum(df["Open"], df["Close"])

    if not high_valid.all() or not low_valid.all():
        # Sanitize inconsistent records
        df["High"] = np.maximum(df["High"], np.maximum(df["Open"], df["Close"]))
        df["Low"] = np.minimum(df["Low"], np.minimum(df["Open"], df["Close"]))

    return df


def calculate_sma(series: pd.Series, period: int) -> pd.Series:
    """Calculate Simple Moving Average."""
    period = max(1, int(period))
    return series.rolling(window=period, min_periods=1).mean()


def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index (RSI)."""
    period = max(2, int(period))
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100.0 - (100.0 / (1.0 + rs))

    # Fill initial NaNs with neutral 50
    return rsi.fillna(50.0)


def calculate_macd(
    series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculate MACD Line, Signal Line, and Histogram (Diff).

    Returns
    -------
    tuple[pd.Series, pd.Series, pd.Series]
        (macd_line, signal_line, macd_histogram)
    """
    fast = max(2, int(fast))
    slow = max(fast + 1, int(slow))
    signal = max(2, int(signal))

    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
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
    """
    Compute technical indicators and append them to DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with SMA, RSI, and MACD columns added.
    """
    data = df.copy()
    data["SMA_Short"] = calculate_sma(data["Close"], sma_short)
    data["SMA_Long"] = calculate_sma(data["Close"], sma_long)
    data["RSI"] = calculate_rsi(data["Close"], rsi_period)

    macd_line, signal_line, macd_hist = calculate_macd(
        data["Close"], fast=macd_fast, slow=macd_slow, signal=macd_signal
    )
    data["MACD_Line"] = macd_line
    data["MACD_Signal"] = signal_line
    data["MACD_Hist"] = macd_hist

    return data
