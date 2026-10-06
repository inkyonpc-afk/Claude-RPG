"""Arms and Arcana (part 1): skill tree and races, the weapon sandbox (generated from the weapon taxonomy), armor, Apotheosis gear, enchanting."""
import sys, os, json, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from questlib import *

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CHAPTERS = []

# =============================================================== SKILL TREE AND RACES ================================================
c = Chapter("skills", "The Constellation of Embers", "minecraft:enchanted_book", "craft", "620 stars. A hundred points. Every road costs something.", bg="skilltree")
c.q("intro", "How to Build a Hero", "minecraft:knowledge_book",
    ["Aldreth has no classes. You have a people, a handful of stars, and whatever you pick up along the way. A warrior who dabbles in spellcraft is a Spellblade; a ranger who prays is a Hunter-Cleric; nobody will stop you.",
     "The tree has four Oaths (Might, Finesse, the Arcane, Faith) and fourteen regions. Every star costs experience. Choose a small number of stars well, rather than many badly."],
    [check()], [xp(20)], shape="diamond", size=1.3)
c.q("peoples", "Eight Peoples", "minecraft:player_head", "Each people carries a gift and a burden: Dwarves dig, Elves dodge, Orcs smash, Halflings stumble into luck. Your choice is permanent: there is no cheap respec for blood.", [check()], [xp(20)], deps=["intro"])
c.q("oath", "Take an Oath", "minecraft:blaze_powder", "Open the tree and pick a starting Oath. It is free, but it decides which regions are nearest.", [check()], [xp(20), points(1)], deps=["intro"])
c.q("region", "A Region of Your Own", "minecraft:iron_sword", "Warrior, Berserker, Guardian, Paladin, Cleric, Druid, Necromancer, Blood Mage, Elementalist, Arcanist, Spellblade, Ranger, Rogue, Wanderer. Pick the one that sounds like you and walk to its first gate.", [check()], [xp(25)], deps=["oath"])
c.q("notable", "Notables", "minecraft:gold_ingot", "Larger stars pair two effects: your first real choice between 'a bit more of everything' and 'a lot more of one thing'.", [check()], [xp(25)], deps=["region"])
c.q("keystone", "A Keystone", "minecraft:nether_star", ["Keystones change how you play, and every one carries a real price: Glass Cannon, Blood Pact, Lone Wolf, Avatar of Flame. There are 42. You will afford maybe two.", "Read the tooltip twice, then a third time."], [check()], [xp(60), points(1)], deps=["notable"], shape="hexagon")
c.q("bridge", "Cross-Region Bridges", "minecraft:chain", "Between every pair of neighbouring regions sit two hybrid stars. They are the only cheap way to mix archetypes: Battlemage, Blood Knight, Druid-Cleric, Shadowblade.", [check()], [xp(40)], deps=["keystone"])
c.q("respec", "A Clean Slate", "minecraft:grindstone", "The Amnesia Scroll resets your tree for a ten percent loss of levels. It is a luxury; use it when your build has changed, not when it has failed.", [check()], [xp(40)], deps=["bridge"])
c.q("xp", "XP Is Currency", "minecraft:experience_bottle", "Skill points are bought with experience, not found. Every quest pays XP; some pay points directly. Enchanting and the tree compete for the same pool: plan.", [check()], [xp(30)], deps=["notable"], optional=True)
c.q("might", "Oath of Might", "minecraft:iron_sword", "Warrior, Berserker and Spellblade begin here. Hit things; get hit less.", [check()], [xp(15)], deps=["oath"], optional=True)
c.q("finesse", "Oath of Finesse", "minecraft:bow", "Ranger, Rogue and Wanderer begin here. Choose your moment.", [check()], [xp(15)], deps=["oath"], optional=True)
c.q("arcane", "Oath of the Arcane", "irons_spellbooks:copper_spell_book", "Blood Mage, Necromancer, Arcanist, Elementalist and Spellblade begin here. Mana is a budget, not a limit.", [check()], [xp(15)], deps=["oath"], optional=True)
c.q("faith", "Oath of Faith", "minecraft:golden_apple", "Paladin, Cleric, Druid and Guardian begin here. Keep the line standing.", [check()], [xp(15)], deps=["oath"], optional=True)
c.q("hybrid", "A True Hybrid", "minecraft:smithing_table", "Reach two keystones from different Oaths. You will be very good at a very specific thing, and noticeably worse at everything else.", [check()], [xp(150), points(2)], deps=["keystone", "bridge"], shape="hexagon", size=1.3)
CHAPTERS.append(c)

# =============================================================== WEAPONS (generated from the taxonomy) ===============================
TAG_DIR = os.path.join(ROOT, "config", "paxi", "datapacks", "aldreth_core", "data", "aldreth", "tags", "items", "weapons")
PREF = ["simplyswords", "magistuarmory", "celestisynth", "soulsweapons", "marium", "ageofweapons", "iceandfire", "irons_spellbooks", "ars_nouveau", "goety", "twilightforest", "aether", "minecraft"]


def pick(cls, avoid=()):
    f = os.path.join(TAG_DIR, cls + ".json")
    if not os.path.isfile(f):
        return "minecraft:iron_sword"
    items = [x for x in json.load(open(f))["values"] if not x.startswith("#")]
    for ns in PREF:
        cand = sorted(i for i in items if i.startswith(ns + ":") and i not in avoid)
        if cand:
            return cand[len(cand) // 3]   # a mid-tier example, not the very first
    return items[0] if items else "minecraft:iron_sword"


CLASSES = [
    ("longsword", "Longsword", "Warrior", "The generalist: balanced speed, reach and damage. Blocks, parries, never lets you down."),
    ("katana", "Katana", "Rogue or Warrior", "Faster than a longsword and quicker to find an opening. Bleed on crits; draw-cut combos."),
    ("rapier", "Rapier", "Rogue or Spellblade", "Thrust, riposte, flourish. Great critical scaling, light armor, light everything."),
    ("dagger", "Dagger", "Rogue", "The fastest weapon in the game. Dual-wielding daggers is an entire build."),
    ("greatsword", "Greatsword", "Warrior or Berserker", "Slow, heavy, wide. The windup is your cost and the stagger is your reward."),
    ("twinblade", "Twinblade", "Berserker", "A double-bladed spin machine. Hits twice, rewards aggression, punishes hesitation."),
    ("axe", "Axe", "Berserker", "One-handed and brutal. Cleaves shields and armor. Bleeds."),
    ("greataxe", "Greataxe", "Berserker", "An axe on steroids. Huge sweeps, huge windup, huge sound."),
    ("hammer", "Warhammer", "Guardian or Paladin", "Staggers and breaks things. The best partner of a shield and a cleric."),
    ("mace", "Mace", "Paladin", "Crushing blows against armor and undead. The paladin's best friend."),
    ("spear", "Spear", "Warrior or Ranger", "Reach and thrust. Keep them away, hit them first, retreat."),
    ("polearm", "Polearm", "Guardian", "Halberds and glaives sweep wide arcs. A fortress built out of one weapon."),
    ("scythe", "Scythe", "Necromancer or Blood Mage", "A reaper's tool: wide arcs, soul-lashing, gets stronger as the dead pile up."),
    ("quarterstaff", "Quarterstaff", "Wanderer", "Two ends, spin and sweep. A traveller's weapon and a warrior's cane."),
    ("whip", "Whip", "Rogue", "Long reach, light damage, every stat that dislikes you being close."),
    ("bow", "Bow", "Ranger", "The classic. Draw speed, arrow velocity, elemental shots and the long wait for the perfect line."),
    ("crossbow", "Crossbow", "Ranger", "Slow, strong, and satisfying. Multishot and piercing bolts reward planning."),
    ("staff", "Staff", "Arcanist, Elementalist", "A conduit for school magic: spell power, mana, and a good grip."),
    ("wand", "Wand and Focus", "Arcanist", "Light, fast casting. Great for a spellblade who still wants a sword in the other hand."),
    ("spellbook", "Spellbook", "Any caster", "Books are the heart of a spellcaster's kit: slots, schools, and the lore of every spell you know."),
    ("shield", "Shield", "Guardian, Paladin", "Raise it in time and the enemy staggers. Block, riposte, repeat."),
]
c = Chapter("weapons", "The Weapon Sandbox", "minecraft:diamond_sword", "craft", "Twenty-one classes of weapon, each with its own rhythm, its own scaling and its own place on the tree.", bg="weapons")
c.q("intro", "An Arsenal of Many Hands", "minecraft:iron_sword",
    ["Every weapon in Aldreth belongs to a class, and every class plays differently: speed, reach, stagger, sweep, windup. Combat has weight and direction: the sword you pick tells the world who you are.",
     "Find an example of each class and see how it feels. Your skill tree rewards sticking to a class, so play with a few before you commit."],
    [check()], [xp(20)], shape="diamond", size=1.3)
used = set()
prev = "intro"
keys = []
for cls, name, branch, blurb in CLASSES:
    it = pick(cls, used)
    used.add(it)
    k = "w_" + cls
    c.q(k, name, it, ["%s Best on: %s." % (blurb, branch), "Obtain any %s to complete this step; every class is represented." % name.lower()], [item(it)], [xp(40)], deps=["intro"], optional=True)
    keys.append(k)
c.q("level", "A Weapon Remembers", "minecraft:experience_bottle", "Weapons gain levels as you use them: hit things, earn bonuses. The best weapon is not the highest-damage one; it is the one you invest in.", [check()], [xp(40)], deps=["intro"])
c.q("rarity", "Rarity", "apotheosis:common_material", "A common sword and a mythic sword differ in affixes, not in kind. Salvage trash, socket gems, reforge: let your favourite weapon grow into its rarity.", [check()], [xp(40)], deps=["level"])
c.q("arsenal", "A Properly Stocked Armory", "minecraft:smithing_table", "A longsword, a bow, a staff and a shield. Four classes, four stances: you have a favourite, but you can swap.", [item(pick("longsword")), item(pick("bow")), item(pick("staff")), item(pick("shield"))], [xp(200), points(1)], deps=["w_longsword", "w_bow", "w_staff", "w_shield"], shape="hexagon", size=1.3)
c.q("master", "Master of Many Hands", "minecraft:netherite_sword", "Own at least one weapon from every melee class. You will not use them all. You will understand them all.", [check()], [xp(400), points(2)], deps=["arsenal", "w_katana", "w_greatsword", "w_dagger", "w_scythe"], shape="diamond", size=1.4)
CHAPTERS.append(c)

# =============================================================== ARMOR AND SHIELDS ==================================================
c = Chapter("armor", "Armor and Defense", "minecraft:iron_chestplate", "craft", "A suit of armor is a decision about what you are afraid of.", bg="armor")
c.q("intro", "What Armor Is For", "minecraft:iron_chestplate", ["Armor reduces physical damage. Toughness caps what each hit can do. Resistances and wards cover magic. Armor is never enough alone."], [check()], [xp(15)], shape="diamond")
c.q("leather", "Leather", "minecraft:leather_chestplate", "Light, quiet, fast. Good for rogues and runners.", [item("minecraft:leather_chestplate")], [xp(15)], deps=["intro"])
c.q("chain", "Chain", "minecraft:chainmail_chestplate", "Middle ground: flexible and decently protective.", [item("minecraft:chainmail_chestplate")], [xp(20)], deps=["intro"])
c.q("iron", "Iron", "minecraft:iron_chestplate", "The honest standard: solid, available, repairable.", [item("minecraft:iron_chestplate")], [xp(20)], deps=["intro"])
c.q("knight", "Knight's Plate", "minecraft:iron_helmet", "Epic Knights armors bring distinct medieval silhouettes: barbute, sallet, armet. Heavy plate slows you; the skill tree decides how much you mind.", [check()], [xp(30)], deps=["iron"])
c.q("shield", "Shield Craft", "minecraft:shield", "Shields block, parry and bash. They use stamina and durability; the best ones are earned, not crafted.", [item("minecraft:shield")], [xp(25)], deps=["iron"])
c.q("naga", "Naga Scale", "twilightforest:naga_chestplate", "Forest-forged scale armor with a real silhouette and real resistance.", [item("twilightforest:naga_chestplate")], [xp(60)], deps=["knight"], optional=True)
c.q("arctic", "Arctic Fur", "twilightforest:arctic_fur", "Warm, light, and surprisingly sturdy. A cold-weather armor for the long road.", [item("twilightforest:arctic_fur", 4)], [xp(40)], deps=["leather"], optional=True)
c.q("netherite", "Netherite Plate", "minecraft:netherite_chestplate", "The last tier of vanilla armor. It is where progression began, not where it ends.", [item("minecraft:netherite_chestplate")], [xp(120)], deps=["knight"])
c.q("mage_robes", "Mage Robes", "irons_spellbooks:pyromancer_helmet", "Robes and cowls add spell power and cooldown reduction at the cost of armor. Choose a school: pyromancer, cryomancer, priest, archevoker.", [item("irons_spellbooks:pyromancer_helmet")], [xp(60)], deps=["intro"])
c.q("mythic_armor", "Mythic Armor", "irons_spellbooks:netherite_mage_chestplate", "Netherite mage armor is the end of the road for plain casters: sturdy, warded, and ready for sockets.", [item("irons_spellbooks:netherite_mage_chestplate")], [xp(150)], deps=["mage_robes", "netherite"], shape="hexagon")
c.q("set", "A Matching Set", "minecraft:diamond_chestplate", "Armor sets give set bonuses when worn together. Mix and match to chase a build, or commit to one set and love it.", [check()], [xp(50)], deps=["knight"])
CHAPTERS.append(c)

# =============================================================== APOTHEOSIS GEAR ====================================================
c = Chapter("gear", "Gear and the Craft of Upgrading", "apotheosis:gem", "craft", "Rarity, affixes, sockets, gems and reforging: the long path from found to forged.", bg="apotheosis")
c.q("intro", "From Found to Forged", "apotheosis:common_material",
    ["Every piece of gear carries a rarity and, from uncommon upward, affixes: extra stats, special effects, even names. Rarity is a ceiling, not a verdict: invest in a favourite and it stays useful.",
     "Rarities: Common, Uncommon, Rare, Epic, Mythic, Ancient. Chests and bosses decide how high they roll."],
    [check()], [xp(20)], shape="diamond", size=1.3)
c.q("salvage", "Salvaging Table", "apotheosis:salvaging_table", "Break gear into materials. A rare weapon yields rare materials: the cost of a wasted drop is never zero.", [item("apotheosis:salvaging_table")], [xp(30)], deps=["intro"])
c.q("reforge", "Reforging Table", "apotheosis:reforging_table", "Reroll an item's affixes using materials and levels. Costs rise with rarity: reforge something worth saving.", [item("apotheosis:simple_reforging_table")], [xp(40)], deps=["salvage"])
c.q("socket", "Socketing", "apotheosis:sigil_of_socketing", "A socket is a slot waiting for a gem. Sigils add sockets; gems fill them.", [item("apotheosis:sigil_of_socketing")], [xp(40)], deps=["salvage"])
c.q("gem", "Gems", "apotheosis:gem", "Gems are keyed to item types: armor gems, weapon gems, tool gems. Pick ones that fit your build.", [item("apotheosis:gem")], [xp(40)], deps=["socket"])
c.q("cut", "Gem Cutting", "apotheosis:gem_cutting_table", "Combine gems to improve their purity. A flawless gem is worth a hundred ordinary ones.", [item("apotheosis:gem_cutting_table")], [xp(60)], deps=["gem"])
c.q("augment", "Augmenting", "apotheosis:augmenting_table", "Sometimes you keep an item and mold its affixes by hand. The augmenting table is expensive and very good.", [item("apotheosis:augmenting_table")], [xp(80)], deps=["reforge"])
c.q("rare", "Rare", "apotheosis:rare_material", "Three affixes, the first set of real choices. It is the first rarity where gear starts to feel like yours.", [adv("apotheosis:affix/rare")], [xp(80)], deps=["intro"])
c.q("epic", "Epic", "apotheosis:epic_material", "Four affixes and a named variant. Your build starts here.", [adv("apotheosis:affix/epic")], [xp(150)], deps=["rare"])
c.q("mythic", "Mythic", "apotheosis:mythic_material", "Five affixes and top-tier potency. A mythic piece is a long-term investment.", [adv("apotheosis:affix/mythic")], [xp(250), points(1)], deps=["epic"], shape="hexagon")
c.q("ancient", "Ancient", "apotheosis:ancient_material", "The rarest tier: only the hardest bosses and the deepest vaults will give you one. They are not 'better': they are scarcer, and that is the point.", [adv("apotheosis:affix/ancient")], [xp(500), points(2)], deps=["mythic"], shape="hexagon", size=1.3)
c.q("boss", "Boss Gear", "apotheosis:boss_summoner", "Apotheosis bosses roam the world carrying specially affixed gear. Defeat one for your first truly named item.", [adv("apotheosis:affix/boss")], [xp(100)], deps=["rare"], optional=True)
c.q("rebirth", "Sigil of Rebirth", "apotheosis:sigil_of_rebirth", "Wipe an item's affixes, keeping its rarity; a second chance for something that nearly worked.", [item("apotheosis:sigil_of_rebirth")], [xp(60)], deps=["reforge"], optional=True)
c.q("tome", "Tomes of Making", "apotheosis:weapon_tome", "Tomes add enchantment rules: weapon tomes unlock weapon enchantments on anything, extraction tomes pull them back out.", [item("apotheosis:weapon_tome")], [xp(60)], deps=["intro"], optional=True)
c.q("gem_ancient", "Ancient Gems", "apotheosis:gem_fused_slate", "Gems can be ancient: fused slate, stronger than any ordinary stone.", [adv("apotheosis:affix/ancient_gem")], [xp(300)], deps=["ancient"], optional=True)
CHAPTERS.append(c)

# =============================================================== ENCHANTING =========================================================
c = Chapter("enchanting", "Enchanting, Beyond the Table", "minecraft:enchanting_table", "craft", "The ceiling is shelves.", bg="enchanting")
c.q("intro", "Beyond Level Thirty", "minecraft:enchanting_table", "The enchanting table stops at thirty in vanilla. Here it does not: bookshelves, hellshelves, seashelves and more drive the maximum up, and with it the quality of enchantments.", [item("minecraft:enchanting_table")], [xp(20)], shape="diamond")
c.q("bookshelf", "A Well-Stocked Shelf", "minecraft:bookshelf", "Plain bookshelves give small, steady power. Bring many.", [item("minecraft:bookshelf", 15)], [xp(25)], deps=["intro"])
c.q("e30", "Level Thirty", "minecraft:experience_bottle", "Reach a thirty-level enchant. This is where normal enchanting tops out.", [adv("apotheosis:enchanting/30ench")], [xp(60)], deps=["bookshelf"])
c.q("hell", "Hellshelf", "apotheosis:hellshelf", "Adds levels and quanta. Made from Nether bricks and fire-touched books.", [item("apotheosis:hellshelf", 8)], [xp(80)], deps=["e30"])
c.q("sea", "Seashelf", "apotheosis:seashelf", "Adds arcana and prismarine-tinted power.", [item("apotheosis:seashelf", 8)], [xp(80)], deps=["e30"])
c.q("e60", "Level Sixty", "apotheosis:infused_hellshelf", "Sixty-level enchants reach into rare and treasure enchantments. Your table is now a project.", [adv("apotheosis:enchanting/60ench")], [xp(150)], deps=["hell", "sea"])
c.q("end", "Endshelf", "apotheosis:endshelf", "Adds levels and a lot of arcana. Made from End stone and dragon fire.", [item("apotheosis:endshelf", 4)], [xp(150)], deps=["e60"])
c.q("e100", "Level One Hundred", "apotheosis:ender_library", "A hundred-level table is the end of enchanting: rare enchants appear at max and some go beyond.", [adv("apotheosis:enchanting/100ench")], [xp(400), points(1)], deps=["end"], shape="hexagon")
c.q("library", "The Library", "apotheosis:library", "Stores enchanted books by type and level: a banker for your best enchants.", [item("apotheosis:library")], [xp(120)], deps=["e60"])
c.q("filter", "Filtering Shelf", "apotheosis:filtering_shelf", "Tune the enchants your table offers by installing a filter.", [item("apotheosis:filtering_shelf")], [xp(120)], deps=["e60"], optional=True)
c.q("treasure", "Treasure Shelf", "apotheosis:treasure_shelf", "Unlocks treasure enchantments: mending, frost walker, soul speed. Opens the door to power that normal tables hide.", [item("apotheosis:treasure_shelf")], [xp(120)], deps=["e60"], optional=True)
c.q("max", "Maxed", "minecraft:enchanted_golden_apple", "Reach maximum stability and rectified enchants: max-level, stable, and without the wild swings.", [adv("apotheosis:enchanting/max_stable")], [xp(500)], deps=["e100"], optional=True)
CHAPTERS.append(c)
