# agenzia-trend-notion

This repository contains a minimal but functional AI agent that:
- searches the web based on a user-defined topic
- analyzes trending signals and themes from the results
- produces a weekly report
- pushes the result into a Notion database

## Features
- Search by topic using SerpAPI when configured, with DuckDuckGo fallback
- AI-powered trend analysis using OpenAI / LangChain
- Weekly scheduler via APScheduler
- Notion page creation for reports
- Ready for local execution and extension

## Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy the environment template:

```bash
cp .env.example .env
```

3. Fill in the required environment values in `.env`.

4. Run the agent once for a topic:

```bash
python main.py --topic "AI trends 2024" --run-once
```

5. Or start the weekly scheduler:

```bash
python main.py --topic "AI trends 2024" --schedule
```

## Environment variables

See `.env.example` for the full list. At minimum, configure:
- OPENAI_API_KEY
- NOTION_TOKEN
- NOTION_DATABASE_ID

Optional but useful:
- SERPAPI_KEY
- NEWSAPI_KEY

## Notion setup

Create a Notion database with the following property names:
- Name (title)
- Topic (rich text)
- Summary (rich text)
- Trend (rich text)
- Source (rich text)
- Confidence (number)
- Date (date)

The script will create pages using these properties.

## Suggested extensions
- Save search results to a local SQLite database
- Add sentiment analysis
- Generate charts in Notion or markdown
- Add email / Slack deliveries
- Compare weekly reports over time

## License

MIT
