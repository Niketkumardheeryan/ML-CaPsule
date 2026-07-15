import json


class AlertManager:
    def __init__(self):
        self.alert_queue = []
        self.alert_levels = ['INFO', 'WARNING', 'CRITICAL']

    def create_alert(self, level, url, risk_score, message, threat_type='phishing'):
        alert = {
            'level': level,
            'url': url,
            'risk_score': float(risk_score),
            'message': message,
            'threat_type': threat_type,
            'action': self._get_recommended_action(level, risk_score)
        }
        self.alert_queue.append(alert)
        return alert

    def _get_recommended_action(self, level, risk_score):
        if level == 'CRITICAL' or risk_score >= 0.8:
            return 'BLOCK'
        elif level == 'WARNING' or risk_score >= 0.6:
            return 'PROMPT_USER'
        else:
            return 'ALLOW'

    def get_alerts(self):
        return self.alert_queue

    def clear_alerts(self):
        self.alert_queue = []

    def display_alert(self, alert):
        levels_symbols = {
            'INFO': 'ℹ️',
            'WARNING': '⚠️',
            'CRITICAL': '🚨'
        }
        symbol = levels_symbols.get(alert['level'], '❓')
        
        print(f"\n{symbol} {alert['level']} - {alert['threat_type'].upper()}")
        print(f"URL: {alert['url']}")
        print(f"Risk Score: {alert['risk_score']:.2f}")
        print(f"Message: {alert['message']}")
        print(f"Recommended Action: {alert['action']}")
        print("-" * 80)

    def export_alerts(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.alert_queue, f, indent=2)
