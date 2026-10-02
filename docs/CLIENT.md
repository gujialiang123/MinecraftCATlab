# Client

The client pack is built from `pack/` using Packwiz. `pack/servers.dat` gives Prism Launcher a preconfigured JialiangCraft entry. Client-only mods are marked in each Packwiz metadata file; server-only mods are excluded by the `.mrpack` environment metadata.

Install Prism Launcher, import `JialiangCraft-1.0.1.mrpack`, use Java 21, sign in with a legitimate Minecraft account, then join the preconfigured public server at `98.93.3.136:25565`. The Minecraft whitelist is disabled. Older 1.0.0 clients can use **Direct Connection** with that address; no mod versions changed in 1.0.1.

No shaders or hardware-specific graphics options are included. The pack contains no account tokens or private keys.

To rebuild: `./jialiangcraft build-client`. This refreshes Packwiz metadata and exports into `dist/`. The export checks loader version, file count, overrides, and client/server environment fields.
