# Embers of Aldreth — Architecture

Source of truth for system decisions. Update deliberately (with a CHANGELOG entry) when testing disproves a choice.

## Platform
- **Minecraft 1.20.1, Forge 47.4.10** (Forge's recommended build; 47.4.26 is latest as of 2026-10-06 but 47.4.10 is the build the instance and every local reference pack were validated on), Java 17.
- **Why not NeoForge 1.21.1 / 26.x** (researched 2026-10-06, see RESEARCH.md): Passive Skill Tree has no official 1.21.1 build; T.O Magic 'n Extras is 1.20.1-only; the official Alex's Mobs/Caves, Tetra, Blue Skies, Aether Redux and Enigmatic Legacy never left 1.20.1. All other major RPG mods (Iron's Spells, Apotheosis 7.x, Cataclysm, Mowzie's, Ars Nouveau, Twilight Forest, Better Combat, Simply Swords, Epic Knights, FTB Quests, KubeJS) have current 1.20.1 builds. 26.x has no Iron's Spells/Mowzie's/Twilight Forest builds. Fabric has a weaker Apotheosis/Cataclysm/Iron's ecosystem and no Passive Skill Tree.
- **Distribution:** personal/friends. Pack is a git repo; jars are reproduced from `pack/mods.lock.json`. `tools/export_curseforge.py` emits a CurseForge-format manifest zip. Cisco's quests are All Rights Reserved: **not used**. Quest campaign is original.

## Core systems
| System | Choice | Rejected |
|---|---|---|
| Combat | Better Combat + Combat Roll (+ Apotheosis/Particle compat) | Epic Fight (control conflict; server attack bug #1582); one framework only |
| Levels/skills | Passive Skill Tree 0.7.6e, ONE custom generated tree (~600 nodes, 14 regions, ~32 keystones). Points via XP levels + quest rewards. Amnesia Scroll respec. | Project MMO / Pufferfish's Skills (second XP system) |
| Keystone mechanics | **As built:** PST's own bonus types and conditions implement all 42 keystones (damage conversion, health reservation, condition-gated multipliers, ignite/kill/crit listeners, taken-damage multipliers as the drawback). No KubeJS flag attributes were needed. | KubeJS flag attributes + custom Java mod (kept only as fallback) |
| Attributes | Apothic Attributes backbone + Iron's spell attrs; AttributeFix + Max Health Fix | RPGStats |
| Races | Origins (Forge), ~8 original races w/ small perks, no class lock | Origins: Classes, Medieval Origins, Strictly Origins (broken powers per Connor RPG) |
| Gear | Apotheosis 7.4.8 (rarity/affixes/sockets/gems/reforge/salvage/enchanting) + Apotheotic Additions + Apothic Curios + Lukas' Weapon Leveling + Ancient Reforging | Tetra, Silent Gear (second gear identity) |
| Rarity | Common, Uncommon, Rare, Epic, Mythic, Ancient (Apotheosis names kept as shipped; the planned "Legendary" display rename was not built) + hand-authored Uniques | |
| Magic | Iron's Spells (combat) + addons; Ars Nouveau/Elemental (utility); Goety (summoning/necro) | Spell Engine/Wizards/Paladins (second spell stat system) |
| Accessories | Curios, Artifacts, Relics, Enigmatic Legacy, Majrusz's Accessories | |
| Quests | FTB Quests + FTB Teams, generated from design JSON | Odyssey (1.21 only) |
| Scripting | KubeJS + LootJS (+ Curios/Iron's addons); no CraftTweaker | |
| Worldgen | Tectonic + Terralith (+ TerraBlender/Lithostitched), OTBWG, Alex's Caves; Incendium, Nullscape | BetterEnd/BetterNether (Fabric-only), Sinytra Connector |
| Rendering | Embeddium 0.3.31 + Oculus 1.8.0 + Complementary Reimagined (optional) | |
| Traversal | see TRAVERSAL.md | |

## Build pipeline
`pack/candidates.txt` -> `tools/resolve.py` -> `pack/mods.lock.json` -> `tools/install.py` -> `mods/`; headless validation by `tools/server_test.py`; log triage by `tools/logscan.py`.
Status flags in candidates: `core` (architecture-critical), `std` (planned), `test` (experimental), `skip` (rejected, reason recorded).
Mods are installed in tiers (see CHANGELOG) so each batch is server-tested before the next.

## Count policy
Target 250 minimum (enforced by verify.py), ceiling set by measured startup/memory/TPS (Phase 14). Candidate pool is intentionally larger than the shipping set; weaker/redundant/problematic mods are cut by test evidence, recorded in `pack/rejects.txt` and KNOWN_ISSUES.

## Rejected-by-evidence list (inherited from prior local attempts)
Sinytra Connector + Fabric-API bundles, TxniLib (+dependents Cerulean/Despawn... check), BCLib/BetterEnd/BetterNether, Dramatic Doors (invalid BWG recipes), Medieval Origins Revival, Strictly Origins, Particle Effects (server cast failure; client-only), AllTheLeaks/Radium (marked broken), Relics-family caution (server issues seen in another pack).


## As built (2026-10-06 audit; supersedes the plan where they differ)
- **Shipping set: 712 jars** (`tools/verify.py` enforces >= 250, one mod id per jar, every mandatory dependency present, no Fabric/NeoForge-only jars). Server set: 678 jars (client-only list in `pack/client_only.txt`, evidence-based only).
- **Eidolon Repraised** stayed in the `test` pool (not shipped); magic is Iron's Spells + Ars + Goety + Forbidden & Arcanus + T.O Magic 'n Extras.
- **Gear spine unchanged:** Apotheosis 7.4.8 + addons, Weapon Leveling, Ancient Reforging. No Tetra, Silent Gear or Epic Fight.
- **Realm gating:** Restricted Portals + Ember Shards/Warden Sigils (PROGRESSION.md); **flight gating:** KubeJS act-gate stage + fenced structures + elytra loot gate (TRAVERSAL.md); **boss rewards:** per-kill tables (LOOT.md).
- **Spacing:** Sparse Structures Reforged is the single spacing system, driven by `tools/tune_structures.py`; Structurify stays installed but neutral (WORLDGEN.md).
- **Resource packs and shaders:** a curated stack referenced by CurseForge id (VISUALS.md); shaders off by default.
- **Dependency hygiene:** `pack/dep_replaced.txt` blocks CurseForge dependencies that duplicate a mod id already provided by another selected file (Ice and Fire original vs Community Edition; Easy NPC vs Easy NPC: Core).
- **Testing doctrine:** every claim above is backed by a headless server boot, a client boot, or the multiplayer join test (`tests/`); nothing is declared working from reading configs.
- **Static checks against mod source (2026-10-07):** some failures are silent in game (FTB Quests ignores unknown keys and unknown dependency ids, and logs nothing). `tools/questmap_check.py` (run by `verify.py`) holds the quest book to what FTB Quests 2001.4.22's code actually reads and does: opening view of every chapter (a replica of its layout code), dependency links and loops, task/reward keys, and structure-hunt gating. `tools/hostility_model.py` derives the L2 Hostility curve from its source. These complement in-game tests; they do not replace them.
