#!/usr/bin/env bash
# Morning Briefing Cron Job (Lobster Workflow)
# Schedule: 6:30 AM PT (US Market Open at 9:30 AM ET)
#
# Uses Lobster workflow to generate and send briefing directly.

set -e

export SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export VFINANCE_NEWS_TARGET="${VFINANCE_NEWS_TARGET:?VFINANCE_NEWS_TARGET must be set}"
export VFINANCE_NEWS_CHANNEL="${VFINANCE_NEWS_CHANNEL:?VFINANCE_NEWS_CHANNEL must be set}"

echo "[$(date)] Starting morning briefing via Lobster..."

lobster run --file "$SKILL_DIR/workflows/briefing-cron.yaml" \
  --args-json '{"time":"morning","lang":"de"}'

echo "[$(date)] Morning briefing complete."
