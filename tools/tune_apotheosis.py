"""Patch config/apotheosis/adventure.cfg: tier affix/gem loot by structure size and container type, set dimension rarity bands, boss spawn dims.
Rules are ordered most specific first. Usage: python tools/tune_apotheosis.py"""
import os, re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
P = os.path.join(ROOT, "config", "apotheosis", "adventure.cfg")
s = open(P, encoding="utf-8").read()

UTILITY = r".*(barrel|food|supply|kitchen|clutter|crate|pantry|trash|bedroom|quarters|storage|gummies|disc|cape|fish|seed|farm|compost|laundry|bath).*"
BOSSY = r".*(treasure|reward|vault|boss|arena|secret|special|apex|armory|key).*"
GREAT = [("dungeons_enhanced", r"chests/(castle|black_citadel|deep_crypt|large_dungeon|monster_maze|tower_of_the_undead|witch_tower)/.*"),
         ("dungeons_arise", r"chests/(keep_kayra|shiraz_palace|coliseum|typhon|heavenly_[a-z]+|illager_fort|monastery|plague_asylum|thornborn_towers|mechanical_nest|foundry)/.*"),
         ("aether", r"chests/dungeon/.*"), ("ancient_aether", r".*dungeon.*"),
         ("twilightforest", r"chests/(labyrinth.*|aurora.*|darktower.*|hill_3|stronghold.*|lich.*|hydra.*|troll.*|tower.*)"),
         ("goety", r"chests/(dark_manor.*|assembly.*|crypt.*|blacksmith.*|final.*|keep.*)"), ("irons_spellbooks", r"chests/catacombs/.*"), ("cataclysm", r"chests/.*"),
         ("blue_skies", r"chests/(blinding_dungeon|nature_dungeon|poison_dungeon|bunker)/.*"), ("deeperdarker", r"chests/ancient_temple.*"), ("prodigium_dungeons", r".*"),
         ("minecraft", r"chests/(stronghold.*|woodland_mansion|end_city.*|bastion.*|ancient_city.*|nether_bridge)")]
MEDIUM = [("dungeons_arise", r"chests/.*"), ("dungeons_enhanced", r"chests/.*"), ("dungeons_plus", r"chests/.*"), ("dungeons_arise_seven_seas", r"chests/.*"), ("betterdungeons", r".*"),
          ("dungeoncrawl", r"chests/.*"), ("repurposed_structures", r"chests/(dungeons|temples|fortresses|mansions|outposts|strongholds|ruined_portals|ancient_cities|bastions|cities)/.*"),
          ("twilightforest", r"chests/.*"), ("goety", r"chests/.*"), ("irons_spellbooks", r"chests/.*"), ("ati_structures", r"chests/.*"), ("mns", r".*"), ("mvs", r".*"),
          ("mss", r".*"), ("mes", r".*"), ("minecraft", r"chests/(abandoned_mineshaft|desert_pyramid|jungle_temple|simple_dungeon|underwater_ruin.*|shipwreck.*|pillager_outpost|ruined_portal)")]


def tier(rules, chance):
    return ["%s:%s|%s" % (d, rx, chance) for d, rx in rules]


item_rules = [UTILITY + "|0.0", "minecraft:chests/(village|igloo|buried_treasure|spawn_bonus_chest).*|0.04", BOSSY + "|0.85"] + tier(GREAT, 0.55) + tier(MEDIUM, 0.26) + [".*chests.*|0.10"]
convert_rules = [".*blocks.*|0", UTILITY + "|0.0", BOSSY + "|0.6"] + tier(GREAT, 0.45) + tier(MEDIUM, 0.25) + [".*|0.12"]
gem_rules = [UTILITY + "|0.0", BOSSY + "|0.50"] + tier(GREAT, 0.38) + tier(MEDIUM, 0.18) + [".*chests.*|0.06"]
convert_rar = ["overworld|common|rare", "the_nether|uncommon|epic", "the_end|rare|mythic", "twilightforest:twilight_forest|uncommon|epic", "undergarden:undergarden|uncommon|epic",
               "aether:the_aether|rare|epic", "blue_skies:everbright|rare|mythic", "blue_skies:everdawn|rare|mythic", "deeperdarker:otherside|epic|mythic"]
gem_rar = ["overworld|common|epic", "the_nether|uncommon|mythic", "the_end|rare|mythic", "twilightforest:twilight_forest|uncommon|mythic", "undergarden:undergarden|uncommon|mythic",
           "aether:the_aether|rare|mythic", "blue_skies:everbright|rare|mythic", "blue_skies:everdawn|rare|mythic", "deeperdarker:otherside|epic|mythic"]
boss_dims = ["minecraft:overworld|0.014|NEEDS_SKY", "minecraft:the_nether|0.022|ANY", "minecraft:the_end|0.018|SURFACE_OUTER_END", "twilightforest:twilight_forest|0.04|NEEDS_SURFACE",
             "undergarden:undergarden|0.02|ANY", "aether:the_aether|0.03|NEEDS_SURFACE", "blue_skies:everbright|0.03|NEEDS_SURFACE", "blue_skies:everdawn|0.03|NEEDS_SURFACE",
             "deeperdarker:otherside|0.02|ANY"]


def patch(key, lines):
    global s
    rx = re.compile(r'(S:"%s" <\r?\n)(.*?)(\r?\n\s*>)' % re.escape(key), re.S)
    if not rx.search(s):
        raise SystemExit("config key not found: " + key)
    s = rx.sub(lambda m: m.group(1) + "\n".join("        " + l for l in lines) + m.group(3), s, count=1)


patch("Affix Item Loot Rules", item_rules)
patch("Affix Convert Loot Rules", convert_rules)
patch("Affix Convert Rarities", convert_rar)
patch("Gem Loot Rules", gem_rules)
patch("Gem Dimensional Rarities", gem_rar)
patch("Boss Spawn Dimensions", boss_dims)
s = re.sub(r'(S:"Random Affix Chance"=)[0-9.]+', r"\g<1>0.04", s)
s = re.sub(r'(S:"Gem Drop Chance"=)[0-9.]+', r"\g<1>0.03", s)
open(P, "w", encoding="utf-8").write(s)
print("patched", P)
