"""
Simple Firebase Realtime Database integration for single boom barrier control
Uses REST API (no auth) with the updated schema:

{
    "barrier": {
        "command": "",
        "state": "OPEN"
    },
    "test": ""
}

Base URL:
https://boom-barrier-24f9b-default-rtdb.asia-southeast1.firebasedatabase.app
"""

import time
from typing import Dict

import requests


BASE_URL = "https://boom-barrier-24f9b-default-rtdb.asia-southeast1.firebasedatabase.app"


def _put(path: str, value):
    """Internal helper to send a PUT to Firebase REST."""
    url = f"{BASE_URL}{path}"
    resp = requests.put(url, json=value, timeout=3)
    resp.raise_for_status()
    return True


def open_gate() -> bool:
    """
    Open the single barrier.
    - Sets /barrier/command = "OPEN"
    - Hardware will update state automatically
    """
    try:
        _put("/barrier/command.json", "OPEN")
        print("🚪 Firebase: barrier OPEN command sent")
        return True
    except Exception as e:
        print(f"❌ Firebase: failed to open barrier: {e}")
        return False


def close_gate() -> bool:
    """
    Close the single barrier.
    - Sets /barrier/command = "CLOSE"
    - Hardware will update state automatically
    """
    try:
        _put("/barrier/command.json", "CLOSE")
        print("🚪 Firebase: barrier CLOSE command sent")
        return True
    except Exception as e:
        print(f"❌ Firebase: failed to close barrier: {e}")
        return False


def control_gate(vehicle_number: str, camera_type: str, is_open: bool) -> bool:
    """
    Unified interface compatible with existing code.

    Args:
        vehicle_number: Plate text (for logging only).
        camera_type: "in" or "out" (ignored here, but kept for compatibility).
        is_open: True to open barrier, False to close barrier.
    """
    action = "OPEN" if is_open else "CLOSE"
    print(f"🔁 Firebase control_gate: vehicle={vehicle_number}, camera_type={camera_type}, action={action}")
    if is_open:
        return open_gate()
    return close_gate()


def test_connection() -> bool:
    """
    Lightweight connectivity check.
    Tries GET /test.json; if 200, we assume Firebase is reachable.
    """
    try:
        url = f"{BASE_URL}/test.json"
        resp = requests.get(url, timeout=3)
        return resp.status_code == 200
    except Exception:
        return False


def get_gate_status() -> Dict[str, str]:
    """
    Optional: read current barrier object for debugging.
    Returns a dict with 'state' and 'command' when available.
    """
    try:
        url = f"{BASE_URL}/barrier.json"
        resp = requests.get(url, timeout=3)
        resp.raise_for_status()
        data = resp.json() or {}
        return {
            "state": data.get("state", ""),
            "command": data.get("command", ""),
        }
    except Exception as e:
        print(f"⚠️ Firebase: failed to read barrier status: {e}")
        return {"state": "", "command": ""}


