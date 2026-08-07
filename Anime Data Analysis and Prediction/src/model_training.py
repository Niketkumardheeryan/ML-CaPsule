import os
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from src.utils import setup_logger, save_model

logger = setup_logger("ModelTraining")

class ModelTrainer:
    """Class responsible for model training, evaluation, and serialization."""

    def __init__(self, config: Dict[str, Any]):
        """Initializes ModelTrainer with configuration dictionary.

        Args:
            config (Dict[str, Any]): Configuration dictionary.
        """
        self.config = config
        self.random_state = self.config["feature_engineering"].get("random_state", 42)
        self.output_dir = self.config["model_training"].get("output_dir", "Model")

    @staticmethod
    def initialize_models() -> Dict[str, Any]:
        """Initializes candidate regression models.

        Returns:
            Dict[str, Any]: Dictionary mapping model names to model instances.
        """
        return {
            "LinearRegression": LinearRegression(),
            "DecisionTreeRegressor": DecisionTreeRegressor(random_state=42),
            "RandomForestRegressor": RandomForestRegressor(random_state=42),
        }

    def train_and_evaluate(
        self,
        model: Any,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.Series,
        y_test: pd.Series,
    ) -> Dict[str, float]:
        """Fits model on training data and computes evaluation metrics on test data.

        Args:
            model (Any): Regression model instance.
            X_train (pd.DataFrame): Training features.
            X_test (pd.DataFrame): Testing features.
            y_train (pd.Series): Training labels.
            y_test (pd.Series): Testing labels.

        Returns:
            Dict[str, float]: Evaluated metrics (Train Score, R2, MAE, MSE, RMSE).
        """
        model.fit(X_train, y_train)
        train_score = float(model.score(X_train, y_train))
        predictions = model.predict(X_test)

        r2 = float(metrics.r2_score(y_test, predictions))
        mae = float(metrics.mean_absolute_error(y_test, predictions))
        mse = float(metrics.mean_squared_error(y_test, predictions))
        rmse = float(np.sqrt(mse))

        eval_results = {
            "train_score": train_score,
            "r2_score": r2,
            "mae": mae,
            "mse": mse,
            "rmse": rmse,
        }
        return eval_results

    def run_pipeline(
        self,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.Series,
        y_test: pd.Series,
    ) -> Dict[str, Dict[str, Any]]:
        """Runs training, evaluation, and saves trained DecisionTreeRegressor and RandomForestRegressor models.

        Args:
            X_train (pd.DataFrame): Training features.
            X_test (pd.DataFrame): Testing features.
            y_train (pd.Series): Training labels.
            y_test (pd.Series): Testing labels.

        Returns:
            Dict[str, Dict[str, Any]]: Results containing models and evaluation metrics.
        """
        models = self.initialize_models()
        results = {}

        os.makedirs(self.output_dir, exist_ok=True)
        model_1_path = os.path.join(
            self.output_dir, self.config["model_training"].get("model_1_filename", "model_1.pkl")
        )
        model_2_path = os.path.join(
            self.output_dir, self.config["model_training"].get("model_2_filename", "model_2.pkl")
        )

        for name, model in models.items():
            logger.info(f"Training model: {name}")
            eval_metrics = self.train_and_evaluate(model, X_train, X_test, y_train, y_test)
            logger.info(f"=== {name} Metrics ===")
            logger.info(f"Training score: {eval_metrics['train_score']:.4f}")
            logger.info(f"R2 score: {eval_metrics['r2_score']:.4f}")
            logger.info(f"MAE: {eval_metrics['mae']:.4f}")
            logger.info(f"MSE: {eval_metrics['mse']:.4f}")
            logger.info(f"RMSE: {eval_metrics['rmse']:.4f}")

            # Pickle model artifacts
            if name == "DecisionTreeRegressor":
                save_model(model, model_1_path)
                logger.info(f"Saved DecisionTreeRegressor artifact to: {model_1_path}")
            elif name == "RandomForestRegressor":
                save_model(model, model_2_path)
                logger.info(f"Saved RandomForestRegressor artifact to: {model_2_path}")

            results[name] = {"model": model, "metrics": eval_metrics}

        return results
