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
Defaults, unchanged except two edits (`tools/tune_mounts.py`): +3 % mob health and +2 % damage per level, +3 levels per 1000 blocks from 0,0 (`distanceFactor` 0.003), +10 player levels per extra dimension visited since the last death (`dimensionFactor`, `deathDecayDimension`), adaptive leveling from kills (`killsPerLevel` 30), 80 % of the adaptive level kept after death. **Changed:** `maxTraitCount` 6 (default 9) and `newPlayerProtectRange` 128 (default 48; the spec maximum, an earlier 160 was clamped by Forge). That setting does not make spawn gentle: a mob spawning within that range of players takes the level of the *lowest*-level player there instead of the nearest one, so a group is scaled to its weakest member.

### Model of the curve (`tools/hostility_model.py`, from the mod's source, not from play)
Mob level = dimension base + distance bonus + player level P x dimension scale (+ biome bonus, +/- variation). Built-in entries: overworld 0 / x1.0, Nether 20 / x1.2, End 40 / x1.5; every other dimension (Twilight, Undergarden, Aether, Blue Skies, Otherside, Iron's pocket dimension) falls back to the config default 20 / x1.5 unless a mod ships its own entry (not checked: needs the jars). P = adaptive level + 10 per extra dimension.

| Act | dims visited | assumed kills (total) | adaptive | P | newest realm: mob lv / HP x / dmg x | overworld at 0 / 3000 blocks: mob lv / HP x |
|---|---|---|---|---|---|---|
| I Awakening | 1 | 300 | 10 | 10 | overworld 10 / 1.3 / 1.2 | 10 / 1.3, 19 / 1.6 |
| II A Wider World | 4 | 800 | 43 | 73 | Nether 108 / 4.2 / 3.2 | 73 / 3.2, 82 / 3.5 |
| III Beyond the Veil | 7 | 1300 | 66 | 126 | Aether 209 / 7.3 / 5.2 | 126 / 4.8, 135 / 5.0 |
| IV Fallen Kingdoms | 8 | 1800 | 87 | 157 | Otherside 256 / 8.7 / 6.1 | 157 / 5.7, 166 / 6.0 |
| V End of the Age | 9 | 2200 | 103 | 183 | End 314 / 10.4 / 7.3 | 183 / 6.5, 192 / 6.8 |

Kill budgets per act are assumptions; adaptive level alone is about 10 after 300 kills, 34 after 1,000 and 100 after 3,000. Reading: Act I is mild, but from Act II on ordinary mobs carry 3-4x health, rising to about 10x health and 7x damage in the End, and the jump comes mostly from the dimension bonus (three realms open at once in Act II = +30 levels) and the steep default for modded realms. If Act II-III feels spongy in play, the first levers are `dimensionFactor` (10) and a datapack `levelMap` entry for the modded realms; `healthFactor`/`damageFactor` scale everything at once.

## Status: what is verified and what is not
- **Verified by test:** every ID, loot table, quest, skill and recipe loads (zero errors on server and client); rarity tiers drop per the Apotheosis rules; boss tables roll; flight, realm and elytra gates work on a dedicated server with a joined client.
- **Not verified (needs human play sessions):** time-to-kill targets above, skill-tree power curve against real gear, L2 Hostility scaling against Apotheosis gear, Act-by-Act pacing. Treat every number in this file as a design target. First things to watch in play: Act II boss HP vs Iron's Spells damage; whether L2's default distance and dimension factors outrun gear in the End; shard income vs sigil costs.
