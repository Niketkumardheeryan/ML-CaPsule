import os
import sys
import logging
import yaml
# Define directory and file path for storing execution logs
LOG_DIR = "logs"
LOG_FILEPATH = os.path.join(LOG_DIR, "running_logs.log")

# Create the logs directory if it does not already exist
os.makedirs(LOG_DIR, exist_ok=True)

# Configure the global logging settings
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILEPATH),
        logging.StreamHandler(sys.stdout)
    ]
)

# Initialize the logger object to be imported across modules
logger = logging.getLogger("anime_pipeline")
def read_yaml(path_to_yaml: str) -> dict:
    """Reads a YAML file and returns its contents as a dictionary.

    Args:
        path_to_yaml (str): Path to the yaml file.

    Returns:
        dict: Dictionary containing configuration parameters.
    """
    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file: {path_to_yaml} loaded successfully")
            return content
    except Exception as e:
        logger.error(f"Error reading yaml file at {path_to_yaml}: {e}")
        raise e

def create_directories(path_to_directories: list) -> None:
    """Creates a list of directories if they do not exist.

    Args:
        path_to_directories (list): List of paths to create.
    """
    for path in path_to_directories:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            logger.info(f"Created directory at: {path}")