import os
import pandas as pd
import numpy as np
from src.utils import read_yaml, create_directories, logger

def initiate_feature_engineering(config_path: str = "config/config.yaml") -> None:
    """Handles data filtering and performs dummy encoding transformations.

    Args:
        config_path (str): Path to the configuration file.
    """
    logger.info("Starting Feature Engineering stage...")
    try:
        config = read_yaml(config_path)
        processed_data_dir = config["artifacts"]["processed_data_dir"]
        ingested_data_dir = config["artifacts"]["ingested_data_dir"]
        raw_data_path = config["artifacts"]["raw_data_path"]
        
        raw_file_name = os.path.basename(raw_data_path)
        input_data_path = os.path.join(ingested_data_dir, raw_file_name)
        
        df = pd.read_csv(input_data_path)
        
        # 1. Rename Name_of_Anime to name as per notebook structure
        if "Name_of_Anime" in df.columns:
            df.rename(columns={"Name_of_Anime": "name"}, inplace=True)
            
        # 2. Drop columns from config file room
        columns_to_drop = config["data_cleaning"]["columns_to_drop"]
        existing_cols_to_drop = [col for col in columns_to_drop if col in df.columns]
        if existing_cols_to_drop:
            df.drop(columns=existing_cols_to_drop, inplace=True)
        
        # 3. Handle Missing Values in Rating column
        if "Rating" in df.columns:
            df["Rating"] = df["Rating"].fillna(0)
            
        # 4. Clean Duration and parse to integer types
        if "Duration" in df.columns:
            df["Duration"] = df["Duration"].astype(str).str.replace(" min", "", case=False, regex=False)
            df["Duration"] = df["Duration"].str.replace(",", "", regex=False)
            df["Duration"] = pd.to_numeric(df["Duration"], errors="coerce").fillna(0).astype(int)

        # 5. Clean Year sequence strings safely with safe pd.to_numeric boundary handlers
        if "Year" in df.columns:
            df["Year"] = df["Year"].astype(str)
            for char in ["-", "I", "II", "III", "IV", "V", "Vide"]:
                df["Year"] = df["Year"].str.replace(char, "", regex=False)
            df["Year"] = df["Year"].str.strip().str[:4].replace(["", "nan"], "0")
            # Bulletproof numeric casting tool added here
            df["Year"] = pd.to_numeric(df["Year"], errors="coerce").fillna(0).astype(int)

        df.sort_values(by="Year", ascending=True, inplace=True)
        
        # 6. Apply Threshold Logic Filter Constraints (latest_df constraints from notebook)
        latest_df = df[(df["Year"] > 2000) & (df["Duration"] > 5) & (df["Rating"] > 0.0)].copy()
        
        # Drop categorical text 'name' before one-hot transformation rules
        if "name" in latest_df.columns:
            latest_df.drop(columns=["name"], inplace=True)
            
        # Drop any missing structural arrays in Genre dimensions
        latest_df.dropna(subset=["Genre"], inplace=True)
        
        # 7. Perform Categorical One-Hot Encoding via dummy vectors
        logger.info("Performing One-Hot Encoding transformation on categorical variables...")
        encoded_df = pd.get_dummies(latest_df, columns=["Genre"], drop_first=True)
        
        create_directories([processed_data_dir])
        save_path = os.path.join(processed_data_dir, "cleaned_anime.csv")
        
        encoded_df.to_csv(save_path, index=False)
        logger.info(f"Feature Engineering finished. Encoded records safely dumped at {save_path}")
        
    except Exception as e:
        logger.error(f"Exception occurred during Feature Engineering: {e}")
        raise e

if __name__ == "__main__":
    initiate_feature_engineering()