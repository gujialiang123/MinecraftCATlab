#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
jc_running && jc_die 'Stop the server before deploying; use ./jialiangcraft update for an existing server'
mkdir -p "$JC_DATA_DIR/config" "$JC_DATA_DIR/defaultconfigs" "$JC_DATA_DIR/backups/daily" "$JC_DATA_DIR/backups/weekly"
if [[ ! -f "$JC_DATA_DIR/run.sh" ]]; then
  NEOFORGE="$(sed -n 's/^neoforge = "\([^"]*\)"/\1/p' "$JC_ROOT/pack/pack.toml")"
  [[ -n "$NEOFORGE" ]] || jc_die 'NeoForge version missing from Packwiz metadata'
  URL="https://maven.neoforged.net/releases/net/neoforged/neoforge/$NEOFORGE/neoforge-$NEOFORGE-installer.jar"
  jc_log "Installing NeoForge $NEOFORGE from official Maven"
  curl -fL --retry 3 "$URL" -o "$JC_DATA_DIR/neoforge-installer.jar"
  (cd "$JC_DATA_DIR" && java -jar neoforge-installer.jar --installServer >installer.log 2>&1)
fi
cp "$JC_ROOT/server/server.properties" "$JC_DATA_DIR/server.properties"
cp -a "$JC_ROOT/pack/config/." "$JC_DATA_DIR/config/"
cp -a "$JC_ROOT/pack/defaultconfigs/." "$JC_DATA_DIR/defaultconfigs/"
if [[ -d "$JC_DATA_DIR/world/serverconfig" ]]; then
  cp -a "$JC_ROOT/pack/defaultconfigs/." "$JC_DATA_DIR/world/serverconfig/"
fi
printf 'eula=true\n' > "$JC_DATA_DIR/eula.txt"
printf '%s\n' '-Xms4G' '-Xmx8G' > "$JC_DATA_DIR/user_jvm_args.txt"
python3 "$JC_ROOT/scripts/sync-server-mods.py"
"$JC_ROOT/scripts/start.sh"
jc_log 'Waiting for Minecraft startup...'
"$JC_ROOT/scripts/wait-ready.sh"
