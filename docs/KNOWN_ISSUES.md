# KNOWN_ISSUES

_Status: skeleton — filled in during its phase (see ARCHITECTURE.md)._

## Fixed / worked-around (compat datapack `config/paxi/datapacks/aldreth_fixes`)
- **Prodigium Dungeons 0.9.2** ships two 0-byte structure files (`glider_tower`, `glider_tower_crystal`) that abort datapack loading ("Not a JSON object: null"). Blocked via pack.mcmeta filter together with their structure_sets.
- **Prodigium Dungeons** also uses Ancient Aether's structure type (`ancient_aether:jigsaw_skylands`) without declaring it: see `pack/extra_deps.txt`.
- **Legendary Monsters 2.2.1** has a common mixin targeting a client class (crashes dedicated servers): rejected.
- **Alshanex's Familiars 1.1.2**, **Born In Configuration**, RPG-Series jewelry (Spell Engine stack): rejected (version/architecture conflicts).
- **Cataclysm: Spellbooks 1.2.x**: extends `Ancient_Remnant_Rework_Renderer`, which Cataclysm 3.24-3.31 no longer has (renamed `Ancient_Remnant_Renderer`): client crash on startup (server unaffected). Rejected; revisit if the addon updates.
- **Chipped 3.0.7**: its JEI category calls `IRecipeSlotBuilder.setPosition`, unimplemented by EMI 1.1.24 (latest) jemi layer -> ~7,200 `AbstractMethodError`s at load and a huge block/recipe count. Rejected.
- **Healing Campfire 6.2**: `CampfireEvent.playerTickEvent` throws ClassCastException every tick near a campfire; Neruina kicks the player ("ticking exception on your player"). Rejected.
- Shiny Trims resource pack: rejected, it disables ImmediatelyFast HUD batching and font atlas resizing (FPS cost for a cosmetic).

## Multiplayer handshake (found 2026-10-06 by the first dedicated-server join test)
Mods that register network channels must be on BOTH sides, or Forge refuses the join ("mismatched mod list"). Earlier `pack/client_only.txt` entries were guesses and wrongly excluded content/channel mods from the server: Blaze Gear (`blazegear:main`), EMI + EMI Loot (loot sync), Relics, CoFH Core, Blowguns, Fragmentum, Certain Questing Additions, Fusion. They are now installed server-side (679-jar server, boots in ~142 s). Rule: add a mod to `client_only.txt` only with evidence (server crash on a client class), never by category.

## Open items (end of session 2026-10-06)
- **Title screen (fixed 2026-10-06, verified in-client):** three mods replaced it (Ancient Aether via Cumulus Menus, the original Ice and Fire bestiary menu, Blue Skies' realm panorama). All three are switched off in `config/` (see `tools/tune_mounts.py`). The STONEBORN UI pack was dropped. Rule: when adding a mod, check whether it hijacks the title screen.
- **Ice and Fire:** the original 2.1.13 is shipped. IceAndFire Community Edition alone crashes the client (registry ID mismatch) and was never tested.
- **Spacing calibration:** first-pass factors applied from one 4 km2 ocean/ice-heavy sample (`config/aldreth/spacing_calibration.json`). A 4-region census run (`tests/census_regions.txt`, tag census2) was started; combine it with the first sample via `tools/calibrate_spacing.py ".build/census1.json@.build/used_cfg_run1.json5" ".build/census2.json@.build/used_cfg_run2.json5"` after `tools/structure_census.py --json .build/census2.json`, then rerun `tools/tune_structures.py`.
- **Not yet done:** PERFORMANCE.md data write-up (1000-block pregen: 16,129 chunks in 18m54s, TPS 20, server 6.8/8 GB, boot ~136-161 s, client title ~150 s), final export run (`tools/export_curseforge.py`), `tools/verify.py` final pass (only PERFORMANCE.md size failed), full server+client re-test of the final mod set, balance play-testing.
