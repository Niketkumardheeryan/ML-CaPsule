import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils import read_yaml, create_directories, logger

def initiate_model_training(config_path: str = "config/config.yaml") -> None:
    """Trains multiple algorithms and checkpoints the highest performing model variant.

    Args:
        config_path (str): Path to the configuration file.
    """
    logger.info("Starting Multi-Model Training and Evaluation Pipeline Stage...")
    try:
        config = read_yaml(config_path)
        processed_data_dir = config["artifacts"]["processed_data_dir"]
        viz_dir = config["artifacts"]["viz_dir"]
        
        data_path = os.path.join(processed_data_dir, "cleaned_anime.csv")
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Cleaned training dataset not found at {data_path}")
            
        df = pd.read_csv(data_path)
        
        # Split independent features X and target vector y
        X = df.drop(columns=["Rating"])
        y = df["Rating"]
        
        logger.info("Splitting data into explicit matrices (test_size=0.33)...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
        
        # Dictionary pooling all targeted algorithms from notebook screenshots
        models_to_evaluate = {
            "LinearRegression": LinearRegression(),
            "DecisionTreeRegressor": DecisionTreeRegressor(random_state=42),
            "RandomForestRegressor": RandomForestRegressor(random_state=42)
        }
        
        model_dir = "Model"
        create_directories([model_dir, viz_dir])
        
        best_r2_score = -float("inf")
        best_model_name = None
        best_model_object = None
        
        for name, model in models_to_evaluate.items():
            logger.info(f"Executing algorithmic fitting run for: {name}")
            model.fit(X_train, y_train)
            
            train_score = model.score(X_train, y_train)
            y_pred = model.predict(X_test)
            
            # Metric evaluations
            r2 = metrics.r2_score(y_test, y_pred)
            mae = metrics.mean_absolute_error(y_test, y_pred)
            mse = metrics.mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            
            logger.info(f"[{name}] Results -> Train Score: {train_score:.4f} | R2 Score: {r2:.4f} | MAE: {mae:.4f} | RMSE: {rmse:.4f}")
            
            # Save specific validation error displot file for each variant matching notebook behavior
            plt.figure(figsize=(8, 5))
            sns.histplot((y_test - y_pred), kde=True, bins=15, color="seagreen")
            plt.title(f"Residual Distribution - {name}")
            plt.xlabel("Errors")
            plt.tight_layout()
            plt.savefig(os.path.join(viz_dir, f"residuals_{name.lower()}.png"))
            plt.close()
            
            # Track the champion model automatically based on R2 Score metric bounds
            if r2 > best_r2_score:
                best_r2_score = r2
                best_model_name = name
                best_model_object = model
        
        logger.info(f"Algorithmic analysis complete. Champion Model: {best_model_name} with R2: {best_r2_score:.4f}")
        
        # Save structural checkpoint file matching target naming conventions
        model_save_name = "model_2.pkl" if best_model_name == "DecisionTreeRegressor" else "model_1.pkl"
        model_save_path = os.path.join(model_dir, model_save_name)
        
        with open(model_save_path, "wb") as file:
            pickle.dump(best_model_object, file)
        logger.info(f"Champion configuration tracking artifact successfully saved via pickle at: {model_save_path}")
        
    except Exception as e:
        logger.error(f"Exception occurred during Model Training: {e}")
        raise e

if __name__ == "__main__":
    initiate_model_training()