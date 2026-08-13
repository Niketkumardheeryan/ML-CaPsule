"""
Web & Knowledge Integrations Module for Voice & CLI Virtual Assistant.
Supports on-demand Wikipedia summarization, Google query launching, and YouTube streaming.
"""

import urllib.parse
import webbrowser


def search_wikipedia(query: str, sentences: int = 2) -> str:
    """
    Fetches a concise Wikipedia summary for the given query.

    Args:
        query (str): The search topic.
        sentences (int): Number of sentences to summarize.

    Returns:
        str: Summary text or descriptive error message.
    """
    if not query or not query.strip():
        return "Please provide a valid topic to search on Wikipedia."

    try:
        import wikipedia
        wikipedia.set_lang("en")
        summary = wikipedia.summary(query, sentences=sentences)
        return f"According to Wikipedia:\n{summary}"
    except ImportError:
        return _fallback_wikipedia_search(query)
    except Exception as e:
        err_type = type(e).__name__
        if "DisambiguationError" in err_type or "Disambiguation" in str(e):
            return f"Multiple topics match '{query}'. Please be more specific with your query."
        elif "PageError" in err_type or "PageError" in str(e):
            return f"No Wikipedia page found matching '{query}'."
        else:
            return f"Failed to fetch Wikipedia information for '{query}': {e}"


def _fallback_wikipedia_search(query: str) -> str:
    """Fallback Wikipedia search using requests if wikipedia module is absent."""
    try:
        import requests
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            extract = data.get("extract")
            if extract:
                return f"According to Wikipedia:\n{extract}"
        return f"No Wikipedia summary could be retrieved for '{query}'."
    except Exception as e:
        return f"Unable to reach Wikipedia REST API: {e}"


def search_google(query: str, open_browser: bool = True) -> str:
    """
    Launches an automated Google query in the system default web browser.

    Args:
        query (str): Search keywords.
        open_browser (bool): Whether to trigger webbrowser.open.

    Returns:
        str: Action status message including target URL.
    """
    if not query or not query.strip():
        return "Please specify a query to search on Google."

    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.google.com/search?q={encoded_query}"

    if open_browser:
        try:
            webbrowser.open(search_url)
        except Exception as e:
            return f"Opened Google search URL: {search_url} (Browser trigger alert: {e})"

    return f"Searching Google for '{query}'...\nURL: {search_url}"


def play_youtube(query: str, open_browser: bool = True) -> str:
    """
    Launches YouTube video search or streaming query in the system default web browser.

    Args:
        query (str): Video search query.
        open_browser (bool): Whether to trigger webbrowser.open.

    Returns:
        str: Action status message including target URL.
    """
    if not query or not query.strip():
        return "Please specify a video title or topic to search on YouTube."

    encoded_query = urllib.parse.quote(query)
    yt_url = f"https://www.youtube.com/results?search_query={encoded_query}"

    if open_browser:
        try:
            webbrowser.open(yt_url)
        except Exception as e:
            return f"Opened YouTube search URL: {yt_url} (Browser trigger alert: {e})"

    return f"Opening YouTube search for '{query}'...\nURL: {yt_url}"
