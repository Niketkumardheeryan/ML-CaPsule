import json
import datetime


class AlertSystem:
    def __init__(self, log_file='alerts.json'):
        self.log_file = log_file

    def generate_alert(self, url, risk_score, risk_level):
        alert = {
            'timestamp': datetime.datetime.now().isoformat(),
            'url': url,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'message': f'⚠️ WARNING: {risk_level} risk QR code detected. Risk Score: {risk_score:.2f}'
        }
        return alert

    def log_alert(self, alert):
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(alert) + '\n')

    def display_alert(self, alert):
        print(alert['message'])
        if alert['risk_level'] == 'HIGH':
            print('❌ DO NOT OPEN THIS LINK - Likely phishing/malicious')
        elif alert['risk_level'] == 'MEDIUM':
            print('⚠️ CAUTION - Verify the link before opening')
