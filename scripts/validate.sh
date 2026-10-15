#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
jc_assert_session_data
python3 - "$JC_ROOT" "$JC_DATA_DIR" <<'PY'
import hashlib, json, sys
from pathlib import Path
root, data = map(Path, sys.argv[1:])
sys.path.insert(0, str(root / 'scripts'))
from nbt import read_gzip
lock = json.loads((root / 'server/vanilla.lock.json').read_text())
assert json.loads((data / '.runtime.json').read_text()) == lock, 'Runtime metadata mismatch'
jar = data / 'server.jar'
assert jar.stat().st_size == lock['server_size'], 'Server JAR size mismatch'
assert hashlib.sha1(jar.read_bytes()).hexdigest() == lock['server_sha1'], 'Server JAR checksum mismatch'
assert not (data / 'mods').exists(), 'Unexpected mod directory'
assert not (data / 'plugins').exists(), 'Unexpected plugin directory'
assert (data / 'world/level.dat').stat().st_size > 0, 'No saved world'
assert not list((data / 'world/datapacks').glob('*')), 'Unexpected custom datapacks'
props = dict(line.split('=', 1) for line in (data / 'server.properties').read_text().splitlines() if '=' in line and not line.startswith('#'))
source_props = dict(line.split('=', 1) for line in (root / 'server/server.properties').read_text().splitlines() if '=' in line and not line.startswith('#'))
difficulty = source_props['difficulty']
for key, value in {'gamemode':'survival', 'difficulty':difficulty, 'hardcore':'false', 'online-mode':'true', 'white-list':'false', 'server-ip':'100.112.93.136', 'server-port':'25565', 'level-name':'world', 'enable-command-block':'false', 'enable-rcon':'false', 'management-server-enabled':'false'}.items():
    assert props.get(key) == value, f'Unexpected {key}: {props.get(key)}'
operators = json.loads((data / 'ops.json').read_text())
assert isinstance(operators, list), 'Invalid private operator list'
world = read_gzip(data / 'world/level.dat')['Data']
assert world['GameType'] == 0 and world['allowCommands'] == 0, 'World must default to survival without global command permissions'
assert world['difficulty_settings']['difficulty'] == difficulty, 'Saved difficulty does not match the configured difficulty'
assert world['difficulty_settings']['hardcore'] == 0, 'Hardcore must be disabled'
assert world['WasModded'] == 0 and world['DataPacks']['Enabled'] == ['vanilla'], 'Unexpected modded world or enabled datapack'
generation = read_gzip(data / 'world/data/minecraft/world_gen_settings.dat')['data']
assert generation['bonus_chest'] == 1, 'Spawn bonus chest was not enabled during world generation'
print(f'Verified official vanilla {lock["minecraft"]}, {difficulty} survival, bonus chest, and {len(operators)} privately managed operator(s)')
PY
jc_running || jc_die 'Minecraft server is not running'
[[ -f "$JC_DATA_DIR/logs/latest.log" ]] || jc_die 'Minecraft log missing'
! grep -Eiq 'Failed to start the minecraft server|Exception in server tick loop|FAILED TO BIND TO PORT' "$JC_DATA_DIR/logs/latest.log" || jc_die 'Fatal startup error found in log'
EXPECTED_VERSION="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["minecraft"])' "$JC_ROOT/server/vanilla.lock.json")"
python3 "$JC_ROOT/scripts/minecraft-status.py" 100.112.93.136 25565 --expect-version "$EXPECTED_VERSION"
ss -ltn '( sport = :25565 )' | grep -Eq '100[.]112[.]93[.]136[]]?:25565' || jc_die 'Minecraft is not listening on Tailscale TCP 25565'
jc_log 'Vanilla artifact, world, survival settings, game protocol, and TCP listener validated'
