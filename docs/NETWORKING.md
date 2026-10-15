# Networking

Players connect to `98.93.3.136:25565` over TCP with a vanilla Java Edition 26.3 client. The address is recorded in `server/public-address.txt`. The lab server binds only to its Tailscale address `100.112.93.136:25565`; VPS service `jialiangcraft-minecraft.service` forwards public TCP 25565 there over Tailscale. Its unit file is in `ops/vps/`. The VPS Tailscale address is `100.74.16.107`.

The VPS AWS security group must allow inbound TCP 25565. Check the relay with `sudo systemctl status jialiangcraft-minecraft` on the VPS. After deliberately changing its unit file, copy it to `/etc/systemd/system/`, reload systemd, and restart the relay. Switching the game server to vanilla keeps the same TCP endpoint and does not require changing the existing SSH relay `portmap-4090-2222.service`.

Minecraft keeps `online-mode=true`. The whitelist is disabled at the owner's request, so any player with a legitimate Minecraft account and the matching Java Edition version can join through the public address. Tailscale members may also use `100.112.93.136:25565` directly. No server password is configured.

The active vanilla server has no Simple Voice Chat mod and does not require UDP 24454 or any additional public port. See [validation results](VALIDATION.md) for the latest tested public status response.
