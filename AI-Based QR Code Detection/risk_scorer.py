class RiskScorer:
    def __init__(self):
        self.risk_thresholds = {
            'safe': (0.0, 0.3),
            'low_risk': (0.3, 0.6),
            'medium_risk': (0.6, 0.8),
            'high_risk': (0.8, 1.0),
        }

    def compute_risk_score(self, features):
        risk_score = 0.0
        
        url_length = features.get('url_length', 0)
        if url_length > 100:
            risk_score += 0.15

        if features.get('num_dots', 0) > 5:
            risk_score += 0.10

        if features.get('num_hyphens', 0) > 3:
            risk_score += 0.10

        if features.get('is_ip_address', 0) == 1:
            risk_score += 0.25

        suspicious_count = features.get('suspicious_term_count', 0)
        if suspicious_count > 0:
            risk_score += min(suspicious_count * 0.15, 0.30)

        if features.get('has_query', 0) == 1:
            risk_score += 0.05

        if features.get('num_percent', 0) > 0:
            risk_score += 0.10

        risk_score = min(risk_score, 1.0)
        return risk_score

    def get_risk_level(self, risk_score):
        for level, (min_score, max_score) in self.risk_thresholds.items():
            if min_score <= risk_score < max_score:
                return level
        return 'high_risk' if risk_score >= 1.0 else 'safe'

    def get_alert_message(self, url, risk_score, risk_level):
        messages = {
            'safe': f'✓ URL appears safe: {url}',
            'low_risk': f'⚠ Low risk detected: {url} (Score: {risk_score:.2f})',
            'medium_risk': f'⚠⚠ Medium risk detected: {url} (Score: {risk_score:.2f}). Use caution.',
            'high_risk': f'🚨 HIGH RISK: {url} (Score: {risk_score:.2f}). DO NOT OPEN.',
        }
        return messages.get(risk_level, 'Unknown risk level')
