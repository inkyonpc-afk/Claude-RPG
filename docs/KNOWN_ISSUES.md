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

## Quest book (found 2026-10-07 by reading FTB Quests 2001.4.22 source; fixed in the generator)
FTB Quests does not log any of these; the book just looks or behaves wrong. `tools/questmap_check.py` (part of `verify.py`) now catches each one.
- **Chapters looked empty:** an image's `x`/`y` is its center, and a chapter opens centered on the bounding box of quests and images, so a backdrop placed by its corner moved the view off the quests. `alpha` is an int 0-255 (a double like 0.55 reads as 0).
- **Cross-chapter dependencies** must hash the target chapter: `chapter.quest` -> `hid(chapter, quest)`. Unknown ids are dropped without a warning.
- **NBT keys:** dimension tasks read `dimension` (the editor shows "dim"); command rewards read `elevate_perms`. Unknown keys are ignored, and without `elevate_perms` a command runs at the player's own permission level.
- **Optional does not unblock dependents:** `Quest.areDependenciesComplete` needs every dependency completed (ALL_COMPLETED); `optional` only keeps a quest out of chapter completion. Dependents of structure hunts therefore get the hunt's own prerequisites (`questlib.gating_deps`).
- **Flexible progression:** tasks progress before their dependencies are done, but the quest completes and pays out only once they are.
- **Certain Questing Additions** draws the selected chapter as "Name ◀" in gray (no white frame) when `panel_button_hover` is on (default). That explains the earlier "clicking a chapter does nothing" observation; it is not a fault. It stays.

## Open items (2026-10-07)
Done and verified earlier: title screen, spacing calibration, performance numbers, export audit, validator, multiplayer join, flight gate, realm gate, boss rewards, elytra loot gate. Done 2026-10-07 from mod source (cloud session, no game): quest book opening view, links, keys and gating; L2 protect range; hostility model.

Still open:
- **Quest book in a running client (do first):** open the book (J) at 1280x720 and confirm the Prologue's quests show at once, each chapter opens on its quests and the backdrops show at about 55 % opacity. Then complete one dimension quest and one command-reward quest as a non-op player (skill point and supply cache arrive), and check that "The Road Calls" completes without a village.
- **Re-run after the quest changes:** `tools/verify.py` with jars installed, `tests/mp_realms.txt`, `tests/mp_flight.txt`, and the export. The mod set did not change on 2026-10-07; quest ids are unchanged.
- **Balance is unverified by play.** Time-to-kill targets, skill-tree power curve, shard income. The L2 Hostility model (BALANCE.md) predicts about 4x mob health in the Act II Nether and 10x in the End, mostly from +10 levels per visited dimension. Check this first in play. Whether any installed mod ships L2 difficulty entries for the modded realms is unchecked (needs the jars).
- **Not measured:** client FPS in combat, long-session client memory, TPS with several players, `/spark` hot spots during boss fights.
- **Spacing:** clutter structures are still somewhat denser than the 12/km2 target (about 16/km2 expected); factors are a first calibration from 6.9 km2 and should be re-censused after any mod change. Boss-tier structures were not seen at all in 2.8 km2 of the second sample (intended rarity, but unconfirmed by data).
- **Cosmetic:** custom skill-tree icons (PST's stock set is used); FancyMenu loading-screen layouts; resource packs are not individually license-checked (they are referenced by CurseForge id, not bundled).
- **Multi-player edge cases not tested:** two simultaneous players (Lootr per-player loot, team quest progress), mount state across dimension changes.
- **Modrinth jars:** Ars 'n Spells and Goety are bundled in the export (GPL, MIT); Wyrmroost (All Rights Reserved) is downloaded by the player via `fetch_extra_mods.py`.
- **Client-mod audit:** `pack/client_only.txt` is evidence-based; any new mod that registers network channels must be on both sides.
