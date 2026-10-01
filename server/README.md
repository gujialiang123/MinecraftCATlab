# Deployment choices

The active installation uses Java 21 and `tmux`; see `../docs/SERVER.md`. The Compose file is a prepared alternative for an account with Docker daemon access. It uses the `itzg/minecraft-server:java21` image, host networking so `server-ip` can bind to the Tailscale interface, persistent `/data`, and `restart: unless-stopped`. Docker mode has not been tested on this host. Do not run it at the same time as the Java service because both need TCP 25565 and UDP 24454.
