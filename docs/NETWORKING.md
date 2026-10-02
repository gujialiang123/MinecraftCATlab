# Networking

Players connect to `98.93.3.136:25565` over TCP. The client pack's preconfigured server entry comes from `server/public-address.txt`. The lab host still binds Minecraft only to its Tailscale address `100.112.93.136:25565`; the VPS service `jialiangcraft-minecraft.service` forwards public TCP 25565 to that address over Tailscale. Its unit file is in `ops/vps/`. The VPS itself has Tailscale address `100.74.16.107`. The existing `portmap-4090-2222.service` for SSH is separate and unchanged.

The VPS AWS security group must allow inbound TCP 25565. Check the relay with `sudo systemctl status jialiangcraft-minecraft` on the VPS. After changing its unit file in this repository, copy it to `/etc/systemd/system/` on the VPS, reload systemd, and restart the service.

Minecraft keeps `online-mode=true`. The whitelist is disabled at the owner's request, so any player with a legitimate Minecraft account and a compatible modpack can join through the public address. Tailscale members may still use `100.112.93.136:25565` directly.

Simple Voice Chat remains bound to `100.112.93.136:24454` over UDP and is not forwarded publicly. Its [server configuration](https://modrepo.de/minecraft/voicechat/wiki/server_config) documents `port`, `bind_address`, and `voice_host`. Public players can join the game without voice chat.
