# Backups

`./jialiangcraft backup` stops the server cleanly, archives the world and server state (including private FTB mod metadata, but not downloaded JARs), verifies the gzip archive, and restarts the server. Backups live outside Git under `/home/jgu7/work/jialiangcraft-data/backups`. Only one backup runs at a time via a file lock.

The daily job runs at 05:00 local system time. Keep the newest **7 daily** and **4 weekly** archives; Sundays also copy the daily archive into the weekly set. Backup time may briefly disconnect players. Run a manual backup before every server-affecting update.

To restore, use `./jialiangcraft restore /absolute/path/to/backup.tar.gz`. Restore first creates a fresh safety backup, stops the server, moves the current state to a timestamped `pre-restore-*` folder, extracts the selected archive, restarts, and validates startup. Review the archive and coordinate with players before restoring a live world.
