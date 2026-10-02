# Troubleshooting

| Problem | Check |
|---|---|
| Mod version mismatch | Import the latest `.mrpack`; compare versions in `docs/MODLIST.md` and the server log. |
| Incompatible loader version | Use Minecraft 1.21.1 with NeoForge 21.1.252 exactly. |
| Failed dependency | Read `./jialiangcraft logs`; verify all server JARs against Packwiz metadata with `./jialiangcraft update`. |
| Client crash | Use Java 21, update Prism Launcher, and inspect its latest instance log. |
| Server crash loop | Check `/home/jgu7/work/jialiangcraft-data/logs/latest.log` and `crash-reports/`; do not delete the world. |
| Cannot connect from the internet | Check VPS `jialiangcraft-minecraft.service`, AWS inbound TCP 25565, and the lab server log. |
| Cannot connect over Tailscale | Check `tailscale status`, shared tailnet access, online authentication, and TCP 25565. |
| Voice chat fails | Voice chat is Tailscale-only. Check UDP 24454, Tailscale policy, in-game V menu, and `voicechat-server.properties`. |
| Out of memory | Check host RAM and Java's `-Xmx8G`; avoid increasing heap without evidence. |
| TPS lag | Inspect loaded chunks, farms, and server log; lower simulation distance only after measuring. |
