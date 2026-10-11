import json
from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config.settings import OPENAI_API_KEY, OPENAI_MODEL


class SearchAgent:
    """Responsible for web search and content collection."""

    def __init__(self, search_service: Any):
        self.search_service = search_service
        self.llm = ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
        ) if OPENAI_API_KEY else None

    def collect_context(self, topic: str, max_results: int = 5) -> List[Dict[str, str]]:
        results = self.search_service.search(topic, max_results=max_results)

        if not results:
            return [{
                "title": f"No search results for: {topic}",
                "url": "",
                "content": "No external data was retrieved. The report is based on the search step only.",
            }]

        context = []
        for item in results:
            context.append({
                "title": item.get("title", "Untitled"),
                "url": item.get("link", ""),
                "content": item.get("snippet", "") or item.get("content", "")
            })
        return context
