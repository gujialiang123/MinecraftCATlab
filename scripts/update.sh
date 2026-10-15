#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
python3 - "$JC_ROOT/server/vanilla.lock.json" "$JC_DATA_DIR/.runtime.json" <<'PY'
import json, sys
from pathlib import Path
expected, installed = map(Path, sys.argv[1:])
if not installed.is_file() or json.loads(installed.read_text()) != json.loads(expected.read_text()):
    raise SystemExit('Update refused: use a separate deployment for a legacy or different runtime')
PY
"$JC_ROOT/scripts/backup.sh"
"$JC_ROOT/scripts/stop.sh"
"$JC_ROOT/scripts/deploy.sh"
"$JC_ROOT/scripts/validate.sh"
