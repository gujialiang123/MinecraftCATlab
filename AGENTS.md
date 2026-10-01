# JialiangCraft agent rules

- Treat `pack/pack.toml`, `pack/index.toml`, and `pack/mods/*.pw.toml` as the sole mod and loader source of truth. Never maintain separate client and server mod lists.
- Never commit secrets, `.env`, live worlds, player data, backups, or downloaded mod JARs.
- Never delete or replace a live world automatically. Create a verified backup before changing server mods or configs.
- Do not add major gameplay mods without explicit user approval. Preserve Vanilla → Create → Modern Industrialization → AE2 progression.
- Do not upgrade Minecraft beyond 1.21.1 without explicit approval. Verify compatibility before changing the NeoForge version family.
- Pin exact mod versions and hashes. Do not bulk update to latest without review.
- Rebuild the client from Packwiz, validate metadata, and verify real server startup after server changes. Do not report deployment success from file existence alone.
- Explain compatibility workarounds in `CHANGELOG.md`.
