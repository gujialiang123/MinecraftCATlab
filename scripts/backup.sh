#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
mkdir -p "$JC_DATA_DIR/backups/daily" "$JC_DATA_DIR/backups/weekly"
exec 9>"$JC_DATA_DIR/backups/.backup.lock"
flock -n 9 || jc_die 'Another backup or restore is already running'
WAS_RUNNING=0
if jc_running; then
  WAS_RUNNING=1
  "$JC_ROOT/scripts/stop.sh"
fi
restart_if_needed() {
  if [[ "$WAS_RUNNING" == 1 ]]; then
    "$JC_ROOT/scripts/start.sh" 9>&-
    "$JC_ROOT/scripts/wait-ready.sh"
  fi
}
trap restart_if_needed EXIT
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
FILE="$JC_DATA_DIR/backups/daily/jialiangcraft-$STAMP.tar.gz"
PATHS=()
for path in world server.properties whitelist.json ops.json banned-ips.json banned-players.json config defaultconfigs private-mods eula.txt; do
  [[ -e "$JC_DATA_DIR/$path" ]] && PATHS+=("$path")
done
[[ ${#PATHS[@]} -gt 0 ]] || jc_die 'No server state to back up'
tar -C "$JC_DATA_DIR" -czf "$FILE.tmp" "${PATHS[@]}"
tar -tzf "$FILE.tmp" >/dev/null
mv "$FILE.tmp" "$FILE"
if [[ "$(date -u +%u)" == 7 ]]; then
  cp "$FILE" "$JC_DATA_DIR/backups/weekly/$(basename "$FILE")"
fi
find "$JC_DATA_DIR/backups/daily" -maxdepth 1 -name 'jialiangcraft-*.tar.gz' -printf '%T@ %p\n' | sort -rn | tail -n +8 | cut -d' ' -f2- | while IFS= read -r old; do rm -f -- "$old"; done
find "$JC_DATA_DIR/backups/weekly" -maxdepth 1 -name 'jialiangcraft-*.tar.gz' -printf '%T@ %p\n' | sort -rn | tail -n +5 | cut -d' ' -f2- | while IFS= read -r old; do rm -f -- "$old"; done
jc_log "Verified backup: $FILE"
