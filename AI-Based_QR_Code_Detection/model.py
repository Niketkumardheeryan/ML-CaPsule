import argparse
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from url_features import extract_url_features
from utils import compute_metrics

MODEL_PATH = 'qr_risk_model.joblib'


def train_classifier(data_csv, model_path=MODEL_PATH):
    df = pd.read_csv(data_csv)
    if 'url' not in df.columns or 'label' not in df.columns:
        raise ValueError('CSV must contain url and label columns')

    X = pd.DataFrame([extract_url_features(url) for url in df['url']])
    y = df['label'].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    metrics = compute_metrics(y_test, y_pred)
    print('Validation metrics:', metrics)

    joblib.dump(pipeline, model_path)
    print('Model saved to', model_path)
    return pipeline, metrics


def predict_url(model_path, url):
    pipeline = joblib.load(model_path)
    features = extract_url_features(url)
    prediction = pipeline.predict([list(features.values())])[0]
    score = pipeline.predict_proba([list(features.values())])[0].max()
    return int(prediction), float(score)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_csv', help='CSV path with url,label columns')
    parser.add_argument('--predict', help='URL to score with the trained model')
    parser.add_argument('--model_path', default=MODEL_PATH)
    args = parser.parse_args()

    if args.data_csv:
        train_classifier(args.data_csv, args.model_path)
    elif args.predict:
        label, score = predict_url(args.model_path, args.predict)
        print('Prediction:', label)
        print('Risk score:', score)
    else:
        parser.print_help()
