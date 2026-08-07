import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split
from src.utils import setup_logger

logger = setup_logger("FeatureEngineering")

class FeatureEngineer:
    """Class responsible for feature transformation, genre filtering, encoding, and train-test split."""

    def __init__(self, config: Dict[str, Any]):
        """Initializes FeatureEngineer with configuration dictionary.

        Args:
            config (Dict[str, Any]): Configuration dictionary.
        """
        self.config = config

    def filter_genres(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filters DataFrame to contain only target anime genres.

        Args:
            df (pd.DataFrame): Filtered dataset.

        Returns:
            pd.DataFrame: DataFrame containing target genres.
        """
        target_genres = self.config["filtering"].get("target_genres", [])
        if "Genre" in df.columns and target_genres:
            genre_df = df[df["Genre"].isin(target_genres)].copy()
            logger.info(f"Filtered target genres. Rows count: {len(genre_df)}")
            return genre_df
        return df.copy()

    def encode_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Encodes categorical features and drops specified non-predictive columns.

        Args:
            df (pd.DataFrame): Genre-filtered DataFrame.

        Returns:
            pd.DataFrame: Feature matrix DataFrame with one-hot encoded variables.
        """
        data = df.copy()

        # Drop non-predictive columns (e.g. name)
        drop_feats = self.config["feature_engineering"].get("drop_features", [])
        existing_drop_feats = [col for col in drop_feats if col in data.columns]
        if existing_drop_feats:
            data.drop(columns=existing_drop_feats, inplace=True)
            logger.info(f"Dropped features: {existing_drop_feats}")

        # One-hot encoding for categorical columns (like Genre)
        categorical_cols = [col for col in data.columns if data[col].dtype == "O"]
        if categorical_cols:
            encoded_dummies = pd.get_dummies(data[categorical_cols], drop_first=True)
            data = pd.concat([data, encoded_dummies], axis=1).drop(columns=categorical_cols)
            logger.info(f"One-hot encoded categorical columns: {categorical_cols}")

        return data

    def prepare_train_test_split(
        self, df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Splits DataFrame into features (X), target (y), and performs train-test split.

        Args:
            df (pd.DataFrame): Encoded DataFrame.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
                (X_train, X_test, y_train, y_test)
        """
        target_col = self.config["feature_engineering"].get("target_column", "Rating")
        test_size = self.config["feature_engineering"].get("test_size", 0.33)
        random_state = self.config["feature_engineering"].get("random_state", 42)

        X = df.drop(columns=[target_col])
        y = df[target_col]

        logger.info(
            f"Splitting features shape {X.shape} and target shape {y.shape} "
            f"with test_size={test_size}, random_state={random_state}"
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        logger.info(f"X_train shape: {X_train.shape}, X_test shape: {X_test.shape}")
        return X_train, X_test, y_train, y_test
