"""
Unit tests for utils/load_credentials.py
"""

import os
import pytest
from utils.load_credentials import get_credential, load_credentials


def test_get_credential_existing(monkeypatch):
    monkeypatch.setenv("TEST_KEY_EXISTING", "secret_value_123")
    assert get_credential("TEST_KEY_EXISTING") == "secret_value_123"


def test_get_credential_default():
    assert get_credential("NON_EXISTENT_KEY_123", default="default_val") == "default_val"


def test_get_credential_required_missing(monkeypatch):
    monkeypatch.delenv("NON_EXISTENT_KEY_456", raising=False)
    with pytest.raises(ValueError, match="CRITICAL SECURITY ERROR"):
        get_credential("NON_EXISTENT_KEY_456", required=True)


def test_load_credentials(monkeypatch):
    monkeypatch.setenv("KEY1", "val1")
    monkeypatch.setenv("KEY2", "val2")
    creds = load_credentials(["KEY1", "KEY2"], required=True)
    assert creds == {"KEY1": "val1", "KEY2": "val2"}
