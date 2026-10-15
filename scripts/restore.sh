#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
ARCHIVE="${1:-}"
[[ -n "$ARCHIVE" && -f "$ARCHIVE" ]] || jc_die 'Usage: ./jialiangcraft restore /absolute/path/to/backup.tar.gz'
ARCHIVE="$(realpath "$ARCHIVE")"
RESTORE_TEMP="$(mktemp -d)"
trap 'rm -rf "$RESTORE_TEMP"' EXIT
SELECTED_ARCHIVE="$RESTORE_TEMP/selected.tar.gz"
cp -- "$ARCHIVE" "$SELECTED_ARCHIVE"
python3 "$JC_ROOT/scripts/check-backup.py" "$SELECTED_ARCHIVE" "$JC_DATA_DIR"
"$JC_ROOT/scripts/backup.sh"
exec 9>"$JC_DATA_DIR/backups/.backup.lock"
flock -n 9 || jc_die 'Another backup or restore is already running'
"$JC_ROOT/scripts/stop.sh"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
SAFETY="$JC_DATA_DIR/backups/pre-restore-$STAMP"
mkdir -p "$SAFETY"
for path in world server.properties whitelist.json ops.json banned-ips.json banned-players.json .runtime.json user_jvm_args.txt eula.txt; do
  [[ -e "$JC_DATA_DIR/$path" ]] && mv "$JC_DATA_DIR/$path" "$SAFETY/"
done
python3 - "$SELECTED_ARCHIVE" "$JC_DATA_DIR" <<'PY'
import sys, tarfile
with tarfile.open(sys.argv[1], 'r:gz') as archive:
    archive.extractall(sys.argv[2], filter='data')
PY
"$JC_ROOT/scripts/start.sh"
"$JC_ROOT/scripts/wait-ready.sh"
"$JC_ROOT/scripts/validate.sh"
jc_log "Restored $ARCHIVE; previous state preserved at $SAFETY"
