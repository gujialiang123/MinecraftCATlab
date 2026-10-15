# Server operations

The active configuration is official **Minecraft Java Edition 26.3 vanilla survival**, with a fresh random world at `/home/jgu7/work/jialiangcraft-vanilla-26.3-data`, outside Git. Exact server and Java downloads are pinned in `server/vanilla.lock.json` and `server/java.lock.json`. The server JAR is checked against its official SHA-1 before use.

Java 25 is isolated under `.tools/java25`; the host's default Java remains available for other users and the archived server. The detached `tmux` session is still named `jialiangcraft`. Startup uses `-Xms1G -Xmx4G -XX:ActiveProcessorCount=4` with nice level 10. The heap limit excludes native JVM memory; the processor setting controls JVM sizing and is not a hard CPU quota. Docker is not the active runtime.

From the repository root:

| Task | Command |
|---|---|
| Deploy the pinned official vanilla runtime | `./jialiangcraft deploy` |
| Start / stop / restart | `./jialiangcraft start`, `./jialiangcraft stop`, `./jialiangcraft restart` |
| Status | `./jialiangcraft status` |
| Follow logs | `./jialiangcraft logs` |
| Back up before applying the pinned runtime/configuration | `./jialiangcraft update` |
| Create a verified state backup | `./jialiangcraft backup` |
| Restore a compatible vanilla backup | `./jialiangcraft restore /absolute/path/to/backup.tar.gz` |
| Validate the active deployment | `./jialiangcraft validate` |

`deploy` uses the pinned official server, Java runtime, and committed server properties. It must not copy Packwiz configs, install NeoForge, or synchronize legacy mods. `update` applies the reviewed pinned configuration after a verified backup; it is not a request to download whatever version is latest. Legacy modpack tooling is disabled for the active vanilla setup.

The world uses survival, normal difficulty, and a four-player maximum. `server/server.properties` keeps `online-mode=true`, `white-list=false`, and `enforce-whitelist=false`. It binds TCP 25565 to `100.112.93.136`; the existing VPS relay exposes `98.93.3.136:25565`. See [networking](NETWORKING.md).

Reboot startup and a daily 05:00 backup are managed by `scripts/install-cron.sh`. Keep the host scheduling timezone at America/New_York and reinstall the managed cron block after changing the active data directory. See [backups](BACKUPS.md) and [performed validation](VALIDATION.md).

## Archived modded server and rollback

The old NeoForge 1.21.1 installation remains at `/home/jgu7/work/jialiangcraft-data`. Preserve its complete world, private FTB metadata, runtime files, and verified pre-switch backup. The fresh vanilla world is independent; never point vanilla at the old world or extract a modded backup over it.

A deliberate rollback uses the historical `v1.1.0` code and the old directory. First stop vanilla with the current checkout's `./jialiangcraft stop`. Then create a separate historical checkout, for example `git worktree add ../MinecraftCATlab-legacy v1.1.0`, and use `JC_DATA_DIR=/home/jgu7/work/jialiangcraft-data ../MinecraftCATlab-legacy/jialiangcraft start`. The archived server requires Java 21 and its matching NeoForge client pack. Confirm the active server before changing the reboot/backup jobs to the legacy checkout.

Both servers share the same tmux name and TCP port, so only one may run at a time. To return to vanilla, stop the legacy server using the historical checkout and explicit old `JC_DATA_DIR`, then start from the current checkout and reinstall its cron block. These are rollback instructions, not an automatic migration or restore.
