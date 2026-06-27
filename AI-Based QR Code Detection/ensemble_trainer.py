import argparse
from url_features import extract_url_features
from advanced_models import build_random_forest_classifier, build_svm_classifier, build_decision_tree_classifier, MultiClassifierEnsemble
from risk_scorer import RiskScorer
from alert_system import AlertSystem
from logger import MaliciousQRLogger
import pandas as pd
from sklearn.model_selection import train_test_split


def train_ensemble_models(data_csv, output_dir='models'):
    df = pd.read_csv(data_csv)
    if 'url' not in df.columns or 'label' not in df.columns:
        raise ValueError('CSV must contain url and label columns')

    X = pd.DataFrame([extract_url_features(url) for url in df['url']])
    y = df['label'].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    ensemble = MultiClassifierEnsemble({
        'random_forest': build_random_forest_classifier(n_estimators=100),
        'svm': build_svm_classifier(kernel='rbf'),
        'decision_tree': build_decision_tree_classifier(max_depth=10),
    })

    ensemble.train_all(X_train, y_train)

    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    X_test_list = X_test.values.tolist()
    predictions = [ensemble.predict_ensemble([x])[0] for x in X_test_list]

    accuracy = accuracy_score(y_test, [1 if p > 0.5 else 0 for p in predictions])
    print(f'Ensemble Accuracy: {accuracy:.4f}')

    ensemble.save_models(f'{output_dir}/ensemble')
    print(f'Models saved to {output_dir}')


def evaluate_qr_with_scoring(url, model_dict):
    features = extract_url_features(url)
    ensemble = MultiClassifierEnsemble(model_dict)

    risk_score, predictions = ensemble.predict_ensemble(extract_url_features(url))

    scorer = RiskScorer()
    final_score = scorer.compute_risk_score(risk_score, features)
    risk_level = scorer.classify_risk_level(final_score)

    alert_sys = AlertSystem()
    alert = alert_sys.generate_alert(url, final_score, risk_level)

    if risk_level in ['HIGH', 'MEDIUM']:
        alert_sys.display_alert(alert)
        alert_sys.log_alert(alert)

        logger = MaliciousQRLogger()
        logger.log_malicious_qr(url, final_score, risk_level)

    return {
        'url': url,
        'risk_score': final_score,
        'risk_level': risk_level,
        'model_predictions': predictions
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_ensemble', help='CSV path for ensemble training')
    parser.add_argument('--evaluate', help='URL to evaluate')
    args = parser.parse_args()

    if args.train_ensemble:
        train_ensemble_models(args.train_ensemble)
    elif args.evaluate:
        print('Ensemble models loading would require pre-trained models.')
    else:
        parser.print_help()
