import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from url_features import extract_url_features
from utils import compute_metrics


class MultiModelClassifier:
    def __init__(self):
        self.models = {}

    def train_all_models(self, data_csv, model_dir='models'):
        df = pd.read_csv(data_csv)
        if 'url' not in df.columns or 'label' not in df.columns:
            raise ValueError('CSV must contain url and label columns')

        X = pd.DataFrame([extract_url_features(url) for url in df['url']])
        y = df['label'].astype(int)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Random Forest
        print('Training Random Forest...')
        rf_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        rf_pipeline.fit(X_train, y_train)
        rf_pred = rf_pipeline.predict(X_test)
        rf_metrics = compute_metrics(y_test, rf_pred)
        print(f'Random Forest metrics: {rf_metrics}')
        self.models['random_forest'] = rf_pipeline
        joblib.dump(rf_pipeline, f'{model_dir}/rf_model.joblib')

        # Decision Tree
        print('Training Decision Tree...')
        dt_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('clf', DecisionTreeClassifier(max_depth=15, random_state=42))
        ])
        dt_pipeline.fit(X_train, y_train)
        dt_pred = dt_pipeline.predict(X_test)
        dt_metrics = compute_metrics(y_test, dt_pred)
        print(f'Decision Tree metrics: {dt_metrics}')
        self.models['decision_tree'] = dt_pipeline
        joblib.dump(dt_pipeline, f'{model_dir}/dt_model.joblib')

        # SVM
        print('Training SVM...')
        svm_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('clf', SVC(kernel='rbf', probability=True, random_state=42))
        ])
        svm_pipeline.fit(X_train, y_train)
        svm_pred = svm_pipeline.predict(X_test)
        svm_metrics = compute_metrics(y_test, svm_pred)
        print(f'SVM metrics: {svm_metrics}')
        self.models['svm'] = svm_pipeline
        joblib.dump(svm_pipeline, f'{model_dir}/svm_model.joblib')

        # XGBoost (Gradient Boosting)
        print('Training XGBoost...')
        xgb_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('clf', GradientBoostingClassifier(n_estimators=100, random_state=42))
        ])
        xgb_pipeline.fit(X_train, y_train)
        xgb_pred = xgb_pipeline.predict(X_test)
        xgb_metrics = compute_metrics(y_test, xgb_pred)
        print(f'XGBoost metrics: {xgb_metrics}')
        self.models['xgboost'] = xgb_pipeline
        joblib.dump(xgb_pipeline, f'{model_dir}/xgb_model.joblib')

        return {
            'random_forest': rf_metrics,
            'decision_tree': dt_metrics,
            'svm': svm_metrics,
            'xgboost': xgb_metrics,
        }

    def predict_ensemble(self, url, model_dir='models'):
        features = extract_url_features(url)
        X = [list(features.values())]

        predictions = {}
        for model_name in ['random_forest', 'decision_tree', 'svm', 'xgboost']:
            try:
                model = joblib.load(f'{model_dir}/{model_name.replace("_", "").lower()}_model.joblib')
                pred = model.predict(X)[0]
                proba = model.predict_proba(X)[0].max() if hasattr(model, 'predict_proba') else 0.5
                predictions[model_name] = {
                    'prediction': int(pred),
                    'confidence': float(proba)
                }
            except Exception as e:
                print(f'Error with {model_name}: {e}')

        # Ensemble: average predictions
        if predictions:
            avg_pred = sum(p['prediction'] for p in predictions.values()) / len(predictions)
            ensemble_pred = 1 if avg_pred > 0.5 else 0
        else:
            ensemble_pred = 0

        return {
            'individual_predictions': predictions,
            'ensemble_prediction': ensemble_pred,
            'ensemble_confidence': sum(p['confidence'] for p in predictions.values()) / len(predictions) if predictions else 0
        }
