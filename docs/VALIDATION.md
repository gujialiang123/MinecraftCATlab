# Deployment validation — 2026-10-01

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
