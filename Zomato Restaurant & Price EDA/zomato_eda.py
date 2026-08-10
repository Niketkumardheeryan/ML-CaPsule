import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style aesthetics
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "font.sans-serif": "DejaVu Sans",
    "axes.edgecolor": "#cccccc",
    "axes.linewidth": 0.8,
    "figure.autolayout": True
})

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data(filepath):
    """Load the raw Zomato dataset."""
    df = pd.read_csv(filepath)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns.")
    return df

def clean_data(df):
    """Clean missing values, convert data types, and normalize rating/cost formats."""
    cleaned = df.copy()
    
    # 1. Clean Average Cost for Two
    cleaned["Average_Cost_for_two"] = (
        cleaned["Average_Cost_for_two"]
        .astype(str)
        .str.replace(",", "")
        .str.extract(r"(\d+)")
        .astype(float)
    )
    cleaned["Average_Cost_for_two"] = cleaned["Average_Cost_for_two"].fillna(cleaned["Average_Cost_for_two"].median())

    # 2. Clean Aggregate Rating
    def parse_rating(val):
        if pd.isna(val) or val in ["NEW", "-", "Not rated"]:
            return np.nan
        val_str = str(val).split("/")[0].strip()
        try:
            return float(val_str)
        except ValueError:
            return np.nan

    cleaned["Rating_Cleaned"] = cleaned["Aggregate_rating_raw"].apply(parse_rating)
    if "Aggregate_rating" in cleaned.columns and cleaned["Rating_Cleaned"].isna().all():
        cleaned["Rating_Cleaned"] = cleaned["Aggregate_rating"].replace(0, np.nan)
        
    # Fill unrated with median for continuous modeling/analysis
    median_rating = cleaned["Rating_Cleaned"].median()
    cleaned["Rating_Cleaned_Imputed"] = cleaned["Rating_Cleaned"].fillna(median_rating)

    # 3. Handle Cuisines
    cleaned["Cuisines"] = cleaned["Cuisines"].fillna("Unknown Cuisine")
    
    # 4. Clean Votes
    cleaned["Votes"] = pd.to_numeric(cleaned["Votes"], errors="coerce").fillna(0).astype(int)

    return cleaned

def engineer_features(df):
    """Derive new analytical features from raw attributes."""
    fe = df.copy()

    # 1. Cuisine Count
    fe["Cuisine_Count"] = fe["Cuisines"].apply(lambda x: len([c.strip() for c in str(x).split(",") if c.strip()]))

    # 2. Cost Category
    cost_bins = [0, 400, 800, 1500, np.inf]
    cost_labels = ["Budget (Under 400)", "Mid-Range (400-800)", "Fine Dining (800-1500)", "Luxury (Above 1500)"]
    fe["Cost_Category"] = pd.cut(fe["Average_Cost_for_two"], bins=cost_bins, labels=cost_labels)

    # 3. Rating Class
    rating_bins = [0, 2.5, 3.5, 4.0, 4.5, 5.0]
    rating_labels = ["Poor (Under 2.5)", "Average (2.5-3.5)", "Good (3.5-4.0)", "Very Good (4.0-4.5)", "Excellent (4.5-5.0)"]
    fe["Rating_Class"] = pd.cut(fe["Rating_Cleaned_Imputed"], bins=rating_bins, labels=rating_labels)

    # 4. Binary Encodings
    fe["Has_Table_booking_num"] = (fe["Has_Table_booking"] == "Yes").astype(int)
    fe["Has_Online_delivery_num"] = (fe["Has_Online_delivery"] == "Yes").astype(int)

    # 5. Votes to Cost Ratio (Popularity Efficiency)
    fe["Votes_per_Cost_Ratio"] = np.where(fe["Average_Cost_for_two"] > 0, fe["Votes"] / fe["Average_Cost_for_two"], 0)

    return fe

def generate_visualizations(df):
    """Create and save EDA charts."""
    palette = sns.color_palette("viridis")

    # Chart 1: Rating Distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["Rating_Cleaned_Imputed"], kde=True, color="#2b5c8f", bins=20, ax=ax)
    mean_val = df["Rating_Cleaned_Imputed"].mean()
    median_val = df["Rating_Cleaned_Imputed"].median()
    ax.axvline(mean_val, color="#e74c3c", linestyle="--", linewidth=1.5, label=f"Mean: {mean_val:.2f}")
    ax.axvline(median_val, color="#2ecc71", linestyle="-.", linewidth=1.5, label=f"Median: {median_val:.2f}")
    ax.set_title("Distribution of Aggregate Restaurant Ratings", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Aggregate Rating (1 - 5 Scale)", fontsize=11)
    ax.set_ylabel("Number of Restaurants", fontsize=11)
    ax.legend(frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "rating_distribution.png"), dpi=300)
    plt.close()

    # Chart 2: Cost Distribution & Category Count
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.boxplot(y=df["Average_Cost_for_two"], x=df["Cost_Category"], hue=df["Cost_Category"], palette="mako", legend=False, ax=axes[0])
    axes[0].set_title("Average Cost for Two by Category", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Cost Category", fontsize=11)
    axes[0].set_ylabel("Average Cost for Two (INR)", fontsize=11)
    axes[0].tick_params(axis="x", rotation=15)

    category_counts = df["Cost_Category"].value_counts().reindex(df["Cost_Category"].cat.categories)
    sns.barplot(x=category_counts.index, y=category_counts.values, hue=category_counts.index, palette="rocket", legend=False, ax=axes[1])
    axes[1].set_title("Restaurant Count per Cost Category", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Cost Category", fontsize=11)
    axes[1].set_ylabel("Count", fontsize=11)
    axes[1].tick_params(axis="x", rotation=15)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "cost_distribution.png"), dpi=300)
    plt.close()

    # Chart 3: Cost vs Rating Scatter & Trend
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.scatterplot(
        data=df,
        x="Average_Cost_for_two",
        y="Rating_Cleaned_Imputed",
        hue="Has_Table_booking",
        size="Votes",
        sizes=(20, 200),
        alpha=0.7,
        palette={"Yes": "#e67e22", "No": "#2980b9"},
        ax=ax
    )
    sns.regplot(
        data=df,
        x="Average_Cost_for_two",
        y="Rating_Cleaned_Imputed",
        scatter=False,
        ax=ax,
        color="#34495e",
        line_kws={"linestyle": "--", "linewidth": 2}
    )
    ax.set_title("Relationship: Average Cost vs. Rating (by Table Booking)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Average Cost for Two (INR)", fontsize=11)
    ax.set_ylabel("Aggregate Rating", fontsize=11)
    ax.legend(title="Table Booking", frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "cost_vs_rating.png"), dpi=300)
    plt.close()

    # Chart 4: Online Delivery & Table Booking Impact
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    sns.boxplot(data=df, x="Has_Online_delivery", y="Rating_Cleaned_Imputed", hue="Has_Online_delivery", palette=["#e74c3c", "#2ecc71"], legend=False, ax=axes[0])
    axes[0].set_title("Rating Impact: Online Delivery", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Has Online Delivery", fontsize=11)
    axes[0].set_ylabel("Aggregate Rating", fontsize=11)

    sns.boxplot(data=df, x="Has_Table_booking", y="Average_Cost_for_two", hue="Has_Table_booking", palette=["#9b59b6", "#1abc9c"], legend=False, ax=axes[1])
    axes[1].set_title("Price Impact: Table Booking", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Has Table Booking", fontsize=11)
    axes[1].set_ylabel("Average Cost for Two (INR)", fontsize=11)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "delivery_booking_impact.png"), dpi=300)
    plt.close()

    # Chart 5: Top 10 Cuisines
    cuisine_series = df["Cuisines"].str.split(", ").explode()
    top10_cuisines = cuisine_series.value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(x=top10_cuisines.values, y=top10_cuisines.index, hue=top10_cuisines.index, palette="crest", legend=False, ax=ax)
    ax.set_title("Top 10 Most Offered Cuisines Across Restaurants", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Number of Restaurants Offering Cuisine", fontsize=11)
    ax.set_ylabel("Cuisine Type", fontsize=11)
    for i, v in enumerate(top10_cuisines.values):
        ax.text(v + 3, i, str(v), color="black", va="center", fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top_cuisines.png"), dpi=300)
    plt.close()
    ax.set_title("Top 10 Most Offered Cuisines Across Restaurants", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Number of Restaurants Offering Cuisine", fontsize=11)
    ax.set_ylabel("Cuisine Type", fontsize=11)
    for i, v in enumerate(top10_cuisines.values):
        ax.text(v + 3, i, str(v), color="black", va="center", fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top_cuisines.png"), dpi=300)
    plt.close()

    # Chart 6: Correlation Matrix Heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    num_cols = ["Average_Cost_for_two", "Rating_Cleaned_Imputed", "Votes", "Price_range", "Cuisine_Count", "Has_Table_booking_num", "Has_Online_delivery_num"]
    corr = df[num_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        linewidths=0.5,
        mask=mask,
        ax=ax,
        cbar_kws={"shrink": 0.8}
    )
    ax.set_title("Feature Correlation Heatmap", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "correlation_heatmap.png"), dpi=300)
    plt.close()

    print(f"All 6 visualizations generated successfully in '{OUTPUT_DIR}'.")

def main():
    dataset_path = os.path.join(os.path.dirname(__file__), "zomato.csv")
    raw_df = load_data(dataset_path)
    cleaned_df = clean_data(raw_df)
    final_df = engineer_features(cleaned_df)
    
    print("\n--- Summary Statistics ---")
    print(final_df[["Average_Cost_for_two", "Rating_Cleaned_Imputed", "Votes", "Cuisine_Count"]].describe())
    
    generate_visualizations(final_df)

if __name__ == "__main__":
    main()
