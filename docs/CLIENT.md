# Client

The client pack is built from `pack/` using Packwiz. `pack/servers.dat` gives Prism Launcher a preconfigured JialiangCraft entry. Client-only mods are marked in each Packwiz metadata file; server-only mods are excluded by the `.mrpack` environment metadata. The GitHub release contains 26 pinned mod entries and does not include the two FTB mods used by the server.

## Install version 1.1.0

1. Import [JialiangCraft-1.1.0.mrpack](https://github.com/gujialiang123/MinecraftCATlab/releases/download/v1.1.0/JialiangCraft-1.1.0.mrpack) into Prism Launcher.
2. Download the exact **NeoForge 1.21.1** files [FTB Ultimine 2101.1.15](https://www.curseforge.com/minecraft/mc-mods/ftb-ultimine-forge/files/8231400) (`ftb-ultimine-neoforge-2101.1.15.jar`) and [FTB Library 2101.1.37](https://www.curseforge.com/minecraft/mc-mods/ftb-library-forge/files/9008089) (`ftb-library-neoforge-2101.1.37.jar`) from CurseForge. In Prism Launcher, open the imported instance's **Mods** tab and add both downloaded JARs. They are required on every player's client and are not supplied by the GitHub release.
3. Select Java 21, sign in with a legitimate Minecraft account, and launch the instance.
4. Join the preconfigured public server at `98.93.3.136:25565`. The Minecraft whitelist is disabled.

Clients on 1.0.0 or 1.0.1 need the new 1.1.0 base pack and both manual FTB mods before joining the updated server. Public connections use Minecraft TCP 25565; Simple Voice Chat's UDP port is not forwarded through the VPS.

No shaders or hardware-specific graphics options are included. The pack contains no account tokens or private keys.

To rebuild the GitHub base pack: `./jialiangcraft build-client`. This refreshes Packwiz metadata and exports into `dist/`. The export checks loader version, file count, overrides, and client/server environment fields. Building the base pack does not add the two FTB mods.
