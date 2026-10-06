"""Arms and Arcana (part 2): the three magic schools and accessories."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from questlib import *

CHAPTERS = []

# =============================================================== IRON'S SPELLS =====================================================
c = Chapter("irons", "Spellcraft: The Schools of Iron", "irons_spellbooks:scroll", "craft", "Nine schools, one grammar: mana, cast time, cooldown.", bg="irons")
c.q("intro", "What a Spell Is", "irons_spellbooks:scroll",
    ["Every spell belongs to a school (fire, ice, lightning, holy, ender, blood, evocation, nature, eldritch) and has a level, a cast time and a cooldown. Spell power scales damage; max mana is your pool.",
     "Cast by selecting a spell in your book and holding the cast key. Start with a scroll and learn the feel before committing to a book."],
    [check()], [xp(20)], shape="diamond", size=1.3)
c.q("scroll", "A Scroll to Learn On", "irons_spellbooks:scroll", "Scrolls hold one spell at one level, once. Collect them from dungeons and trade for the rest.", [item("irons_spellbooks:scroll")], [xp(25)], deps=["intro"])
c.q("inscription", "Inscription Table", "irons_spellbooks:inscription_table", "Writes spells into books. The difference between a mage and a person holding a scroll.", [item("irons_spellbooks:inscription_table")], [xp(30)], deps=["scroll"])
c.q("copper", "Copper Spell Book", "irons_spellbooks:copper_spell_book", "Two spell slots and a lot of ambition.", [item("irons_spellbooks:copper_spell_book")], [xp(30)], deps=["inscription"])
c.q("iron", "Iron Spell Book", "irons_spellbooks:iron_spell_book", "More slots, slightly more power.", [item("irons_spellbooks:iron_spell_book")], [xp(45)], deps=["copper"])
c.q("gold", "Gold Spell Book", "irons_spellbooks:gold_spell_book", "A book fit for a dungeon-delver.", [item("irons_spellbooks:gold_spell_book")], [xp(60)], deps=["iron"])
c.q("diamond", "Diamond Spell Book", "irons_spellbooks:diamond_spell_book", "A real tool for a real caster. Heavily sought, hard to craft.", [item("irons_spellbooks:diamond_spell_book")], [xp(100)], deps=["gold"])
c.q("netherite", "Netherite Spell Book", "irons_spellbooks:netherite_spell_book", "Nine slots. The last craftable tier; the best ones are found, not made.", [item("irons_spellbooks:netherite_spell_book")], [xp(200), points(1)], deps=["diamond"], shape="hexagon")
c.q("legendary", "A Legendary Book", "irons_spellbooks:legendary_spell_book", "Legendary tomes hold twelve slots and a name. Only the deepest vaults and the hardest bosses give them.", [item("irons_spellbooks:legendary_spell_book")], [xp(400), points(1)], deps=["netherite"], shape="hexagon", size=1.3)
c.q("anvil", "Arcane Anvil", "irons_spellbooks:arcane_anvil", "Upgrade scrolls and merge spells; imbue weapons with a spell. This is the heart of the Spellblade.", [item("irons_spellbooks:arcane_anvil")], [xp(40)], deps=["inscription"])
c.q("cauldron", "Alchemist Cauldron", "irons_spellbooks:alchemist_cauldron", "Brewing is a second kind of casting: ingredient combinations with real consequences.", [item("irons_spellbooks:alchemist_cauldron")], [xp(40)], deps=["intro"], optional=True)
c.q("forge", "The Scroll Forge", "irons_spellbooks:scroll_forge", "Turn ink and parchment into scrolls with the right pigments.", [item("irons_spellbooks:scroll_forge")], [xp(40)], deps=["scroll"], optional=True)
c.q("fire", "Fire Rune", "irons_spellbooks:fire_rune", "Runes unlock school specializations. Fire is hungry; ice is patient; lightning is impatient.", [item("irons_spellbooks:fire_rune")], [xp(60)], deps=["copper"], optional=True)
c.q("upgrade", "Upgrade Orbs", "irons_spellbooks:mana_upgrade_orb", "Orbs boost mana, cooldown, spell power, and school stats on your gear. Choose one for each piece.", [item("irons_spellbooks:mana_upgrade_orb")], [xp(80)], deps=["anvil"])
c.q("wizard", "Robes", "irons_spellbooks:pyromancer_helmet", "Wizard gear brings spell power and mana in exchange for armor.", [item("irons_spellbooks:pyromancer_helmet")], [xp(60)], deps=["copper"])
c.q("ring", "Ring of Power", "irons_spellbooks:mana_ring", "Casters carry rings: mana, cooldown, cast time. They are cheap, and critical.", [item("irons_spellbooks:mana_ring")], [xp(50)], deps=["copper"])
c.q("catacombs", "The Catacombs", "irons_spellbooks:cultist_helmet", "A dungeon of cultists, wraiths and the Dead King. Your first real boss in the schools of Iron.", [adv("irons_spellbooks:irons_spellbooks/enter_catacombs")], [xp(150)], deps=["gold"])
c.q("master", "Master of a School", "irons_spellbooks:nature_rune", "Choose a school and drive it as far as you can. The tree, the gear and your books can focus on one at a time.", [check()], [xp(300), points(1)], deps=["upgrade", "wizard"], shape="hexagon")
CHAPTERS.append(c)

# =============================================================== ARS NOUVEAU ======================================================
c = Chapter("ars", "Spellcraft: Glyphs and Source", "ars_nouveau:novice_spell_book", "craft", "Build your own spells, glyph by glyph.", bg="ars")
c.q("intro", "Glyph by Glyph", "ars_nouveau:novice_spell_book", ["Ars Nouveau spells are assembled from three parts: a form (how it is delivered), an effect (what it does) and augments (how it does it). Source mana comes from the world, not from you.", "It is a different kind of magic from Iron's: more utility, more freedom, more patience."], [item("ars_nouveau:novice_spell_book")], [xp(30)], shape="diamond", size=1.3)
c.q("source", "Source Gems", "minecraft:amethyst_shard", "Source is gathered from the world and fed into jars and machines. Without it, nothing works.", [check()], [xp(25)], deps=["intro"])
c.q("glyph", "A First Glyph", "ars_nouveau:glyph_projectile", "Glyphs are learned and crafted. Start with projectile, harm and a little amplify.", [item("ars_nouveau:glyph_projectile")], [xp(40)], deps=["intro"])
c.q("heal", "Heal", "ars_nouveau:glyph_heal", "A heal glyph on yourself: the first healing spell any traveller learns.", [item("ars_nouveau:glyph_heal")], [xp(40)], deps=["glyph"])
c.q("blink", "Blink", "ars_nouveau:glyph_blink", "A short-range teleport you own. It does not replace Waystones, but it makes cliffs and doorways optional.", [item("ars_nouveau:glyph_blink")], [xp(60)], deps=["glyph"])
c.q("glide", "Glide", "ars_nouveau:glyph_glide", "A glyph for controlled falls. Not true flight: just a very good descent.", [item("ars_nouveau:glyph_glide")], [xp(60)], deps=["glyph"], optional=True)
c.q("apparatus", "Enchanting Apparatus", "ars_nouveau:enchanting_apparatus", "A workbench for the high end: imbue gear, craft glyphs, make ritual items.", [item("ars_nouveau:enchanting_apparatus")], [xp(80)], deps=["heal"])
c.q("apprentice", "Apprentice Spell Book", "ars_nouveau:apprentice_spell_book", "More glyph slots, more complex spells.", [adv("ars_nouveau:apprentice_spell_book")], [xp(100)], deps=["apparatus"])
c.q("archmage", "Archmage Spell Book", "ars_nouveau:archmage_spell_book", "The final tier: huge, powerful, expensive.", [adv("ars_nouveau:archmage_spell_book")], [xp(250), points(1)], deps=["apprentice"], shape="hexagon")
c.q("imbuement", "Imbuement Chamber", "ars_nouveau:imbuement_chamber", "Imbues items with spell-like properties. A craftsman's cathedral.", [item("ars_nouveau:imbuement_chamber")], [xp(80)], deps=["apparatus"], optional=True)
c.q("ritual", "A Ritual", "ars_nouveau:ritual_awakening", "Rituals do big things slowly: summon, bless, awaken. Set up a brazier and be patient.", [check()], [xp(120)], deps=["apparatus"], optional=True)
c.q("combo", "Spell Fusion", "ars_nouveau:arcane_core", "Mix Iron's and Ars spells in the same loadout: one for combat, one for utility. Bring both.", [check()], [xp(150)], deps=["archmage"], optional=True)
CHAPTERS.append(c)

# =============================================================== GOETY ============================================================
c = Chapter("goety", "Necromancy and the Dark Arts", "goety:dark_wand", "craft", "A different kind of power: servants, curses, and the price of command.", bg="goety")
c.q("intro", "The Dark Altar", "goety:dark_altar", ["Goety is the school of the summoner and necromancer: minions that fight for you, foci that cast for you, and an altar to bring it all together.", "The Dark Wand and Nameless Staff are your tools; foci are your spells. Servants cost souls."], [item("goety:dark_altar")], [xp(30)], shape="diamond", size=1.3)
c.q("wand", "Dark Wand", "goety:dark_wand", "A short staff with a long reach. It fires foci and holds your power.", [item("goety:dark_wand")], [xp(40)], deps=["intro"])
c.q("focus", "A First Focus", "goety:empty_focus", "Foci are the spells you swap into a wand: fireball, ice, summon, command. Mix them for your build.", [item("goety:empty_focus")], [xp(40)], deps=["wand"])
c.q("robe", "Dark Robe", "goety:dark_robe", "Robes boost soul cost reduction and casting power. Put them on before you summon.", [item("goety:dark_robe")], [xp(50)], deps=["wand"])
c.q("bag", "Focus Bag", "goety:focus_bag", "Carry a dozen foci in a bag. Quick-swap in the middle of a fight.", [item("goety:focus_bag")], [xp(40)], deps=["focus"], optional=True)
c.q("servant", "A Servant", "goety:animation_core", "Animation cores bind minions: undead, blazes, bears, ghasts. They die, you rebuild, the soul bill keeps coming.", [item("goety:animation_core")], [xp(60)], deps=["focus"])
c.q("lich", "Become a Lich", "goety:black_crystal", "The long road ends in a transformation. It makes you stronger and worse at being alive.", [adv("goety:goety/become_lich")], [xp(300), points(1)], deps=["servant"], shape="hexagon")
c.q("crypt", "Crypt Dwellers", "goety:crypt_bookshelf", "Crypts, graveyards, ruined monasteries: Goety's structures are full of loot and the occasional necromancer.", [struct("goety:crypt")], [xp(100)], deps=["intro"])
c.q("manor", "The Dark Manor", "minecraft:dark_oak_door", "A haunted manor with a ritual at its heart and a very bad host.", [struct("goety:dark_manor")], [xp(120), cache(3)], deps=["crypt"])
c.q("apostle", "The Apostle", "goety:nameless_staff", "A priest of the old order, forced to serve a thing he no longer remembers. His staff is one of the best minion casters in the game.", [kill("goety:apostle")], [xp(500), points(1), cache(5)], deps=["manor", "lich"], shape="octagon", size=1.5)
c.q("cage", "Cursed Cage", "goety:cursed_cage", "Cages capture creatures for your use. Capture is easier than command, and command is easier than keeping them alive.", [item("goety:cursed_cage")], [xp(60)], deps=["servant"], optional=True)
CHAPTERS.append(c)

# =============================================================== ACCESSORIES AND RELICS ===========================================
c = Chapter("accessories", "Rings, Relics and Trinkets", "artifacts:feral_claws", "craft", "Slots for the small things that make the big difference.", bg="accessories")
c.q("intro", "Beyond Armor", "artifacts:cloud_in_a_bottle", ["Rings, necklaces, charms, belts, trinkets: accessory slots add power without costing armor. Each slot is one decision; fill them thoughtfully.", "Slots are limited; the skill tree can add more."], [check()], [xp(20)], shape="diamond", size=1.3)
c.q("ring", "A Ring", "irons_spellbooks:silver_ring", "Rings are the cheapest accessory and the first one you will find. Wear two.", [item("irons_spellbooks:silver_ring")], [xp(25)], deps=["intro"])
c.q("claws", "Feral Claws", "artifacts:feral_claws", "Faster attacks. A thoughtful trade for a warrior's off hand.", [item("artifacts:feral_claws")], [xp(40)], deps=["intro"])
c.q("gauntlet", "Power Glove", "artifacts:power_glove", "More damage, no cost: the classic. Some artifacts are simply good.", [item("artifacts:power_glove")], [xp(40)], deps=["intro"])
c.q("hopper", "Bunny Hoppers", "artifacts:bunny_hoppers", "Jump higher, land softer. A traveller's staple.", [item("artifacts:bunny_hoppers")], [xp(40)], deps=["intro"])
c.q("flippers", "Flippers", "artifacts:flippers", "Swim faster. For anyone planning to meet the ocean.", [item("artifacts:flippers")], [xp(40)], deps=["intro"])
c.q("cloud", "Cloud in a Bottle", "artifacts:cloud_in_a_bottle", "A mid-air double jump: the best accessory for dungeon-diving and ledge-climbing.", [item("artifacts:cloud_in_a_bottle")], [xp(80)], deps=["hopper"], shape="hexagon")
c.q("crystal", "Crystal Heart", "artifacts:crystal_heart", "More hearts, forever. Don't leave without one.", [item("artifacts:crystal_heart")], [xp(80)], deps=["intro"])
c.q("pendant", "Elemental Pendants", "artifacts:flame_pendant", "Pendants ignite, shock, and ward. Choose the element to match your build.", [item("artifacts:flame_pendant")], [xp(60)], deps=["intro"], optional=True)
c.q("horseshoe", "Horseshoe", "majruszsaccessories:horseshoe", "A little luck and a faster mount. The first accessory every rider wants.", [item("majruszsaccessories:horseshoe")], [xp(40)], deps=["intro"])
c.q("scarab", "Ancient Scarab", "majruszsaccessories:ancient_scarab", "Majrusz's accessories are subtle, cumulative boosts. A collection is worth more than any one of them.", [item("majruszsaccessories:ancient_scarab")], [xp(60)], deps=["horseshoe"], optional=True)
c.q("eye", "The Enigmatic Eye", "enigmaticlegacy:enigmatic_eye", "Enigmatic Legacy brings a family of powerful, cursed relics. They are among the strongest items in the pack and every one of them has a price.", [item("enigmaticlegacy:enigmatic_eye")], [xp(150)], deps=["crystal"], optional=True)
c.q("magnet", "Magnet Ring", "enigmaticlegacy:magnet_ring", "Items fly to you. A QoL luxury that sometimes feels like a necessity.", [item("enigmaticlegacy:magnet_ring")], [xp(60)], deps=["ring"], optional=True)
c.q("slots", "More Slots", "artifacts:villager_hat", "The skill tree and certain relics add slots. Fill them with trinkets that overlap: speed, health, and a good luck charm.", [check()], [xp(100), points(1)], deps=["cloud", "crystal"], shape="hexagon")
CHAPTERS.append(c)
