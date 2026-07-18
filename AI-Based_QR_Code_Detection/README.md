# AI-Based QR Code Detection

This feature adds an AI-enabled QR code detection and quishing prevention system that can detect QR codes from images, decode embedded URLs, extract URL-based features, and classify suspicious links.

## Features

- Detect QR codes in images using OpenCV and Pyzbar
- Decode QR payloads and extract embedded URLs or data
- Analyze URL features for phishing and suspicious patterns
- Train a supervised classifier on URL data using scikit-learn
- **Multiple ML classifiers**: Random Forest, SVM, Decision Tree, XGBoost ensemble
- **Real-time risk scoring**: Generate security risk scores (0-1) for each QR code
- **Alerts and warnings**: Display real-time alerts with recommended actions (ALLOW, PROMPT, BLOCK)
- **Malicious QR logging**: Maintain structured logs of detected malicious QR codes
- **Threat intelligence integration**: Optional VirusTotal and AbuseIPDB integration
- Includes sample pipeline and smoke-test utilities

## Folder structure

- `qr_detection.py` — QR code detection and decoding utilities
- `url_features.py` — URL feature extraction for phishing classification
- `model.py` — classifier training, prediction, and persistence
- `train.py` — command-line training script
- `utils.py` — dataset loading and metric evaluation
- `risk_scorer.py` — compute risk scores and alert messages
- `logger.py` — log malicious QR codes and alerts to JSON files
- `alerts.py` — manage and display real-time alerts with recommended actions
- `advanced_models.py` — train and predict using multiple ML models (RF, SVM, DT, XGBoost)
- `threat_intelligence.py` — integrate with VirusTotal and AbuseIPDB APIs
- `tests/test_qr_detection.py` — basic unit tests
- `requirements.txt` — dependencies

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Detect QR codes in an image:

```bash
python qr_detection.py --image path/to/qr_image.png
```

3. Train the classifier on a CSV dataset of labeled URLs:

```bash
python train.py --data_csv data/qr_url_labels.csv --model_path qr_risk_model.joblib
```

4. Train multiple ML models (Random Forest, SVM, Decision Tree, XGBoost):

```python
from advanced_models import MultiModelClassifier
clf = MultiModelClassifier()
metrics = clf.train_all_models('data/qr_url_labels.csv', 'models/')
print(metrics)
```

5. Predict using ensemble of models:

```python
result = clf.predict_ensemble('http://example.com', 'models/')
print(result)
```

6. Use risk scoring and alerts:

```python
from url_features import extract_url_features
from risk_scorer import RiskScorer
from alerts import AlertManager

scorer = RiskScorer()
alerts = AlertManager()

url = 'http://suspicious-bank-login.com'
features = extract_url_features(url)
risk_score = scorer.compute_risk_score(features)
risk_level = scorer.get_risk_level(risk_score)

message = scorer.get_alert_message(url, risk_score, risk_level)
alert = alerts.create_alert(
    level='CRITICAL' if risk_score > 0.8 else 'WARNING',
    url=url,
    risk_score=risk_score,
    message=message
)
alerts.display_alert(alert)
```

7. Log malicious QR codes:

```python
from logger import QRLogger

logger = QRLogger()
logger.log_malicious_qr(url, risk_score, features)
logger.log_alert('CRITICAL', 'Malicious QR code detected', url)

# View logs
print(logger.get_malicious_logs())
print(logger.get_alerts())
```

## Notes

- This implementation uses classical ML for URL classification. It can be extended with NLP or deep learning models for richer phishing detection.
- For threat intelligence, set API keys:
  ```python
  ti = ThreatIntelligence()
  ti.set_virustotal_key('YOUR_VIRUSTOTAL_API_KEY')
  ti.set_abuseipdb_key('YOUR_ABUSEIPDB_API_KEY')
  ```
- For live camera support, use the `scan_live_camera` function in `qr_detection.py`.
- If you want to add this feature to the repo, keep it as a self-contained folder and follow the contribution guidelines in the root `CONTRIBUTING.md`.
