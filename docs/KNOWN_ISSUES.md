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
