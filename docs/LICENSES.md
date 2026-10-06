# Licenses and asset provenance

Distribution target: **personal use and friends**. The rules below keep it that way without copying anyone's rights.

## What is original (ours)
Everything generated or written in this repository:
- the quest campaign (29 chapters, 499 quests), its lore, chapter art and the Embers of Aldreth setting;
- the 620-node skill tree, the 8 races, the weapon taxonomy tags, the Ember Shard / Warden Sigil items and their textures;
- the title-screen panorama, logo and tagline, quest-book backgrounds, splash texts;
- all tools, KubeJS scripts, loot tables, datapacks and docs.

None of it is copied from another modpack. **Cisco's Fantasy Medieval RPG quests were not used**: that pack is All Rights Reserved, so its quest files were treated as inspiration for chapter structure only and nothing was reproduced. Other local instances were read only for jar caches and tooling lessons; nothing from them was altered.

## Third-party mods
- The export zip **references** CurseForge-hosted mods, resource packs and shader packs by project and file id (`manifest.json`); the CurseForge app downloads them from the authors' pages. Nothing is re-hosted.
- Jars that are not on CurseForge (published on Modrinth) are handled by license, decided automatically by `tools/export_curseforge.py` from the license declared in each jar's own `mods.toml`:
  - **Bundled** only when the declared license permits redistribution (MIT, LGPL, GPL, Apache, BSD, MPL, CC0...). The zip lists each one with its license in `overrides/THIRD_PARTY.md`.
  - **Not bundled** otherwise. They are listed in `overrides/EXTRA_DOWNLOADS.json` with their official URL and sha1, and `overrides/fetch_extra_mods.py` downloads and verifies them on the player's own machine.
- Current Modrinth-sourced jars and their declared licenses: Jupiter (LGPL-3.0), Uranus (LGPL-3.0), Ars 'n Spells (GNU GPLv3), Goety (MIT), IceAndFire Community Edition (LGPL-3.0), **Wyrmroost (All Rights Reserved: never bundled; downloaded by the player)**.

## Resource and shader packs
Referenced by CurseForge id (see `pack/visual_packs.json` for names, ids and the instance each was found in). Not copied into the export. Each remains under its author's license; players who change or redistribute them must follow those licenses. Complementary Reimagined/Unbound by EminGT are used as unmodified shader packs; our presets are separate option files.

## Local files that are never published
`mods/*.jar`, `resourcepacks/*.zip`, `shaderpacks/*.zip`, saves, logs and the offline test identity are git-ignored; the repository holds only our own sources and the lock file that reproduces the jar set.

## If this ever goes public
Re-check every bundled item against its current license, add each mod author's required attributions, get the authors' permission for any All Rights Reserved content (Wyrmroost is confirmed; the resource packs have not been license-checked individually), and decide how the Mojang EULA and CurseForge's modpack terms apply to the final download.
