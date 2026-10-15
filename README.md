# JialiangCraft

**Minecraft Java Edition 26.3 · Official vanilla survival · Up to 4 players**

The current server configuration uses a fresh random world, hard difficulty, and the official Minecraft server. A bonus chest is generated near the initial world spawn. Players have no operator permissions, and command blocks are disabled. No mods, plugins, or extra datapacks are required.

## How to play

1. Select **Minecraft: Java Edition 26.3** in the official launcher, or create a fresh vanilla 26.3 instance in Prism Launcher.
2. Sign in with a legitimate Microsoft/Minecraft account and launch the game.
3. Open **Multiplayer → Add Server** and enter **`98.93.3.136:25565`**.

The whitelist is disabled and there is no server password. Tailscale members can also connect directly to `100.112.93.136:25565`.

The new world lives outside Git at `/home/jgu7/work/jialiangcraft-vanilla-26.3-data`. The old NeoForge 1.21.1 world remains separately at `/home/jgu7/work/jialiangcraft-data`; it is not imported into vanilla. The [v1.1.0 modpack release](https://github.com/gujialiang123/MinecraftCATlab/releases/tag/v1.1.0) is historical and is not the client for this server.

The server uses isolated Java 25, a 1 GiB initial / 4 GiB maximum heap, four JVM-visible processors, and lower scheduling priority to reduce its impact on the shared lab machine. These settings do not impose a hard total memory or CPU quota. Daily backups and reboot startup use the existing operations CLI.

See [client setup](docs/CLIENT.md), [server operations](docs/SERVER.md), [backups](docs/BACKUPS.md), [networking](docs/NETWORKING.md), and [validation results](docs/VALIDATION.md).
