#!/usr/bin/env bash
set -euo pipefail
JC_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JC_DATA_DIR="${JC_DATA_DIR:-$(dirname "$JC_ROOT")/jialiangcraft-data}"
JC_SESSION=jialiangcraft
export JC_ROOT JC_DATA_DIR JC_SESSION

jc_packwiz() {
  if [[ -x "$JC_ROOT/.tools/packwiz" ]]; then printf '%s\n' "$JC_ROOT/.tools/packwiz";
  elif command -v packwiz >/dev/null 2>&1; then command -v packwiz;
  else echo 'Packwiz is missing. See docs/SERVER.md.' >&2; return 1; fi
}

jc_running() { tmux has-session -t "$JC_SESSION" 2>/dev/null; }
jc_log() { printf '[JialiangCraft] %s\n' "$*"; }
jc_die() { printf '[JialiangCraft] ERROR: %s\n' "$*" >&2; exit 1; }
