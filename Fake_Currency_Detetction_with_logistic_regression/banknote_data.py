"""Loader for the UCI banknote authentication dataset.

The dataset is the standard benchmark for this problem: 1,372 banknote images
reduced to four statistics computed from a wavelet transform, with a label
saying whether the note was genuine or forged.

| Column   | Meaning                                   |
|----------|-------------------------------------------|
| variance | Variance of the wavelet transformed image |
| skewness | Skewness of the wavelet transformed image |
| kurtosis | Kurtosis of the wavelet transformed image |
| entropy  | Entropy of the image                      |
| class    | 0 = genuine, 1 = forged                   |

It is downloaded on first use and cached next to this file, so no Kaggle
account or API token is needed. Only NumPy is required.
"""

import urllib.request
from pathlib import Path

import numpy as np

COLUMNS = ["variance", "skewness", "kurtosis", "entropy", "class"]
FEATURE_NAMES = COLUMNS[:4]
CLASS_NAMES = {0: "Genuine", 1: "Forged"}

CACHE_PATH = Path(__file__).resolve().parent / "data" / "data_banknote_authentication.csv"

# The UCI archive first, then a well known mirror if it is unreachable.
SOURCES = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00267/"
    "data_banknote_authentication.txt",
    "https://raw.githubusercontent.com/jbrownlee/Datasets/master/"
    "banknote_authentication.csv",
)


def download(cache_path=CACHE_PATH, sources=SOURCES):
    """Fetch the dataset into ``cache_path`` unless it is already there."""
    cache_path = Path(cache_path)
    if cache_path.exists() and cache_path.stat().st_size > 0:
        return cache_path

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    errors = []
    for url in sources:
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                payload = response.read()
            if payload:
                cache_path.write_bytes(payload)
                return cache_path
        except Exception as error:  # try the next mirror
            errors.append(f"{url}: {error}")

    raise RuntimeError(
        "Could not download the banknote dataset. Tried:\n  " + "\n  ".join(errors)
    )


def load_banknote_data(cache_path=CACHE_PATH):
    """Return ``(X, y)`` as float arrays of shape ``(1372, 4)`` and ``(1372,)``."""
    path = download(cache_path)
    table = np.loadtxt(path, delimiter=",", dtype=float)
    return table[:, :4], table[:, 4].astype(int)


def train_test_split(X, y, test_size=0.2, seed=42):
    """Shuffle and split into train/test, keeping the class balance of ``y``.

    Written with NumPy rather than scikit-learn so the whole pipeline stays
    dependency-light and in the spirit of the from-scratch model.
    """
    rng = np.random.default_rng(seed)
    train_index, test_index = [], []

    for label in np.unique(y):
        positions = np.flatnonzero(y == label)
        rng.shuffle(positions)
        cut = int(round(len(positions) * test_size))
        test_index.extend(positions[:cut])
        train_index.extend(positions[cut:])

    train_index = np.array(train_index)
    test_index = np.array(test_index)
    rng.shuffle(train_index)
    rng.shuffle(test_index)
    return X[train_index], X[test_index], y[train_index], y[test_index]


def standardize(train, test):
    """Z-score both splits using only the training statistics.

    Fitting the scaler on the training split alone avoids leaking test
    information into the model.
    """
    mean = train.mean(axis=0)
    std = train.std(axis=0)
    std[std == 0] = 1.0
    return (train - mean) / std, (test - mean) / std, (mean, std)


def summary(X, y):
    """Return a short human readable description of the loaded data."""
    genuine = int((y == 0).sum())
    forged = int((y == 1).sum())
    return (
        f"{len(y)} banknotes, {X.shape[1]} features "
        f"({genuine} genuine / {forged} forged)"
    )
