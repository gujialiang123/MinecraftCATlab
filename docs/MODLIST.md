# Mod list

The GitHub base pack uses `pack/mods/*.pw.toml` as its source of truth. Its 26 files use exact versions and SHA-512 hashes. FTB Ultimine and FTB Library are required separately on the server and on every player's client; they are not in the GitHub `.mrpack`.

| Mod | Exact version | Side | Purpose | Source |
|---|---|---|---|---|
| Applied Energistics 2 | `19.2.18` | both | Mid/late-game digital storage and automation | [Modrinth](https://modrinth.com/mod/ae2/version/KDnFUmMm) |
| Architectury API | `13.0.11` | both | Dependency for new mods | [Modrinth](https://modrinth.com/mod/architectury-api/version/1IiqEQGl) |
| AppleSkin | `3.0.9+mc1.21` | both | Show hunger and saturation restored by food | [Modrinth](https://modrinth.com/mod/appleskin/version/uAKA6Laj) |
| Balm | `21.0.66+neoforge-1.21.1` | both | Waystones dependency | [Modrinth](https://modrinth.com/mod/balm/version/CquiaiDj) |
| Create | `6.0.10+mc1.21.1` | both | Mechanical automation | [Modrinth](https://modrinth.com/mod/create/version/UjX6dr61) |
| Corpse | `1.21.1-1.1.13` | both | Preserve a recoverable body after death | [Modrinth](https://modrinth.com/mod/corpse/version/Zwf8nv8y) |
| Explorer's Compass | `1.21.1-3.4.0-neoforge` | both | Locate structures | [Modrinth](https://modrinth.com/mod/explorers-compass/version/hIJ2Ev1Q) |
| Farmer's Delight | `1.21.1-1.3.4` | both | Food and cooking | [Modrinth](https://modrinth.com/mod/farmers-delight/version/XTVZDOol) |
| FerriteCore | `7.0.3-neoforge` | both | Reduce memory use | [Modrinth](https://modrinth.com/mod/ferrite-core/version/x7kQWVju) |
| GuideME | `21.1.19` | both | AE2 in-game guide dependency | [Modrinth](https://modrinth.com/mod/guideme/version/hFpGwC6q) |
| Jade 🔍 | `15.10.6+neoforge` | both | Block and entity information | [Modrinth](https://modrinth.com/mod/jade/version/eYz2YBGT) |
| Just Enough Items (JEI) | `19.51.0.418` | client | Recipe lookup | [Modrinth](https://modrinth.com/mod/jei/version/ufHUqt9b) |
| Modern Industrialization | `2.5.8` | both | Primary electrical industry | [Modrinth](https://modrinth.com/mod/modern-industrialization/version/s5PDXbfR) |
| ModernFix | `5.27.24+mc1.21.1` | both | Startup and memory optimizations | [Modrinth](https://modrinth.com/mod/modernfix/version/5HLHxQ2F) |
| Mouse Tweaks | `1.21-2.26.1-neoforge` | client | Inventory interaction | [Modrinth](https://modrinth.com/mod/mouse-tweaks/version/9I21YYxf) |
| Nature's Compass | `1.21.1-3.4.0-neoforge` | both | Locate biomes | [Modrinth](https://modrinth.com/mod/natures-compass/version/nFniEtJV) |
| oωo (owo-lib) | `0.12.15.5-beta.1+1.21` | both | Aether dependency | [Modrinth](https://modrinth.com/mod/owo-lib/version/NMCHU6DZ) |
| Simple Voice Chat | `neoforge-1.21.1-2.6.22` | both | Proximity voice chat | [Modrinth](https://modrinth.com/mod/simple-voice-chat/version/2s7zUspF) |
| Sophisticated Backpacks | `1.21.1-3.26.6.2174` | both | Portable storage | [Modrinth](https://modrinth.com/mod/sophisticated-backpacks/version/pJxNzk4X) |
| Sophisticated Core | `1.21.1-1.5.2.2343` | both | Backpacks dependency | [Modrinth](https://modrinth.com/mod/sophisticated-core/version/blXGSmAb) |
| The Aether | `1.21.1-1.5.10-neoforge` | both | One exploration dimension | [Modrinth](https://modrinth.com/mod/aether/version/K5X5qMwG) |
| Waystones | `21.1.46+neoforge-1.21.1` | both | Costed fast travel | [Modrinth](https://modrinth.com/mod/waystones/version/6Z6MQ6os) |
| Xaero's Minimap | `neoforge-1.21.1-26.5.0` | client | Client minimap | [Modrinth](https://modrinth.com/mod/xaeros-minimap/version/Q1tuMQBB) |
| Xaero's World Map | `neoforge-1.21.1-1.46.0` | client | Client world map | [Modrinth](https://modrinth.com/mod/xaeros-world-map/version/9Ckiihkz) |
| YUNG's API | `1.21.1-NeoForge-5.1.9` | server | YUNG structures dependency | [Modrinth](https://modrinth.com/mod/yungs-api/version/2prKITKh) |
| YUNG's Better Dungeons | `1.21.1-NeoForge-5.1.4` | server | Improved dungeon structures | [Modrinth](https://modrinth.com/mod/yungs-better-dungeons/version/D6aZn0Em) |

## Required manual additions

These files are installed privately on the server. Each player must download and add the exact matching **NeoForge 1.21.1** files to their Prism Launcher instance's **Mods** tab before joining.

| Mod | Exact version and file | Side | Purpose | Official download |
|---|---|---|---|---|
| FTB Library | `2101.1.37` · `ftb-library-neoforge-2101.1.37.jar` | both | FTB Ultimine dependency | [CurseForge](https://www.curseforge.com/minecraft/mc-mods/ftb-library-forge/files/9008089) |
| FTB Ultimine | `2101.1.15` · `ftb-ultimine-neoforge-2101.1.15.jar` | both | Mine connected blocks and fell trees | [CurseForge](https://www.curseforge.com/minecraft/mc-mods/ftb-ultimine-forge/files/8231400) |

Total at runtime: 28 mods (26 in the GitHub base pack and 2 installed separately).
