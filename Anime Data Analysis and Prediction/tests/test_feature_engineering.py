import pytest
import pandas as pd
from src.feature_engineering import FeatureEngineer

@pytest.fixture
def sample_config():
    return {
        "filtering": {
            "target_genres": ["Animation, Action, Comedy", "Animation, Adventure, Drama"],
        },
        "feature_engineering": {
            "target_column": "Rating",
            "drop_features": ["name"],
            "test_size": 0.5,
            "random_state": 42,
        },
    }

@pytest.fixture
def sample_filtered_df():
    data = {
        "name": ["Anime 1", "Anime 2", "Anime 3", "Anime 4"],
        "Year": [2010, 2012, 2015, 2018],
        "Duration": [24, 48, 24, 12],
        "Genre": [
            "Animation, Action, Comedy",
            "Animation, Adventure, Drama",
            "Animation, Action, Comedy",
            "Other Genre",
        ],
        "Rating": [8.0, 7.5, 9.0, 6.0],
    }
    return pd.DataFrame(data)

def test_filter_genres(sample_config, sample_filtered_df):
    engineer = FeatureEngineer(sample_config)
    genre_df = engineer.filter_genres(sample_filtered_df)

    assert len(genre_df) == 3
    assert "Other Genre" not in genre_df["Genre"].values

def test_encode_features(sample_config, sample_filtered_df):
    engineer = FeatureEngineer(sample_config)
    genre_df = engineer.filter_genres(sample_filtered_df)
    encoded_df = engineer.encode_features(genre_df)

    assert "name" not in encoded_df.columns
    assert "Genre" not in encoded_df.columns
    assert "Rating" in encoded_df.columns

def test_prepare_train_test_split(sample_config, sample_filtered_df):
    engineer = FeatureEngineer(sample_config)
    genre_df = engineer.filter_genres(sample_filtered_df)
    encoded_df = engineer.encode_features(genre_df)

    X_train, X_test, y_train, y_test = engineer.prepare_train_test_split(encoded_df)

    assert len(X_train) + len(X_test) == len(encoded_df)
    assert len(y_train) + len(y_test) == len(encoded_df)
    assert "Rating" not in X_train.columns
