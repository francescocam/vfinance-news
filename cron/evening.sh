#!/usr/bin/env bash
# Evening Briefing Cron Job (Lobster Workflow)
# Schedule: 1:00 PM PT (US Market Close at 4:00 PM ET)
#
# Uses Lobster workflow to generate and send briefing directly.

set -e

export SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export VFINANCE_NEWS_TARGET="${VFINANCE_NEWS_TARGET:?VFINANCE_NEWS_TARGET must be set}"
export VFINANCE_NEWS_CHANNEL="${VFINANCE_NEWS_CHANNEL:?VFINANCE_NEWS_CHANNEL must be set}"

echo "[$(date)] Starting evening briefing via Lobster..."

lobster run --file "$SKILL_DIR/workflows/briefing-cron.yaml" \
  --args-json '{"fast":"false"}'

echo "[$(date)] Evening briefing complete."
