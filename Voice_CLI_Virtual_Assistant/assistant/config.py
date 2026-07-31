"""Runtime configuration for the virtual assistant.

Every setting has a sensible default so the assistant runs out of the box with
no configuration at all. API keys are optional: when they are absent the
assistant falls back to keyless public endpoints (see :mod:`assistant.live_data`).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_CITY = "Jamshedpur"
DEFAULT_WAKE_WORD = "capsule"
DEFAULT_TIMEOUT = 10.0
DEFAULT_HEADLINES = 5


def _env_str(name: str, default: str) -> str:
    value = os.environ.get(name, "").strip()
    return value or default


def _env_int(name: str, default: int) -> int:
    """Read an integer environment variable, ignoring malformed values."""
    raw = os.environ.get(name, "").strip()
    try:
        return int(raw)
    except ValueError:
        return default


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name, "").strip()
    try:
        return float(raw)
    except ValueError:
        return default


def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    if not raw:
        return default
    return raw in {"1", "true", "yes", "on"}


@dataclass
class AssistantConfig:
    """Settings that control assistant behaviour."""

    city: str = DEFAULT_CITY
    wake_word: str = DEFAULT_WAKE_WORD
    screenshot_dir: Path = field(default_factory=lambda: Path.home() / "Pictures")
    request_timeout: float = DEFAULT_TIMEOUT
    max_headlines: int = DEFAULT_HEADLINES
    news_edition: str = "IN"
    speech_rate: int = 175
    speech_volume: float = 1.0
    wikipedia_sentences: int = 2
    openweather_api_key: str = ""
    newsapi_key: str = ""
    # Power commands (shutdown / restart / logout) are irreversible, so they stay
    # disabled unless the user opts in explicitly *and* confirms interactively.
    allow_power_commands: bool = False

    def screenshot_target(self, filename: str) -> Path:
        """Return the absolute path a screenshot should be written to."""
        return self.screenshot_dir.expanduser() / filename


def load_config() -> AssistantConfig:
    """Build an :class:`AssistantConfig` from the process environment."""
    screenshot_dir = _env_str("ASSISTANT_SCREENSHOT_DIR", "")
    return AssistantConfig(
        city=_env_str("ASSISTANT_CITY", DEFAULT_CITY),
        wake_word=_env_str("ASSISTANT_WAKE_WORD", DEFAULT_WAKE_WORD).lower(),
        screenshot_dir=Path(screenshot_dir) if screenshot_dir else Path.home() / "Pictures",
        request_timeout=_env_float("ASSISTANT_TIMEOUT", DEFAULT_TIMEOUT),
        max_headlines=_env_int("ASSISTANT_HEADLINES", DEFAULT_HEADLINES),
        news_edition=_env_str("ASSISTANT_NEWS_EDITION", "IN"),
        speech_rate=_env_int("ASSISTANT_SPEECH_RATE", 175),
        speech_volume=_env_float("ASSISTANT_SPEECH_VOLUME", 1.0),
        wikipedia_sentences=_env_int("ASSISTANT_WIKI_SENTENCES", 2),
        openweather_api_key=_env_str("OPENWEATHER_API_KEY", ""),
        newsapi_key=_env_str("NEWSAPI_KEY", ""),
        allow_power_commands=_env_flag("ASSISTANT_ALLOW_POWER", False),
    )
