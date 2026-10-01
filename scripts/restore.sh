#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
ARCHIVE="${1:-}"
[[ -n "$ARCHIVE" && -f "$ARCHIVE" ]] || jc_die 'Usage: ./jialiangcraft restore /absolute/path/to/backup.tar.gz'
ARCHIVE="$(realpath "$ARCHIVE")"
tar -tzf "$ARCHIVE" >/dev/null || jc_die 'Backup archive is corrupt'
"$JC_ROOT/scripts/backup.sh"
"$JC_ROOT/scripts/stop.sh"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
SAFETY="$JC_DATA_DIR/backups/pre-restore-$STAMP"
mkdir -p "$SAFETY"
for path in world server.properties whitelist.json ops.json banned-ips.json banned-players.json config defaultconfigs eula.txt; do
  [[ -e "$JC_DATA_DIR/$path" ]] && mv "$JC_DATA_DIR/$path" "$SAFETY/"
done
tar -C "$JC_DATA_DIR" -xzf "$ARCHIVE"
"$JC_ROOT/scripts/start.sh"
"$JC_ROOT/scripts/wait-ready.sh"
"$JC_ROOT/scripts/validate.sh"
jc_log "Restored $ARCHIVE; previous state preserved at $SAFETY"
