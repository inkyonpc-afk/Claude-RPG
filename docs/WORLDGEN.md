# Worldgen

## Terrain stack (one terrain generator, no conflicts)
**Tectonic + Terralith** (via TerraBlender/Lithostitched) plus Oh The Biomes We've Gone and Oh The Trees You'll Grow; Alex's Caves for deep cave biomes; Underground Rivers; Vanilla Backport content; Nether: Incendium, Nether Depths Upgrade, Gardens of the Dead, Bygone Nether, Formations Nether; End: Nullscape, End Remastered, YUNG's End Island, MES (Moog's End Structures). Rejected: BetterEnd/BetterNether (Fabric-only), second terrain generators (Biomes O' Plenty, Regions Unexplored kept as test-status only), Every Compat (registry mismatches).

## Dimensions (all load; portal order enforced by quests + Restricted Portals in Phase 7)
Twilight Forest, Undergarden, Aether (+Deep Aether, Aether Redux, Lost Content, Ancient Aether), Blue Skies (Everbright, Everdawn), Deeper and Darker (Otherside), Iron's Spells pocket dimension, Nether, End.

## Structures (about 1,600 registered; tiers)
| Tier | Examples | Intended loot |
|---|---|---|
| Common | camps, small ruins, minor caves, mineshafts, villages | supplies, common gear |
| Uncommon | towers, forts, village variants, Dungeons Arise towers | uncommon gear, gems |
| Rare | dungeons, castles, large temples (Dungeons Enhanced, Prodigium, Better Strongholds) | rare/epic gear |
| Very rare | mega-dungeons, boss fortresses (Keep Kayra, Black Citadel, Cataclysm arenas) | epic/mythic, boss gear |

Spacing is tuned with **Structurify** (per-structure spacing/separation/frequency) and Structure Essentials / Sparse Structures Reforged; goal: adventure without every structure spawning in sight of another. Known: `Non-unique structure_set salt:0` warning from Structure Essentials (cosmetic).

## Performance note
Registry size: ~31k items, ~22k blocks (decor mods dominate). Startup: ~150 s to world on a Ryzen 9 5900X. See PERFORMANCE.md.

## Known issues
Prodigium Dungeons ships 2 empty structure files (blocked by `aldreth_fixes` datapack). Structure-tag/loot-table references to removed mods log harmless "Load My Tags" errors.
