#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
PACKWIZ="$(jc_packwiz)"
cd "$JC_ROOT/pack"
"$PACKWIZ" refresh >/dev/null
[[ "$(sed -n 's/^minecraft = "\([^"]*\)"/\1/p' pack.toml)" == 1.21.1 ]] || jc_die 'Wrong Minecraft version'
[[ "$(sed -n 's/^neoforge = "\([^"]*\)"/\1/p' pack.toml)" == 21.1.252 ]] || jc_die 'Wrong NeoForge version'
for mod in create modern-industrialization ae2 farmers-delight aether yungs-better-dungeons appleskin corpse natures-compass explorers-compass architectury-api; do
  [[ -f "mods/$mod.pw.toml" ]] || jc_die "Missing core mod: $mod"
done
for mod in create modern-industrialization ae2 farmers-delight aether yungs-better-dungeons appleskin corpse natures-compass explorers-compass architectury-api; do
  filename="$(sed -n 's/^filename = "\([^"]*\)"/\1/p' "mods/$mod.pw.toml")"
  [[ -f "$JC_DATA_DIR/mods/$filename" ]] || jc_die "Core server JAR missing: $filename"
done
for mod in ftb-ultimine ftb-library; do
  metadata="$JC_DATA_DIR/private-mods/$mod.pw.toml"
  [[ -f "$metadata" ]] || jc_die "Private server metadata missing: $mod"
  filename="$(sed -n 's/^filename = "\([^"]*\)"/\1/p' "$metadata")"
  [[ -f "$JC_DATA_DIR/mods/$filename" ]] || jc_die "Private server JAR missing: $filename"
done
VERSION="$(tr -d '\n' < "$JC_ROOT/VERSION")"
MRPACK="$JC_ROOT/dist/JialiangCraft-$VERSION.mrpack"
[[ -f "$MRPACK" ]] || jc_die 'Client pack was not built'
python3 "$JC_ROOT/scripts/inspect-mrpack.py" "$MRPACK"
jc_running || jc_die 'Minecraft server is not running'
[[ -f "$JC_DATA_DIR/logs/latest.log" ]] || jc_die 'Minecraft log missing'
grep -Eq 'Done \([0-9.]+s\)! For help' "$JC_DATA_DIR/logs/latest.log" || jc_die 'No successful startup marker in log'
! grep -Eiq 'ModLoadingException|Missing mandatory dependencies|Failed to load mod|Failed to start the minecraft server' "$JC_DATA_DIR/logs/latest.log" || jc_die 'Fatal mod or startup error found in log'
ss -ltn '( sport = :25565 )' | grep -Fq '100.112.93.136:25565' || jc_die 'Minecraft is not listening on Tailscale TCP 25565'
ss -lun '( sport = :24454 )' | grep -Eq '100[.]112[.]93[.]136[]]?:24454' || jc_die 'Voice chat is not listening on Tailscale UDP 24454'
grep -Fq 'scaled_add_xp_cost(distance, 0.02)' "$JC_DATA_DIR/config/waystones-common.toml" || jc_die 'Waystones cost config was not deployed'
jc_log 'Pack metadata, core mods, client export, startup log, and private ports validated'
