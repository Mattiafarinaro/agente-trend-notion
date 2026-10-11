import time
from datetime import datetime
from typing import Any, Dict, List

from apscheduler.schedulers.background import BackgroundScheduler

from agents.analysis_agent import AnalysisAgent
from agents.search_agent import SearchAgent
from config.settings import WEEKLY_REPORT_HOUR, WEEKLY_REPORT_MINUTE
from services.notion_service import NotionService
from services.search_service import SearchService


class WeeklyReportWorkflow:
    """Runs a weekly pipeline to gather data, analyze trends, and push report to Notion."""

    def __init__(self):
        self.search_service = SearchService()
        self.search_agent = SearchAgent(self.search_service)
        self.analysis_agent = AnalysisAgent()
        self.notion_service = NotionService()

    def execute(self, topic: str) -> Dict[str, Any]:
        context = self.search_agent.collect_context(topic, max_results=5)

        analysis = self.analysis_agent.analyze_trends(topic, context)

        report = {
            "title": analysis.get("title", f"Weekly trend report: {topic}"),
            "topic": topic,
            "summary": analysis.get("summary", "No summary generated."),
            "trend": analysis.get("trend", "No clear trend detected."),
            "source": analysis.get("source", "search + analysis"),
            "confidence": float(analysis.get("confidence", 0.0)),
            "date": datetime.utcnow().date().isoformat(),
        }

        try:
            page = self.notion_service.create_report_page(report)
            report["notion_page_id"] = page.get("id")
            report["notion_url"] = page.get("url")
        except ValueError:
            report["notion_page_id"] = None
            report["notion_url"] = None

        return report

    def schedule_weekly(self, topic: str):
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            self.execute,
            trigger="cron",
            day_of_week="mon",
            hour=WEEKLY_REPORT_HOUR,
            minute=WEEKLY_REPORT_MINUTE,
            args=[topic],
        )
        scheduler.start()
        return scheduler
