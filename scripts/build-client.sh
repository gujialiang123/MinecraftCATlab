#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
jc_die 'The active server is vanilla 26.3: use the standard Java 26.3 client. Historical modpack tooling is preserved at tag v1.1.0.'
PACKWIZ="$(jc_packwiz)"
VERSION="$(tr -d '\n' < "$JC_ROOT/VERSION")"
mkdir -p "$JC_ROOT/dist"
python3 "$JC_ROOT/scripts/make-servers-dat.py"
cd "$JC_ROOT/pack"
"$PACKWIZ" refresh
"$PACKWIZ" modrinth export -o "$JC_ROOT/dist/JialiangCraft-$VERSION.mrpack"
python3 "$JC_ROOT/scripts/inspect-mrpack.py" "$JC_ROOT/dist/JialiangCraft-$VERSION.mrpack"
