# Troubleshooting

| Problem | Check |
|---|---|
| Incompatible client version | Launch vanilla Minecraft Java Edition 26.3 in a fresh instance. The old NeoForge 1.21.1 modpack is historical. |
| Account authentication fails | Sign in with a legitimate Microsoft/Minecraft account; the server keeps `online-mode=true`. |
| Server fails to start | Read `./jialiangcraft logs` and `/home/jgu7/work/jialiangcraft-vanilla-26.3-data/logs/latest.log`; preserve the world and crash reports. |
| Wrong Java version | The active server uses isolated `.tools/java25`; inspect the pinned Java runtime rather than changing the host default. |
| Cannot connect from the internet | Check VPS `jialiangcraft-minecraft.service`, AWS inbound TCP 25565, and the lab server log. |
| Cannot connect over Tailscale | Check Tailscale connectivity, the `100.112.93.136:25565` listener, and account authentication. |
| Restore rejected | Use a backup for the matching vanilla runtime. Restore old modded backups only with historical tooling and the old data directory after stopping vanilla. |
| Legacy Packwiz command rejected | The active server is vanilla. Use `deploy`, `update`, and `validate`; historical pack tooling must not modify the active installation. |
| Out of memory or resource pressure | Inspect process memory and host load. The JVM heap is limited to 4 GiB, but native memory adds overhead; four JVM-visible processors are not a CPU quota. |
| TPS lag | Measure loaded chunks, farms, and tick load before changing view/simulation distance or raising resource limits on the shared lab machine. |
| Voice chat unavailable | The active vanilla server does not include a voice chat mod. |

The old modded world is retained at `/home/jgu7/work/jialiangcraft-data`. Follow [server rollback instructions](SERVER.md) if intentionally returning to it; never copy that world into the vanilla directory.
