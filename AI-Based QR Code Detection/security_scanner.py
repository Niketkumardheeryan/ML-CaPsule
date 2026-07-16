import argparse
from qr_detection import detect_qr_codes_from_image
from url_features import extract_url_features
from nlp_analyzer import URLTextAnalyzer
from risk_scorer import RiskScorer
from alert_system import AlertSystem
from logger import MaliciousQRLogger
import joblib
import os


class QRSecurityScanner:
    def __init__(self, model_path=None):
        self.model = None
        if model_path and os.path.exists(model_path):
            self.model = joblib.load(model_path)

        self.scorer = RiskScorer()
        self.alert_sys = AlertSystem()
        self.logger = MaliciousQRLogger()
        self.nlp_analyzer = URLTextAnalyzer()

    def scan_image(self, image_path):
        qr_results = detect_qr_codes_from_image(image_path)
        security_results = []

        for qr_data in qr_results:
            url = qr_data['data']
            result = self.analyze_url(url, image_path)
            security_results.append(result)

        return security_results

    def analyze_url(self, url, image_path=None):
        url_features = extract_url_features(url)
        nlp_features = self.nlp_analyzer.extract_text_features(url)

        model_risk = 0.5
        if self.model:
            model_risk = self.model.predict_proba([list(url_features.values())])[0][1]

        final_score = self.scorer.compute_risk_score(model_risk, url_features)
        risk_level = self.scorer.classify_risk_level(final_score)

        result = {
            'url': url,
            'risk_score': float(final_score),
            'risk_level': risk_level,
            'url_features': url_features,
            'nlp_features': nlp_features,
        }

        alert = self.alert_sys.generate_alert(url, final_score, risk_level)
        self.alert_sys.display_alert(alert)
        self.alert_sys.log_alert(alert)

        if risk_level in ['HIGH', 'MEDIUM']:
            self.logger.log_malicious_qr(url, final_score, risk_level, image_path)

        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Secure QR Code Scanner')
    parser.add_argument('--image', help='Path to QR code image')
    parser.add_argument('--url', help='Direct URL to analyze')
    parser.add_argument('--model', help='Path to trained model')
    args = parser.parse_args()

    scanner = QRSecurityScanner(model_path=args.model)

    if args.image:
        results = scanner.scan_image(args.image)
        for result in results:
            print(f"URL: {result['url']}")
            print(f"Risk Score: {result['risk_score']:.4f}")
            print(f"Risk Level: {result['risk_level']}\n")
    elif args.url:
        result = scanner.analyze_url(args.url)
        print(f"URL: {result['url']}")
        print(f"Risk Score: {result['risk_score']:.4f}")
        print(f"Risk Level: {result['risk_level']}")
    else:
        parser.print_help()
