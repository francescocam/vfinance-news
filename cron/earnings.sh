#!/usr/bin/env bash
# Earnings Alert Cron Job (Lobster Workflow)
# Schedule: 6:00 AM PT / 9:00 AM ET (30 min before market open)
#
# Sends today's earnings calendar to WhatsApp/Telegram.
# Alerts users about portfolio stocks reporting today.

set -e

export SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export VFINANCE_NEWS_TARGET="${VFINANCE_NEWS_TARGET:?VFINANCE_NEWS_TARGET must be set}"
export VFINANCE_NEWS_CHANNEL="${VFINANCE_NEWS_CHANNEL:?VFINANCE_NEWS_CHANNEL must be set}"

echo "[$(date)] Checking today's earnings via Lobster..."

lobster run --file "$SKILL_DIR/workflows/earnings-cron.yaml" \
  --args-json '{}'

echo "[$(date)] Earnings alert complete."
