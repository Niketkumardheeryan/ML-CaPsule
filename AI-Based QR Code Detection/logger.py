import json
import datetime
from pathlib import Path


class QRLogger:
    def __init__(self, log_dir='qr_logs'):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.malicious_log = self.log_dir / 'malicious_qr_codes.json'
        self.alerts_log = self.log_dir / 'alerts.json'

    def log_malicious_qr(self, url, risk_score, features):
        entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'url': url,
            'risk_score': float(risk_score),
            'features': {k: float(v) if isinstance(v, (int, float)) else v for k, v in features.items()}
        }
        
        logs = []
        if self.malicious_log.exists():
            with open(self.malicious_log, 'r') as f:
                logs = json.load(f)
        
        logs.append(entry)
        with open(self.malicious_log, 'w') as f:
            json.dump(logs, f, indent=2)
        
        return entry

    def log_alert(self, alert_level, message, url=None):
        entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'level': alert_level,
            'message': message,
            'url': url
        }
        
        logs = []
        if self.alerts_log.exists():
            with open(self.alerts_log, 'r') as f:
                logs = json.load(f)
        
        logs.append(entry)
        with open(self.alerts_log, 'w') as f:
            json.dump(logs, f, indent=2)
        
        return entry

    def get_malicious_logs(self):
        if self.malicious_log.exists():
            with open(self.malicious_log, 'r') as f:
                return json.load(f)
        return []

    def get_alerts(self):
        if self.alerts_log.exists():
            with open(self.alerts_log, 'r') as f:
                return json.load(f)
        return []
