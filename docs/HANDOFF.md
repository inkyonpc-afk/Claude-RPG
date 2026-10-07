# Handoff: Embers of Aldreth (Claude RPG modpack)

You are continuing an autonomous build of a large fantasy action-RPG Minecraft modpack. Read this whole file before acting. The user's standing instruction: work through remaining items autonomously, test everything for real (no "works" claims from reading configs), fix verified problems, commit as you go, and do not repeatedly ask permission.

## 1. Where everything is
- **Instance / git repo:** `G:\curseforge\Instances\Claude RPG` (CurseForge instance; repo root = instance root). Latest commit: `88e821e`. Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- **Platform:** Minecraft 1.20.1, Forge 47.4.10, Java 17 at `C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot`, Python 3.12 (Pillow, numpy). Shell: Git Bash (PowerShell also available). Machine: Ryzen 9 5900X, RTX 4070, 32 GB RAM.
- **Distribution:** personal / friends only. Cisco's quests are All Rights Reserved: never copy them; the campaign is original.
- **Memory file (auto-loaded):** `C:\Users\notyo\.claude\projects\G--curseforge-Instances-Claude-RPG\memory\modpack-build-pipeline.md` has pipeline gotchas; keep it updated.
- **Docs (source of truth):** `docs/` has ARCHITECTURE, MODLIST (generated), PROGRESSION, SKILL_TREE, QUESTS (generated), GEAR, LOOT, BALANCE, WORLDGEN, TRAVERSAL, PERFORMANCE, VISUALS, KNOWN_ISSUES, INSTALL, CHANGELOG, LICENSES, RACES, WEAPON_CLASSES, RESEARCH, plus `README.md` at the root. Machine-readable manifest: `pack/manifest.json`, `pack/mods.lock.json`.

## 2. Safety rules (non-negotiable)
- Never `taskkill /IM java.exe` (would kill the user's own Minecraft). Stop only recorded PIDs: `tools/stop_server.py` (server, `.build/server.pid`), or `Stop-Process -Id (Get-Content .build/client.pid)` for the test client. The launcher kills its own client at the end of `--wait`.
- Other CurseForge instances under `G:\curseforge\Instances\` are **read-only** (jar cache and references only).
- Only the local test server in `.build/server` has `eula=true` (user approved). Test identity is offline `AldrethTest`; never use the user's account.
- Never bundle All Rights Reserved content in the export (Wyrmroost is ARR: download script instead).

## 3. Pipeline (all idempotent; never hand-edit generated files)
```
pack/candidates.txt  ->  tools/resolve.py  ->  pack/mods.lock.json  ->  tools/install.py --status core,std  ->  mods/
```
- `candidates.txt` line format: `category | name(::filename fragment) | status | note`; statuses `core`, `std` (release set), `test` (NOT shipped, untested pool), `skip` (rejected, reason recorded). `ext |` lines are Modrinth pins in `pack/pinned.json`.
- `pack/dep_replaced.txt`: projects never pulled in as dependencies (duplicate mod ids). `pack/client_only.txt`: excluded from server installs; **add only with evidence** (a server crash on a client class); names must match the lock's exact name.
- `install.py --dry` must never write the tracker (fixed). `install.py --server --dest .build/server/mods` for the server set.
- Generators (design sources in `design/`): `build_skilltree.py` (620 nodes, validates textures), `build_quests.py` (from `design/quests/*.py`), `build_origins.py`, `build_loot.py` (quest caches + boss tables + `kubejs/server_scripts/boss_rewards.js` from `design/bosses.py`), `build_traversal.py` (flight guard + elytra loot gate), `build_sigils.py` (Ember Shards / Warden Sigils from `design/custom_items.py`, Restricted Portals config), `build_tags.py`, `build_art.py`, `build_menu_art.py`, `build_visuals.py [--options]` (resource/shader packs + presets, writes `pack/visual_packs.json`), `tune_apotheosis.py`, `tune_structures.py` (spacing from `tools/spacing_tiers.py` + `config/aldreth/spacing_calibration.json`), `tune_mounts.py` (mounts, waystones XP, L2 Hostility safety, title-screen hijack switches).
- **Release gate:** `python tools/verify.py` (43 checks: >=250 mods, one mod id per jar, all deps, no Fabric jars, builders 0 errors, data files, docs). Was green at last run.
- **Export:** `python tools/export_curseforge.py --version 0.1.0` -> `dist/EmbersOfAldreth-0.1.0.zip` (98.5 MB; 732 CurseForge-referenced files incl. resource/shader packs; bundles only license-permissive Modrinth jars: Ars 'n Spells GPL, Goety MIT; Wyrmroost via `fetch_extra_mods.py`; options via Default Options; no caches/runtime state).

## 4. Test harness
- **Server:** `python tools/server_test.py [--fresh] --cmds "cmd;wait N;cmd" | tests/file.txt --tag T [--timeout S] [--xmx 8G]` (default status `core,std`; has a lock file; logs `.build/logs/<tag>.log`; result line `RESULT DONE|BOOT_FAIL`). Commands start right after "Done"; `wait N` = seconds. Server log while running: `.build/server/logs/latest.log`.
- **Client:** `python tools/launch_client.py --world AldrethTest01 | --join 127.0.0.1:25599 --wait S --xmx 10G --size 1280x720 --script "j62:key j;j67:click 38,390;j71:scroll 300,300,3600;j74:shot name"`. `jN` = seconds after the "joined" log marker; plain N = seconds after launch. Shots land in `.build/shots/`. Actions: `click x,y` (pre-move + 220 ms hold), `key` (SendKeys syntax, e.g. `{ESC}`, `{F3}`), `scroll x,y,delta`, `shot`. Window-relative coordinates incl. title bar. World becomes interactive ~50-75 s after join; first 1-2 min in world are slow (EMI/JEI background indexing).
- **Multiplayer tests:** start server_test with `tests/mp_flight.txt` or `tests/mp_realms.txt`, wait for "Done (" in `.build/server/logs/latest.log`, then launch the client with `--join 127.0.0.1:25599 --wait 420`. Both passed (see section 6).
- **Measurement tools:** `tools/structure_census.py [world] --json out` (structure starts per tier/km2), `tools/calibrate_spacing.py "census.json@used_cfg.json5" ...` (use `@`, MSYS rewrites `:`), `tools/entity_census.py <world>`, dev-only KubeJS scripts in `tools/dev_scripts/` (registry dump, keybind dump, FPS probe): copy into `kubejs/...` for a run, then delete; they must never ship. `jcmd <pid> GC.run` + `GC.heap_info` / `GC.class_histogram`, `jstack <pid>` for stalls.
- **Shell gotchas:** bash heredocs collapse backslashes (write regex/`\n` code with the Write/Edit tools); KubeJS Rhino: no `const` inside nested blocks in repeated handlers (use `var`); `java.lang.Runtime` is blocked by KubeJS class filter; KubeJS script globals collide across files (prefix names).

## 5. What the pack is (as built)
- **705 client jars / 665 server jars** (Forge reports ~753 incl. nested). Key systems: Better Combat + Combat Roll; Passive Skill Tree with one custom 620-node tree (14 regions, 42 keystones; key K); Origins with 8 original races; Apotheosis 7.4.8 gear spine (+ addons, Weapon Leveling, Ancient Reforging); Iron's Spells + Ars Nouveau + Goety + Forbidden & Arcanus; Curios/Artifacts/Relics/Enigmatic Legacy; FTB Quests campaign: 29 chapters, 499 quests, 5 groups (quest book key J); KubeJS + LootJS; Tectonic/Terralith worldgen; 10 dimensions; 39 bosses; Ice and Fire **original 2.1.13** (Community Edition crashes alone: registry ID mismatch), Wyrmroost, Tameable Beasts etc.
- **Gating:** flight act-gate (KubeJS stage `aldreth_flight` from the Act III Aether quest; unstaged flying mounts drop riders), 490 fenced no-flight structures, elytra loot gate (only End tables keep elytra), realm gating via Ember Shards + 7 Warden Sigils + Restricted Portals (advancement on holding the sigil), boss per-kill tables `aldreth:boss/t<tier>`, waystone XP costs.
- **Spacing:** Sparse Structures Reforged only, calibrated from two censuses (6.9 km2): boss 2.55, great 2.35, settlement 1.4, vanilla 2.5, dungeon 3.55, clutter 4.25, ocean_decor 4.5 (fixed), realm 1.0.
- **Visuals:** 23 resource packs (Fresh Animations, audio, Eclectic Trove, FTB quest shapes...; STONEBORN dropped), Complementary Reimagined/Unbound with 4 presets in `config/aldreth/shader_presets/` (shaders OFF by default in `config/oculus.properties`). Title screen fixed: Cumulus Menus API off, Ice and Fire `Custom main menu` off, Blue Skies `custom_panorama` off; logo in 1.20 format (1024x256 sheet). Keybind scheme applied once by `kubejs/client_scripts/01_default_keybinds.js`.
- All structure-task quests are forced optional (`tools/questlib.py`) so far/biome-bound structures never gate the story.

## 6. Verified this session (real tests)
- Dedicated server boots (665 jars, ~126 s, 20 TPS); client joins and stays connected.
- `tests/mp_flight.txt`: unstaged rider dropped, staged rider keeps flying, elytra gate (Nether table 0 items, End table 13), boss kill drops an Apotheosis material.
- `tests/mp_realms.txt`: Nether teleport refused without the Sigil of Flame, advancement on receiving it, teleport then works, Aether stays sealed; 6/6 KubeJS server scripts, 0 errors.
- Pregeneration: 16,129 chunks in 18 min 54 s at 20 TPS; server heap 6.8/8 GB.
- **Client memory (major finding):** 8 GB heap freezes the game (live set ~8.7 GB -> GC death spiral; 1,400 ticks in 13 min). 10 GB works: idle 300-390 FPS shaders off, 160-260 Balanced, 195-260 High (1280x720, RD 12). Recommended 12 GB. `config/memorysettings.json` now warns <9000 MB and >16000 MB (old 8500 max caused a blocking dialog that also breaks quick-play). Launcher default `--xmx 10G`. ModernFix dynamic_resources saves ~1.6 GB but is NOT enabled (compat unverified).
- Removed: ProbeJS (dev tool, hooks translatable components under a lock), 4 Fabric-format jars, duplicate Ice and Fire / Easy NPC jars, Better Clouds made client-only (crashed server login), Shiny Trims RP, More Beautiful Torches + Diagonal Walls/Fences/Windows (memory).
- **Quest id bug fixed:** FTB parses ids with signed `Long.parseLong(hex,16)`; ids >= 2^63 silently failed (3 of 5 chapter groups lost; dependency links likely dropped too). `hid()` in `tools/questlib.py` now masks to 63 bits; all 2,340 ids valid; chapter list now shows all 5 groups in order (verified in-client). Note: this changed every quest id, so existing worlds' quest progress resets (fine: unreleased).

## 7. IN PROGRESS when handed off (do this first)
**Quest chapters may not open in the quest book.** Findings so far:
- The harness click works on list widgets (expand arrow, group headers collapse).
- With **Certain Questing Additions** (`certain_questing_additions-forge-1.2.0.2+mc1.20.1.jar`, currently in `pack/client_only.txt`, installed in `mods/`) present, clicking a chapter row only shows the hover icon, no selection.
- With that jar temporarily moved out, the click **selects** the chapter (white frame appears), but the quest map area still renders nothing (run tag `g34`, shots `.build/shots/map1.png`, `map2.png`; check `map2.png`, not yet viewed). `.build/modbak/` is empty; the jar is back in `mods/`.
- FTB code facts (javap on `mods/ftb-quests-forge-2001.4.22.jar`): `ChapterButton.onClicked` opens only if `canEdit || chapter.hasAnyVisibleChildren()` (= chapter has quests), then `QuestScreen.open(chapter)`. `Quest.isVisible` depends only on `invisibleUntilCompleted`/`invisibleUntilTasks`. The server log shows "Loaded 6 chapter groups, 29 chapters, 499 quests"; the client reads ~1,767 objects.
- **Next steps:** view `map2.png`; try scrolling/zooming the map (scroll on map area, or `old_scroll_wheel`); compare with a minimal hand-made chapter; check whether quest `x/y` units or `images` entries break rendering; check whether CQA must be removed (it is also on the server side? it was moved to both sides earlier, see KNOWN_ISSUES handshake note) and whether the quest map renders with editing mode (`/ftbquests editing_mode` gives canEdit). Prior pre-fix screenshots never showed a chapter either, so this predates the id fix. **If chapters cannot be shown, the whole quest campaign is unusable: highest priority.**

## 8. Still open (after section 7)
1. **Commit + docs** for anything new; refresh `docs/KNOWN_ISSUES.md` "Open items" and CHANGELOG; rerun `tools/verify.py`; re-export.
2. **Re-run multiplayer smoke** after mod changes (`tests/mp_realms.txt`, `tests/mp_flight.txt`) since the mod set changed (ProbeJS, decor prune, quest ids).
3. **Spacing:** clutter still above target (~16 vs 12/km2); optional third census to confirm final factors (`tests/census_regions.txt`, radius 400, 480 s per region).
4. **Balance is unverified by play** (TTK, skill-tree power, L2 Hostility vs gear, shard income). Possible automated work: measure L2 Hostility mob HP/damage at distances with a joined client (`summon` then `data get entity ... Attributes`).
5. **Not tested:** two simultaneous players (Lootr per-player loot, team quests), mounts across dimension changes, long-session client memory, FPS in combat, low-end GPUs.
6. **Cosmetic backlog:** custom skill-tree icons (PST stock icons used), Drippy/FancyMenu loading-screen layouts, resource-pack license checks.
7. Consider enabling ModernFix dynamic resources only after visual verification across many blocks/items.

## 9. Key file map
- `design/`: `skilltree_content.py`, `quests/*.py` (story_1-3, craft_1-2, road_1-2, hearth), `bosses.py`, `custom_items.py`.
- `tools/`: everything in section 3/4, plus `questlib.py`, `skilltree_lib.py`, `spacing_tiers.py`, `nbtlite.py`, `gui.ps1`, `shot.ps1`, `crashsum.py`, `logscan.py`, `ddmin.py`, `autofix_client.py` (do NOT trust its client-only guesses).
- Game data: `config/paxi/datapacks/aldreth_core` (skills, skill tree, loot tables, tags), `config/paxi/resourcepacks/aldreth_core` (title art, quest backgrounds), `kubejs/` (startup items, server scripts, client keybinds/tooltips, item textures), `config/ftbquests/quests/`, `defaultconfigs/skilltree-server.toml`.
- Tests: `tests/mp_flight.txt`, `tests/mp_realms.txt`, `tests/perf_pregen.txt`, `tests/census_regions.txt`.
