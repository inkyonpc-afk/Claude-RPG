"""Generate Aldreth loot tables (quest caches t1..t6, boss tables t1..t6), the boss-reward KubeJS hook and docs/LOOT.md. Validates item ids against the registry snapshot.
Output: config/paxi/datapacks/aldreth_core/data/aldreth/loot_tables/quest/t<N>.json
Usage: python tools/build_loot.py"""
import json, os

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
reg = json.load(open(os.path.join(ROOT, "pack", "registries_snapshot.json"), encoding="utf-8"))
import sys
sys.path.insert(0, os.path.join(ROOT, "design"))
import custom_items  # noqa: E402
ITEMS = set(reg["item"]) | set(custom_items.ITEMS)
out = os.path.join(ROOT, "config", "paxi", "datapacks", "aldreth_core", "data", "aldreth", "loot_tables", "quest")
os.makedirs(out, exist_ok=True)
errors = []


def it(item, lo=1, hi=1, weight=10):
    if item not in ITEMS:
        errors.append("unknown item " + item)
    e = {"type": "minecraft:item", "name": item, "weight": weight}
    if (lo, hi) != (1, 1):
        e["functions"] = [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": lo, "max": hi}}]
    return e


def affix(rarity, weight=10):
    return {"type": "apotheosis:random_affix_item", "weight": weight, "quality": 0, "rarity": rarity}


def gem(weight=10):
    return {"type": "apotheosis:random_gem", "weight": weight, "quality": 0}


def pool(rolls, entries, name):
    return {"name": name, "rolls": rolls if isinstance(rolls, dict) else {"min": rolls, "max": rolls, "type": "minecraft:uniform"}, "entries": entries}


def uniform(a, b):
    return {"min": a, "max": b, "type": "minecraft:uniform"}


T = {}
# supplies: cheap, always useful
SUP = [it("minecraft:bread", 4, 8), it("minecraft:cooked_beef", 3, 6), it("minecraft:torch", 8, 16), it("minecraft:arrow", 16, 32), it("minecraft:iron_nugget", 6, 14),
       it("minecraft:golden_carrot", 2, 5), it("minecraft:experience_bottle", 1, 3)]
MATS = {1: "apotheosis:common_material", 2: "apotheosis:uncommon_material", 3: "apotheosis:rare_material", 4: "apotheosis:epic_material", 5: "apotheosis:mythic_material", 6: "apotheosis:ancient_material"}
T[1] = [pool(uniform(3, 4), SUP, "supplies"), pool(1, [affix("common", 70), affix("uncommon", 30)], "gear"), pool(uniform(1, 2), [it(MATS[1], 2, 5, 70), it("apotheosis:gem_dust", 2, 5, 30)], "materials")]
T[2] = [pool(uniform(3, 4), SUP, "supplies"), pool(1, [affix("uncommon", 70), affix("rare", 30)], "gear"), pool(uniform(1, 2), [it(MATS[2], 2, 5, 60), it(MATS[1], 3, 8, 40)], "materials"), pool(uniform(0, 1), [gem(1)], "gem")]
T[3] = [pool(uniform(2, 3), SUP, "supplies"), pool(1, [affix("rare", 80), affix("epic", 20)], "gear"), pool(uniform(1, 2), [it(MATS[3], 2, 5, 60), it(MATS[2], 3, 8, 40)], "materials"), pool(1, [gem(1)], "gem")]
T[4] = [pool(uniform(2, 3), SUP, "supplies"), pool(1, [affix("rare", 40), affix("epic", 60)], "gear"), pool(uniform(1, 2), [it(MATS[4], 2, 4, 60), it(MATS[3], 3, 6, 40)], "materials"), pool(uniform(1, 2), [gem(1)], "gem")]
T[5] = [pool(uniform(2, 3), SUP, "supplies"), pool(1, [affix("epic", 55), affix("mythic", 45)], "gear"), pool(uniform(1, 2), [it(MATS[5], 2, 4, 60), it(MATS[4], 3, 6, 40)], "materials"), pool(uniform(1, 2), [gem(1)], "gem")]
T[6] = [pool(uniform(2, 3), SUP, "supplies"), pool(1, [affix("mythic", 75), affix("ancient", 25)], "gear"), pool(uniform(1, 2), [it(MATS[6], 1, 3, 40), it(MATS[5], 3, 6, 60)], "materials"), pool(uniform(1, 3), [gem(1)], "gem")]
for n, pools in T.items():
    json.dump({"type": "minecraft:chest", "pools": pools}, open(os.path.join(out, "t%d.json" % n), "w"), indent=1)

# boss tables: rolled on every boss kill (the quest cache pays the first kill). Gear of the act's band, materials, a gem chance; no supplies.
GEAR = {1: [affix("common", 50), affix("uncommon", 50)], 2: [affix("uncommon", 60), affix("rare", 40)], 3: [affix("rare", 75), affix("epic", 25)],
        4: [affix("rare", 30), affix("epic", 70)], 5: [affix("epic", 50), affix("mythic", 50)], 6: [affix("mythic", 70), affix("ancient", 30)]}
bout = os.path.join(os.path.dirname(out), "boss")
os.makedirs(bout, exist_ok=True)
for n in range(1, 7):
    shards = {1: (0, 0), 2: (0, 1), 3: (0, 1), 4: (1, 1), 5: (1, 1), 6: (1, 2)}[n]
    pools = [pool(1, GEAR[n], "gear"), pool(uniform(1, 2), [it(MATS[n], 2, 4, 70), it(MATS[max(1, n - 1)], 3, 6, 30)], "materials"),
             pool(uniform(0, 1) if n < 4 else 1, [gem(1)], "gem")]
    if shards[1]:
        pools.append(pool(uniform(*shards), [it(custom_items.EMBER_SHARD)], "ember_shards"))
    json.dump({"type": "minecraft:chest", "pools": pools}, open(os.path.join(bout, "t%d.json" % n), "w"), indent=1)

# boss-reward hook
import sys
sys.path.insert(0, os.path.join(ROOT, "design"))
from bosses import BOSSES, KILL_CHANCE  # noqa: E402
ENT = set(reg["entity_type"])
tiers = {}
for key, name, icon, ent, xpv, tier in BOSSES:
    if ent not in ENT:
        errors.append("unknown boss entity " + ent)
    tiers[ent] = tier
js = """// Embers of Aldreth: boss rewards (generated by tools/build_loot.py from design/bosses.py; edit those, not this file).
// Every boss kill rolls aldreth:boss/t<tier> at the corpse, on top of the boss's own unique drops. Credit: the killer is a player, or a player
// is within 48 blocks (summoners and pet builds count). The Ender Dragon's table lands on the exit fountain.
const ALD_BOSS_TIER = %s
const ALD_BOSS_CHANCE = %s

EntityEvents.death(event => {
  const e = event.entity
  const id = String(e.type)
  const tier = ALD_BOSS_TIER[id]
  if (!tier || e.level.isClientSide()) return
  const near = event.source.player || e.level.getNearestPlayer(e.x, e.y, e.z, 48, false)
  if (!near) return
  const chance = ALD_BOSS_CHANCE[id]
  if (chance && Math.random() > chance) return
  const dim = String(e.level.dimension)
  const pos = id == 'minecraft:ender_dragon' ? '0 80 0' : Math.floor(e.x) + ' ' + Math.floor(e.y + 1) + ' ' + Math.floor(e.z)
  event.server.runCommandSilent('execute in ' + dim + ' run loot spawn ' + pos + ' loot aldreth:boss/t' + tier)
})
""" % (json.dumps(tiers, indent=1), json.dumps(KILL_CHANCE))
open(os.path.join(ROOT, "kubejs", "server_scripts", "boss_rewards.js"), "w", encoding="utf-8").write(js)

doc = ["# Loot", "", "_Generated in part by `tools/build_loot.py`._", "",
       "## Principle", "Difficulty and rewards correlate: tiny ruin -> supplies; small dungeon -> uncommon gear; large dungeon -> rare/epic; mega-dungeon -> epic/legendary; boss -> unique equipment and materials; late boss -> mythic/ancient. A house five minutes from spawn never gives endgame gear.", "",
       "## Rarity ladder (Apotheosis)", "Common, Uncommon, Rare, Epic, Mythic (shown as Legendary), Ancient. **Unique** items (boss weapons, relics) are fixed, hand-authored drops.", "",
       "## Quest caches", "Quest rewards call `loot give {p} loot aldreth:quest/t<N>`:", "", "| Tier | Gear rarity | Materials | Gems |", "|---|---|---|---|",
       "| t1 | common/uncommon | common | none |", "| t2 | uncommon/rare | uncommon | 0-1 |", "| t3 | rare/epic | rare | 1 |", "| t4 | rare/epic | epic | 1-2 |", "| t5 | epic/mythic | mythic | 1-2 |", "| t6 | mythic/ancient | ancient/mythic | 1-3 |", "",
       "## Boss tables", "Every boss kill (39 bosses in `design/bosses.py`) rolls `aldreth:boss/t<tier>` at the corpse through `kubejs/server_scripts/boss_rewards.js`, on top of the boss's own unique drops: one affix item of the act's band (t2 uncommon/rare ... t6 mythic/ancient), 1-2 material stacks, and a gem (guaranteed from t4) and Ember Shards (t2-t3 50 %, t4-t5 one, t6 one or two: a backup source for the realm Sigils). The quest cache pays the first kill; the boss table pays every kill, so bosses stay worth farming. Multi-entity fights (Phantom Knights) roll once on average.", "",
       "## World loot (Apotheosis config, `config/apotheosis/adventure.cfg`)", "See the Apotheosis tuning section: affix conversion chances per loot table tier, dimension rarity bands (overworld common-rare, Nether uncommon-epic, End rare-mythic, plus Aether/Blue Skies/Undergarden/Otherside bands), and gem rules.", ""]
open(os.path.join(ROOT, "docs", "LOOT.md"), "w", encoding="utf-8").write("\n".join(doc))
print("loot tiers:", len(T), "errors:", errors)
