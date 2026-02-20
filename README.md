# Value Investor Tailored Finance News Skill for OpenClaw

AI-powered market news briefings tailored to value investors.

## Features

- **Multi-source aggregation:** Reuters, WSJ, FT, Bloomberg, CNBC, Yahoo Finance, Tagesschau, Handelsblatt
- **Global markets:** US (S&P, Dow, NASDAQ), Europe (DAX, STOXX, FTSE), Japan (Nikkei)
- **AI summaries:** LLM-powered analysis in English
- **Automated briefings:** Morning (market open) and evening (market close)
- **Portfolio tracking:** Personalized news for your stocks with price alerts
- **Customizable:** Configure sources, markets

## Quick Start


### CLI

```bash
# Generate a briefing
vfinance-news briefing

# Use fast mode + deadline (recommended)
vfinance-news briefing --fast --deadline 300
```

Full command reference: `docs/CLI_USAGE.md`

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SKILL_DIR` | Path to skill directory (for Lobster) | `$HOME/projects/vfinance-news-openclaw-skill` |

## Installation

### Native Python Package (`.venv`)

```bash
# Clone repository
git clone https://github.com/kesslerio/vfinance-news-openclaw-skill.git \
    ~/openclaw/skills/vfinance-news

# Create virtual environment
cd ~/openclaw/skills/vfinance-news
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Development Setup

Use this section when contributing code or running tests locally.

Prerequisites:
- Python 3.10+
- `uv.lock` is included for reproducible locking, but the primary dev workflow here is `.venv` + `pip`.

```bash
# From repo root
python3 -m venv .venv
source .venv/bin/activate

# Install project + dev dependencies
pip install -e ".[dev]"

# Fallback if extras are unavailable
pip install -e .
pip install -r requirements-test.txt
```

### Common Dev Commands

```bash
# Lint
.venv/bin/ruff check .

# Run all tests
.venv/bin/python -m pytest

# Run one test file
.venv/bin/python -m pytest tests/test_portfolio.py

# Run tests with coverage
.venv/bin/python -m pytest --cov=vfinance_news --cov-report=term-missing --cov-report=html

# CLI smoke check
.venv/bin/vfinance-news --help
```

Troubleshooting:
- If `pytest` or `ruff` is not found, activate `.venv` or run tools via `.venv/bin/...`.
- If `vfinance-news` is missing, reinstall: `pip install -e ".[dev]"`.

## Configuration

Configuration is stored in `config/config.json`:

- **RSS Feeds:** Enable/disable news sources per region
- **Markets:** Choose which indices to track
- **Schedule:** Cron times for morning/evening briefings

Run the setup wizard for interactive configuration:

```bash
vfinance-news setup
```

## Lobster Workflow

The skill includes a Lobster workflow (`workflows/briefing.yaml`) that:

1. **Generates** briefing via local `.venv` CLI
2. **Validates** deterministic structure
3. **Halts** for approval (shows preview)

### Workflow Arguments

| Arg | Default | Description |
|-----|---------|-------------|
| `fast` | `false` | Use fast mode (shorter timeouts) |

## Portfolio

Manage your stock watchlist in `config/portfolio.csv`:

```bash
vfinance-news portfolio list              # View portfolio
vfinance-news portfolio add NVDA          # Add stock
vfinance-news portfolio remove TSLA       # Remove stock
vfinance-news portfolio import stocks.csv # Import from CSV
```

Portfolio briefings show:
- Top gainers and losers from your holdings
- Relevant news articles
- Shortened hyperlinks for easy access

## Dependencies

- Python 3.10+
- openclaw CLI (for LLM access)
- Lobster (for workflow automation)

## License

Apache 2.0 - See [LICENSE](LICENSE) file for details.

## Related Skills

- **[task-tracker](https://github.com/kesslerio/task-tracker-openclaw-skill):** Personal task management with daily standups

# Credits

Based on [vfinance-news-openclaw-skill](https://github.com/kesslerio/vfinance-news-openclaw-skill)
