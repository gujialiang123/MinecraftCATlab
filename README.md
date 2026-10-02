# JialiangCraft

**Minecraft 1.21.1 · NeoForge 21.1.252 · 2–4 players**

A small survival pack that grows from **Vanilla → Create → Modern Industrialization → Applied Energistics 2**. Farmer's Delight, The Aether, and improved dungeons add food and exploration without replacing the main progression.

Waystones cost experience (3–50 points based on distance; interdimensional travel costs 50 points), so Create trains and other physical travel remain useful.

## How to play

1. Install [Prism Launcher](https://prismlauncher.org/).
2. Download [JialiangCraft-1.1.0.mrpack](https://github.com/gujialiang123/MinecraftCATlab/releases/download/v1.1.0/JialiangCraft-1.1.0.mrpack) from GitHub Releases.
3. In Prism Launcher, select **Add Instance → Import** and choose the `.mrpack`.
4. Download [FTB Ultimine 2101.1.15](https://www.curseforge.com/minecraft/mc-mods/ftb-ultimine-forge/files/8231400) and [FTB Library 2101.1.37](https://www.curseforge.com/minecraft/mc-mods/ftb-library-forge/files/9008089) from their official CurseForge pages. Add both **NeoForge 1.21.1** JARs to the imported instance's **Mods** tab before launching. These two required mods are not included in the GitHub `.mrpack`.
5. Use Java 21, sign in with a legitimate Microsoft/Minecraft account, then click **Launch**.
6. Open **Multiplayer → JialiangCraft**. The server is preconfigured as `98.93.3.136:25565`.

Version 1.1.0 adds Corpse, AppleSkin, Nature's Compass, and Explorer's Compass to the base pack; Architectury API is included as a dependency. The server also runs the two FTB mods, so both manual client downloads are required to join. There is no server password or whitelist. Players with permitted Tailscale access can also connect directly to `100.112.93.136:25565`. Simple Voice Chat remains on the private Tailscale network; its UDP port is not forwarded publicly.

For details: [client](docs/CLIENT.md), [mod list](docs/MODLIST.md), [networking](docs/NETWORKING.md), [troubleshooting](docs/TROUBLESHOOTING.md).
