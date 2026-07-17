import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from model_evaluation import (
    build_preprocessor,
    build_model_pipelines,
    evaluate_models,
    plot_confusion_matrix,
    plot_comparison
)

class TestModelEvaluation(unittest.TestCase):
    def setUp(self):
        # Create a synthetic dataset matching the Autism screening structure
        np.random.seed(42)
        n_samples = 50
        
        # 10 binary scores
        data = {f"A{i}_Score": np.random.choice([0, 1], size=n_samples) for i in range(1, 11)}
        
        # Continuous age
        data["age"] = np.random.uniform(18, 70, size=n_samples)
        
        # Categorical strings
        data["gender"] = np.random.choice(["m", "f"], size=n_samples)
        data["ethnicity"] = np.random.choice(["White-European", "Latino", "Asian", "Others"], size=n_samples)
        data["jundice"] = np.random.choice(["yes", "no"], size=n_samples)
        data["austim"] = np.random.choice(["yes", "no"], size=n_samples)
        data["contry_of_res"] = np.random.choice(["United States", "Spain", "Brazil"], size=n_samples)
        data["relation"] = np.random.choice(["Self", "Parent", "Relative"], size=n_samples)
        
        # Screening result score (sum of questionnaire scores)
        data["result"] = sum(data[f"A{i}_Score"] for i in range(1, 11))
        
        self.X = pd.DataFrame(data)
        
        # Target variable (ASD)
        # Create a clean YES/NO classification based on result threshold to guarantee clean train sets
        self.y = pd.Series(["YES" if r >= 7 else "NO" for r in data["result"]])

    def test_build_preprocessor(self):
        preprocessor = build_preprocessor(self.X)
        self.assertIsInstance(preprocessor, ColumnTransformer)
        
        # Test fitting preprocessor
        preprocessor.fit(self.X)
        X_trans = preprocessor.transform(self.X)
        self.assertGreater(X_trans.shape[0], 0)
        self.assertGreater(X_trans.shape[1], 0)

    def test_build_model_pipelines(self):
        preprocessor = build_preprocessor(self.X)
        pipelines = build_model_pipelines(preprocessor)
        
        self.assertIsInstance(pipelines, dict)
        expected_models = ['LogisticRegression', 'SVC', 'RandomForestClassifier', 'DummyClassifier']
        for model in expected_models:
            self.assertIn(model, pipelines)
            self.assertIsInstance(pipelines[model], Pipeline)

    def test_evaluate_models(self):
        X_train = self.X.iloc[:40]
        X_test = self.X.iloc[40:]
        y_train = self.y.iloc[:40]
        y_test = self.y.iloc[40:]
        
        preprocessor = build_preprocessor(self.X)
        pipelines = build_model_pipelines(preprocessor)
        
        metrics_df, reports, cms, roc_data = evaluate_models(pipelines, X_train, X_test, y_train, y_test)
        
        # Verify metrics DataFrame columns
        self.assertIsInstance(metrics_df, pd.DataFrame)
        expected_columns = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
        for col in expected_columns:
            self.assertIn(col, metrics_df.columns)
            
        # Verify output dictionaries
        self.assertEqual(len(reports), len(pipelines))
        self.assertEqual(len(cms), len(pipelines))
        
        for name in pipelines:
            self.assertIn(name, reports)
            self.assertIsInstance(reports[name], str)
            self.assertIn(name, cms)
            self.assertEqual(cms[name].shape, (2, 2))

    def test_plot_confusion_matrix(self):
        cm = np.array([[10, 2], [1, 7]])
        fig_abs = plot_confusion_matrix(cm, labels=['No ASD', 'ASD'], normalize=False)
        fig_norm = plot_confusion_matrix(cm, labels=['No ASD', 'ASD'], normalize=True)
        
        self.assertIsInstance(fig_abs, plt.Figure)
        self.assertIsInstance(fig_norm, plt.Figure)
        plt.close(fig_abs)
        plt.close(fig_norm)

    def test_plot_comparison(self):
        metrics_data = [
            {'Model': 'ModelA', 'Accuracy': 0.9, 'Precision': 0.85, 'Recall': 0.9, 'F1-Score': 0.87, 'ROC-AUC': 0.95},
            {'Model': 'ModelB', 'Accuracy': 0.8, 'Precision': 0.75, 'Recall': 0.8, 'F1-Score': 0.77, 'ROC-AUC': 0.85}
        ]
        metrics_df = pd.DataFrame(metrics_data)
        fig = plot_comparison(metrics_df)
        
        self.assertIsInstance(fig, plt.Figure)
        plt.close(fig)

if __name__ == "__main__":
    unittest.main()
