#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
for _ in {1..600}; do
  if [[ -f "$JC_DATA_DIR/logs/latest.log" ]] && grep -Eq 'Done \([0-9.]+s\)! For help' "$JC_DATA_DIR/logs/latest.log"; then
    jc_log 'Minecraft reached the successful startup marker'
    exit 0
  fi
  jc_running || jc_die "Server exited before startup; inspect $JC_DATA_DIR/logs/latest.log"
  sleep 2
done
jc_die 'Server did not start within 20 minutes'
