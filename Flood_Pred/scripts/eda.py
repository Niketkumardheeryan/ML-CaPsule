import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

def clean_col_names(df):
    """
    Cleans all column names in the DataFrame by making them lowercase,
    replacing special characters and spaces with underscores.
    """
    new_columns = []
    for col in df.columns:
        new_col = col.lower()
        new_col = re.sub(r'[^a-zA-Z0-9]+', '_', new_col)
        new_col = new_col.strip('_')
        new_columns.append(new_col)
    df.columns = new_columns
    return df

def explore_flood_data(file_path='flood.csv'):
    """
    Loads the flood dataset and performs exploratory data analysis (EDA)
    to visualize the relationship between features and the target variable.
    """
    # 1. Load Data
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return

    # 2. Data Preprocessing and Cleaning
    df = clean_col_names(df)
    
    if 'flood_occurred' not in df.columns:
        print("Error: Target column 'flood_occurred' not found after cleaning.")
        return
        
    print("Data successfully loaded. Starting exploratory analysis...")

    # Create a directory to save plots
    output_dir = 'eda_plots'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # 3. Analyze Numerical Features
    numerical_features = df.select_dtypes(include=np.number).columns.tolist()
    # Remove the target from the feature list
    if 'flood_occurred' in numerical_features:
        numerical_features.remove('flood_occurred')

    print("\nAnalyzing numerical features...")
    for feature in numerical_features:
        plt.figure(figsize=(10, 6))
        # Plot distribution for both classes
        sns.kdeplot(df[df['flood_occurred'] == 0][feature], label='No Flood', shade=True)
        sns.kdeplot(df[df['flood_occurred'] == 1][feature], label='Flood', shade=True)
        plt.title(f'Distribution of {feature} by Flood Occurrence')
        plt.legend()
        plt.tight_layout()
        save_path = os.path.join(output_dir, f'numerical_{feature}_distribution.png')
        plt.savefig(save_path)
        plt.close()
        print(f"  - Saved plot for '{feature}' to {save_path}")

    # 4. Analyze Categorical Features
    categorical_features = ['land_cover', 'soil_type']
    print("\nAnalyzing categorical features...")
    for feature in categorical_features:
        if feature in df.columns:
            plt.figure(figsize=(12, 7))
            sns.countplot(data=df, x=feature, hue='flood_occurred', palette='viridis')
            plt.title(f'Count of {feature} by Flood Occurrence')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            save_path = os.path.join(output_dir, f'categorical_{feature}_counts.png')
            plt.savefig(save_path)
            plt.close()
            print(f"  - Saved plot for '{feature}' to {save_path}")
            
    print("\nExploratory data analysis complete. Check the 'eda_plots' directory for the saved images.")


if __name__ == '__main__':
    explore_flood_data('flood.csv')
