# vfinance-news CLI Usage

Detailed command reference for the `vfinance-news` command-line interface.

## Install And Run

```bash
# From repository root
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# CLI entrypoint
vfinance-news --help
```

## Top-Level Commands

```text
vfinance-news {setup,config,briefing,market,portfolio,portfolio-only,news,alerts,earnings}
```

| Command | Purpose |
|---|---|
| `setup` | Run interactive setup wizard |
| `config` | Show current configuration |
| `briefing` | Generate formatted market briefing |
| `market` | Market overview + headlines |
| `portfolio` | Portfolio news, or portfolio management subcommands |
| `portfolio-only` | Top portfolio gainers/losers with news |
| `news` | News for one ticker |
| `alerts` | Price target alerts management |
| `earnings` | Earnings calendar tracking |

## Important Routing Behavior

`portfolio` supports two modes:

1. `vfinance-news portfolio` (and flags) routes to news mode (`fetch_news.py`).
2. `vfinance-news portfolio <subcommand>` routes to portfolio manager (`portfolio.py`), where `<subcommand>` is one of:
   - `list`
   - `add`
   - `remove`
   - `import`
   - `create`
   - `symbols`

Examples:

```bash
# Portfolio news mode
vfinance-news portfolio --limit 10 --max-stocks 8

# Portfolio management mode
vfinance-news portfolio add NVDA --name "NVIDIA Corporation" --type Holding
```

## `briefing`

Generate market briefing, optionally with LLM summary.

```text
vfinance-news briefing [briefing options...]
```

Briefing period is selected automatically using a hard local-time cutoff:
morning before 12:00, evening from 12:00 onward.

Forwarded options (implemented in `vfinance_news/briefing.py`):

| Option | Description |
|---|---|
| `--style {briefing,analysis,headlines}` | Summary style |
| `--lang {en,de}` | Output language |
| `--json` | Output JSON |
| `--deadline <seconds>` | Global timeout/deadline |
| `--llm` | Enable LLM-generated summary |
| `--fast` | Faster mode with reduced work |
| `--debug` | Write debug log with source details |

Model/provider selection for summary generation is handled by OpenClaw gateway configuration, not CLI flags.

Examples:

```bash
vfinance-news briefing --lang de
vfinance-news briefing --style analysis --llm
```

## `market`

Market overview and headlines.

```text
vfinance-news market [options]
```

Options:

| Option | Description |
|---|---|
| `--json` | Output JSON |
| `--limit <int>` | Max articles per source (default: `5`) |
| `--deadline <seconds>` | Global deadline |

Examples:

```bash
vfinance-news market
vfinance-news market --limit 8 --deadline 120
vfinance-news market --json
```

## `portfolio` (News Mode)

Portfolio-specific market/news summary.

```text
vfinance-news portfolio [options]
```

Options:

| Option | Description |
|---|---|
| `--json` | Output JSON |
| `--limit <int>` | Max articles per source (default: `5`) |
| `--max-stocks <int>` | Max portfolio symbols to fetch (default: `5`) |
| `--deadline <seconds>` | Global deadline |

Examples:

```bash
vfinance-news portfolio
vfinance-news portfolio --max-stocks 10 --limit 3
vfinance-news portfolio --json
```

## `portfolio-only`

Top gainers and losers from your portfolio, with related news.

```text
vfinance-news portfolio-only [options]
```

Options:

| Option | Description |
|---|---|
| `--json` | Output JSON |
| `--limit <int>` | Max news items per ticker (default: `5`) |

Examples:

```bash
vfinance-news portfolio-only
vfinance-news portfolio-only --limit 2
```

## `news`

Ticker-specific news.

```text
vfinance-news news <symbol>
```

Examples:

```bash
vfinance-news news AAPL
vfinance-news news CSU.TO
```

## `portfolio` (Management Subcommands)

### `portfolio list`

List all stocks grouped by type/category.

```text
vfinance-news portfolio list
```

### `portfolio add`

Add one symbol to portfolio CSV.

```text
vfinance-news portfolio add <symbol> [--name <name>] [--category <category>] [--notes <notes>] [--type {Holding,Watchlist}]
```

Examples:

```bash
vfinance-news portfolio add NVDA
vfinance-news portfolio add CSU.TO --name "Capstone Copper" --category Materials --type Holding
```

### `portfolio remove`

Remove one symbol from portfolio CSV.

```text
vfinance-news portfolio remove <symbol>
```

### `portfolio import`

Import from external CSV file.

```text
vfinance-news portfolio import <file>
```

### `portfolio create`

Interactive portfolio creation mode.

```text
vfinance-news portfolio create
```

### `portfolio symbols`

Print symbols only.

```text
vfinance-news portfolio symbols [--json]
```

## `alerts`

Price target alert management.

```text
vfinance-news alerts <subcommand> [...]
```

Subcommands:

| Subcommand | Usage |
|---|---|
| `list` | `vfinance-news alerts list` |
| `set` | `vfinance-news alerts set <ticker> <target> [--note <text>] [--user <name>] [--currency <code>]` |
| `delete` | `vfinance-news alerts delete <ticker>` |
| `snooze` | `vfinance-news alerts snooze <ticker> [--days <int>]` |
| `update` | `vfinance-news alerts update <ticker> <target> [--note <text>]` |
| `check` | `vfinance-news alerts check [--json] [--lang <en|de>]` |

Examples:

```bash
vfinance-news alerts set CRWD 400 --note "Buy zone" --currency USD
vfinance-news alerts update CRWD 420 --note "Raised target"
vfinance-news alerts snooze CRWD --days 14
vfinance-news alerts check --lang de
```

## `earnings`

Track upcoming earnings for portfolio symbols.

```text
vfinance-news earnings <subcommand> [...]
```

Subcommands:

| Subcommand | Usage |
|---|---|
| `list` | `vfinance-news earnings list [--refresh|-r]` |
| `check` | `vfinance-news earnings check [--verbose|-v] [--json] [--lang <en|de>] [--week]` |
| `refresh` | `vfinance-news earnings refresh` |

Examples:

```bash
vfinance-news earnings list --refresh
vfinance-news earnings check --week --lang en
vfinance-news earnings refresh
```

## `setup` And `config`

These are top-level convenience wrappers around setup module subcommands.

### `setup`

Runs setup wizard.

```text
vfinance-news setup
```

Underlying setup module supports:

```text
wizard [--reset] [--section {feeds,markets,language,schedule}]
```

### `config`

Prints current configuration.

```text
vfinance-news config
```

Underlying setup module command:

```text
show
```

## Environment Variables

| Variable | Description |
|---|---|
| `PORTFOLIOS_DIR` | Optional shared portfolio location; uses `$PORTFOLIOS_DIR/watchlists/portfolio.csv` |

## Data Files

| File | Purpose |
|---|---|
| `config/config.json` | Main source/market/language configuration |
| `config/portfolio.csv` | Portfolio/watchlist records |
| `config/alerts.json` | Stored alert definitions |
| `cache/earnings_cache.json` | Earnings cache data |

## Troubleshooting

1. `vfinance-news portfolio add ...` reports unrecognized args:
   - Ensure you are on a version with `portfolio <subcommand>` routing.
   - Reinstall editable package: `pip install -e .`
2. Commands seem missing after code changes:
   - Confirm active virtual environment: `which vfinance-news`
   - Reinstall inside active env: `pip install -e .`
