#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
if jc_running; then jc_assert_session_data; jc_log "tmux session: running ($JC_DATA_DIR)"; else jc_log 'tmux session: stopped'; fi
ss -ltn '( sport = :25565 )' | tail -n +2
