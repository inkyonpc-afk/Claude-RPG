# Traversal, Mounts and Flight

Principle: **exploration is fun before and after flight.** Every method keeps a niche, flight is the last thing earned and the most fenced, and no method makes all earlier ones obsolete.

## Progression ladder (act-gated)
| Act | Unlocks | Source |
|---|---|---|
| Prologue | sprint, **Combat Roll**, vanilla horse, boats, first Waystone | base, Combat Roll, Waystones |
| I | **Paraglider** (stamina glide), better climbing, **ReHooked** wood/iron hooks, Cloud in a Bottle (double jump), AstikorCarts | quests, Artifacts |
| II | **Chocobo** (fast, jumpy land mount), tusklin/elephant (lasso), crystal camel, Small Ships (sea), grapple tiers, Blink glyph | Chocobos, Alex's Mobs, Blue Skies, Small Ships, Ars Nouveau |
| III | **First flight, confined:** Aether phyg/flying cow/Aerwhale (Aether only), Moa, **Hippogryph** (overworld, slow), Subterranodon (caves), Straddleboard | Aether, Deep Aether, Ice and Fire CE, Alex's Caves |
| IV | **Dragons** (egg -> stage 3 to ride), Wyrmroost wyverns/drakes, Waystone portstones, recall | Ice and Fire CE, Wyrmroost, Waystones |
| V | **Elytra** (End city), **Icarus wings** (End materials), final dragon tier | End |
| Post | legendary mount line (dragon stage 5, rare drakes), global waystone network | quests |

## Mounts (verified in the entity registry)
- **Land:** horse/donkey/mule/llama (vanilla); `chocobos:chocobo` (+barding); Alex's Mobs elephant/tusklin/bison/kangaroo/emu/komodo (vine lasso + saddles); Blue Skies crystal camel; Alex's Caves vallumraptor/tremorsaurus; Unusual Prehistory rex; Born in Chaos Felsteed.
- **Aquatic:** Small Ships (cogs, galleys, brigs, drakkars), Straddleboard (water/ice), Upgrade Aquatic fauna.
- **Flying:** Aether phyg/flying cow/aerwhale/moa; `iceandfire:hippogryph`, `amphithere`, fire/ice/lightning dragons; Wyrmroost canari wyvern, royal red, overworld drake, silver glider; Alex's Caves subterranodon.
- **Gear:** horse/chocobo armor, dragon armor, saddles are dungeon loot; Waystones Teleport Pets keeps tamed mounts with you.

## Flight guardrails (Phase 6 implementation: KubeJS `server_scripts/traversal_flight_guard.js`)
1. Entity tag `#aldreth:flying_mounts` (hippogryph, amphithere, dragons, wyverns, subterranodon, aerwhale/aether flyers) and flight items (elytra, Icarus wings) are blocked inside structure tag `#aldreth:no_flight` (boss arenas, mega-dungeon interiors, Warden cities, Cataclysm arenas): rider is dismounted with a lore message every 20 ticks check.
2. Aether flyers only fly in the Aether (dimension check); hippogryph speed/stamina reduced in config; dragon riding needs stage >= 3.
3. Elytra and Icarus wings are End-gated: crafting recipes removed except through End materials; early-game Icarus loot tables stripped.
4. Enigmatic Legacy / Artifacts / Relics items that grant flight or free teleport are audited and gated (Phase 17).
5. Multiplayer: mount state and dismount logic are server-side; verified with a dedicated server + client join test.

## Traversal variety (why you keep using the old ways)
Roads and forests favour land mounts; rivers and oceans favour ships and the Straddleboard; dungeons favour grapples, climbing and the double jump; known places favour Waystones; emergencies favour recall and Blink; the sky favours hippogryphs and dragons, but not inside fenced places.

## Status
Quests for the whole ladder are written (`The Many Roads`, `The Stable`, `The Sky Is a Reward`). The anti-flight script, per-mount stat tuning and multiplayer mount tests are Phase 6 work items tracked in KNOWN_ISSUES.md.
