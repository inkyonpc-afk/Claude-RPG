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

## Open items (2026-10-06, end of build session)
Done and verified this session: title screen, spacing calibration, performance numbers, export audit, validator (43/43), multiplayer join, flight gate, realm gate, boss rewards, elytra loot gate.

Still open:
- **Balance is unverified by play.** Time-to-kill targets, skill-tree power curve, L2 Hostility scaling against Apotheosis gear and shard income all need real play sessions (BALANCE.md lists what to watch first).
- **Not measured:** client FPS (vanilla and shaders), long-session client memory, TPS with several players, `/spark` hot spots during boss fights.
- **Spacing:** clutter structures are still somewhat denser than the 12/km2 target (about 16/km2 expected); factors are a first calibration from 6.9 km2 and should be re-censused after any mod change. Boss-tier structures were not seen at all in 2.8 km2 of the second sample (intended rarity, but unconfirmed by data).
- **Quest book:** chapter list and groups render, but the story group's position in the scrolled list was not checked visually (data order is correct).
- **Cosmetic:** custom skill-tree icons (PST's stock set is used); FancyMenu loading-screen layouts; resource packs are not individually license-checked.
- **Multi-player edge cases not tested:** two simultaneous players (Lootr per-player loot, team quest progress), mount state across dimension changes.
- **Modrinth jars:** Ars 'n Spells and Goety are bundled in the export (GPL, MIT); Wyrmroost (All Rights Reserved) is downloaded by the player via `fetch_extra_mods.py`.
- **Client-mod audit:** `pack/client_only.txt` is evidence-based; any new mod that registers network channels must be on both sides.
