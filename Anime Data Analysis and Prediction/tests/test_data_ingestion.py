import os
import pytest
import pandas as pd
from src.utils import load_config
from src.data_ingestion import DataIngestion

@pytest.fixture
def sample_config(tmp_path):
    config = {
        "data": {
            "raw_path": str(tmp_path / "sample.csv"),
            "drop_columns": ["Story", "Certificate", "Unnamed: 0"],
        },
        "filtering": {
            "min_year": 2000,
            "min_duration": 5,
            "min_rating": 0.0,
            "target_genres": ["Animation, Action, Comedy"],
        },
        "feature_engineering": {
            "target_column": "Rating",
            "drop_features": ["name"],
            "test_size": 0.33,
            "random_state": 42,
        },
        "model_training": {
            "output_dir": str(tmp_path / "Model"),
            "model_1_filename": "model_1.pkl",
            "model_2_filename": "model_2.pkl",
        },
    }
    return config

@pytest.fixture
def sample_raw_df():
    data = {
        "Unnamed: 0": [0, 1, 2],
        "Name_of_Anime": ["Anime A", "Anime B", "Anime C"],
        "Story": ["Story A", "Story B", "Story C"],
        "Year": ["I 2005-2008", "2010-", "1999"],
        "Duration": ["24 min", "12 min", "3 min"],
        "Certificate": ["TV-MA", "TV-14", "PG"],
        "Genre": ["Animation, Action, Comedy", "Animation, Action, Comedy", "Other"],
        "Rating": [7.5, 8.0, 5.0],
    }
    return pd.DataFrame(data)

def test_clean_data(sample_config, sample_raw_df):
    ingestion = DataIngestion(sample_config)
    cleaned_df = ingestion.clean_data(sample_raw_df)

    assert "Story" not in cleaned_df.columns
    assert "Certificate" not in cleaned_df.columns
    assert "Unnamed: 0" not in cleaned_df.columns
    assert "name" in cleaned_df.columns

    assert cleaned_df["Year"].dtype == "int64"
    assert cleaned_df["Duration"].dtype == "int64"
    assert cleaned_df.loc[0, "Duration"] == 24
    assert cleaned_df.loc[0, "Year"] == 2005

def test_filter_data(sample_config, sample_raw_df):
    ingestion = DataIngestion(sample_config)
    cleaned_df = ingestion.clean_data(sample_raw_df)
    filtered_df = ingestion.filter_data(cleaned_df)

    # Year > 2000, Duration > 5, Rating > 0.0
    # Row 0: 2005 > 2000, 24 > 5, 7.5 > 0.0 (Keep)
    # Row 1: 2010 > 2000, 12 > 5, 8.0 > 0.0 (Keep)
    # Row 2: 1999 <= 2000 (Filtered out)
    assert len(filtered_df) == 2
