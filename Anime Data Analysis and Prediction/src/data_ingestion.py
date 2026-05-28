import os
import pandas as pd
from src.utils import read_yaml, create_directories, logger

def initiate_data_ingestion(config_path: str = "config/config.yaml") -> str:
    """Loads raw data from source and stores it in artifacts.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        str: Path to the ingested raw data file.
    """
    logger.info("Starting Data Ingestion stage...")
    try:
        config = read_yaml(config_path)
        
        raw_data_path = config["artifacts"]["raw_data_path"]
        ingested_data_dir = config["artifacts"]["ingested_data_dir"]
        
        create_directories([ingested_data_dir])
        
        logger.info(f"Reading raw data from {raw_data_path}")
        df = pd.read_csv(raw_data_path)
        
        raw_file_name = os.path.basename(raw_data_path)
        save_path = os.path.join(ingested_data_dir, raw_file_name)
        
        df.to_csv(save_path, index=False)
        logger.info(f"Data Ingestion completed successfully. File saved at {save_path}")
        
        return save_path
        
    except Exception as e:
        logger.error(f"Exception occurred during Data Ingestion: {e}")
        raise e

if __name__ == "__main__":
    initiate_data_ingestion()