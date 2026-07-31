"""Web and knowledge integrations: Wikipedia, Google search, YouTube.

URL builders are pure functions so they can be unit tested without touching the
network or opening a browser window.
"""

from __future__ import annotations

import re
import webbrowser
from urllib.parse import quote, quote_plus

GOOGLE_SEARCH = "https://www.google.com/search?q={}"
YOUTUBE_SEARCH = "https://www.youtube.com/results?search_query={}"
WIKIPEDIA_SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def google_search_url(query: str) -> str:
    """Build the Google results URL for ``query``."""
    return GOOGLE_SEARCH.format(quote_plus(query.strip()))


def youtube_search_url(query: str) -> str:
    """Build the YouTube results URL for ``query``."""
    return YOUTUBE_SEARCH.format(quote_plus(query.strip()))


def trim_sentences(text: str, limit: int) -> str:
    """Return at most ``limit`` sentences from ``text``."""
    if limit <= 0 or not text:
        return text.strip()
    sentences = _SENTENCE_SPLIT.split(text.strip())
    return " ".join(sentences[:limit]).strip()


def open_in_browser(url: str, opener=None) -> str:
    """Open ``url`` with the default browser and return the URL that was used."""
    (opener or webbrowser.open)(url)
    return url


def search_google(query: str, opener=None) -> str:
    """Launch a Google search for ``query`` in the default browser."""
    return open_in_browser(google_search_url(query), opener=opener)


def play_on_youtube(query: str, opener=None) -> str:
    """Open YouTube results for ``query`` so the first hit can be streamed."""
    return open_in_browser(youtube_search_url(query), opener=opener)


def _summarise_with_library(query: str, sentences: int) -> str | None:
    """Summarise using the ``wikipedia`` package when it is installed."""
    try:
        import wikipedia
    except ImportError:
        return None

    try:
        return wikipedia.summary(query, sentences=sentences, auto_suggest=True)
    except Exception as exc:  # DisambiguationError, PageError, network errors
        options = getattr(exc, "options", None)
        if options:
            return (
                f"'{query}' matches several Wikipedia pages, for example: "
                + ", ".join(list(options)[:3])
                + ". Please be more specific."
            )
        return None


def _summarise_with_rest_api(query: str, sentences: int, timeout: float) -> str | None:
    """Keyless fallback that queries the public Wikipedia REST endpoint."""
    try:
        import requests

        response = requests.get(
            WIKIPEDIA_SUMMARY.format(quote(query.strip().replace(" ", "_"))),
            timeout=timeout,
            headers={"User-Agent": "ML-CaPsule-Virtual-Assistant/1.0"},
        )
        if response.status_code != 200:
            return None
        extract = response.json().get("extract", "")
        return trim_sentences(extract, sentences) or None
    except Exception:  # offline, DNS failure, malformed payload
        return None


def search_wikipedia(query: str, sentences: int = 2, timeout: float = 10.0) -> str:
    """Return a short Wikipedia summary for ``query``.

    The ``wikipedia`` package is preferred; if it is not installed or fails, the
    keyless REST API is used before giving up with a readable message.
    """
    query = query.strip()
    if not query:
        return "Please tell me what you would like me to look up on Wikipedia."

    summary = _summarise_with_library(query, sentences)
    if summary:
        return trim_sentences(summary, sentences)

    summary = _summarise_with_rest_api(query, sentences, timeout)
    if summary:
        return summary

    return f"I could not find a Wikipedia article for '{query}'."
