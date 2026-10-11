import re
from typing import Any, Dict, List

import requests

from config.settings import SERPAPI_KEY


class SearchService:
    """Fetches online results for a given topic."""

    def __init__(self):
        self.serpapi_key = SERPAPI_KEY

    def search(self, topic: str, max_results: int = 5) -> List[Dict[str, Any]]:
        if self.serpapi_key:
            try:
                return self._search_serpapi(topic, max_results=max_results)
            except Exception:
                pass

        return self._search_duckduckgo(topic, max_results=max_results)

    def _search_serpapi(self, topic: str, max_results: int = 5) -> List[Dict[str, Any]]:
        url = "https://serpapi.com/search"
        params = {
            "q": topic,
            "engine": "google",
            "api_key": self.serpapi_key,
            "num": max_results,
            "hl": "en",
        }
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        payload = response.json()

        results = []
        for item in payload.get("organic_results", [])[:max_results]:
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
            })
        return results

    def _search_duckduckgo(self, topic: str, max_results: int = 5) -> List[Dict[str, Any]]:
        url = "https://lite.duckduckgo.com/lite/"
        params = {"q": topic}
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()

        html = response.text
        pattern = re.compile(r'<a rel="nofollow" class="result-link" href="(.*?)">(.*?)</a>.*?<td class="result-snippet">(.*?)</td>', re.DOTALL)
        matches = pattern.findall(html)

        results = []
        for href, title_raw, snippet_raw in matches[:max_results]:
            title = re.sub(r'<.*?>', '', title_raw)
            snippet = re.sub(r'<.*?>', '', snippet_raw)
            results.append({
                "title": title.strip(),
                "link": href,
                "snippet": snippet.strip(),
            })

        return results
