# Hard survival and bonus-chest refresh — 2026-10-15

- At the owner's request, backed up the unused vanilla world before refreshing it. Kept the verified `pre-hard-bonus-20261015T052640Z.tar.gz` backup and the prior world at `jialiangcraft-vanilla-26.3-data/archives/world-before-hard-bonus-20261015T052640Z`. The historical NeoForge directory was not changed.
- Regenerated the vanilla world using `difficulty=hard` and the official `--bonusChest` startup option. Read the actual saved NBT: `difficulty_settings.difficulty=hard`, `hardcore=0`, `GameType=0`, `allowCommands=0`, and `bonus_chest=1` in `data/minecraft/world_gen_settings.dat`.
- Inspected saved overworld region data and found the actual unopened bonus chest at `(-57, 63, 54)`, with the `minecraft:chests/spawn_bonus_chest` loot table. The global spawn is nearby at `(-64, 64, 48)`.
- Verified an empty operator list, disabled command blocks, RCON, and management API, and only the vanilla datapack enabled. The validation command now checks the saved hard/no-cheat/bonus-chest settings as well as server properties.
- Saved and verified the refreshed world's initial backup `jialiangcraft-20261015T052924Z.tar.gz`; its automatic restart retained the hard/no-cheat/bonus-chest settings, and the backup compatibility check passed.
- Local and public Minecraft status requests returned the running vanilla 26.3 server. Actual player login and gameplay remain untested.

# Vanilla 26.3 fresh-world migration — 2026-10-15

- The owner requested an official vanilla 26.3 survival server and a new world. Mojang's release metadata confirms version 26.3 requires Java 25. The official server JAR's size and SHA-1 match `server/vanilla.lock.json`; the isolated Temurin 25 archive was checked against the SHA-256 in `server/java.lock.json`. Host Java remains 21.
- Before the change, the old NeoForge world was cleanly stopped, archived, verified, and restarted. A permanent migration backup is retained at `/home/jgu7/work/jialiangcraft-data/backups/pre-vanilla-26.3-20261015T051233Z.tar.gz`. The complete old installation and world remain in that old data directory.
- Vanilla uses the separate `/home/jgu7/work/jialiangcraft-vanilla-26.3-data` directory. Its first startup log reported `No existing world data, creating new world` and `Default game type: SURVIVAL`. No old world, mod JARs, plugins, or custom datapacks were imported.
- Fixed an inherited tmux environment that initially restarted the legacy runtime: the launcher now explicitly sets the session's data directory. After the correction and a backup/restart cycle, the actual Java process runs the official `server.jar` from the new vanilla directory.
- `./jialiangcraft validate` passed artifact, runtime marker, saved-world, survival/normal-difficulty settings, account authentication, disabled whitelist, and listener checks. Java's IPv4-mapped IPv6 listener is handled correctly.
- Game status requests through both Tailscale and public `98.93.3.136:25565` returned version 26.3 (protocol 777), the vanilla MOTD, and a four-player maximum. The former voice UDP listener is absent.
- The first vanilla backup, `jialiangcraft-20261015T051906Z.tar.gz`, was verified and followed by a successful vanilla restart. The backup compatibility checker accepts it and refuses the old modded archive before live-state changes. Twelve safety tests cover incompatible backups, unsafe archive entries, refusal to install over existing modded/unmarked worlds, and restoring from a stable copy when backup retention deletes the selected original archive.
- Reinstalled the managed user cron block for the new directory: reboot startup and daily 05:00 America/New_York backups. No reboot or live-world restore was performed.
- Runtime uses a 1 GiB initial / 4 GiB maximum heap, four JVM-visible processors, and nice level 10. With zero players, a five-second sample measured approximately 0.98 GiB resident memory and 0.01 CPU cores. These are idle measurements, and JVM settings are not a hard total resource quota.
- Actual player login and gameplay remain untested. Players should use a vanilla Java Edition 26.3 client.

# 1.1.0 mod update validation — 2026-10-02

- Created and verified a fresh backup before changing server mods: `jialiangcraft-20261002T051931Z.tar.gz`. It contains the world and private FTB metadata.
- Built `JialiangCraft-1.1.0.mrpack` from Packwiz with 26 pinned mod references, including AppleSkin, Corpse, both compasses, and Architectury API. The archive contains neither FTB JARs nor FTB metadata; client installation of FTB Ultimine and FTB Library is manual.
- Installed 24 server-side mods with SHA-512 checks, including both private FTB mods. The live NeoForge log lists all five requested mods and reports a successful `Done (...)!` startup.
- `./jialiangcraft validate` passed for client metadata, required server JARs, startup log, and the Tailscale listeners.
- A Minecraft status request through the VPS public address `98.93.3.136:25565` returned version 1.21.1, the expected MOTD, and a four-player maximum. It reported zero connected players at the time of the check.
- GitHub Actions completed both the client-pack build and v1.1.0 release successfully. The public `.mrpack` was downloaded and inspected; its manifest and archive entries match the locally validated build.
- With zero players online, the Java process used about 3.20 GiB resident memory and effectively no CPU over a five-second sample. Gameplay load was not measured.
- A full client login and in-game use of the five mods remain untested; the client must first add both FTB JARs manually.

# Public relay validation — 2026-10-02

- The VPS `jialiangcraft-minecraft.service` is enabled and active, listening on public IPv4 TCP 25565. Its unit has a 128 MiB memory cap and allows at most 16 relay children. The existing SSH mapping service was left unchanged.
- A TCP connection from the lab host to `98.93.3.136:25565` succeeded after AWS inbound TCP 25565 was opened.
- A Minecraft status request through that public address returned protocol 1.21.1, the expected `JialiangCraft - Create / MI / AE2` MOTD, and the server's four-player limit.
- The server still binds to Tailscale, keeps `online-mode=true`, and has the whitelist disabled at the owner's request. UDP voice chat is not publicly forwarded.
- `JialiangCraft-1.0.1.mrpack` built with the public server entry and 21 pinned files. `./jialiangcraft validate` passed for the client pack, mod metadata, startup log, and private listeners.
- A real player login from an external device has not been tested; the public network check reached the game's status protocol.

# Original deployment validation — 2026-10-01

## Machine and runtime

- OS: Ubuntu 24.04.4 LTS, x86_64.
- CPU: AMD Ryzen Threadripper PRO 5975WX, 32 cores / 64 threads.
- RAM: 503 GiB total, approximately 488 GiB available at initial inspection.
- Disk: 3.5 TiB filesystem, 147 GiB available at initial inspection (96% used).
- Java: OpenJDK 21.0.12.1. JVM heap: 4 GiB initial, 8 GiB maximum.
- Active runtime: Java 21 in a detached `tmux` session. Docker Compose is prepared but untested because this account cannot access the Docker socket; Docker container status is **not running**.

## Verified

- Official NeoForge 21.1.252 installer completed successfully.
- Packwiz contains Minecraft 1.21.1, NeoForge 21.1.252, 21 pinned mods (16 requested mods and 5 dependencies) with SHA-512 download hashes and side metadata.
- All 17 server-side mod JARs downloaded from pinned Modrinth URLs and matched SHA-512.
- Server log reached `Done (...)! For help` with no fatal dependency or mod load errors. Create, Waystones, and voice chat initialization were observed.
- TCP `100.112.93.136:25565` and UDP `100.112.93.136:24454` listened on the Tailscale interface.
- `online-mode=true`; whitelist disabled at owner's request; no public port forwarding configured.
- Waystones live config has a 3–50 XP point bounded travel cost and 50 points for cross-dimension travel.
- `JialiangCraft-1.0.0.mrpack` exported successfully and contains correct game/loader versions, client/server mod environment metadata, client server list, and configs.
- A clean temporary Packwiz directory rebuilt the same `.mrpack` manifest.
- GitHub Release v1.0.0 was published by GitHub Actions. The public asset was downloaded, inspected, and its Modrinth manifest matched the local build.
- Safe backup created and gzip archive verified under `jialiangcraft-data/backups/daily/`; server restarted and validated afterward.
- User crontab contains `@reboot` startup and 05:00 America/New_York daily backup. No reboot or live-world restore test was performed.

## Limits

- Docker container launch and automatic Docker restart could not be tested without Docker group access. The active `tmux` service and user cron provide current operation and reboot startup.
- Remote gameplay from a second Tailscale device and voice audio have not been tested with a real player.
