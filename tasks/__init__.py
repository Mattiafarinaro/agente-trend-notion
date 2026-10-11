from datetime import datetime
from typing import Dict, Any

from notion_client import Client

from config.settings import NOTION_TOKEN, NOTION_DATABASE_ID


class NotionService:
    """Pushes weekly reports into a Notion database."""

    def __init__(self):
        self.client = Client(auth=NOTION_TOKEN) if NOTION_TOKEN else None
        self.database_id = NOTION_DATABASE_ID

    def create_report_page(self, report: Dict[str, Any]) -> Dict[str, Any]:
        if self.client is None:
            raise ValueError("Notion is not configured. Set NOTION_TOKEN and NOTION_DATABASE_ID before creating a page.")

        properties = {
            "Name": {
                "title": [{"text": {"content": report.get("title", "Weekly report")}}],
            },
            "Topic": {
                "rich_text": [{"text": {"content": report.get("topic", "")}}],
            },
            "Summary": {
                "rich_text": [{"text": {"content": report.get("summary", "")[:2000]}}],
            },
            "Trend": {
                "rich_text": [{"text": {"content": report.get("trend", "")}}],
            },
            "Source": {
                "rich_text": [{"text": {"content": report.get("source", "")}}],
            },
            "Confidence": {
                "number": float(report.get("confidence", 0.0)),
            },
            "Date": {
                "date": {"start": report.get("date") or datetime.utcnow().date().isoformat()},
            },
        }

        return self.client.pages.create(
            parent={"database_id": self.database_id},
            properties=properties,
        )
