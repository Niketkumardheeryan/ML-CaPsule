import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from url_features import extract_url_features
from qr_detection import detect_qr_codes_from_image


def test_extract_url_features():
    features = extract_url_features('http://example.com/test?param=1')
    assert features['url_length'] > 0
    assert features['has_query'] == 1
    assert features['num_dots'] >= 1


def test_detect_qr_code_import():
    assert callable(detect_qr_codes_from_image)
