import os
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.1")
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "")
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
WEEKLY_REPORT_HOUR = int(os.getenv("WEEKLY_REPORT_HOUR", "9"))
WEEKLY_REPORT_MINUTE = int(os.getenv("WEEKLY_REPORT_MINUTE", "0"))


def get_required_setting(name: str) -> str:
    value = os.getenv(name, "")
    if not value:
        raise ValueError(f"Missing required env var: {name}")
    return value
