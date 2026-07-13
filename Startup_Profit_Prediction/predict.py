"""
Inference script for Startup Profit Prediction.
Loads a serialized model (Linear, Lasso, or Ridge Regression) and predicts profit.
"""
import argparse
from pathlib import Path
import pandas as pd

import utils

# Resolve defaults relative to script location
DEFAULT_BASE_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL_DIR = DEFAULT_BASE_DIR / "models"

# Mapping model identifiers to serialized file names
MODEL_FILES = {
    "linear": "linear_regression.joblib",
    "lasso": "lasso_regression.joblib",
    "ridge": "ridge_regression.joblib",
}


def predict_profit(
    rd_spend: float,
    admin_spend: float,
    marketing_spend: float,
    state: str,
    model_type: str = "ridge",
    model_dir: Path = DEFAULT_MODEL_DIR,
    model_path: Path = None
) -> tuple:
    """
    Loads selected model and predicts startup profit.

    Parameters:
    -----------
    rd_spend : float
        R&D Spend amount.
    admin_spend : float
        Administration Spend amount.
    marketing_spend : float
        Marketing Spend amount.
    state : str
        State location (e.g., 'New York', 'California', 'Florida').
    model_type : str
        Name of the model to load: 'linear', 'lasso', or 'ridge'.
    model_dir : Path
        Directory where serialized models are stored. Ignored if model_path is explicitly set.
    model_path : Path (optional)
        Direct path to a joblib model file.

    Returns:
    --------
    tuple (float, str)
        Predicted profit and the name of the model version used.
    """
    # 1. Resolve model file path
    if model_path is not None:
        resolved_path = Path(model_path)
        model_name_label = resolved_path.name
    else:
        model_type_key = model_type.lower()
        if model_type_key not in MODEL_FILES:
            raise ValueError(
                f"Unknown model type: '{model_type}'. Choose from: {list(MODEL_FILES.keys())}"
            )
        resolved_path = Path(model_dir) / MODEL_FILES[model_type_key]
        model_name_label = f"{model_type_key.upper()} Regression"

    if not resolved_path.exists():
        raise FileNotFoundError(
            f"Trained model not found at {resolved_path.resolve()}.\n"
            "Please train the models first by running:\n"
            "  python train.py"
        )

    # 2. Formulate individual dataframe input row
    input_data = pd.DataFrame([{
        "R&D Spend": rd_spend,
        "Administration": admin_spend,
        "Marketing Spend": marketing_spend,
        "State": state
    }])

    # 3. Preprocess identically to training
    preprocessed_x = utils.preprocess_data(input_data, is_training=False)

    # 4. Deserialize selected model estimator
    model = utils.load_model(resolved_path)

    # 5. Predict
    prediction = model.predict(preprocessed_x)
    return float(prediction[0]), model_name_label


def main():
    parser = argparse.ArgumentParser(description="Predict profit of a startup using a trained model.")
    parser.add_argument(
        "--rd",
        type=float,
        required=True,
        help="R&D Spend (float value)"
    )
    parser.add_argument(
        "--admin",
        type=float,
        required=True,
        help="Administration Spend (float value)"
    )
    parser.add_argument(
        "--marketing",
        type=float,
        required=True,
        help="Marketing Spend (float value)"
    )
    parser.add_argument(
        "--state",
        type=str,
        required=True,
        help="State of the startup (e.g., 'New York', 'California', 'Florida')"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="ridge",
        choices=list(MODEL_FILES.keys()),
        help="Specific model estimator to load (linear, lasso, ridge) [default: ridge]"
    )
    parser.add_argument(
        "--model-dir",
        type=str,
        default=str(DEFAULT_MODEL_DIR),
        help="Directory containing the model joblib files."
    )
    parser.add_argument(
        "--model-path",
        type=str,
        default=None,
        help="Explicit, direct path to a model joblib file (overrides --model and --model-dir)."
    )

    args = parser.parse_args()

    model_dir = Path(args.model_dir)
    model_path = Path(args.model_path) if args.model_path else None

    try:
        predicted, model_used = predict_profit(
            rd_spend=args.rd,
            admin_spend=args.admin,
            marketing_spend=args.marketing,
            state=args.state,
            model_type=args.model,
            model_dir=model_dir,
            model_path=model_path
        )
        print(f"\n--- Prediction Input ---")
        print(f"R&D Spend:       ${args.rd:,.2f}")
        print(f"Administration:  ${args.admin:,.2f}")
        print(f"Marketing Spend: ${args.marketing:,.2f}")
        print(f"State:           {args.state}")
        print(f"Model Used:      {model_used}")
        print(f"------------------------")
        print(f"Predicted Profit: ${predicted:,.2f}\n")
    except FileNotFoundError as e:
        print(f"\nError: {e}\n")
    except Exception as e:
        print(f"\nAn error occurred during prediction:\n{e}\n")


if __name__ == "__main__":
    main()
