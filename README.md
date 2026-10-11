# agente-trend-notion

This repository contains an AI agent that:
- searches the web by topic
- summarizes trend signals from online search results
- creates a weekly report
- pushes the report into a Notion database

## Features
- Web search with SerpAPI when configured, fallback to DuckDuckGo
- AI-powered trend analysis via HuggingFace Inference API (free tier)
- Weekly scheduler via APScheduler
- Notion page creation for reports

## Quick start

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:
```bash
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment template:

```bash
cp .env.example .env
```

4. Fill in `.env` with your credentials:

```
HUGGINGFACE_API_KEY=hf_...
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.1
NOTION_TOKEN=secret_...
NOTION_DATABASE_ID=...
```

5. Run once:

```bash
python main.py --topic "AI trends 2024" --run-once
```

6. Or schedule weekly runs:

```bash
python main.py --topic "AI trends 2024" --schedule
```

## Environment variables

See `.env.example` for all settings.

**Required:**
- `HUGGINGFACE_API_KEY` - Your HuggingFace API token
- `HUGGINGFACE_MODEL` - Model to use (default: mistralai/Mistral-7B-Instruct-v0.1)
- `NOTION_TOKEN` - Your Notion integration token
- `NOTION_DATABASE_ID` - The ID of your Notion database

**Optional:**
- `SERPAPI_KEY` - For enhanced Google search (uses DuckDuckGo fallback)
- `WEEKLY_REPORT_HOUR` - Hour for weekly report (default: 9)
- `WEEKLY_REPORT_MINUTE` - Minute for weekly report (default: 0)

## Notion database setup

Create a Notion database with these properties:
- **Name** (title)
- **Topic** (rich text)
- **Summary** (rich text)
- **Trend** (rich text)
- **Source** (rich text)
- **Confidence** (number 0-1)
- **Date** (date)

## Using HuggingFace free tier

1. Sign up at https://huggingface.co
2. Generate API token at https://huggingface.co/settings/tokens
3. Set token in `.env` as `HUGGINGFACE_API_KEY`

Free tier includes:
- Up to 60 requests per minute
- Access to thousands of open-source models
- No credit card required

## Recommended models

- `mistralai/Mistral-7B-Instruct-v0.1` - Fast and accurate
- `HuggingFaceH4/zephyr-7b-beta` - Faster inference
- `meta-llama/Llama-2-7b-chat-hf` - Requires approval

## License

MIT
