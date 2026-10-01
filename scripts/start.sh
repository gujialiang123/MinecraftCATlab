#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
[[ -f "$JC_DATA_DIR/run.sh" ]] || jc_die 'Server is not deployed. Run ./jialiangcraft deploy.'
if jc_running; then jc_log 'Already running'; exit 0; fi
if [[ -f "$JC_DATA_DIR/logs/latest.log" ]]; then
  mv "$JC_DATA_DIR/logs/latest.log" "$JC_DATA_DIR/logs/previous-$(date -u +%Y%m%dT%H%M%S%NZ).log"
fi
tmux new-session -d -s "$JC_SESSION" -c "$JC_DATA_DIR" "bash '$JC_ROOT/scripts/run-server.sh'" 9>&-
jc_log "Started tmux session $JC_SESSION"
