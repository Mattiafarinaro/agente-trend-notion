import json
from typing import Any, Dict, List

from config.settings import HUGGINGFACE_API_KEY, HUGGINGFACE_MODEL


class SearchAgent:
    """Collects search results for a topic."""

    def __init__(self, search_service: Any):
        self.search_service = search_service
        self.api_key = HUGGINGFACE_API_KEY
        self.model = HUGGINGFACE_MODEL

    def collect_context(self, topic: str, max_results: int = 5) -> List[Dict[str, str]]:
        results = self.search_service.search(topic, max_results=max_results)

        if not results:
            return [{
                "title": f"No search results for: {topic}",
                "url": "",
                "content": "No external data was retrieved.",
            }]

        context = []
        for item in results:
            context.append({
                "title": item.get("title", "Untitled"),
                "url": item.get("link", ""),
                "content": item.get("snippet", "") or item.get("content", "")
            })
        return context
