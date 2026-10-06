# Traversal, Mounts and Flight

Principle: exploration is fun before and after flight. Every method keeps a niche.

| Stage | Methods | Source |
|---|---|---|
| Early | sprint, Combat Roll, vanilla horse, boats, first Waystones | base + Waystones |
| Early-mid | Paraglider (glide), better climbing, ladders, tamed fast land mounts, carts | Paragliders, Better Climbing, AstikorCarts, Alex's Mobs/Caves tameables, Horseman, Crazy Chocobos |
| Mid | grapple (ReHooked), sea travel (Small Ships, Ice and Fire hippocampus), Iron's mobility spells, Via Romana roads | |
| Mid-late | **first flight**: hippogryph / Aether flyers / Alex's Caves flyer; Wyrmroost dragons | IaF CE, Aether, Alex's Caves, Wyrmroost |
| Late | Ice and Fire dragons (egg + boss kill + stage 3 for riding), long-range recall scrolls | IaF CE |
| End | Elytra/wings (Icarus, Elytra Slot) gated to End progression via KubeJS | |
| Post | legendary mount questline | quests |

Flight guardrails (implemented in KubeJS `server_scripts/traversal_flight_guard.js`, Phase 6):
- Flight-capable mounts and wings are blocked inside `#aldreth:no_flight` structures (boss arenas, mega-dungeon interiors): rider is dismounted with a lore message.
- Aether flyers function only in the Aether; hippogryphs fly slowly; dragon riding needs dragon stage >= 3.
- Elytra/wing items need End-tier materials.
- Per-mount design variety (speed, stamina, inventory, armor, terrain strength) is documented per mount in this file as mounts are verified in-game (Phase 6).

Status: design only; mounts verified in-client during Phase 6.
