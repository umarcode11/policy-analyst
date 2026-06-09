import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_pakistan_news(topic: str) -> str:
    """
    Fetches recent news about a topic using Serper News API.
    Focused on Pakistan policy and government news.
    """
    api_key = os.getenv("SERPER_API_KEY")

    if not api_key:
        return "[News Error] SERPER_API_KEY not found in environment."

    url = "https://google.serper.dev/news"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": f"{topic} Pakistan",
        "num": 5
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("news", []):
            title = item.get("title", "No title")
            snippet = item.get("snippet", "No snippet")
            source = item.get("source", "Unknown source")
            date = item.get("date", "Unknown date")
            link = item.get("link", "")
            results.append(
                f"- [{source}] {title}\n"
                f"  {snippet}\n"
                f"  Date: {date} | Source: {link}"
            )

        if not results:
            return f"[News] No recent news found for: {topic}"

        return "\n\n".join(results)

    except requests.exceptions.Timeout:
        return "[News Error] Request timed out. Using fallback search instead."
    except requests.exceptions.RequestException as e:
        return f"[News Error] {str(e)}" 