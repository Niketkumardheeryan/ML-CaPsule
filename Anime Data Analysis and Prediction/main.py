import os
import argparse
from src.utils import setup_logger, load_config
from src.data_ingestion import DataIngestion
from src.feature_engineering import FeatureEngineer
from src.model_training import ModelTrainer

logger = setup_logger("MainPipeline")

def run_pipeline(config_path: str) -> None:
    """Orchestrates end-to-end anime data ingestion, feature engineering, and model training pipeline.

    Args:
        config_path (str): Path to configuration YAML file.
    """
    logger.info("Starting Anime Data Analysis and Prediction Pipeline")
    config = load_config(config_path)

    # 1. Data Ingestion & Preprocessing
    ingestion = DataIngestion(config)
    raw_df = ingestion.load_data()
    cleaned_df = ingestion.clean_data(raw_df)
    filtered_df = ingestion.filter_data(cleaned_df)

    # 2. Feature Engineering & Split
    engineer = FeatureEngineer(config)
    genre_filtered_df = engineer.filter_genres(filtered_df)
    encoded_df = engineer.encode_features(genre_filtered_df)
    X_train, X_test, y_train, y_test = engineer.prepare_train_test_split(encoded_df)

    # 3. Model Training & Evaluation
    trainer = ModelTrainer(config)
    results = trainer.run_pipeline(X_train, X_test, y_train, y_test)

    logger.info("Pipeline execution completed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Anime Data Analysis and Prediction Pipeline")
    default_config = os.path.join(os.path.dirname(__file__), "config", "config.yaml")
    parser.add_argument(
        "--config",
        type=str,
        default=default_config,
        help="Path to YAML configuration file",
    )
    args = parser.parse_args()
    run_pipeline(args.config)
