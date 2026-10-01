# Private networking

This machine's Tailscale IPv4 address is `100.112.93.136`. Minecraft listens on TCP `100.112.93.136:25565`; Simple Voice Chat listens on UDP `100.112.93.136:24454`. The server binds to that interface instead of the public or LAN wildcard. No public port forwarding is configured.

The host and every player must join the same permitted Tailscale network. Confirm the address with `tailscale ip -4`; if it changes, update `server/server.properties`, `pack/config/voicechat/voicechat-server.properties`, rebuild the client pack, and redeploy. The preconfigured `servers.dat` is generated from `server/server.properties`.

Simple Voice Chat's [official server configuration](https://modrepo.de/minecraft/voicechat/wiki/server_config) documents UDP port 24454 and `bind_address`. If voice chat is disconnected, confirm the Tailscale network policy allows UDP 24454 between players and this host, and check the server log.
