# Changelog

## 2.0.0 — 2026-10-15

- Configure official Minecraft Java Edition 26.3 vanilla survival with a fresh random world, normal difficulty, and up to four players.
- Separate new state into `jialiangcraft-vanilla-26.3-data`; preserve the old NeoForge world and pre-switch backup at `jialiangcraft-data` without converting that world.
- Pin the official server and an isolated Java 25 runtime. Configure a 1 GiB initial / 4 GiB maximum heap, four JVM-visible processors, and nice level 10 to reduce impact on the shared lab machine.
- Keep the existing public TCP address, online account authentication, disabled whitelist, reboot startup, and daily backups. Require compatible vanilla runtime metadata for restore.
- Retain `pack/` and public release `v1.1.0` as historical modpack material; disable legacy modpack operations for the active vanilla deployment. This repository version does not announce a new public release.

## 1.1.0 — 2026-10-02

- Added AppleSkin, Corpse, Nature's Compass, and Explorer's Compass for food information, death recovery, and finding biomes and structures. Added Architectury API as a dependency.
- Added FTB Ultimine and FTB Library to the server. Players must install the exact matching NeoForge 1.21.1 JARs from official CurseForge pages; these two mods are not included in the GitHub `.mrpack`.

## 1.0.1 — 2026-10-02

- Added a public VPS relay for Minecraft TCP 25565 while keeping the lab server bound to Tailscale.
- Updated the preconfigured client server address; mod and loader versions are unchanged.
- Kept Microsoft/Minecraft account verification on and left the whitelist disabled at the owner's request.

## 1.0.0 — 2026-10-01

- Initial Minecraft 1.21.1 / NeoForge 21.1.252 pack.
- Create → Modern Industrialization → Applied Energistics 2 progression.
- Exploration, food, building, navigation, voice chat, and lightweight performance mods.
- Pinned Packwiz metadata, client export, private Tailscale server setup, and rotating backups.
