import os
import pytest
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from src.utils import load_model
from src.model_training import ModelTrainer

@pytest.fixture
def sample_config(tmp_path):
    return {
        "feature_engineering": {
            "random_state": 42,
        },
        "model_training": {
            "output_dir": str(tmp_path / "Model"),
            "model_1_filename": "model_1.pkl",
            "model_2_filename": "model_2.pkl",
        },
    }

@pytest.fixture
def sample_data():
    X_train = pd.DataFrame({"Year": [2005, 2010, 2015, 2020], "Duration": [24, 48, 24, 12]})
    y_train = pd.Series([7.0, 8.0, 8.5, 9.0])
    X_test = pd.DataFrame({"Year": [2008, 2018], "Duration": [24, 12]})
    y_test = pd.Series([7.5, 8.8])
    return X_train, X_test, y_train, y_test

def test_train_and_evaluate(sample_config, sample_data):
    X_train, X_test, y_train, y_test = sample_data
    trainer = ModelTrainer(sample_config)
    model = DecisionTreeRegressor(random_state=42)

    eval_metrics = trainer.train_and_evaluate(model, X_train, X_test, y_train, y_test)

    assert "train_score" in eval_metrics
    assert "r2_score" in eval_metrics
    assert "mae" in eval_metrics
    assert "mse" in eval_metrics
    assert "rmse" in eval_metrics

def test_run_pipeline_and_serialization(sample_config, sample_data):
    X_train, X_test, y_train, y_test = sample_data
    trainer = ModelTrainer(sample_config)

    results = trainer.run_pipeline(X_train, X_test, y_train, y_test)

    assert "LinearRegression" in results
    assert "DecisionTreeRegressor" in results
    assert "RandomForestRegressor" in results

    model_1_path = os.path.join(sample_config["model_training"]["output_dir"], "model_1.pkl")
    model_2_path = os.path.join(sample_config["model_training"]["output_dir"], "model_2.pkl")

    assert os.path.exists(model_1_path)
    assert os.path.exists(model_2_path)

    loaded_model_1 = load_model(model_1_path)
    assert isinstance(loaded_model_1, DecisionTreeRegressor)
