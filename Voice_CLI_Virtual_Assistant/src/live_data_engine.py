"""
Live Data Orchestration Engine for Voice & CLI Virtual Assistant.
Fetches real-time localized weather indexing (Jamshedpur default) and live top news headlines.
"""

import xml.etree.ElementTree as ET
import requests


def get_weather(city: str = "Jamshedpur") -> str:
    """
    Fetches real-time localized weather index for a given location.

    Args:
        city (str): City name. Defaults to "Jamshedpur".

    Returns:
        str: Formatted weather report string.
    """
    city_name = city.strip() if city and city.strip() else "Jamshedpur"
    
    # Try wttr.in JSON API
    try:
        url = f"https://wttr.in/{requests.utils.quote(city_name)}?format=j1"
        headers = {"User-Agent": "Voice-CLI-Virtual-Assistant/1.0"}
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            data = response.json()
            current = data["current_condition"][0]
            temp_c = current.get("temp_C", "N/A")
            feels_c = current.get("FeelsLikeC", "N/A")
            weather_desc = current.get("weatherDesc", [{}])[0].get("value", "N/A")
            humidity = current.get("humidity", "N/A")
            wind_kmh = current.get("windspeedKmph", "N/A")

            return (
                f"🌤️ Live Weather Report for {city_name.title()}:\n"
                f"• Condition: {weather_desc}\n"
                f"• Temperature: {temp_c}°C (Feels like {feels_c}°C)\n"
                f"• Humidity: {humidity}%\n"
                f"• Wind Speed: {wind_kmh} km/h"
            )
    except Exception as e:
        pass

    # Secondary lightweight text format fallback from wttr.in
    try:
        url_text = f"https://wttr.in/{requests.utils.quote(city_name)}?format=3"
        resp_text = requests.get(url_text, timeout=5)
        if resp_text.status_code == 200 and resp_text.text.strip():
            return f"🌤️ Weather Update ({city_name.title()}): {resp_text.text.strip()}"
    except Exception:
        pass

    return f"⚠️ Unable to fetch live weather for {city_name}. Please check your internet connection."


def get_top_news(limit: int = 5) -> str:
    """
    Parses and returns live top news headlines from trusted open news RSS feeds.

    Args:
        limit (int): Number of top headlines to return (default 5).

    Returns:
        str: Formatted news headlines string.
    """
    rss_urls = [
        "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en",
        "http://feeds.bbci.co.uk/news/rss.xml",
    ]

    headlines = []
    headers = {"User-Agent": "Voice-CLI-Virtual-Assistant/1.0"}

    for rss_url in rss_urls:
        try:
            resp = requests.get(rss_url, headers=headers, timeout=5)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                items = root.findall(".//item")
                for item in items:
                    title_elem = item.find("title")
                    if title_elem is not None and title_elem.text:
                        title_text = title_elem.text.strip()
                        if title_text and title_text not in headlines:
                            headlines.append(title_text)
                            if len(headlines) >= limit:
                                break
            if len(headlines) >= limit:
                break
        except Exception:
            continue

    if headlines:
        output_lines = [f"📰 Top Live News Headlines:"]
        for idx, headline in enumerate(headlines[:limit], 1):
            output_lines.append(f"{idx}. {headline}")
        return "\n".join(output_lines)

    return "⚠️ Unable to fetch live news headlines at this moment. Please check network connectivity."
