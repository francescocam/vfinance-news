#!/usr/bin/env bash
set -euo pipefail

# Optional user config (edit these defaults if you want).
DEFAULT_REMOTE_HOST="fcamisa@100.86.145.121"
DEFAULT_REMOTE_DIR="/home/fcamisa/.openclaw/workspace/skills/vfinance-news"
DEFAULT_DRY_RUN=0
DEFAULT_USE_DELETE=1

# Sync this repository to a remote host using rsync.
#
# Required env:
#   REMOTE_HOST            e.g. user@remote-host
#
# Optional env:
#   REMOTE_DIR             default: /tmp/vfinance-news-sync
#
# Usage:
#   REMOTE_HOST=user@host ./tools/rsync-repo.sh
#   REMOTE_HOST=user@host ./tools/rsync-repo.sh --remote-dir /tmp/my-copy
#   REMOTE_HOST=user@host ./tools/rsync-repo.sh --dry-run

usage() {
  cat <<'EOF'
Usage: REMOTE_HOST=user@host ./tools/rsync-repo.sh [options]

Options:
  --remote-dir <path>  Destination path on remote host
  --dry-run            Show what would be synced without writing changes
  --no-delete          Do not delete remote files missing locally
  -h, --help           Show this help
EOF
}

REMOTE_HOST="${REMOTE_HOST:-${DEFAULT_REMOTE_HOST}}"
REMOTE_DIR="${REMOTE_DIR:-${DEFAULT_REMOTE_DIR}}"
DRY_RUN="${DEFAULT_DRY_RUN}"
USE_DELETE="${DEFAULT_USE_DELETE}"

if [[ -z "${REMOTE_HOST}" ]]; then
  echo "ERROR: REMOTE_HOST is required (e.g. export REMOTE_HOST=user@host)." >&2
  exit 2
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --remote-dir)
      [[ $# -ge 2 ]] || { echo "ERROR: --remote-dir requires a value." >&2; exit 2; }
      REMOTE_DIR="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --no-delete)
      USE_DELETE=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if ! command -v rsync >/dev/null 2>&1; then
  echo "ERROR: rsync not found locally." >&2
  exit 10
fi

if ! ssh "${REMOTE_HOST}" "command -v rsync >/dev/null 2>&1"; then
  echo "ERROR: rsync not found on remote host ${REMOTE_HOST}." >&2
  exit 11
fi

echo "Syncing repo to ${REMOTE_HOST}:${REMOTE_DIR}"
ssh "${REMOTE_HOST}" "mkdir -p '${REMOTE_DIR}'"

RSYNC_ARGS=(-az)
if [[ "${USE_DELETE}" -eq 1 ]]; then
  RSYNC_ARGS+=(--delete)
fi
if [[ "${DRY_RUN}" -eq 1 ]]; then
  RSYNC_ARGS+=(--dry-run --itemize-changes)
fi

rsync "${RSYNC_ARGS[@]}" \
  --exclude '.git/' \
  --exclude '.venv/' \
  --exclude '__pycache__/' \
  --exclude '.pytest_cache/' \
  --exclude 'htmlcov/' \
  --exclude '.mypy_cache/' \
  --exclude '.ruff_cache/' \
  --exclude 'cache/' \
  --exclude 'tmp/remote-llm-runs/' \
  --exclude '*.pyc' \
  "${REPO_ROOT}/" "${REMOTE_HOST}:${REMOTE_DIR}/"

echo "Done."
