# Server operations

The live server is at `/home/jgu7/work/jialiangcraft-data`, outside Git. NeoForge 21.1.252 uses Java 21 with a 4 GiB initial and 8 GiB maximum heap. The Java server runs in a detached `tmux` session because this account currently cannot access the host Docker daemon. The Docker Compose definition is in `server/docker-compose.yml` for a future Docker-enabled deployment; it has not been used or validated.

From the repository root:

| Task | Command |
|---|---|
| Deploy from Packwiz metadata | `./jialiangcraft deploy` |
| Start / stop / restart | `./jialiangcraft start`, `./jialiangcraft stop`, `./jialiangcraft restart` |
| Status | `./jialiangcraft status` |
| Follow logs | `./jialiangcraft logs` |
| Update pack | `./jialiangcraft update` |
| Validate | `./jialiangcraft validate` |

`deploy` installs the pinned NeoForge loader if needed, copies committed configs, downloads only server-side mod JARs from the pinned Packwiz URLs, verifies SHA-512, and starts Minecraft. Never manually copy client-only JARs to the server. `update` builds the client, backs up the live state, stops the server, deploys, and validates startup. Review compatibility and bump `VERSION` before running it.

Waystones rules are in `pack/config/waystones-common.toml`: travel costs 0.02 XP points per block, bounded to 3–50 points, with 50 points for interdimensional travel. This is a common mod config, and the deployment copies it to the live `config/` directory.

`server.properties` binds TCP 25565 to the Tailscale IP. Online authentication remains enabled. The whitelist is disabled at the owner's request, so any authenticated player permitted by the Tailscale network policy may join. To re-enable a whitelist later, change `white-list` and `enforce-whitelist` to `true`, restart, then add player names with `tmux send-keys -t jialiangcraft 'whitelist add PLAYER_NAME' Enter`.

Packwiz is needed to build and validate the client. Use an installed `packwiz` or place the official Linux binary at `.tools/packwiz` (ignored by Git). For source builds, follow [Packwiz installation](https://packwiz.infra.link/installation/). Python 3.12, Java 21, `tmux`, `curl`, and `tar` are also used.
