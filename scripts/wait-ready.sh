#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
SERVER_IP="$(sed -n 's/^server-ip=//p' "$JC_DATA_DIR/server.properties" | tail -1)"
SERVER_PORT="$(sed -n 's/^server-port=//p' "$JC_DATA_DIR/server.properties" | tail -1)"
EXPECTED_VERSION=''
if [[ -f "$JC_DATA_DIR/.runtime.json" ]]; then
  EXPECTED_VERSION="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["minecraft"])' "$JC_DATA_DIR/.runtime.json")"
fi
for _ in {1..600}; do
  jc_assert_session_data
  if [[ -n "$EXPECTED_VERSION" ]]; then
    if [[ -s "$JC_DATA_DIR/world/level.dat" ]] && python3 "$JC_ROOT/scripts/minecraft-status.py" "$SERVER_IP" "${SERVER_PORT:-25565}" --expect-version "$EXPECTED_VERSION" >/dev/null 2>&1; then
      jc_log "Minecraft $EXPECTED_VERSION has a saved world and answers game status requests"
      exit 0
    fi
  elif [[ -f "$JC_DATA_DIR/logs/latest.log" ]] && grep -Eq 'Done \([0-9.]+s\)! For help' "$JC_DATA_DIR/logs/latest.log"; then
      jc_log 'Legacy Minecraft reached the successful startup marker'
      exit 0
  fi
  jc_running || jc_die "Server exited before startup; inspect $JC_DATA_DIR/logs/latest.log"
  sleep 2
done
jc_die 'Server did not start within 20 minutes'
