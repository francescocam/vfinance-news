#!/usr/bin/env bash
set -euo pipefail

# Temporary remote LLM test wrapper.
# Syncs local workspace to remote, bootstraps venv, runs summarize --llm --json,
# streams output live, and stores local artifacts.
#
# Required env:
#   REMOTE_HOST            e.g. user@remote-host
#
# Optional env:
#   REMOTE_BASE_DIR        default: /tmp/vfinance-news-remote-tests
#   REMOTE_PYTHON          default: python3
#   REMOTE_RUN_BRIEFING_CHECK=1   run secondary briefing CLI check
#
# Usage:
#   ./tools/remote-llm-test.sh [summarize args...]
# Example:
#   ./tools/remote-llm-test.sh --style briefing --llm --json

if [[ -z "${REMOTE_HOST:-}" ]]; then
  echo "ERROR: REMOTE_HOST is required (e.g. export REMOTE_HOST=user@host)." >&2
  exit 2
fi

REMOTE_BASE_DIR="${REMOTE_BASE_DIR:-/tmp/vfinance-news-remote-tests}"
REMOTE_PYTHON="${REMOTE_PYTHON:-python3}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
RUN_ID="$(date +%Y%m%d-%H%M%S)"
REMOTE_RUN_DIR="${REMOTE_BASE_DIR}/${RUN_ID}"
LOCAL_ARTIFACT_DIR="${REPO_ROOT}/tmp/remote-llm-runs/${RUN_ID}"

mkdir -p "${LOCAL_ARTIFACT_DIR}"
STDOUT_FILE="${LOCAL_ARTIFACT_DIR}/stdout.json"
STDERR_FILE="${LOCAL_ARTIFACT_DIR}/stderr.log"
COMMAND_FILE="${LOCAL_ARTIFACT_DIR}/command.txt"
REMOTE_PATH_FILE="${LOCAL_ARTIFACT_DIR}/remote_path.txt"

echo "${REMOTE_RUN_DIR}" > "${REMOTE_PATH_FILE}"

echo "=== Remote LLM Test ==="
echo "Host: ${REMOTE_HOST}"
echo "Remote run dir: ${REMOTE_RUN_DIR}"
echo "Local artifacts: ${LOCAL_ARTIFACT_DIR}"

echo "[1/6] SSH preflight..."
if ! ssh "${REMOTE_HOST}" "echo ok" >/dev/null 2>&1; then
  echo "ERROR: SSH preflight failed for ${REMOTE_HOST}." >&2
  echo "Try: ssh ${REMOTE_HOST}" >&2
  exit 10
fi

echo "[2/6] Remote OpenClaw preflight..."
REMOTE_SHELL_MODE="login"
REMOTE_OPENCLAW_BIN="$(
  ssh "${REMOTE_HOST}" "bash -lc '
    if command -v openclaw >/dev/null 2>&1; then
      command -v openclaw
    elif [ -x \"\$HOME/.local/bin/openclaw\" ]; then
      echo \"\$HOME/.local/bin/openclaw\"
    elif [ -x \"\$HOME/bin/openclaw\" ]; then
      echo \"\$HOME/bin/openclaw\"
    else
      exit 1
    fi
  '" 2>/dev/null || true
)"

if [[ -z "${REMOTE_OPENCLAW_BIN}" ]]; then
  REMOTE_OPENCLAW_BIN="$(
    ssh "${REMOTE_HOST}" "bash -ic '
      if command -v openclaw >/dev/null 2>&1; then
        command -v openclaw
      elif [ -x \"\$HOME/.local/bin/openclaw\" ]; then
        echo \"\$HOME/.local/bin/openclaw\"
      elif [ -x \"\$HOME/bin/openclaw\" ]; then
        echo \"\$HOME/bin/openclaw\"
      else
        exit 1
      fi
    '" 2>/dev/null || true
  )"
  if [[ -n "${REMOTE_OPENCLAW_BIN}" ]]; then
    REMOTE_SHELL_MODE="interactive"
  fi
fi

if [[ -z "${REMOTE_OPENCLAW_BIN}" ]]; then
  echo "ERROR: 'openclaw' not found on remote host ${REMOTE_HOST}." >&2
  echo "Install/open PATH on remote, then retry." >&2
  echo "Debug with: ssh ${REMOTE_HOST} \"bash -lc 'command -v openclaw; echo PATH=\\\$PATH'\"" >&2
  echo "Also try: ssh ${REMOTE_HOST} \"bash -ic 'command -v openclaw; type -a openclaw; echo PATH=\\\$PATH'\"" >&2
  exit 11
fi
echo "Resolved remote openclaw: ${REMOTE_OPENCLAW_BIN} (shell=${REMOTE_SHELL_MODE})"

# Optional sanity probe only; do not fail hard because some openclaw builds
# return non-zero for --help/--version despite being usable.
if [[ "${REMOTE_SHELL_MODE}" == "interactive" ]]; then
  ssh "${REMOTE_HOST}" "bash -ic '${REMOTE_OPENCLAW_BIN} --version >/dev/null 2>&1 || ${REMOTE_OPENCLAW_BIN} --help >/dev/null 2>&1 || true'"
else
  ssh "${REMOTE_HOST}" "bash -lc '${REMOTE_OPENCLAW_BIN} --version >/dev/null 2>&1 || ${REMOTE_OPENCLAW_BIN} --help >/dev/null 2>&1 || true'"
fi

echo "[3/6] Sync workspace..."
ssh "${REMOTE_HOST}" "mkdir -p '${REMOTE_RUN_DIR}'"

SYNC_DONE=0
if command -v rsync >/dev/null; then
  if ssh "${REMOTE_HOST}" "command -v rsync >/dev/null"; then
    rsync -az --delete \
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
      "${REPO_ROOT}/" "${REMOTE_HOST}:${REMOTE_RUN_DIR}/"
    SYNC_DONE=1
  fi
fi

if [[ "${SYNC_DONE}" -eq 0 ]]; then
  echo "rsync unavailable locally/remotely, using tar-over-ssh fallback..."
  ssh "${REMOTE_HOST}" "mkdir -p '${REMOTE_RUN_DIR}'"
  tar -C "${REPO_ROOT}" \
    --exclude='.git' \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='.pytest_cache' \
    --exclude='htmlcov' \
    --exclude='.mypy_cache' \
    --exclude='.ruff_cache' \
    --exclude='cache' \
    --exclude='tmp/remote-llm-runs' \
    --exclude='*.pyc' \
    -cf - . | ssh "${REMOTE_HOST}" "tar -xf - -C '${REMOTE_RUN_DIR}'"
fi

echo "[4/6] Remote bootstrap (.venv + editable install)..."
if [[ "${REMOTE_SHELL_MODE}" == "interactive" ]]; then
  ssh "${REMOTE_HOST}" "bash -ic 'cd \"${REMOTE_RUN_DIR}\" && ${REMOTE_PYTHON} -m venv .venv && .venv/bin/pip install -e . >/dev/null'"
else
  ssh "${REMOTE_HOST}" "bash -lc 'cd \"${REMOTE_RUN_DIR}\" && ${REMOTE_PYTHON} -m venv .venv && .venv/bin/pip install -e . >/dev/null'"
fi

FORWARDED_ARGS=("$@")

# Enforce LLM/json mode for this test helper.
HAS_LLM=0
HAS_JSON=0
for arg in "${FORWARDED_ARGS[@]}"; do
  [[ "$arg" == "--llm" ]] && HAS_LLM=1
  [[ "$arg" == "--json" ]] && HAS_JSON=1
done
[[ "${HAS_LLM}" -eq 0 ]] && FORWARDED_ARGS+=("--llm")
[[ "${HAS_JSON}" -eq 0 ]] && FORWARDED_ARGS+=("--json")

REMOTE_ARGS_QUOTED=""
for arg in "${FORWARDED_ARGS[@]}"; do
  REMOTE_ARGS_QUOTED+=" $(printf '%q' "$arg")"
done

REMOTE_SUMMARIZE_CMD=".venv/bin/python -m vfinance_news.summarize${REMOTE_ARGS_QUOTED}"
echo "${REMOTE_SUMMARIZE_CMD}" > "${COMMAND_FILE}"

echo "[5/6] Run remote summarize..."
set +e
if [[ "${REMOTE_SHELL_MODE}" == "interactive" ]]; then
  ssh "${REMOTE_HOST}" "bash -ic 'cd \"${REMOTE_RUN_DIR}\" && ${REMOTE_SUMMARIZE_CMD}'" \
    > >(tee "${STDOUT_FILE}") \
    2> >(tee "${STDERR_FILE}" >&2)
else
  ssh "${REMOTE_HOST}" "bash -lc 'cd \"${REMOTE_RUN_DIR}\" && ${REMOTE_SUMMARIZE_CMD}'" \
    > >(tee "${STDOUT_FILE}") \
    2> >(tee "${STDERR_FILE}" >&2)
fi
RUN_EXIT=$?
set -e

if [[ "${REMOTE_RUN_BRIEFING_CHECK:-0}" == "1" ]]; then
  echo "[6/6] Optional briefing CLI check..."
  BRIEFING_OUT="${LOCAL_ARTIFACT_DIR}/briefing.stdout.json"
  BRIEFING_ERR="${LOCAL_ARTIFACT_DIR}/briefing.stderr.log"
  set +e
  if [[ "${REMOTE_SHELL_MODE}" == "interactive" ]]; then
    ssh "${REMOTE_HOST}" "bash -ic 'cd \"${REMOTE_RUN_DIR}\" && .venv/bin/vfinance-news briefing --llm --json'" \
      > >(tee "${BRIEFING_OUT}") \
      2> >(tee "${BRIEFING_ERR}" >&2)
  else
    ssh "${REMOTE_HOST}" "bash -lc 'cd \"${REMOTE_RUN_DIR}\" && .venv/bin/vfinance-news briefing --llm --json'" \
      > >(tee "${BRIEFING_OUT}") \
      2> >(tee "${BRIEFING_ERR}" >&2)
  fi
  BRIEFING_EXIT=$?
  set -e
  echo "briefing_exit=${BRIEFING_EXIT}" >> "${COMMAND_FILE}"
fi

echo
echo "=== Run Summary ==="
echo "remote_host=${REMOTE_HOST}"
echo "remote_run_dir=${REMOTE_RUN_DIR}"
echo "exit_code=${RUN_EXIT}"

python3 - "${STDOUT_FILE}" "${RUN_EXIT}" <<'PY'
import json
import pathlib
import sys

stdout_path = pathlib.Path(sys.argv[1])
run_exit = int(sys.argv[2])

def out(line: str) -> None:
    print(line)

if not stdout_path.exists():
    out("stdout_valid_json=false")
    out("validation=FAIL (missing stdout file)")
    raise SystemExit(1 if run_exit == 0 else 0)

raw = stdout_path.read_text(encoding="utf-8", errors="replace").strip()
try:
    data = json.loads(raw)
except Exception:
    out("stdout_valid_json=false")
    out("validation=FAIL (invalid JSON)")
    raise SystemExit(1 if run_exit == 0 else 0)

summary_mode = data.get("summary_mode")
summary_model_used = data.get("summary_model_used")
summary_model_attempts = data.get("summary_model_attempts")
summary = str(data.get("summary", "") or "")

out("stdout_valid_json=true")
out(f"summary_mode={summary_mode}")
out(f"summary_model_used={summary_model_used}")
out(f"summary_model_attempts={summary_model_attempts}")

is_success = (
    run_exit == 0
    and summary_mode == "llm"
    and summary_model_used == "openclaw"
    and summary_model_attempts == ["openclaw"]
    and summary.strip() != ""
    and not summary.startswith("⚠️")
)
out("validation=PASS" if is_success else "validation=FAIL")
PY

if [[ "${RUN_EXIT}" -ne 0 ]]; then
  echo "Remote command failed. See ${STDERR_FILE}" >&2
  exit "${RUN_EXIT}"
fi

echo "Artifacts saved under ${LOCAL_ARTIFACT_DIR}"
