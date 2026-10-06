# Loot

_Generated in part by `tools/build_loot.py`._

## Principle
Difficulty and rewards correlate: tiny ruin -> supplies; small dungeon -> uncommon gear; large dungeon -> rare/epic; mega-dungeon -> epic/legendary; boss -> unique equipment and materials; late boss -> mythic/ancient. A house five minutes from spawn never gives endgame gear.

## Rarity ladder (Apotheosis)
Common, Uncommon, Rare, Epic, Mythic (shown as Legendary), Ancient. **Unique** items (boss weapons, relics) are fixed, hand-authored drops.

## Quest caches
Quest rewards call `loot give {p} loot aldreth:quest/t<N>`:

| Tier | Gear rarity | Materials | Gems |
|---|---|---|---|
| t1 | common/uncommon | common | none |
| t2 | uncommon/rare | uncommon | 0-1 |
| t3 | rare/epic | rare | 1 |
| t4 | rare/epic | epic | 1-2 |
| t5 | epic/mythic | mythic | 1-2 |
| t6 | mythic/ancient | ancient/mythic | 1-3 |

## Boss tables
Every boss kill (39 bosses in `design/bosses.py`) rolls `aldreth:boss/t<tier>` at the corpse through `kubejs/server_scripts/boss_rewards.js`, on top of the boss's own unique drops: one affix item of the act's band (t2 uncommon/rare ... t6 mythic/ancient), 1-2 material stacks, and a gem (guaranteed from t4) and Ember Shards (t2-t3 50 %, t4-t5 one, t6 one or two: a backup source for the realm Sigils). The quest cache pays the first kill; the boss table pays every kill, so bosses stay worth farming. Multi-entity fights (Phantom Knights) roll once on average.

## World loot (Apotheosis config, `config/apotheosis/adventure.cfg`)
See the Apotheosis tuning section: affix conversion chances per loot table tier, dimension rarity bands (overworld common-rare, Nether uncommon-epic, End rare-mythic, plus Aether/Blue Skies/Undergarden/Otherside bands), and gem rules.
