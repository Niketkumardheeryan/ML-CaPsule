import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils import read_yaml, create_directories, logger

def generate_eda_reports(config_path: str = "config/config.yaml") -> None:
    """Generates and saves all detailed EDA subplots and scatter variants.

    Args:
        config_path (str): Path to the configuration file.
    """
    logger.info("Starting Data Visualization and EDA Report stage...")
    try:
        config = read_yaml(config_path)
        processed_data_dir = config["artifacts"]["processed_data_dir"]
        viz_dir = config["artifacts"]["viz_dir"]
        
        create_directories([viz_dir])
        
        cleaned_data_path = os.path.join(processed_data_dir, "cleaned_anime.csv")
        logger.info(f"Loading cleaned data from {cleaned_data_path}")
        df = pd.read_csv(cleaned_data_path)
        
        # 1. Global Metrics Histogram Subplot Matrix
        logger.info("Generating Combined Histograms grid matrix...")
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.flatten()
        
        numeric_cols = ["Year", "Duration", "Rating"]
        for i, col in enumerate(numeric_cols):
            if col in df.columns:
                clean_series = pd.to_numeric(df[col], errors="coerce").dropna().astype(float)
                axes[i].hist(clean_series, label=col, bins=15, rwidth=0.9, color="dodgerblue")
                axes[i].set_title(col)
                axes[i].grid(True)
                axes[i].legend()
                
        fig.delaxes(axes[3])
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, "combined_metrics_histograms.png"))
        plt.close()
        
        # 2. Mean Rating distribution per year
        if "Year" in df.columns and "Rating" in df.columns:
            logger.info("Generating Mean Rating distribution per year bar sequence...")
            # Convert series using numeric handlers to safely avoid float NaN to int drops
            df["Year"] = pd.to_numeric(df["Year"], errors="coerce").fillna(0).astype(int)
            df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce").fillna(0.0).astype(float)
            
            grouped_df = df.groupby("Year")["Rating"].mean().reset_index()
            plt.figure(figsize=(12, 6))
            sns.barplot(x="Year", y="Rating", data=grouped_df, color="skyblue")
            plt.xticks(rotation=90)
            plt.title("Average Rating Distribution Per Year")
            plt.tight_layout()
            plt.savefig(os.path.join(viz_dir, "average_rating_displot.png"))
            plt.close()

        # 3. Scatter Variant: Duration vs Rating
        if "Duration" in df.columns and "Rating" in df.columns:
            logger.info("Generating Duration vs Rating Scatter Plot mapping...")
            clean_dur = pd.to_numeric(df["Duration"], errors="coerce").fillna(0).astype(float)
            clean_rat = pd.to_numeric(df["Rating"], errors="coerce").fillna(0.0).astype(float)
            
            plt.figure(figsize=(15, 7))
            plt.scatter(clean_dur, clean_rat, alpha=0.7, color="salmon")
            plt.xlabel("Duration", fontsize=14)
            plt.ylabel("Rating", fontsize=14)
            plt.title("Latest Data Frame Scatter Phase: Duration vs Rating")
            plt.tight_layout()
            plt.savefig(os.path.join(viz_dir, "duration_vs_rating_scatter.png"))
            plt.close()
            
        logger.info(f"All refined EDA charts and reports saved successfully in: {viz_dir}")
        
    except Exception as e:
        logger.error(f"Exception occurred during Data Visualization: {e}")
        raise e

if __name__ == "__main__":
    generate_eda_reports()