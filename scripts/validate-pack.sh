#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
PACKWIZ="$(jc_packwiz)"
VERSION="$(tr -d '\n' < "$JC_ROOT/VERSION")"
ORIGINAL="$JC_ROOT/dist/JialiangCraft-$VERSION.mrpack"
[[ -f "$ORIGINAL" ]] || jc_die 'Build the client pack first'
TEMP="$(mktemp -d)"
trap 'rm -rf "$TEMP"' EXIT
cp -a "$JC_ROOT/pack" "$TEMP/pack"
(cd "$TEMP/pack" && "$PACKWIZ" refresh >/dev/null && "$PACKWIZ" modrinth export -o "$TEMP/rebuilt.mrpack" >/dev/null)
python3 - "$ORIGINAL" "$TEMP/rebuilt.mrpack" <<'PY'
import json, sys, zipfile
def manifest(path):
    with zipfile.ZipFile(path) as archive:
        return json.loads(archive.read('modrinth.index.json'))
assert manifest(sys.argv[1]) == manifest(sys.argv[2]), 'Clean rebuild manifest differs'
print('Clean temporary rebuild matches original .mrpack manifest')
PY
git -C "$JC_ROOT" diff --exit-code -- pack
