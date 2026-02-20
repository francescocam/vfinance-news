#!/usr/bin/env bash
# Price Alerts Cron Job (Lobster Workflow)
# Schedule: 2:00 PM PT / 5:00 PM ET (1 hour after market close)
#
# Checks price alerts against current prices including after-hours.
# Sends triggered alerts and watchlist status to WhatsApp/Telegram.

set -e

export SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export VFINANCE_NEWS_TARGET="${VFINANCE_NEWS_TARGET:?VFINANCE_NEWS_TARGET must be set}"
export VFINANCE_NEWS_CHANNEL="${VFINANCE_NEWS_CHANNEL:?VFINANCE_NEWS_CHANNEL must be set}"

echo "[$(date)] Checking price alerts via Lobster..."

lobster run --file "$SKILL_DIR/workflows/alerts-cron.yaml" \
  --args-json '{}'

echo "[$(date)] Price alerts check complete."
