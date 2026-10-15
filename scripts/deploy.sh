#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
jc_running && jc_die 'Stop the server before deploying; use ./jialiangcraft update for an existing server'
python3 "$JC_ROOT/scripts/install-vanilla.py"
mkdir -p "$JC_DATA_DIR/backups/daily" "$JC_DATA_DIR/backups/weekly"
"$JC_ROOT/scripts/start.sh"
jc_log 'Waiting for Minecraft startup...'
"$JC_ROOT/scripts/wait-ready.sh"
