import os
import pandas as pd
from sklearn.model_selection import train_test_split
from model_evaluation import (
    build_preprocessor, 
    build_model_pipelines, 
    evaluate_models, 
    plot_confusion_matrix, 
    plot_comparison
)

def main():
    csv_path = "Data.csv"
    if not os.path.exists(csv_path):
        # Check if we are running from repository root instead of the directory
        csv_path = "Autism Identification System/Data.csv"
        if not os.path.exists(csv_path):
            raise FileNotFoundError("Could not locate Data.csv in current or subdirectory path.")

    print(f"Loading dataset from: {csv_path}...")
    df = pd.read_csv(csv_path)

    print("Cleaning missing values and grouping equivalents...")
    # Clean "?" values in relation with the mode
    df['relation'] = df['relation'].replace('?', df['relation'].mode()[0])
    # Clean "?" and "others" in ethnicity
    df['ethnicity'] = df['ethnicity'].replace('?', 'Others')
    df['ethnicity'] = df['ethnicity'].replace('others', 'Others')

    # Drop target and uninformative columns
    X = df.drop(['Class/ASD', 'age_desc', 'used_app_before'], axis=1)
    y = df['Class/ASD']

    print(f"Split data into features X shape: {X.shape} and label y shape: {y.shape}")

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training split: {X_train.shape[0]} samples. Testing split: {X_test.shape[0]} samples.")

    # Build pipelines
    preprocessor = build_preprocessor(X)
    pipelines = build_model_pipelines(preprocessor)

    # Evaluate
    metrics_df, reports, cms, roc_data = evaluate_models(pipelines, X_train, X_test, y_train, y_test)

    # Print results
    print("\n--- Model Evaluation Results ---")
    print(metrics_df.to_string(index=False))
    print("\n--------------------------------")

    # Generate and save comparison plot
    print("\nGenerating model comparison plot...")
    fig_comp = plot_comparison(metrics_df)
    fig_comp.savefig("metrics_comparison.png", dpi=300)
    print("Saved metrics_comparison.png to current directory.")

    # Generate and save a sample confusion matrix for Random Forest
    if 'RandomForestClassifier' in cms:
        print("Generating confusion matrix plot for RandomForestClassifier...")
        fig_cm = plot_confusion_matrix(cms['RandomForestClassifier'], labels=['No ASD', 'ASD'], normalize=False)
        fig_cm.savefig("rf_confusion_matrix.png", dpi=300)
        print("Saved rf_confusion_matrix.png to current directory.")

if __name__ == "__main__":
    main()
