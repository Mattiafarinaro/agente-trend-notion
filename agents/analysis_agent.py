import json
import re
from typing import Any, Dict

import requests

from config.settings import HUGGINGFACE_API_KEY, HUGGINGFACE_MODEL


class AnalysisAgent:
    """Analyzes search results and generates trend intelligence using HuggingFace."""

    def __init__(self):
        self.api_key = HUGGINGFACE_API_KEY
        self.model = HUGGINGFACE_MODEL
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def analyze_trends(self, topic: str, search_results: Any) -> Dict[str, Any]:
        if not search_results:
            return {
                "title": f"Weekly trend report: {topic}",
                "summary": "No results were returned from the web search stage.",
                "trend": "No trend detected",
                "confidence": 0,
                "source": "local fallback",
            }

        if not self.api_key:
            return self._fallback_analysis(topic, search_results)

        prompt = self._build_prompt(topic, search_results)
        response = self._call_huggingface(prompt)

        if response:
            return self._parse_response(response, topic, search_results)
        else:
            return self._fallback_analysis(topic, search_results)

    def _build_prompt(self, topic: str, search_results: Any) -> str:
        search_data = json.dumps(search_results, ensure_ascii=False, indent=2)
        return f"""
        You are an AI analyst. Analyze the following web search results for the topic: {topic}

        Focus on:
        1. The dominant trend
        2. Why it matters
        3. Signs of acceleration, stagnation, or decline
        4. A concise weekly summary

        After your analysis, return ONLY a JSON block (no other text) with this exact structure:
        {{
          "title": "Weekly trend report: {topic}",
          "summary": "[2-3 sentence summary]",
          "trend": "[main trend description]",
          "confidence": 0.75,
          "source": "HuggingFace analysis"
        }}

        Search results:
        {search_data}
        """

    def _call_huggingface(self, prompt: str) -> str:
        """Call HuggingFace Inference API."""
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
            }
        }

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result[0].get("generated_text", "") if result else ""
        except Exception as e:
            print(f"HuggingFace API error: {e}")
            return ""

    def _parse_response(self, response_text: str, topic: str, search_results: Any) -> Dict[str, Any]:
        """Extract JSON from model response."""
        # Remove markdown code blocks if present
        text = response_text.replace("```json", "").replace("```", "").strip()

        # Try to extract JSON object
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                data = json.loads(json_str)
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                pass

        # Fallback if JSON parsing fails
        return self._fallback_analysis(topic, search_results)

    @staticmethod
    def _fallback_analysis(topic: str, search_results: Any) -> Dict[str, Any]:
        """Generate fallback analysis from search results."""
        items = search_results[:3]
        snippets = [item.get("content") or item.get("snippet") or "" for item in items]
        combined = " ".join(snippets)

        return {
            "title": f"Weekly trend report: {topic}",
            "summary": combined[:900] if combined else f"Fallback analysis for: {topic}",
            "trend": "Signals detected; LLM context unavailable.",
            "confidence": 0.4,
            "source": "fallback heuristic",
        }
