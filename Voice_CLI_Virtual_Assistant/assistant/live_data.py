"""Live data orchestration: localised weather and top news headlines.

Both providers work without an API key:

* weather  -> ``wttr.in`` JSON (OpenWeatherMap is used when a key is exported)
* headlines -> Google News RSS (NewsAPI is used when a key is exported)

Network access is confined to the ``fetch_*`` helpers; the payload parsers are
pure functions and therefore unit tested offline.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote
from xml.etree import ElementTree

WTTR_ENDPOINT = "https://wttr.in/{}?format=j1"
OPENWEATHER_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"
GOOGLE_NEWS_RSS = "https://news.google.com/rss?hl=en-{edition}&gl={edition}&ceid={edition}:en"
NEWSAPI_ENDPOINT = "https://newsapi.org/v2/top-headlines"

USER_AGENT = {"User-Agent": "ML-CaPsule-Virtual-Assistant/1.0"}


@dataclass
class WeatherReport:
    """Normalised weather snapshot, independent of the provider used."""

    city: str
    description: str
    temperature_c: float
    feels_like_c: float
    humidity: int
    wind_kmph: float
    source: str = "wttr.in"

    def describe(self) -> str:
        """Render the report as a single sentence suitable for speech."""
        return (
            f"{self.description} in {self.city}. "
            f"It is {self.temperature_c:.0f} degrees Celsius and feels like "
            f"{self.feels_like_c:.0f}, with {self.humidity}% humidity and "
            f"{self.wind_kmph:.0f} kilometres per hour of wind."
        )


def _to_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def parse_wttr_payload(payload: dict, city: str) -> WeatherReport:
    """Convert a ``wttr.in`` ``format=j1`` payload into a :class:`WeatherReport`."""
    current = (payload.get("current_condition") or [{}])[0]
    descriptions = current.get("weatherDesc") or [{}]
    return WeatherReport(
        city=city,
        description=(descriptions[0].get("value") or "Current conditions").strip(),
        temperature_c=_to_float(current.get("temp_C")),
        feels_like_c=_to_float(current.get("FeelsLikeC")),
        humidity=_to_int(current.get("humidity")),
        wind_kmph=_to_float(current.get("windspeedKmph")),
        source="wttr.in",
    )


def parse_openweather_payload(payload: dict, city: str) -> WeatherReport:
    """Convert an OpenWeatherMap payload into a :class:`WeatherReport`."""
    weather = (payload.get("weather") or [{}])[0]
    main = payload.get("main") or {}
    wind_ms = _to_float((payload.get("wind") or {}).get("speed"))
    return WeatherReport(
        city=payload.get("name") or city,
        description=(weather.get("description") or "Current conditions").capitalize(),
        temperature_c=_to_float(main.get("temp")),
        feels_like_c=_to_float(main.get("feels_like")),
        humidity=_to_int(main.get("humidity")),
        wind_kmph=wind_ms * 3.6,
        source="OpenWeatherMap",
    )


def parse_news_rss(xml_text: str, limit: int = 5) -> list[str]:
    """Extract up to ``limit`` headline titles from an RSS document."""
    try:
        root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError:
        return []

    headlines: list[str] = []
    for item in root.iterfind(".//item"):
        title = (item.findtext("title") or "").strip()
        if title:
            headlines.append(title)
        if len(headlines) >= limit:
            break
    return headlines


def fetch_weather(city: str, config) -> str:
    """Return a spoken weather report for ``city``."""
    try:
        import requests
    except ImportError:  # pragma: no cover - requests ships with the repo deps
        return "The requests package is required for weather lookups."

    if config.openweather_api_key:
        try:
            response = requests.get(
                OPENWEATHER_ENDPOINT,
                params={
                    "q": city,
                    "appid": config.openweather_api_key,
                    "units": "metric",
                },
                timeout=config.request_timeout,
                headers=USER_AGENT,
            )
            if response.status_code == 200:
                return parse_openweather_payload(response.json(), city).describe()
        except Exception:
            pass  # fall through to the keyless provider

    try:
        response = requests.get(
            WTTR_ENDPOINT.format(quote(city.strip())),
            timeout=config.request_timeout,
            headers=USER_AGENT,
        )
        if response.status_code != 200:
            return f"The weather service returned status {response.status_code}."
        return parse_wttr_payload(response.json(), city).describe()
    except Exception:
        return f"I could not reach the weather service for {city} right now."


def fetch_headlines(config, limit: int | None = None) -> list[str]:
    """Return the current top news headlines."""
    limit = limit or config.max_headlines
    try:
        import requests
    except ImportError:  # pragma: no cover - requests ships with the repo deps
        return []

    if config.newsapi_key:
        try:
            response = requests.get(
                NEWSAPI_ENDPOINT,
                params={
                    "country": config.news_edition.lower(),
                    "pageSize": limit,
                    "apiKey": config.newsapi_key,
                },
                timeout=config.request_timeout,
                headers=USER_AGENT,
            )
            if response.status_code == 200:
                articles = response.json().get("articles") or []
                titles = [a.get("title", "").strip() for a in articles if a.get("title")]
                if titles:
                    return titles[:limit]
        except Exception:
            pass  # fall through to the keyless provider

    try:
        response = requests.get(
            GOOGLE_NEWS_RSS.format(edition=config.news_edition.upper()),
            timeout=config.request_timeout,
            headers=USER_AGENT,
        )
        if response.status_code != 200:
            return []
        return parse_news_rss(response.text, limit)
    except Exception:
        return []


def format_headlines(headlines: list[str]) -> str:
    """Render headlines as a numbered, speech friendly block."""
    if not headlines:
        return "I could not fetch the news headlines right now."
    lines = [f"Here are the top {len(headlines)} headlines."]
    lines += [f"{index}. {title}" for index, title in enumerate(headlines, start=1)]
    return "\n".join(lines)
