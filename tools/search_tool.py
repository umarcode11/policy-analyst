import os
import requests
from dotenv import load_dotenv

load_dotenv()

def search_web(query: str) -> str:
    """
    Searches the web using Serper API and returns top results.
    """
    api_key = os.getenv("SERPER_API_KEY")

    if not api_key:
        return "[Search Error] SERPER_API_KEY not found in environment."

    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "num": 5
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("organic", []):
            title = item.get("title", "No title")
            snippet = item.get("snippet", "No snippet")
            link = item.get("link", "")
            results.append(f"- {title}\n  {snippet}\n  Source: {link}")

        if not results:
            return "[Search] No results found."

        return "\n\n".join(results)

    except requests.exceptions.Timeout:
        return "[Search Error] Request timed out. Try again later."
    except requests.exceptions.RequestException as e:
        return f"[Search Error] {str(e)}"