import os
import pickle
import logging
from typing import Any, Dict
import yaml

def setup_logger(name: str = "AnimePipeline", level: int = logging.INFO) -> logging.Logger:
    """Configures and returns a structured logger.

    Args:
        name (str): Name of the logger.
        level (int): Logging level (e.g. logging.INFO).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger

def load_config(config_path: str) -> Dict[str, Any]:
    """Loads YAML configuration file.

    Args:
        config_path (str): Path to YAML config file.

    Returns:
        Dict[str, Any]: Configuration dictionary.

    Raises:
        FileNotFoundError: If configuration file does not exist.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def save_model(model: Any, filepath: str) -> None:
    """Pickles and saves a trained machine learning model to disk.

    Args:
        model (Any): Trained ML model object.
        filepath (str): Target destination file path.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as file:
        pickle.dump(model, file)

def load_model(filepath: str) -> Any:
    """Loads a pickled machine learning model from disk.

    Args:
        filepath (str): Path to serialized model file.

    Returns:
        Any: Unpickled ML model object.

    Raises:
        FileNotFoundError: If model file does not exist.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model file not found at: {filepath}")
    with open(filepath, "rb") as file:
        return pickle.load(file)
