#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
if jc_running; then jc_log 'tmux session: running'; else jc_log 'tmux session: stopped'; fi
ss -ltn '( sport = :25565 )' | tail -n +2
ss -lun '( sport = :24454 )' | tail -n +2
