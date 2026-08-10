from pathlib import Path

import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "financial_data.csv"
MODEL_PATH = PROJECT_DIR / "financial_model.keras"
FEATURE_COLUMNS = ["Revenue", "Expenses", "Profit", "Assets", "Liabilities"]
TARGET_COLUMN = "Equity"
RANDOM_STATE = 42


def main():
    tf.keras.utils.set_random_seed(RANDOM_STATE)
    data = pd.read_csv(DATA_PATH)
    X_train, _, y_train, _ = train_test_split(
        data[FEATURE_COLUMNS],
        data[TARGET_COLUMN],
        test_size=0.2,
        random_state=RANDOM_STATE,
    )

    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(len(FEATURE_COLUMNS),)),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(1),
        ]
    )
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    model.fit(X_train_scaled, y_train, epochs=200, batch_size=8, verbose=0)
    model.save(MODEL_PATH)
    print(f"Saved a valid Keras model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
