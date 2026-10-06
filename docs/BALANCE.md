# Balance

## Philosophy
Fun, challenging RPG, not punishing hardcore. Difficulty comes from mechanics and progression, not health sponges. Early game approachable; mid-game substantial build growth; late game the player is very powerful; endgame still has genuinely hard optional content. Avoid one-shots, grind walls, artificial scarcity, bosses with millions of HP.

## Power budget (design numbers; verified in Phase 16)
| Source | Budget |
|---|---|
| Skill tree | 100 points, avg ~350 XP each (~35k XP total). Minor 2-4%, notable 5-8%, major 10-15% (conditional), mastery 15-25% (conditional), keystone 30-60% with a real drawback. A focused build reaches 1-2 keystones. |
| Races | one small identity bonus and one drawback each (+-2 armor, +-4 HP, +-4% dodge, +-10% a school) |
| Gear (Apotheosis) | rarity ceilings by act: Act I common-rare, II rare-epic, III epic-mythic, IV mythic, V+ ancient only from top bosses and vaults |
| Accessories | limited slots; slot count grows via tree/quests, no stacking of the same effect |
| Enchanting | table maxes by shelf tier: 30 (shelves), 60 (hell/sea), 100 (end) with quanta/arcana limiting reliability |
| Spells | school spell power scales ~linearly; cooldown reduction capped (Iron's) |

## Levers (where numbers live)
- Skill tree amounts: `design/skilltree_content.py` (rebuild with `tools/build_skilltree.py`).
- XP/points curve: `defaultconfigs/skilltree-server.toml`.
- Race values: `tools/build_origins.py`.
- Loot rarity: Apotheosis `adventure.cfg` rules + `affix_loot_entries` overrides (LOOT.md); quest caches `tools/build_loot.py`.
- Mob scaling: L2 Hostility config (distance/dimension difficulty), Apotheosis boss spawn rules.
- Boss HP: each mod's config (Cataclysm, Mowzie's, Ice and Fire); target TTK per act in the table below.

## Target time-to-kill (solo, build-appropriate gear)
| Act | Regional boss | Elite | Trash |
|---|---|---|---|
| I | 2-4 min | 20-40 s | 2-5 s |
| II | 3-5 min | 30-50 s | 3-6 s |
| III | 4-6 min | 40-60 s | 3-6 s |
| IV | 5-8 min | 50-80 s | 4-8 s |
| V/Post | 6-12 min (superbosses 12-20) | 60-100 s | 4-8 s |

## Mob scaling as configured (L2 Hostility 2.5.19)
Defaults, unchanged except two safety edits (`tools/tune_mounts.py`): +3 % mob health and +2 % damage per level, +0.3 levels per 100 blocks from spawn (`distanceFactor` 0.003), +10 levels per dimension tier, adaptive leveling from the nearest player's kills, 30 kills per level, 80 % difficulty kept after death. **Changed:** `newPlayerProtectRange` 160 (spawn stays gentle) and `maxTraitCount` 6 (default 9).

## Status: what is verified and what is not
- **Verified by test:** every ID, loot table, quest, skill and recipe loads (zero errors on server and client); rarity tiers drop per the Apotheosis rules; boss tables roll; flight, realm and elytra gates work on a dedicated server with a joined client.
- **Not verified (needs human play sessions):** time-to-kill targets above, skill-tree power curve against real gear, L2 Hostility scaling against Apotheosis gear, Act-by-Act pacing. Treat every number in this file as a design target. First things to watch in play: Act II boss HP vs Iron's Spells damage; whether L2's default distance and dimension factors outrun gear in the End; shard income vs sigil costs.
