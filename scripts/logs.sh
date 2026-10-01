#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
[[ -f "$JC_DATA_DIR/logs/latest.log" ]] || jc_die 'No server log yet'
tail -n 150 -f "$JC_DATA_DIR/logs/latest.log"
