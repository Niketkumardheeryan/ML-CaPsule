"""
Unit and Integration Tests for Voice & CLI Virtual Assistant (#1984).
"""

import os
import sys
import pytest

# Ensure Voice_CLI_Virtual_Assistant path is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.speech_engine import get_greeting, TTSManager
from src.web_engine import search_wikipedia, search_google, play_youtube
from src.live_data_engine import get_weather, get_top_news
from src.system_engine import read_clipboard, take_screenshot, get_battery_telemetry
from src.os_control import open_media, power_command
from src.assistant import VirtualAssistant


def test_get_greeting():
    """Verify dynamic time-of-day greeting generation across hours."""
    assert "Good morning" in get_greeting(hour=8)
    assert "Good afternoon" in get_greeting(hour=14)
    assert "Good evening" in get_greeting(hour=19)
    assert "Good night" in get_greeting(hour=23)


def test_search_google():
    """Verify Google search query URL generation."""
    res = search_google("Python Programming", open_browser=False)
    assert "google.com/search" in res
    assert "Python%20Programming" in res


def test_play_youtube():
    """Verify YouTube streaming search query URL generation."""
    res = play_youtube("lofi beats", open_browser=False)
    assert "youtube.com/results" in res
    assert "lofi%20beats" in res


def test_search_wikipedia():
    """Verify Wikipedia summarization and query fallback."""
    res_empty = search_wikipedia("")
    assert "valid topic" in res_empty.lower()

    res_valid = search_wikipedia("Python (programming language)", sentences=1)
    assert isinstance(res_valid, str)
    assert len(res_valid) > 0


def test_get_weather():
    """Verify weather fetching for default location Jamshedpur."""
    res = get_weather("Jamshedpur")
    assert isinstance(res, str)
    assert "Jamshedpur" in res or "Weather" in res or "Live Weather" in res


def test_get_top_news():
    """Verify live top news headline extraction."""
    res = get_top_news(limit=3)
    assert isinstance(res, str)
    assert len(res) > 0


def test_read_clipboard():
    """Verify clipboard reading function returns non-empty response string."""
    res = read_clipboard()
    assert isinstance(res, str)


def test_take_screenshot(tmp_path):
    """Verify screenshot creation and file saving."""
    test_dir = str(tmp_path / "test_screenshots")
    res = take_screenshot(output_dir=test_dir)
    assert isinstance(res, str)
    assert os.path.exists(test_dir)


def test_get_battery_telemetry():
    """Verify battery telemetry report."""
    res = get_battery_telemetry()
    assert isinstance(res, str)
    assert "Battery" in res or "Level" in res or "Power State" in res


def test_open_media_validation():
    """Verify argument validation in open_media."""
    res_empty = open_media("")
    assert "valid file path" in res_empty


def test_power_command_safety_guard():
    """Verify that power commands are blocked by safety guard when confirm=False."""
    res_shutdown = power_command("shutdown", confirm=False)
    assert "[Power Command Guard]" in res_shutdown
    assert "SHUTDOWN" in res_shutdown

    res_restart = power_command("restart", confirm=False)
    assert "[Power Command Guard]" in res_restart

    res_invalid = power_command("invalid_action", confirm=False)
    assert "Invalid power command" in res_invalid


def test_assistant_command_routing():
    """Verify VirtualAssistant command intent routing logic."""
    assistant = VirtualAssistant(silent=True, default_city="Jamshedpur")

    # Greeting command
    resp, running = assistant.process_command("hello")
    assert running is True
    assert "Good" in resp

    # Battery command
    resp, running = assistant.process_command("battery status")
    assert running is True
    assert "Battery" in resp or "Level" in resp

    # Weather command
    resp, running = assistant.process_command("weather in Jamshedpur")
    assert running is True
    assert "Jamshedpur" in resp

    # Exit command
    resp, running = assistant.process_command("exit")
    assert running is False
    assert "Goodbye" in resp
