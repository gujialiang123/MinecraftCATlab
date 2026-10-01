#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
if ! jc_running; then jc_log 'Already stopped'; exit 0; fi
tmux send-keys -t "$JC_SESSION" 'stop' Enter
for _ in {1..180}; do
  if ! jc_running; then jc_log 'Stopped cleanly'; exit 0; fi
  sleep 1
done
jc_die 'Server did not stop within 180 seconds; no force kill was attempted'
