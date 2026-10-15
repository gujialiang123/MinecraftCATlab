# Backups

`./jialiangcraft backup` stops the active server cleanly, archives the world and server state with runtime identification, verifies the archive, and restarts the server if it was running. Active backups live outside Git under `/home/jgu7/work/jialiangcraft-vanilla-26.3-data/backups`. Downloaded server JARs and Java runtimes are recreated from pinned metadata rather than included as world state. A file lock prevents overlapping backup and restore operations.

The daily job runs at **05:00 America/New_York**. Keep the newest **7 daily** and **4 weekly** archives; Sundays also copy the daily archive into the weekly set. Backup time may briefly disconnect players. Run a manual backup before every server-affecting update.

To restore, use `./jialiangcraft restore /absolute/path/to/backup.tar.gz`. The archive must identify a compatible vanilla runtime. Legacy modded archives and backups for a different runtime are rejected before changing the running server or live state. A valid restore first creates a fresh safety backup, preserves the current state in a timestamped `pre-restore-*` folder, then extracts, starts, and validates the restored server.

The old NeoForge world and its verified pre-switch backup belong to `/home/jgu7/work/jialiangcraft-data`. Keep them separate from vanilla backups. An old modded archive must only be restored with the historical server tooling and old data directory after stopping vanilla; see [rollback instructions](SERVER.md). Do not upgrade the old world or use it to seed the new vanilla world.

Installing the current managed cron block with `scripts/install-cron.sh` must point both reboot startup and backup logging to the vanilla installation. Check [validation results](VALIDATION.md) for the checks actually performed; a successful archive verification does not establish that a live restore has been tested.
