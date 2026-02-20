#!/usr/bin/env bash
# Weekly Earnings Alert Cron Job (Lobster Workflow)
# Schedule: Sunday 7:00 AM PT (before market week starts)
#
# Sends upcoming week's earnings calendar to WhatsApp/Telegram.
# Shows all portfolio stocks reporting Mon-Fri.

set -e

export SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export VFINANCE_NEWS_TARGET="${VFINANCE_NEWS_TARGET:?VFINANCE_NEWS_TARGET must be set}"
export VFINANCE_NEWS_CHANNEL="${VFINANCE_NEWS_CHANNEL:?VFINANCE_NEWS_CHANNEL must be set}"

echo "[$(date)] Checking next week's earnings via Lobster..."

lobster run --file "$SKILL_DIR/workflows/earnings-weekly-cron.yaml" \
  --args-json '{}'

echo "[$(date)] Weekly earnings alert complete."
