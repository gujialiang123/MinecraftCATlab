# Deployment configuration

The active server uses the official Minecraft Java Edition 26.3 JAR, isolated Java 25, and a detached `tmux` session. Runtime sources and hashes are pinned in `vanilla.lock.json` and `java.lock.json`; gameplay and networking are configured in `server.properties`. See [server operations](../docs/SERVER.md).

Active state belongs to `/home/jgu7/work/jialiangcraft-vanilla-26.3-data`. The old `/home/jgu7/work/jialiangcraft-data` installation is retained separately for deliberate rollback. Both use TCP 25565 and the `jialiangcraft` tmux name, so only one may run at a time.

Docker is not used by this deployment. The historical `v1.1.0` checkout contains the old, unvalidated NeoForge Docker Compose definition; it must not be used to manage the active vanilla world.
