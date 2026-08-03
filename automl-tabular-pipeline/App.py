import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification

from Preprocessing import get_preprocessing_pipeline
from Training import AutoMLTrainer
from Utils import save_model, generate_report

if __name__ == "__main__":
    print("Generating Mock Tabular Dataset for Pipeline Verification...")
    X_raw, y_raw = make_classification(n_samples=300, n_features=6, random_state=42)
    
    df = pd.DataFrame(X_raw, columns=['Feature_1', 'Feature_2', 'Feature_3', 'Feature_4', 'Feature_5', 'Feature_6'])
    df['Category_Feature'] = ['High' if x > 0 else 'Low' for x in df['Feature_1']]
    df['Target'] = y_raw

    X = df.drop(columns=['Target'])
    y = df['Target']

    numeric_cols = ['Feature_1', 'Feature_2', 'Feature_3', 'Feature_4', 'Feature_5', 'Feature_6']
    categorical_cols = ['Category_Feature']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = get_preprocessing_pipeline(numeric_cols, categorical_cols)
    trainer = AutoMLTrainer(preprocessor=preprocessor, n_trials=10)
    
    print("Initializing AutoML Optimization Loop...")
    best_pipeline = trainer.optimize_and_fit(X_train, y_train)

    generate_report(best_pipeline, X_test, y_test)
    save_model(best_pipeline)
