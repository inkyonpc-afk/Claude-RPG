"""Build the Aldreth weapon taxonomy item tags from the registry snapshot.

Output datapack: config/paxi/datapacks/aldreth_core/data/aldreth/tags/items/weapons/<class>.json (+ weapons/melee, weapons/ranged, weapons/magic).
Also writes docs/WEAPON_CLASSES.md (counts and samples). Usage: python tools/build_tags.py [--registry pack/registries_snapshot.json]
Rules are ordered: the first matching rule wins, so specific classes (greatsword) precede generic ones (sword).
"""
import json, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
reg = sys.argv[sys.argv.index("--registry") + 1] if "--registry" in sys.argv else os.path.join(ROOT, "pack", "registries_snapshot.json")
items = json.load(open(reg, encoding="utf-8"))["item"]

NOT_WEAPON = re.compile(r"(_part|_head|_handle|_pole|_tip|_hilt|_guard|_grip|_binding|_template|_pommel|_blade_part|_spawn_egg|_smithing|_upgrade|_pattern|_mold|_cast|_fragment|_shard|_scrap|_stick$|_icon|_display|_model|_recipe|painting|_pod$|flask|cannon|_tome$|boots_tome|_spawn)")
NOT_NS = re.compile(r"^(minecraft:(wooden|stone|golden|iron|diamond|netherite)_(pickaxe|shovel|hoe)|.*delight.*|farmersdelight|.*:.*_pickaxe|.*:.*_shovel|.*:.*_hoe)$")

# (class, regex on path, kind)
RULES = [
    ("shield",     r"(^|_)(shield|buckler|pavise|kite_shield|heater|tower_shield|ecu)(_|$)", "defense"),
    ("crossbow",   r"crossbow|arbalest|repeater|ballista", "ranged"),
    ("bow",        r"(^|_)(bow|longbow|shortbow|recurve|composite_bow|compound_bow|warbow)(_|$)", "ranged"),
    ("spellbook",  r"spell_?book|grimoire|codex", "magic"),
    ("wand",       r"(^|_)(wand|focus|orb)(_|$)", "magic"),
    ("quarterstaff", r"heavy_staff|quarterstaff|bo_staff|electrostaff|battle_staff|combat_staff", "melee"),
    ("staff",      r"(^|_)(staff|stave|scepter|sceptre|caduceus|crook)(_|$)|spellbook_staff", "magic"),
    ("scythe",     r"scythe|sickle|reaper|harvester", "melee"),
    ("twinblade",  r"twinblade|twin_blade|dual_blade|double_blade|double_sword|lightsaber_double|double_lightsaber", "melee"),
    ("greataxe",   r"greataxe|great_axe|battle_axe|battleaxe|double_axe|executioner|labrys", "melee"),
    ("hammer",     r"hammer|maul|mallet|sledge|warhammer|gavel", "melee"),
    ("mace",       r"(^|_)(mace|flail|morning_star|morningstar|club|cudgel|bludgeon|bat)(_|$)", "melee"),
    ("polearm",    r"halberd|glaive|naginata|poleaxe|guisarme|bardiche|voulge|bec_de_corbin|partisan|ranseur|fauchard|pike", "melee"),
    ("spear",      r"spear|lance|javelin|trident|harpoon|pilum|shortspear", "melee"),
    ("greatsword", r"greatsword|great_sword|claymore|zweihander|flamberge|buster|bastard|two_handed|executioner_sword|nodachi|odachi|tyrfing|grosse|longsword_great|massive", "melee"),
    ("katana",     r"katana|tachi|wakizashi|ninjato|kodachi|uchigatana", "melee"),
    ("rapier",     r"rapier|estoc|foil|sabre|saber|cutlass|scimitar|falchion|sabre|shamshir|khopesh|kopis|spatha", "melee"),
    ("dagger",     r"(^|_)(dagger|knife|dirk|stiletto|kris|kunai|sai|poniard|misericorde|rondel|cinquedea|tanto|shiv|stinger|claw|katar|fang)(_|$)", "melee"),
    ("whip",       r"(^|_)(whip|chakram|bola)(_|$)", "melee"),
    ("longsword",  r"(^|_)(sword|longsword|broadsword|arming_sword|blade|saber)(_|$)|longsword|broadsword|arming|gladius|sword$", "melee"),
    ("axe",        r"(^|_)(axe|hatchet|tomahawk|cleaver)(_|$)|_axe$", "melee"),
]
tags = {r[0]: [] for r in RULES}
kinds = {r[0]: r[2] for r in RULES}
for it in sorted(items):
    ns, path = it.split(":", 1)
    if NOT_WEAPON.search(path) or NOT_NS.match(it):
        continue
    if ns in ("chipped", "minecraft") and not path.endswith(("sword", "axe", "bow", "crossbow", "trident", "shield")):
        continue
    if ns in ("quark", "supplementaries", "create", "cluttered", "valhelsia_furniture", "mcwfurnitures", "mcwroofs", "stoneworks", "refurbished_furniture", "botania"):
        continue
    for cls, rx, _ in RULES:
        if re.search(rx, path):
            if cls == "axe" and ns == "minecraft" and "pickaxe" in path:
                break
            tags[cls].append(it)
            break

out_dir = os.path.join(ROOT, "config", "paxi", "datapacks", "aldreth_core")
tag_dir = os.path.join(out_dir, "data", "aldreth", "tags", "items", "weapons")
os.makedirs(tag_dir, exist_ok=True)
json.dump({"pack": {"pack_format": 15, "description": "Embers of Aldreth core data (weapon taxonomy tags, skill tree, races, loot)"}},
          open(os.path.join(out_dir, "pack.mcmeta"), "w"), indent=2)


def write(name, values):
    json.dump({"replace": True, "values": sorted(set(values))}, open(os.path.join(tag_dir, name + ".json"), "w"), indent=1)


for cls, vals in tags.items():
    write(cls, vals)
groups = {"melee": [c for c in tags if kinds[c] == "melee"], "ranged": [c for c in tags if kinds[c] == "ranged"], "magic": [c for c in tags if kinds[c] == "magic"]}
for g, cl in groups.items():
    json.dump({"replace": True, "values": ["#aldreth:weapons/" + c for c in cl]}, open(os.path.join(tag_dir, g + ".json"), "w"), indent=1)
# two-handed / heavy and light sets for conditions
heavy = ["greatsword", "greataxe", "hammer", "polearm", "scythe", "twinblade"]
light = ["dagger", "rapier", "katana", "whip"]
for nm, cl in (("heavy", heavy), ("light", light), ("onehand", ["longsword", "axe", "mace", "spear", "rapier", "katana", "dagger"])):
    json.dump({"replace": True, "values": ["#aldreth:weapons/" + c for c in cl]}, open(os.path.join(tag_dir, nm + ".json"), "w"), indent=1)

lines = ["# Weapon classes", "", "_Generated by `tools/build_tags.py` from the registry snapshot. Tags: `aldreth:weapons/<class>`, plus groups `melee`, `ranged`, `magic`, `heavy`, `light`, `onehand`._", "",
         "| Class | Items | Kind | Examples |", "|---|---|---|---|"]
for cls, vals in tags.items():
    lines.append("| %s | %d | %s | %s |" % (cls, len(vals), kinds[cls], ", ".join(sorted(set(vals))[:4])))
open(os.path.join(ROOT, "docs", "WEAPON_CLASSES.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print({c: len(v) for c, v in tags.items()})
