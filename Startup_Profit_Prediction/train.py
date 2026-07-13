"""
Training script for Startup Profit Prediction models.
Trains Linear Regression, Lasso Regression, and Ridge Regression models,
evaluates their performance, and serializes each trained model to a Joblib file.
"""
import argparse
from pathlib import Path
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import mean_squared_error

import utils

# Resolve defaults relative to script location
DEFAULT_BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = DEFAULT_BASE_DIR / "dataset" / "50_Startups.csv"
DEFAULT_OUTPUT_DIR = DEFAULT_BASE_DIR / "models"


def main():
    parser = argparse.ArgumentParser(
        description="Train and serialize Startup Profit Prediction models (Linear, Lasso, Ridge)."
    )
    parser.add_argument(
        "--data",
        type=str,
        default=str(DEFAULT_DATA_PATH),
        help="Path to the training data CSV."
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Proportion of the dataset to include in the test split (0.0 to 1.0)."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random state seed for train-test split reproducibility."
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory to save the serialized models."
    )

    args = parser.parse_args()

    data_path = Path(args.data)
    output_dir = Path(args.output_dir)

    print(f"Loading dataset from: {data_path}")
    try:
        data = utils.load_dataset(data_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please check the dataset path or ensure the dataset file is in the right directory.")
        return

    print("Preprocessing data...")
    try:
        x, y = utils.preprocess_data(data, is_training=True)
    except Exception as e:
        print(f"Preprocessing error: {e}")
        return

    print(f"Splitting dataset into train/test (test_size={args.test_size}, seed={args.seed})...")
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=args.test_size, random_state=args.seed
    )

    # Dictionary of models to train
    models = {
        "Linear Regression": {
            "instance": LinearRegression(),
            "filename": "linear_regression.joblib",
        },
        "Lasso Regression": {
            "instance": Lasso(),
            "filename": "lasso_regression.joblib",
        },
        "Ridge Regression": {
            "instance": Ridge(),
            "filename": "ridge_regression.joblib",
        },
    }

    print("\nTraining and evaluating models...")
    results = {}

    for name, config in models.items():
        model = config["instance"]
        filename = config["filename"]
        save_path = output_dir / filename

        # Fit model
        model.fit(x_train, y_train)

        # Evaluate performance
        predictions = model.predict(x_test)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        accuracy = model.score(x_train, y_train)

        results[name] = {"rmse": rmse, "accuracy": accuracy}

        # Save serialization object
        try:
            utils.save_model(model, save_path)
            print(f"Saved {name} estimator to: {save_path}")
        except Exception as e:
            print(f"Error saving model {name}: {e}")

    # Output metric table matching notebook styling
    print("\n" + "=" * 65)
    print(f"{'Model':<22} | {'RootMeanSquareError':<22} | {'Accuracy of the model':<21}")
    print("=" * 65)
    for name, metrics in results.items():
        print(f"{name:<22} | {metrics['rmse']:<22.4f} | {metrics['accuracy']:<21.4f}")
    print("=" * 65 + "\n")

    print("All models trained and saved successfully!")


if __name__ == "__main__":
    main()
