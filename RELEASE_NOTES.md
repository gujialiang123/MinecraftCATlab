# JialiangCraft 2.0.0 configuration notes

Official Minecraft Java Edition 26.3 vanilla survival, with a fresh random world, hard difficulty, a spawn bonus chest, and a four-player maximum.

- Use a vanilla **Java Edition 26.3** client and connect to `98.93.3.136:25565`. No modpack or manual FTB downloads are required.
- Keep online account authentication enabled, hard difficulty, and the owner's disabled whitelist. Generate the initial spawn bonus chest with the official `--bonusChest` option.
- Disable player cheats: leave the operator list empty, disable command blocks, and keep the saved world's `allowCommands=false`.
- Store new server state at `/home/jgu7/work/jialiangcraft-vanilla-26.3-data`; preserve the old NeoForge 1.21.1 world separately without upgrading it.
- Pin the official server and isolated Java 25 runtime. Use a 1 GiB initial / 4 GiB maximum heap, four JVM-visible processors, and nice level 10 on the shared lab machine.
- Keep the existing TCP relay, reboot startup, and daily backups. Restore accepts only compatible vanilla backups.

Version 2.0.0 identifies the repository configuration; these notes do not announce a new public GitHub Release. The existing [v1.1.0 release](https://github.com/gujialiang123/MinecraftCATlab/releases/tag/v1.1.0) is an archived NeoForge modpack. See [validation results](docs/VALIDATION.md) for deployment checks and remaining limits.
