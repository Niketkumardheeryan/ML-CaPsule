import re
from collections import Counter


class URLTextAnalyzer:
    def __init__(self):
        self.phishing_keywords = [
            'verify', 'confirm', 'update', 'secure', 'account', 'login', 'signin',
            'password', 'urgent', 'action', 'click', 'immediately', 'reactivate',
            'suspended', 'locked', 'limited', 'unusual', 'activity', 'confirm',
            'validate', 'authentication', 'authorization', 'suspicious', 'alert'
        ]

    def extract_text_features(self, url):
        features = {
            'phishing_keyword_count': self._count_phishing_keywords(url),
            'entropy': self._calculate_entropy(url),
            'uppercase_ratio': self._calculate_uppercase_ratio(url),
            'digit_ratio': self._calculate_digit_ratio(url),
            'special_char_ratio': self._calculate_special_char_ratio(url),
        }
        return features

    def _count_phishing_keywords(self, text):
        text_lower = text.lower()
        count = sum(1 for keyword in self.phishing_keywords if keyword in text_lower)
        return count

    def _calculate_entropy(self, text):
        if len(text) == 0:
            return 0
        counter = Counter(text)
        entropy = 0.0
        for count in counter.values():
            p = count / len(text)
            entropy -= p * (p ** 0.5)
        return entropy

    def _calculate_uppercase_ratio(self, text):
        uppercase_count = sum(1 for c in text if c.isupper())
        return uppercase_count / len(text) if len(text) > 0 else 0

    def _calculate_digit_ratio(self, text):
        digit_count = sum(1 for c in text if c.isdigit())
        return digit_count / len(text) if len(text) > 0 else 0

    def _calculate_special_char_ratio(self, text):
        special_count = sum(1 for c in text if not c.isalnum())
        return special_count / len(text) if len(text) > 0 else 0
