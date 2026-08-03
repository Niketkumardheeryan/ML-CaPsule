import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model import build_model


def test_build_model():
    m = build_model((224, 224, 3), num_classes=3)
    assert m.output_shape == (None, 3)
