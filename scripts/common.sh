#!/usr/bin/env bash
set -euo pipefail
JC_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JC_DATA_DIR="${JC_DATA_DIR:-$(dirname "$JC_ROOT")/jialiangcraft-vanilla-26.3-data}"
JC_SESSION=jialiangcraft
JC_JAVA="$JC_ROOT/.tools/java25/bin/java"
export JC_ROOT JC_DATA_DIR JC_SESSION JC_JAVA

jc_packwiz() {
  if [[ -x "$JC_ROOT/.tools/packwiz" ]]; then printf '%s\n' "$JC_ROOT/.tools/packwiz";
  elif command -v packwiz >/dev/null 2>&1; then command -v packwiz;
  else echo 'Packwiz is missing. See docs/SERVER.md.' >&2; return 1; fi
}

jc_running() { tmux has-session -t "$JC_SESSION" 2>/dev/null; }
jc_assert_session_data() {
  if jc_running; then
    local actual session_data
    session_data="$(tmux show-environment -t "$JC_SESSION" JC_DATA_DIR 2>/dev/null || true)"
    if [[ "$session_data" != JC_DATA_DIR=* ]]; then
      session_data="$(tmux show-environment -g JC_DATA_DIR 2>/dev/null || true)"
    fi
    if [[ "$session_data" == JC_DATA_DIR=* ]]; then
      actual="${session_data#JC_DATA_DIR=}"
    else
      actual="$(tmux display-message -p -t "$JC_SESSION:0.0" '#{pane_current_path}')"
    fi
    [[ "$(realpath "$actual")" == "$(realpath "$JC_DATA_DIR")" ]] || jc_die "Session $JC_SESSION belongs to $actual, not $JC_DATA_DIR; use the correct JC_DATA_DIR"
  fi
}
jc_log() { printf '[JialiangCraft] %s\n' "$*"; }
jc_die() { printf '[JialiangCraft] ERROR: %s\n' "$*" >&2; exit 1; }
