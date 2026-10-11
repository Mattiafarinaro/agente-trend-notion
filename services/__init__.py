import json
from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config.settings import OPENAI_API_KEY, OPENAI_MODEL


class AnalysisAgent:
    """Analyzes search results and produces trend intelligence."""

    def __init__(self):
        self.llm = ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
        ) if OPENAI_API_KEY else None

    def analyze_trends(self, topic: str, search_results: Any) -> Dict[str, Any]:
        if not search_results:
            return {
                "title": f"Weekly trend report: {topic}",
                "summary": "No results were returned from the web search stage.",
                "trend": "No trend detected",
                "confidence": 0,
                "source": "local fallback",
            }

        if self.llm is None:
            return self._fallback_analysis(topic, search_results)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an analyst that summarizes market and trend information. Return valid JSON only."),
            ("user", """
            Analyze the following web search results for the topic: {topic}

            Focus on:
            1. The dominant trend
            2. Why it matters
            3. Any signals of acceleration, stagnation, or decline
            4. A clear weekly summary

            Return a JSON object with these fields:
            {
              "title": "...",
              "summary": "...",
              "trend": "...",
              "confidence": 0.0,
              "source": "..."
            }

            Search data:
            {search_data}
            """)
        ])

        response = self.llm.invoke(prompt.format(
            topic=topic,
            search_data=json.dumps(search_results, ensure_ascii=False, indent=2)
        ))

        text = getattr(response, "content", str(response)).strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Best-effort fallback if the model returns non-JSON text
            return {
                "title": f"Weekly trend report: {topic}",
                "summary": text[:800],
                "trend": "AI-generated trend summary",
                "confidence": 0.5,
                "source": "LLM fallback parser",
            }

    @staticmethod
    def _fallback_analysis(topic: str, search_results: Any) -> Dict[str, Any]:
        items = search_results[:3]
        snippets = [item.get("snippet") or item.get("content") or "" for item in items]
        combined = " ".join(snippets)

        return {
            "title": f"Weekly trend report: {topic}",
            "summary": combined[:900] if combined else f"Fallback analysis for: {topic}",
            "trend": "Trend signals require a configured LLM to be more precise.",
            "confidence": 0.4,
            "source": "fallback heuristic",
        }
