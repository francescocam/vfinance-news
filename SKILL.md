---
name: vfinance-news
description: Market news briefings with AI summaries and price alerts. Aggregates headlines from US/Europe/Japan markets. Use when: 'stock news', 'market updates', 'morning briefing', 'evening market wrap', 'financial headlines', 'price alerts', 'what happened in the market'. Outputs in English. NOT for fundamental analysis or scoring (use equity-research). NOT for raw financial data queries.
---

# Finance News Skill

AI-powered market news briefings.

## First-Time Setup

Run the interactive setup wizard to configure your sources and schedule:

```bash
{baseDir}/.venv/bin/vfinance-news setup
```

The wizard will guide you through:
- 📰 **RSS Feeds:** Enable/disable WSJ, Barron's, CNBC, Yahoo, etc.
- 📊 **Markets:** Choose regions (US, Europe, Japan, Asia)
- ⏰ **Schedule:** Configure morning/evening cron times

You can also configure specific sections:
```bash
{baseDir}/.venv/bin/vfinance-news setup --section feeds     # Just RSS feeds
{baseDir}/.venv/bin/vfinance-news setup --section schedule  # Just cron schedule
{baseDir}/.venv/bin/vfinance-news setup --reset             # Reset to defaults
{baseDir}/.venv/bin/vfinance-news config                    # Show current config
```

## Quick Start

```bash
# Generate briefing
{baseDir}/.venv/bin/vfinance-news briefing

# View market overview
{baseDir}/.venv/bin/vfinance-news market

# Get news for your portfolio
{baseDir}/.venv/bin/vfinance-news portfolio

# Get news for specific stock
{baseDir}/.venv/bin/vfinance-news news AAPL
```

## Features

### 📊 Market Coverage
- **US Markets:** S&P 500, Dow Jones, NASDAQ
- **Europe:** DAX, STOXX 50, FTSE 100
- **Japan:** Nikkei 225

### 📰 News Sources
- **Premium:** WSJ, Barron's (RSS feeds)
- **Free:** CNBC, Yahoo Finance, Finnhub
- **Portfolio:** Ticker-specific news from Yahoo

### 🤖 AI Summaries
- LLM poweredanalysis
- English-only output
- Briefing styles: summary, analysis, headlines

### 📅 Automated Briefings
- **Morning:** 6:30 AM PT (US market open)
- **Evening:** 1:00 PM PT (US market close)

## Commands

### Briefing Generation

```bash
# Briefing
{baseDir}/.venv/bin/vfinance-news briefing --llm

# Analysis style (more detailed)
{baseDir}/.venv/bin/vfinance-news briefing --style analysis --llm
```

### Market Data

```bash
# Market overview (indices + top headlines)
{baseDir}/.venv/bin/vfinance-news market

# JSON output for processing
{baseDir}/.venv/bin/vfinance-news market --json
```

### Portfolio Management

```bash
# List portfolio
{baseDir}/.venv/bin/vfinance-news portfolio list

# Add stock
{baseDir}/.venv/bin/vfinance-news portfolio add NVDA --name "NVIDIA Corporation" --category Tech

# Remove stock
{baseDir}/.venv/bin/vfinance-news portfolio remove TSLA

# Import from CSV
{baseDir}/.venv/bin/vfinance-news portfolio import ~/my_stocks.csv

# Interactive portfolio creation
{baseDir}/.venv/bin/vfinance-news portfolio create
```

### Ticker News

```bash
# News for specific stock
{baseDir}/.venv/bin/vfinance-news news AAPL
{baseDir}/.venv/bin/vfinance-news news TSLA
```

## Configuration

### Portfolio CSV Format

Location: `{baseDir}/config/portfolio.csv`

```csv
symbol,name,category,notes
AAPL,Apple Inc.,Tech,Core holding
NVDA,NVIDIA Corporation,Tech,AI play
MSFT,Microsoft Corporation,Tech,
```

### Sources Configuration

Location: `{baseDir}/config/config.json`
  
- RSS feeds for WSJ, Barron's, CNBC, Yahoo
- Market indices by region

## Sample Output

```markdown
🌅 **Börsen-Morgen-Briefing**
Dienstag, 21. Januar 2026 | 06:30 Uhr

📊 **Märkte**
• S&P 500: 5.234 (+0,3%)
• DAX: 16.890 (-0,1%)
• Nikkei: 35.678 (+0,5%)

📈 **Dein Portfolio**
• AAPL $256 (+1,2%) — iPhone-Verkäufe übertreffen Erwartungen
• NVDA $512 (+3,4%) — KI-Chip-Nachfrage steigt

🔥 **Top Stories**
• [WSJ] Fed signalisiert mögliche Zinssenkung im März
• [CNBC] Tech-Sektor führt Rally an

🤖 **Analyse**
Der S&P zeigt Stärke. Dein Portfolio profitiert von NVDA's 
Momentum. Fed-Kommentare könnten Volatilität auslösen.
```

## Integration

### With OpenClaw Agent
The agent will automatically use this skill when asked about:
- "What's the market doing?"
- "News for my portfolio"
- "Generate morning briefing"
- "What's happening with AAPL?"

## Files

```
skills/vfinance-news/
├── SKILL.md              # This documentation
├── config/
│   ├── portfolio.csv     # Your watchlist
│   ├── config.json       # RSS/API configuration
│   ├── alerts.json       # Price target alerts
│   └── manual_earnings.json  # Earnings calendar overrides
├── vfinance_news/
│   ├── cli.py            # Main CLI entrypoint
│   ├── briefing.py       # Briefing generator
│   ├── fetch_news.py     # News aggregator
│   ├── portfolio.py      # Portfolio CRUD
│   ├── summarize.py      # AI summarization
│   ├── alerts.py         # Price alert management
│   ├── earnings.py       # Earnings calendar
│   ├── ranking.py        # Headline ranking
│   └── stocks.py         # Stock management
├── workflows/
│   ├── briefing.yaml     # Lobster workflow with approval gate
│   └── README.md         # Workflow documentation
├── cron/
│   ├── morning.sh        # Morning cron
│   └── evening.sh        # Evening cron
└── cache/                # 15-minute news cache
```

## Dependencies

- Python 3.10+
- `feedparser` (`pip install feedparser`)

## Troubleshooting

### RSS feeds timing out
- Check network connectivity
- WSJ/Barron's may require subscription cookies for some content
- Free feeds (CNBC, Yahoo) should always work
