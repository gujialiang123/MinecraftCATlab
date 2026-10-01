# Client

The client pack is built from `pack/` using Packwiz. `pack/servers.dat` gives Prism Launcher a preconfigured JialiangCraft entry. Client-only mods are marked in each Packwiz metadata file; server-only mods are excluded by the `.mrpack` environment metadata.

Install Prism Launcher, import `JialiangCraft-1.0.0.mrpack`, use Java 21, sign in with a legitimate Minecraft account, then join the preconfigured server. Both you and the host must be connected through Tailscale and permitted by the Tailscale network policy. The Minecraft whitelist is disabled.

No shaders or hardware-specific graphics options are included. The pack contains no account tokens or private keys.

To rebuild: `./jialiangcraft build-client`. This refreshes Packwiz metadata and exports into `dist/`. The export checks loader version, file count, overrides, and client/server environment fields.
