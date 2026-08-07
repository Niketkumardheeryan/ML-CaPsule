import os
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from src.utils import setup_logger

logger = setup_logger("DataIngestion")

class DataIngestion:
    """Class responsible for loading, cleaning, and filtering raw anime data."""

    def __init__(self, config: Dict[str, Any]):
        """Initializes DataIngestion with configuration dictionary.

        Args:
            config (Dict[str, Any]): Configuration settings dictionary.
        """
        self.config = config

    def load_data(self, file_path: str = None) -> pd.DataFrame:
        """Loads raw CSV dataset into a pandas DataFrame.

        Args:
            file_path (str, optional): Path to CSV file. Defaults to config raw_path.

        Returns:
            pd.DataFrame: Raw dataset.

        Raises:
            FileNotFoundError: If dataset file is missing.
        """
        path = file_path or self.config["data"]["raw_path"]
        if not os.path.exists(path):
            logger.error(f"Raw data file not found at: {path}")
            raise FileNotFoundError(f"Raw data file not found at: {path}")
        
        logger.info(f"Loading raw dataset from: {path}")
        df = pd.read_csv(path)
        logger.info(f"Successfully loaded dataset with shape: {df.shape}")
        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans columns, missing values, and formats data types.

        Args:
            df (pd.DataFrame): Input raw DataFrame.

        Returns:
            pd.DataFrame: Cleaned DataFrame.
        """
        df_clean = df.copy()

        # Drop columns specified in config
        drop_cols = self.config["data"].get("drop_columns", [])
        existing_drop_cols = [col for col in drop_cols if col in df_clean.columns]
        if existing_drop_cols:
            df_clean.drop(columns=existing_drop_cols, inplace=True)
            logger.info(f"Dropped columns: {existing_drop_cols}")

        # Clean Rating column
        if "Rating" in df_clean.columns:
            df_clean["Rating"] = df_clean["Rating"].replace(np.nan, 0.0)

        # Clean Duration column
        if "Duration" in df_clean.columns:
            df_clean["Duration"] = (
                df_clean["Duration"]
                .astype(str)
                .str.replace(" min", "", regex=False)
                .str.replace(",", "", regex=False)
            )
            df_clean["Duration"] = pd.to_numeric(df_clean["Duration"], errors="coerce").fillna(0).astype("int64")

        # Rename Name_of_Anime -> name
        if "Name_of_Anime" in df_clean.columns:
            df_clean.rename(columns={"Name_of_Anime": "name"}, inplace=True)

        # Clean Year column
        if "Year" in df_clean.columns:
            df_clean["Year"] = df_clean["Year"].astype(str).str.replace("-", " ", regex=False)
            roman_numerals = ["I", "II", "III", "IV", "Vide", "V", " "]
            for r in roman_numerals:
                df_clean["Year"] = df_clean["Year"].str.replace(r, "", regex=False)
            
            df_clean["Year"] = df_clean["Year"].apply(lambda val: val[:4] if len(val) >= 4 else val)
            df_clean["Year"] = df_clean["Year"].replace(["", "nan"], "0")
            df_clean["Year"] = pd.to_numeric(df_clean["Year"], errors="coerce").fillna(0).astype("int64")

        logger.info(f"Data cleaning completed. DataFrame shape: {df_clean.shape}")
        return df_clean

    def filter_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filters DataFrame based on minimum year, duration, and rating thresholds.

        Args:
            df (pd.DataFrame): Cleaned DataFrame.

        Returns:
            pd.DataFrame: Filtered DataFrame.
        """
        min_year = self.config["filtering"].get("min_year", 2000)
        min_duration = self.config["filtering"].get("min_duration", 5)
        min_rating = self.config["filtering"].get("min_rating", 0.0)

        filtered_df = df[
            (df["Year"] > min_year) &
            (df["Duration"] > min_duration) &
            (df["Rating"] > min_rating)
        ].copy()

        logger.info(
            f"Filtered data (Year>{min_year}, Duration>{min_duration}, Rating>{min_rating}). "
            f"Resulting shape: {filtered_df.shape}"
        )
        return filtered_df
