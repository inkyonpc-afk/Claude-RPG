# Progression: Prologue to Postgame

**Lore frame.** Aldreth was held together by the Covenant of Seven Wardens. Each realm (dimension) is a sealed Warden-domain. The Hollow Crown shattered; its Ember Shards are held by corrupted guardians (the bosses). The player is an *Emberbound*, carrying a shard-fragment. The skill tree is the "Constellation of Embers".

Power curve: ordinary adventurer -> specialised hero -> legendary. Gear tiers (rarity) are gated by *where* loot comes from (LOOT.md), never by raw mod defaults.

| Act | Realms / areas | Bosses (examples) | Gear tier | Level band | Magic | Traversal unlocks |
|---|---|---|---|---|---|---|
| Prologue | Spawn region | none | Common | 1-5 | first spell scroll | sprint, roll, horse, boat |
| I Awakening | Overworld ruins, small dungeons (WDA, YUNG, Dungeons and Taverns) | Apotheosis elites, Ferrous Wroughtnaut, Twilight-style minibosses | Uncommon-Rare | 5-18 | Iron's tier 1-2 schools, Ars glyph basics | Waystones, Paraglider, climbing, first land mount |
| II A Wider World | Twilight Forest, Undergarden, Nether | Naga, Lich, Hydra, Ur-Ghast, Netherite Monstrosity, Forgotten Guardian | Rare-Epic | 15-35 | school specialisation | fantasy land mounts, grapple, sea mounts/ships |
| III Beyond the Veil | Aether line, Blue Skies, Alex's Caves | Slider, Valkyrie Queen, Sun Spirit, Ignis | Epic-Legendary | 30-50 | advanced spells, summoning | **first flight** (constrained, see TRAVERSAL.md) |
| IV Fallen Kingdoms | Deeper and Darker, mega-dungeons | Harbinger, Leviathan, Ancient Remnant, dragons, necromancers | Legendary | 45-65 | spellbook upgrades | dragons (egg + boss gate), long-range recall |
| V End of the Age | End (Nullscape) | Ender Dragon (reworked), Ender Guardian | Legendary-Ancient | 60-75 | endgame spells | wings/Elytra (End-gated) |
| Postgame | Gateways, secret realms | Maledictus, Scylla, superbosses | Ancient + Unique | 75+ | all | legendary mount line |

Rules: no tier-skipping via chests (see LOOT.md); portals to later realms are gated (Restricted Portals + quest dependencies); the skill tree budget (~110 points by level 75 + quest points) is deliberately smaller than the tree so builds specialise.

## Realm gating: Ember Shards and Warden Sigils (`tools/build_sigils.py`, source `design/custom_items.py`)
Each realm's portal is sealed per player by Restricted Portals until that player **crafts** the realm's Sigil (an advancement is granted; the portal then works for them forever). Sigils are shapeless recipes around **Ember Shards**.

| Sigil | Unseals | Recipe | Act |
|---|---|---|---|
| Sigil of Flame | Nether | 1 shard, flint and steel, 2 obsidian | II |
| Sigil of Root | Twilight Forest | 1 shard, diamond, any sapling, moss block | II |
| Sigil of Stone | Undergarden | 1 shard, iron block, cobbled deepslate, glow berries | II |
| Sigil of Sky | Aether | 2 shards, glowstone, feather, Naga scale | III |
| Sigil of Dream | Everbright + Everdawn | 2 shards, amethyst shard, diamond, blaze rod | III |
| Sigil of Echo | Otherside | 3 shards, echo shard, sculk catalyst | IV |
| Sigil of the End | End | 4 shards, eye of ender, nether star | V |

**Shard income:** Act I finale 3, Act II finale 4, Act III finale 3, Act IV finale 4 (14, one short of all 15 by design), plus boss kills (t2-t3 50 %, t4-t5 one, t6 one or two). The Naga scale, blaze rod, echo shard and nether star tie each Sigil to the previous act's content. The Doors chapter has a quest per Sigil, and each realm quest depends on its Sigil.
