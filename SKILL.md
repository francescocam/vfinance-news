---
name: vfinance-news
description: Market news briefings with AI summaries and price alerts. Aggregates headlines from US/Europe/Japan markets. Use when: 'stock news', 'market updates', 'morning briefing', 'evening market wrap', 'financial headlines', 'price alerts', 'what happened in the market'. Supports English/German output. NOT for fundamental analysis or scoring (use equity-research). NOT for raw financial data queries.
---

# Finance News Skill

AI-powered market news briefings with configurable language output.

## First-Time Setup

Run the interactive setup wizard to configure your sources and schedule:

```bash
vfinance-news setup
```

The wizard will guide you through:
- 📰 **RSS Feeds:** Enable/disable WSJ, Barron's, CNBC, Yahoo, etc.
- 📊 **Markets:** Choose regions (US, Europe, Japan, Asia)
- 🌐 **Language:** Set default language (English/German)
- ⏰ **Schedule:** Configure morning/evening cron times

You can also configure specific sections:
```bash
vfinance-news setup --section feeds     # Just RSS feeds
vfinance-news setup --section schedule  # Just cron schedule
vfinance-news setup --reset             # Reset to defaults
vfinance-news config                    # Show current config
```

## Quick Start

```bash
# Generate briefing
vfinance-news briefing

# View market overview
vfinance-news market

# Get news for your portfolio
vfinance-news portfolio

# Get news for specific stock
vfinance-news news AAPL
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
- Gemini-powered analysis
- Configurable language (English/German)
- Briefing styles: summary, analysis, headlines

### 📅 Automated Briefings
- **Morning:** 6:30 AM PT (US market open)
- **Evening:** 1:00 PM PT (US market close)

## Commands

### Briefing Generation

```bash
# Briefing (English is default)
vfinance-news briefing

# German language option
vfinance-news briefing --lang de

# Analysis style (more detailed)
vfinance-news briefing --style analysis
```

### Market Data

```bash
# Market overview (indices + top headlines)
vfinance-news market

# JSON output for processing
vfinance-news market --json
```

### Portfolio Management

```bash
# List portfolio
vfinance-news portfolio list

# Add stock
vfinance-news portfolio add NVDA --name "NVIDIA Corporation" --category Tech

# Remove stock
vfinance-news portfolio remove TSLA

# Import from CSV
vfinance-news portfolio import ~/my_stocks.csv

# Interactive portfolio creation
vfinance-news portfolio create
```

### Ticker News

```bash
# News for specific stock
vfinance-news news AAPL
vfinance-news news TSLA
```

## Configuration

### Portfolio CSV Format

Location: `~/clawd/skills/vfinance-news/config/portfolio.csv`

```csv
symbol,name,category,notes
AAPL,Apple Inc.,Tech,Core holding
NVDA,NVIDIA Corporation,Tech,AI play
MSFT,Microsoft Corporation,Tech,
```

### Sources Configuration

Location: `~/clawd/skills/vfinance-news/config/config.json` (legacy fallback: `config/sources.json`)

- RSS feeds for WSJ, Barron's, CNBC, Yahoo
- Market indices by region
- Language settings

## Cron Jobs

### Setup via OpenClaw

```bash
# Add morning briefing cron job
openclaw cron add --schedule "30 6 * * 1-5" \
  --timezone "America/Los_Angeles" \
  --command "bash ~/clawd/skills/vfinance-news/cron/morning.sh"

# Add evening briefing cron job
openclaw cron add --schedule "0 13 * * 1-5" \
  --timezone "America/Los_Angeles" \
  --command "bash ~/clawd/skills/vfinance-news/cron/evening.sh"
```

### Manual Cron (crontab)

```cron
# Morning briefing (6:30 AM PT, weekdays)
30 6 * * 1-5 bash ~/clawd/skills/vfinance-news/cron/morning.sh

# Evening briefing (1:00 PM PT, weekdays)
0 13 * * 1-5 bash ~/clawd/skills/vfinance-news/cron/evening.sh
```

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

### With Lobster (Workflow Engine)

Run briefings via [Lobster](https://github.com/openclaw/lobster) for approval gates and resumability:

```bash
# Run with approval
lobster "workflows.run --file workflows/briefing.yaml"

# With custom args
lobster "workflows.run --file workflows/briefing.yaml --args-json '{\"lang\":\"en\"}'"
```

See `workflows/README.md` for full documentation.

## Files

```
skills/vfinance-news/
├── SKILL.md              # This documentation
├── config/
│   ├── portfolio.csv     # Your watchlist
│   ├── config.json       # RSS/API/language configuration
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
- Gemini CLI (`brew install gemini-cli`)

## Troubleshooting

### Gemini not working
```bash
# Authenticate Gemini
gemini  # Follow login flow
```

### RSS feeds timing out
- Check network connectivity
- WSJ/Barron's may require subscription cookies for some content
- Free feeds (CNBC, Yahoo) should always work
