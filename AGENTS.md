# JialiangCraft agent rules

- The active server is official Minecraft Java Edition **26.3 vanilla survival**, authorized by the owner on 2026-10-15, with hard difficulty, a fresh random world, and a spawn bonus chest. Keep player cheats disabled (`allowCommands=false`, no operators, command blocks disabled). Do not add mods, plugins, third-party datapacks, or a server fork without explicit approval.
- Treat `server/vanilla.lock.json`, `server/java.lock.json`, and `server/server.properties` as the active runtime and configuration sources. Pin exact official server and Java downloads with hashes; do not silently track latest releases.
- Active data is `/home/jgu7/work/jialiangcraft-vanilla-26.3-data`. Preserve the old NeoForge installation at `/home/jgu7/work/jialiangcraft-data` and its verified pre-switch backup. Never open that old world with vanilla or upgrade it during deployment.
- Never commit secrets, `.env`, live worlds, player data, backups, downloaded JARs, or downloaded Java runtimes.
- Never delete or replace a live world automatically. Create and verify a backup before changing server binaries or configs. Reject restores from a different runtime or a legacy modded archive before changing live state.
- Keep the isolated Java 25 runtime under `.tools/java25`; do not change the host's default Java. Keep the configured 1 GiB initial / 4 GiB maximum heap, four JVM-visible processors, and nice level 10 unless measured load and the owner justify a change. These JVM settings are not a hard process memory or CPU quota.
- Keep `online-mode=true`, the owner's disabled whitelist, the Tailscale bind, and the existing public TCP relay unless asked to change them.
- Verify real server startup and Minecraft status through the public endpoint after runtime changes. Do not report deployment success from file existence alone. Record performed checks and remaining limits in `docs/VALIDATION.md`.
- `pack/` and GitHub release `v1.1.0` are historical NeoForge 1.21.1 material. Legacy Packwiz deploy/build tooling must not modify the active vanilla server or publish an old pack under a vanilla version. FTB private metadata and JARs must never be published.
- Explain migration and compatibility decisions in `CHANGELOG.md`. Repository version 2.0.0 does not itself authorize creating a new public GitHub Release.
