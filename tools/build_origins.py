"""Generate the Aldreth races (Origins/Apoli datapack) into config/paxi/datapacks/aldreth_core and docs/RACES.md.

Eight peoples, each with a small identity bonus and a real drawback; no class lock (classes come from the skill tree).
The default Origins list is replaced (no Elytrian/Phantom: their built-in flight would bypass the flight-progression design).
Usage: python tools/build_origins.py
"""
import json, os, shutil

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
pack = os.path.join(ROOT, "config", "paxi", "datapacks", "aldreth_core", "data")
reg = json.load(open(os.path.join(ROOT, "pack", "registries_snapshot.json"), encoding="utf-8"))
ATTR = set(reg["attribute"])
ADD, MB = "addition", "multiply_base"

RACES = [
    dict(key="human", name="Emberborn Human", impact=0, icon="minecraft:player_head",
         blurb="Adaptable and driven: the Ember burns brightest in those who never settle.",
         powers=[("Adaptable", "You learn faster than the other peoples (+10% experience).", [("attributeslib:experience_gained", MB, 0.10)]),
                 ("Fortunate Birth", "A little luck follows the Emberborn.", [("minecraft:generic.luck", ADD, 1.0)])]),
    dict(key="elf", name="Sylvan Elf", impact=1, icon="minecraft:bow",
         blurb="Forest-keepers of old Aldreth: swift, keen and slight of frame.",
         powers=[("Keen Senses", "+4% dodge chance and +10% bow draw speed.", [("attributeslib:dodge_chance", ADD, 0.04), ("attributeslib:draw_speed", MB, 0.10)]),
                 ("Wildspeaker", "+5% nature spell power.", [("irons_spellbooks:nature_spell_power", MB, 0.05)]),
                 ("Slender Frame", "-2 maximum health.", [("minecraft:generic.max_health", ADD, -2.0)])]),
    dict(key="dwarf", name="Stoneborn Dwarf", impact=2, icon="minecraft:iron_pickaxe",
         blurb="Delvers under the Hollow Crown's mountains: sturdy, stubborn and tireless miners.",
         powers=[("Stoneskin", "+2 armor and +10% knockback resistance.", [("minecraft:generic.armor", ADD, 2.0), ("minecraft:generic.knockback_resistance", ADD, 0.10)]),
                 ("Master Delver", "+15% mining speed.", [("attributeslib:mining_speed", MB, 0.15)]),
                 ("Short Stride", "-6% movement speed.", [("minecraft:generic.movement_speed", MB, -0.06)])]),
    dict(key="orc", name="Ashen Orc", impact=2, icon="minecraft:iron_axe",
         blurb="Hardened by the ashlands: strong, hardy and impatient with spellcraft.",
         powers=[("Ashen Might", "+2 attack damage and +4 maximum health.", [("minecraft:generic.attack_damage", ADD, 2.0), ("minecraft:generic.max_health", ADD, 4.0)]),
                 ("Thick Skull", "+5% knockback resistance.", [("minecraft:generic.knockback_resistance", ADD, 0.05)]),
                 ("Dull to Magic", "-10% spell power.", [("irons_spellbooks:spell_power", MB, -0.10)])]),
    dict(key="halfling", name="Hearthfolk Halfling", impact=1, icon="minecraft:bread",
         blurb="Small, quick and unreasonably lucky: they find fortune where others find trouble.",
         powers=[("Lucky Foot", "+2 luck.", [("minecraft:generic.luck", ADD, 2.0)]),
                 ("Nimble", "+3% dodge chance.", [("attributeslib:dodge_chance", ADD, 0.03)]),
                 ("Small Frame", "-4 maximum health.", [("minecraft:generic.max_health", ADD, -4.0)])]),
    dict(key="hexblood", name="Hexblood", impact=2, icon="minecraft:blaze_powder",
         blurb="Descendants of a banished coven: fire in the veins, holy light a burn.",
         powers=[("Infernal Gift", "+10% fire spell power and +15% fire magic resistance.", [("irons_spellbooks:fire_spell_power", MB, 0.10), ("irons_spellbooks:fire_magic_resist", MB, 0.15)]),
                 ("Cursed Line", "-15% holy magic resistance.", [("irons_spellbooks:holy_magic_resist", MB, -0.15)]),
                 ("Frail Plating", "-1 armor.", [("minecraft:generic.armor", ADD, -1.0)])]),
    dict(key="scaleborn", name="Scaleborn", impact=3, icon="minecraft:dragon_breath",
         blurb="Thin-blooded kin of the old dragons: armored, proud and heavy.",
         powers=[("Scaled Hide", "+3 armor and +2 armor toughness.", [("minecraft:generic.armor", ADD, 3.0), ("minecraft:generic.armor_toughness", ADD, 2.0)]),
                 ("Draconic Blood", "+20% fire magic resistance and +5% fire spell power.", [("irons_spellbooks:fire_magic_resist", MB, 0.20), ("irons_spellbooks:fire_spell_power", MB, 0.05)]),
                 ("Heavy Frame", "-8% movement speed and -20% swim speed.", [("minecraft:generic.movement_speed", MB, -0.08), ("forge:swim_speed", MB, -0.20)])]),
    dict(key="wisp", name="Wisp-touched", impact=1, icon="minecraft:amethyst_shard",
         blurb="Spirit-kissed wanderers, half in the world and half in the Veil.",
         powers=[("Veilborn Mind", "+25 maximum mana and +8% mana regeneration.", [("irons_spellbooks:max_mana", ADD, 25.0), ("irons_spellbooks:mana_regen", MB, 0.08)]),
                 ("Flicker", "+3% dodge chance.", [("attributeslib:dodge_chance", ADD, 0.03)]),
                 ("Insubstantial", "-2 armor.", [("minecraft:generic.armor", ADD, -2.0)])]),
]

for d in ("origins", "powers"):
    p = os.path.join(pack, "aldreth", d)
    shutil.rmtree(p, ignore_errors=True)
    os.makedirs(p)
errors = []
docs = ["# Races", "", "_Generated by `tools/build_origins.py`. Each people has a small identity bonus and a real drawback; there is no class lock (see SKILL_TREE.md). Flight-granting default origins (Elytrian, Phantom, Avian) are removed on purpose._", ""]
for i, r in enumerate(RACES):
    pids = []
    docs += ["## %s" % r["name"], "", "_%s_" % r["blurb"], ""]
    for j, (pname, pdesc, mods) in enumerate(r["powers"]):
        pid = "%s_%d" % (r["key"], j)
        mlist = []
        for attr, op, val in mods:
            if attr not in ATTR:
                errors.append("%s: unknown attribute %s" % (pid, attr))
            mlist.append({"attribute": attr, "name": "%s: %s" % (r["name"], pname), "operation": op, "value": val})
        pj = {"type": "apoli:multiple" if False else "apoli:attribute", "name": pname, "description": pdesc}
        if len(mlist) == 1:
            pj["modifier"] = mlist[0]
        else:
            pj["modifiers"] = mlist
        json.dump(pj, open(os.path.join(pack, "aldreth", "powers", pid + ".json"), "w", encoding="utf-8"), indent=1)
        pids.append("aldreth:" + pid)
        docs.append("- **%s**: %s" % (pname, pdesc))
    oj = {"icon": {"item": r["icon"]}, "order": i, "impact": r["impact"], "name": r["name"], "description": r["blurb"], "powers": pids}
    json.dump(oj, open(os.path.join(pack, "aldreth", "origins", r["key"] + ".json"), "w", encoding="utf-8"), indent=1)
    docs.append("")
layer = {"replace": True, "order": 0, "enabled": True, "origins": ["aldreth:" + r["key"] for r in RACES], "allow_random": True,
         "exclude_random": ["aldreth:human"], "allow_random_unchoosable": False, "hidden": False}
os.makedirs(os.path.join(pack, "origins", "origin_layers"), exist_ok=True)
json.dump(layer, open(os.path.join(pack, "origins", "origin_layers", "origin.json"), "w"), indent=1)
open(os.path.join(ROOT, "docs", "RACES.md"), "w", encoding="utf-8").write("\n".join(docs) + "\n")
print("races:", len(RACES), "errors:", errors)
