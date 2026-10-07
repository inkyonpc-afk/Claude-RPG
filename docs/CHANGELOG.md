# Changelog

## 2026-10-06 — Phase 0: baseline architecture
- Chose Forge 1.20.1 / 47.4.10 after ecosystem research (RESEARCH.md).
- Built `tools/local_union.py` (index of 1,319 CurseForge addons across local 1.20.1 Forge instances, read-only) and `tools/resolve.py`.
- Candidate pool `pack/candidates.txt` (resolves to ~817 incl. dependencies; to be tiered/cut by testing).

## 2026-10-06: Phases 1-3, 10, 11 (first pass)
- **Base:** 666-jar server boot clean (Done in ~78 s, 20 TPS); client enters a world with 720 mods (~150 s to world, ~230 s to interactive).
- **Compat fixes (evidence-driven):** AzureLib 3.1.17, OPAC 0.32.7, Drippy 3.1.5, ETF 7.1 + EMF 3.2.4 (Oculus compat), KubeJS Iron's Spells 6.5-3.14, Miner's Delight 1.4.5, Iron's RPG Tweaks 2.2.3. Rejected: Spell Engine stack, Legendary Monsters, Alshanex's Familiars, Cataclysm: Spellbooks, Chipped, WorldEdit, Every Compat, Healing Campfire, Subtle Effects, Despawn Tweaks (TxniLib), FTB Quests Optimizer, Born In Configuration.
- **Skill tree:** 620 custom nodes (14 regions, 42 keystones, 28 bridges, 4 Oaths), loads with zero PST errors. Economy: 100 points, 8-700 XP each.
- **Races:** 8 original Origins races; default (flight-granting) origins removed.
- **Weapon taxonomy:** 21 classes tagged `aldreth:weapons/*` (~1,000 items).
- **Quests:** 29 chapters, 491 quests across 5 groups, every ID registry-validated; chapter art generated.
- **Tooling:** resolve/install/server_test/autofix/ddmin/launch_client (GUI-automated), build_skilltree/origins/quests/tags/art, registry dump via KubeJS.

## 2026-10-06: Phases 6-9, 13 (traversal, realms, loot, visuals)
- **Flight:**
  - The KubeJS stage `aldreth_flight` (granted on entering the Aether in Act III) gates overworld flying mounts.
  - Fenced structures (490) block flying mounts, elytra and ability flight.
  - A LootJS gate strips elytra from every loot table except the End's own.
  - Every forced dismount grants slow falling.
- **Realms:** Ember Shards + 7 Warden Sigils (KubeJS items, textures, recipes) unseal portals per player through Restricted Portals. Sigil quests are in the Doors chapter; the act finales grant shards. 499 quests total.
- **Boss rewards:** every kill of the 39 bosses rolls `aldreth:boss/t<tier>`: affix gear, materials, gems, shards.
- **World:** tiered structure spacing over all 859 structure sets (Sparse Structures only; Structurify neutral).
- **Mounts and travel:**
  - Ice and Fire tuned: slow hippogryph, weak-block-only dragon griefing, tamed dragons never grief, server moved-wrongly fix.
  - Waystone travel costs XP.
- **Visuals:**
  - 27 curated resource packs, including the STONEBORN UI theme, Fresh Animations and audio packs. They are referenced by CurseForge id in the export, not bundled.
  - Complementary Reimagined/Unbound with 4 presets, shaders off by default.
  - Logo rebuilt for the 1.20 single-strip format; FancyMenu editor overlay hidden; accessibility onboarding off.
- **Fixes:**
  - Missing PST icon `potion_blue_big`; the tree build now validates every texture.
  - The keybind scheme is applied by KubeJS: skill tree K, quests J, roll R.
  - `server_test` now defaults to the release set `core,std`; the `test` pool caused an Enhanced AI dependency crash.
- **Exports:** Default Options carries options.txt (first launch only).

## 2026-10-06: first multiplayer pass (dedicated server + joining client)
- Dedicated server (678 jars, boots in ~135 s, 20 TPS idle, overall mean tick about 1.2-17 ms with a player) accepts a joining client with the full client mod set.
- Bugs found and fixed:
  - Wrong `client_only` guesses blocked the join (Forge "mismatched mod list").
  - Better Clouds (client mod) threw on the server's login event (fixed: client-only, name must match the lock's name exactly).
  - The flight guard hit a Rhino scripting bug (`const` inside a nested block): fixed.
  - `install.py --dry` rewrote the install tracker and orphaned a jar.
- Verified server-side with `tests/mp_flight.txt`: unstaged flying-mount riders are dropped; staged riders keep flying; elytra loot gate strips the Nether table and keeps the End table; boss kills roll `aldreth:boss/t<tier>` (Naga dropped Apotheosis materials).

## 2026-10-06: later fixes (validator, title, quest gating)
- `tools/verify.py` (43 checks, green): found and removed 4 Fabric-format jars, duplicate Ice and Fire and Easy NPC jars; `pack/dep_replaced.txt` stops dependencies re-adding duplicates.
- Ice and Fire: the original 2.1.13 ships; Community Edition alone crashes client and server (registry ID mismatch).
- Title screen: three mods that hijacked it (Ancient Aether menu, Ice and Fire bestiary menu, Blue Skies panorama) switched off; our panorama and logo verified in-client.
- Quests: every quest with a structure task is now optional (233 optional quests), intended so a far-away or biome-bound structure can never stall the story (rewards are kept). _Corrected 2026-10-07: optional did not achieve that; see below._
- Realm gate messages no longer print raw item keys; PERFORMANCE.md filled with measured data; first export built and audited (no caches or runtime state).

## 2026-10-06: spacing calibration, realm gate verified
- Structure spacing calibrated from two world censuses (6.9 km2 pooled, `tools/calibrate_spacing.py`); final tier factors boss 2.55, great 2.35, settlement 1.4, vanilla 2.5, dungeon 3.55, clutter 4.25, ocean decor 4.5 (WORLDGEN.md has the measurements and caveats).
- Realm gate verified on a dedicated server with a joined client (`tests/mp_realms.txt`): teleport into the Nether refused without the Sigil of Flame, advancement fires on receiving it, teleport then succeeds, the Aether stays sealed; 6/6 KubeJS server scripts, 0 errors, 20 TPS.

## 2026-10-06: client memory finding
- **8 GB heap freezes the client** (live set about 8.7 GB, GC death spiral). Minimum is now 10 GB, recommended 12 GB (INSTALL.md, PERFORMANCE.md, `config/memorysettings.json`). Measured idle FPS at 10 GB: 300 to 390 shaders off, 160 to 260 Balanced, 195 to 260 High.
- **ProbeJS removed** (dev tool hooking every translatable component under a global lock); **dev scripts moved out of `kubejs/`** to `tools/dev_scripts/` (registry dump, keybind dump, FPS probe).
- Pruned four cosmetic decor mods (More Beautiful Torches, Diagonal Walls/Fences/Windows): 705 client jars, 665 server jars; server boots in 126 s; `tools/verify.py` green.

## 2026-10-07: quest book fixed from FTB Quests' source (cloud session; not yet confirmed in a running client)
This session ran in a cloud container that cannot download Minecraft, Forge or mods, so these fixes were derived from FTB Quests 2001.4.22, FTB Library 2001.2.13, Certain Questing Additions and L2 Hostility 2.5.19 source code and checked by `tools/questmap_check.py`, not by playing.
- **Empty quest map (the "chapters don't open" bug):** FTB places a chapter image by its center and opens a chapter centered on the bounding box of quests and images. The generator wrote each 30x17-unit backdrop's top-left corner, so the opening view landed on empty space: at 1280x720, 26 of 29 chapters opened with no quest on screen. The backdrop itself was invisible (`alpha: 0.55d` is read as an int, 0). Now the backdrop is centered on the quests with `alpha: 140`; every chapter opens with quests in view.
- **Certain Questing Additions stays:** its "click does nothing" look is its own selection marker (a gray "◀" after the chapter name instead of FTB's white frame, `panel_button_hover`, default on). It does not change the opening view or quest sync.
- **17 cross-chapter dependencies pointed at no quest** (wrong id hash) and FTB dropped them silently: act entries lost their order, the finale needed only the dragon, and the Postgame's first quest was a free checkmark from the start.
- **17 dimension tasks could never complete** (`dim` instead of `dimension`; FTB read an empty dimension). This included "A Country in the Clouds", which grants the flight stage.
- **193 command rewards ran without permissions** (`elevate` instead of `elevate_perms`): supply caches, quest skill points and the flight stage failed for non-op players.
- **Structure hunts still gated 47 quests:** FTB makes dependents wait for optional quests too (`Quest.areDependenciesComplete`). Dependents now inherit the structure quest's own prerequisites. "Explorer" and "Delver of Legends" are exploration capstones and keep theirs.
- `tools/verify.py` now runs `tools/questmap_check.py`: opening views, dependency links and loops, task/reward keys against FTB's readers, structure gating. It flags all of the above in the old files and nothing now. Quest ids are unchanged, so progress is kept.
- **L2 Hostility:** `newPlayerProtectRange` 160 was outside the spec (0-128) and Forge clamped it; now 128, and the docs describe what it really does (a group is scaled to its lowest-level player). `tools/hostility_model.py` adds a source-derived difficulty curve to BALANCE.md (about 4x mob health in the Act II Nether, 10x in the End, mostly from +10 levels per visited dimension).
