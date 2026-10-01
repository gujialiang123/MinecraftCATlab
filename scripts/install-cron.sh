#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
TEMP="$(mktemp)"
trap 'rm -f "$TEMP"' EXIT
crontab -l 2>/dev/null | sed '/^# BEGIN JialiangCraft$/,/^# END JialiangCraft$/d' > "$TEMP" || true
cat >> "$TEMP" <<EOF
# BEGIN JialiangCraft
@reboot /bin/bash "$JC_ROOT/scripts/start.sh" >> "$JC_DATA_DIR/cron.log" 2>&1
0 5 * * * /bin/bash "$JC_ROOT/scripts/backup.sh" >> "$JC_DATA_DIR/cron.log" 2>&1
# END JialiangCraft
EOF
crontab "$TEMP"
jc_log 'Installed reboot startup and 05:00 daily backup in user crontab'
