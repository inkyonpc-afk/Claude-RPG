"""Aldreth skill tree content: 14 regions x (1 entry, 20 minors, 8 notables, 5 majors, 4 masteries, 3 keystones) + bridges.

Each region: dict(key, name, blurb, start, color, icons, minors=[4 templates], notables=[8], majors=[5], masteries=[4], keystones=[3]).
Each node: (title, icon, [bonus builders]).  See tools/skilltree_lib.py for the DSL.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from skilltree_lib import *

ATK, AS, ARM, TOU, HP, MS, KB, LUCK = ("minecraft:generic.attack_damage", "minecraft:generic.attack_speed", "minecraft:generic.armor", "minecraft:generic.armor_toughness",
                                        "minecraft:generic.max_health", "minecraft:generic.movement_speed", "minecraft:generic.knockback_resistance", "minecraft:generic.luck")
CRITC, CRITD, DODGE, LIFE, APIERCE, ASHRED = ("attributeslib:crit_chance", "attributeslib:crit_damage", "attributeslib:dodge_chance", "attributeslib:life_steal",
                                               "attributeslib:armor_pierce", "attributeslib:armor_shred")
ARROWD, ARROWV, DRAW, COLD, FIREDMG, CURHP = ("attributeslib:arrow_damage", "attributeslib:arrow_velocity", "attributeslib:draw_speed", "attributeslib:cold_damage",
                                               "attributeslib:fire_damage", "attributeslib:current_hp_damage")
HEALR, OVERHEAL, PPIERCE, PSHRED, XPG = ("attributeslib:healing_received", "attributeslib:overheal", "attributeslib:prot_pierce", "attributeslib:prot_shred", "attributeslib:experience_gained")
SP, MANA, MREG, CDR, CAST, CMS, SRES, SUMM = ("irons_spellbooks:spell_power", "irons_spellbooks:max_mana", "irons_spellbooks:mana_regen", "irons_spellbooks:cooldown_reduction",
                                              "irons_spellbooks:cast_time_reduction", "irons_spellbooks:casting_movespeed", "irons_spellbooks:spell_resist", "irons_spellbooks:summon_damage")
FIRE_SP, ICE_SP, LIGHT_SP, HOLY_SP, ENDER_SP, BLOOD_SP, EVOC_SP, NATURE_SP, ELD_SP = [("irons_spellbooks:%s_spell_power" % s) for s in ("fire", "ice", "lightning", "holy", "ender", "blood", "evocation", "nature", "eldritch")]
FIRE_R, ICE_R, LIGHT_R, HOLY_R, ENDER_R, BLOOD_R, EVOC_R, NATURE_R, ELD_R = [("irons_spellbooks:%s_magic_resist" % s) for s in ("fire", "ice", "lightning", "holy", "ender", "blood", "evocation", "nature", "eldritch")]
GPOT, GNEC, GCAST, GCDR, GDUR, GRAD = "goety:spell_potency", "goety:necromancy_potency", "goety:casting_speed", "goety:cooldown_discount", "goety:spell_duration", "goety:spell_radius"
ROLL_N, ROLL_D, ROLL_R = "combatroll:count", "combatroll:distance", "combatroll:recharge"
STEP, SWIM, REACH = "forge:step_height_addition", "forge:swim_speed", "forge:entity_reach"
W = lambda c: "aldreth:weapons/" + c

# icon palette (PST ships 80 icons; custom icons arrive with the visuals pass)
I = lambda n: "skilltree:textures/icons/%s.png" % n

REGIONS = []

# ======================================================================== WARRIOR (Might) =====================================================
REGIONS.append(dict(
    key="warrior", name="Warrior", start="might", color="d9a441", blurb="Master of the blade: swords, axes, great weapons, armor and the rhythm of the front line.",
    minors=[("Sword Drill", "sword_iron", [D(0.025, "melee")]), ("Hardened Plate", "chestplate_bronze_fur", [A(ARM, 1.0)]),
            ("Trained Grip", "glove_iron", [A(AS, 0.02, 1)]), ("Veteran's Eye", "eye_green", [CC(0.012)])],
    entry=("Warrior's Oath", "sword_gold", [A(ATK, 1.0), A(ARM, 1.0)]),
    notables=[("Bladework", "sword_iron", [D(0.06, "melee", when="hand:" + W("longsword")), A(AS, 0.03, 1)]),
              ("Axe Discipline", "sword_bronze", [D(0.06, "melee", when="hand:" + W("axe")), A(APIERCE, 1.0)]),
              ("Heavy Hands", "glove_gold", [D(0.07, "melee", when="hand:" + W("heavy")), A(KB, 0.1)]),
              ("Spear Reach", "arrow_steel", [A(REACH, 0.5), D(0.05, "melee", when="hand:" + W("spear"))]),
              ("Battle Armor", "chestplate_leather", [A(ARM, 2.0), A(TOU, 1.0)]),
              ("Steady Footing", "boots_bronze", [A(KB, 0.15), A(STEP, 0.2)]),
              ("Cut Deep", "sword_gold", [CD(0.12), CC(0.02)]),
              ("Shield Wall Basics", "helmet_leather", [T(-0.06, "melee"), A(ARM, 1.0, when="worn:shield")])],
    majors=[("Armor Breaker", "sword_bronze", [A(ASHRED, 0.08), D(0.06, "melee", when="hp>0.7")]),
            ("Stagger Specialist", "glove_diamond", [FX("minecraft:slowness", 3, 1, "crit", 0.4), D(0.08, "melee", when="hand:" + W("hammer"))]),
            ("Fighting Retreat", "boots_gold", [T(-0.10, when="hp<0.5"), A(MS, 0.05, 1, when="hp<0.5")]),
            ("Parry Master", "glove_steel", [HEAL(0.03, "block", cooldown=40), D(0.10, "melee", when="worn:shield")]),
            ("Rallying Cry", "heart_red", [HEAL(0.04, "kill"), A(HP, 4.0)])],
    masteries=[("Weapon Master", "sword_gold", [D(0.10, "melee"), CD(0.15)]),
               ("Bulwark Stance", "glove_emerald", [A(ARM, 4.0, when="sneak"), A(TOU, 2.0, when="sneak"), T(-0.10, when="sneak")]),
               ("Reaper of Ranks", "skull", [D(0.05, "melee", by="debuffs/1"), HEAL(0.02, "hit", cooldown=20)]),
               ("Relentless Advance", "boots_leather", [A(MS, 0.06, 1), A(AS, 0.05, 1, when="hp>0.8")])],
    keystones=[("Unbroken Line", "chestplate_bronze_fur", [A(ARM, 0.5, 1), A(TOU, 0.5, 1), A(MS, -0.15, 1)]),
               ("Executioner's Edge", "sword_gold", [CD(0.60), CC(-0.10)]),
               ("Warlord's Will", "heart_red", [A(HP, 0.20, 1), D(0.12, "melee", by="armor/8"), A(AS, -0.10, 1)])]))

# ======================================================================== BERSERKER (Might) ===================================================
REGIONS.append(dict(
    key="berserker", name="Berserker", start="might", color="c0392b", blurb="Rage, blood and speed: the lower your health, the harder you hit. Life steal, executions and fury.",
    minors=[("Raw Fury", "chili_pepper_red", [D(0.025, "melee")]), ("Thick Hide", "heart_red", [A(HP, 2.0)]),
            ("Quickened Pulse", "glove_bronze", [A(AS, 0.02, 1)]), ("Bloodthirst", "heart_black", [A(LIFE, 0.005)])],
    entry=("Berserker's Howl", "chili_pepper_red", [A(ATK, 1.0), A(HP, 2.0)]),
    notables=[("Frenzied Strikes", "glove_gold", [A(AS, 0.05, 1), D(0.04, "melee", when="hp<0.6")]),
              ("Pain Fuels Rage", "heart_red", [D(0.04, "melee", by="missinghp/0.1")]),
              ("Savage Cleave", "sword_bronze", [D(0.07, "melee", when="hand:" + W("axe")), CD(0.08)]),
              ("Crimson Recovery", "heart_violet", [A(LIFE, 0.01), HEAL(0.02, "kill")]),
              ("Reckless Charge", "boots_gold", [A(MS, 0.05, 1), A(KB, 0.1)]),
              ("Iron Jaw", "skull", [A(KB, 0.2), A(HP, 4.0)]),
              ("Bleeding Wounds", "cross_red", [FX("minecraft:wither", 4, 0, "hit", 0.2), D(0.04, "melee")]),
              ("Wolfish Hunger", "bone", [HEAL(0.03, "crit", cooldown=30), CC(0.02)])],
    majors=[("Last Stand", "heart_red", [T(-0.12, when="hp<0.35"), D(0.12, "melee", when="hp<0.35")]),
            ("Blood Frenzy", "potion_red", [A(AS, 0.10, 1, when="hp<0.5"), A(LIFE, 0.02, when="hp<0.5")]),
            ("Dual Fury", "sword_iron", [D(0.12, "melee", when="dual"), A(AS, 0.06, 1, when="dual")]),
            ("Rending Blows", "chili_pepper_red", [FX("minecraft:weakness", 4, 0, "crit", 0.5), CD(0.12)]),
            ("Warcry Recovery", "heart_green", [HEAL(0.05, "kill"), A(MS, 0.04, 1)])],
    masteries=[("Rampage", "skull", [D(0.06, "melee", by="effects/1"), FX("minecraft:strength", 6, 0, "kill", 0.5, target="player")]),
               ("Executioner", "sword_gold", [D(0.20, "melee", target="hp<0.3")]),
               ("Unstoppable", "boots_bronze", [T(-0.08), A(KB, 0.25), A(MS, 0.04, 1)]),
               ("Heart of the Beast", "heart_violet", [A(HP, 8.0), A(LIFE, 0.02)])],
    keystones=[("Blood Pact", "heart_black", [RESERVE(0.25), A(LIFE, 0.05), D(0.25, "melee")]),
               ("Glass Cannon", "chili_pepper_red", [D(0.40, "melee"), A(HP, -0.25, 1)]),
               ("Undying Rage", "potion_red", [A(AS, 0.20, 1, when="hp<0.4"), D(0.30, "melee", when="hp<0.4"), A(ARM, -0.30, 1)])]))

# ======================================================================== GUARDIAN (Might/Faith) ==============================================
REGIONS.append(dict(
    key="guardian", name="Guardian", start="faith", color="5d7fa3", blurb="The immovable defender: health, armor, shields, retaliation, crowd control and recovery.",
    minors=[("Stout Heart", "heart_red", [A(HP, 2.0)]), ("Plating", "chestplate_leather", [A(ARM, 1.0)]),
            ("Resolve", "helmet_leather", [A(TOU, 0.5)]), ("Ironskin", "glove_steel", [T(-0.015)])],
    entry=("Guardian's Vow", "helmet_leather", [A(HP, 4.0), A(ARM, 1.0)]),
    notables=[("Shield Mastery", "glove_steel", [T(-0.08, when="worn:shield"), A(ARM, 2.0, when="worn:shield")]),
              ("Thorned Armor", "chestplate_bronze_fur", [A(ARM, 2.0), D(0.06, "thorns")]),
              ("Layered Defense", "chestplate_fur", [A(ARM, 3.0), A(TOU, 1.0)]),
              ("Fortitude", "heart_green", [A(HP, 6.0), A(OVERHEAL, 0.05)]),
              ("Unflinching", "boots_leather", [A(KB, 0.25), T(-0.04)]),
              ("Counterstrike", "sword_iron", [D(0.08, "melee", when="worn:shield"), HEAL(0.02, "block", cooldown=30)]),
              ("Rampart", "glove_bronze", [A(ARM, 2.0), A(KB, 0.1)]),
              ("Second Wind", "potion_green", [HEAL(0.02, "tick", cooldown=60), A(HEALR, 0.05)])],
    majors=[("Immovable Object", "glove_diamond", [A(KB, 0.4), T(-0.08, when="stand")]),
            ("Shield Bash Training", "glove_steel", [FX("minecraft:slowness", 3, 2, "block", 0.6, cooldown=60), A(ARM, 2.0, when="worn:shield")]),
            ("Bastion of Hope", "heart_cyan", [HEAL(0.04, "hurt", 0.25, cooldown=100), A(HP, 6.0)]),
            ("Spiked Plate", "chestplate_bronze_fur", [D(0.12, "thorns"), A(ARM, 3.0)]),
            ("Stalwart Recovery", "apple_green", [A(HEALR, 0.12), HEAL(0.01, "tick", cooldown=20)])],
    masteries=[("Fortress", "chestplate_leather", [A(ARM, 0.15, 1), A(TOU, 0.15, 1)]),
               ("Reprisal", "sword_bronze", [D(0.15, "melee", when="hp<0.5"), T(-0.06)]),
               ("Living Wall", "helmet_leather", [A(HP, 0.10, 1), A(KB, 0.3)]),
               ("Guardian's Grace", "heart_green", [A(OVERHEAL, 0.10), HEAL(0.03, "block", cooldown=40)])],
    keystones=[("Bastion", "chestplate_leather", [A(ARM, 0.40, 1), A(KB, 0.5), D(-0.20)]),
               ("Eternal Sentinel", "heart_cyan", [A(HP, 0.30, 1), HEAL(0.01, "tick", cooldown=20), A(MS, -0.12, 1)]),
               ("Retribution", "skull", [D(0.35, "thorns"), A(ARM, 0.20, 1), NOUSE(W("ranged"))])]))

# ======================================================================== PALADIN (Faith) =====================================================
REGIONS.append(dict(
    key="paladin", name="Paladin", start="faith", color="f4e3a1", blurb="Holy warrior: radiant magic, heavy armor, healing and wrath against the undead.",
    minors=[("Blessed Armor", "chestplate_bronze_fur", [A(ARM, 1.0)]), ("Radiance", "potion_yellow_big", [A(HOLY_SP, 0.03, 1)]),
            ("Sanctified Strike", "sword_gold", [D(0.02, "melee")]), ("Devotion", "heart_yellow", [A(HP, 2.0)])],
    entry=("Paladin's Oath", "sword_gold", [A(ARM, 1.0), A(HOLY_SP, 0.03, 1)]),
    notables=[("Holy Armor", "chestplate_bronze_fur", [A(ARM, 2.0), A(HOLY_R, 0.08, 1)]),
              ("Smite", "sword_gold", [D(0.06, "melee"), A(HOLY_SP, 0.05, 1)]),
              ("Lay on Hands", "heart_yellow", [A(HEALR, 0.08), HEAL(0.03, "tick", cooldown=80)]),
              ("Consecration", "torch", [A(HOLY_SP, 0.06, 1), A(CDR, 0.03, 1)]),
              ("Aegis of Faith", "glove_gold", [T(-0.05, "magic"), A(SRES, 0.05, 1)]),
              ("Zealous Charge", "boots_gold", [A(MS, 0.04, 1), D(0.05, "melee")]),
              ("Mercy", "potion_white", [A(HEALR, 0.10), A(HP, 4.0)]),
              ("Divine Favor", "apple_green", [A(MANA, 40.0), A(MREG, 0.06, 1)])],
    majors=[("Judgement", "sword_gold", [D(0.12, "melee", target="hp<0.5"), A(HOLY_SP, 0.06, 1)]),
            ("Ward of Light", "potion_yellow_big", [T(-0.08, "magic"), A(HOLY_R, 0.15, 1)]),
            ("Radiant Aura", "torch", [HEAL(0.02, "tick", cooldown=40), A(HOLY_SP, 0.08, 1)]),
            ("Holy Mantle", "chestplate_fur", [A(ARM, 3.0), A(TOU, 2.0), A(HOLY_R, 0.10, 1)]),
            ("Martyr's Resolve", "heart_yellow", [T(-0.15, when="hp<0.4"), HEAL(0.05, "hurt", 0.2, cooldown=100)])],
    masteries=[("Crusader", "sword_gold", [D(0.12, "melee"), A(HOLY_SP, 0.10, 1)]),
               ("Bastion of Light", "glove_diamond", [A(ARM, 0.12, 1), A(HOLY_R, 0.20, 1)]),
               ("Healer's Touch", "heart_green", [A(HEALR, 0.15), HEAL(0.04, "kill")]),
               ("Sanctuary", "potion_white_big", [T(-0.10), HEAL(0.02, "tick", cooldown=40)])],
    keystones=[("Divine Intervention", "potion_yellow_big", [AV(0.10), HEAL(0.10, "hurt", 0.15, cooldown=300), A(MS, -0.08, 1)]),
               ("Wrath of the Righteous", "sword_gold", [D(0.30, "melee"), A(HOLY_SP, 0.25, 1), T(0.12)]),
               ("Eternal Flame", "torch", [A(HOLY_SP, 0.30, 1), A(MREG, 0.30, 1), A(MANA, -0.30, 1)])]))

# ======================================================================== CLERIC (Faith) ======================================================
REGIONS.append(dict(
    key="cleric", name="Cleric", start="faith", color="7fd1b9", blurb="Support and restoration: healing power, wards, blessings and sustained recovery.",
    minors=[("Gentle Touch", "heart_green", [A(HEALR, 0.03)]), ("Calm Mind", "potion_blue_small", [A(MANA, 15.0)]),
            ("Warding", "potion_cyan", [A(SRES, 0.02, 1)]), ("Vitality", "heart_red", [A(HP, 2.0)])],
    entry=("Cleric's Calling", "potion_white", [A(MANA, 30.0), A(HEALR, 0.04)]),
    notables=[("Restoration", "potion_green", [A(HEALR, 0.08), HEAL(0.02, "tick", cooldown=60)]),
              ("Ward", "potion_cyan", [A(SRES, 0.06, 1), T(-0.04, "magic")]),
              ("Meditation", "potion_blue", [A(MREG, 0.10, 1), A(CAST, 0.05, 1)]),
              ("Prayer", "potion_white_big", [A(HOLY_SP, 0.06, 1), A(CDR, 0.03, 1)]),
              ("Cleansing Light", "potion_yellow_big", [A(HEALR, 0.05), A(HOLY_R, 0.10, 1)]),
              ("Soothing Presence", "heart_cyan", [HEAL(0.015, "tick", cooldown=40), A(HP, 4.0)]),
              ("Protective Bubble", "potion_gray", [T(-0.06), A(OVERHEAL, 0.06)]),
              ("Scholar of Mercy", "eye_green", [A(MANA, 50.0), XP(0.05)])],
    majors=[("Miracle", "heart_green", [HEAL(0.08, "hurt", 0.2, cooldown=200), A(HEALR, 0.10)]),
            ("Spirit Link", "potion_indigo", [A(MREG, 0.15, 1), HEAL(0.02, "kill")]),
            ("Warding Prayer", "potion_cyan", [A(SRES, 0.12, 1), T(-0.08, "magic")]),
            ("Overflowing Grace", "potion_green_big", [A(OVERHEAL, 0.15), A(HP, 6.0)]),
            ("Benediction", "potion_white_big", [A(CDR, 0.08, 1), A(HOLY_SP, 0.08, 1)])],
    masteries=[("Font of Life", "heart_green", [A(HEALR, 0.20), HEAL(0.03, "tick", cooldown=40)]),
               ("Archpriest", "potion_yellow_big", [A(HOLY_SP, 0.12, 1), A(MANA, 80.0)]),
               ("Warded Soul", "potion_cyan", [A(SRES, 0.18, 1), A(DODGE, 0.04)]),
               ("Tranquility", "potion_blue", [A(MREG, 0.20, 1), A(CAST, 0.08, 1)])],
    keystones=[("Martyrdom", "heart_green", [HEAL(0.04, "tick", cooldown=20), A(HEALR, 0.30), D(-0.25)]),
               ("Pillar of Grace", "potion_white_big", [A(HOLY_SP, 0.30, 1), A(CDR, 0.15, 1), A(HP, -0.15, 1)]),
               ("Ascension", "potion_yellow_big", [A(MANA, 0.40, 1), A(MREG, 0.40, 1), A(CAST, 0.10, 1), A(MS, -0.08, 1)])]))

# ======================================================================== DRUID (Faith/Arcane) ================================================
REGIONS.append(dict(
    key="druid", name="Druid", start="faith", color="5fae4b", blurb="Nature's keeper: wild magic, beast bonds, mounts, foraging and the cycle of growth.",
    minors=[("Green Thumb", "apple_green", [A(NATURE_SP, 0.03, 1)]), ("Wild Vigor", "heart_green", [A(HP, 2.0)]),
            ("Thick Bark", "chestplate_fur", [A(ARM, 1.0)]), ("Forager's Luck", "treasure_chest", [A(LUCK, 0.2)])],
    entry=("Druid's Bond", "apple_green", [A(NATURE_SP, 0.04, 1), A(HP, 2.0)]),
    notables=[("Verdant Power", "potion_green", [A(NATURE_SP, 0.07, 1), A(MANA, 25.0)]),
              ("Barkskin", "chestplate_fur", [A(ARM, 3.0), T(-0.04, "fire")]),
              ("Beast Friend", "bone", [A(SUMM, 0.08, 1), A(HP, 4.0)]),
              ("Wild Gait", "boots_leather", [A(MS, 0.05, 1), A(STEP, 0.2)]),
              ("Thorn Whip", "arrow_bronze", [D(0.06, "thorns"), A(NATURE_SP, 0.04, 1)]),
              ("Harvest Blessing", "chicken_leg", [XP(0.08, "any"), LOOT(0.04, "fishing")]),
              ("Natural Remedy", "potion_green_small", [A(HEALR, 0.08), HEAL(0.015, "tick", cooldown=40)]),
              ("Swiftwater", "boots_gold", [A(SWIM, 0.15), A(MS, 0.03, 1, when="underwater")])],
    majors=[("Heart of the Forest", "heart_green", [A(HP, 8.0), HEAL(0.02, "tick", cooldown=40)]),
            ("Companion's Strength", "bone", [A(SUMM, 0.15, 1), A(ARM, 2.0)]),
            ("Rooted", "chestplate_fur", [T(-0.10, when="stand"), A(KB, 0.3)]),
            ("Hunter's Mark", "eye_green", [D(0.10, "projectile", target="hp>0.5"), A(DRAW, 0.08)]),
            ("Mount Bond", "boots_bronze", [A(MS, 0.08, 1), A(LUCK, 0.3), JUMP(0.10)])],
    masteries=[("Archdruid", "potion_green_big", [A(NATURE_SP, 0.14, 1), A(MANA, 60.0)]),
               ("Primal Fury", "bone", [D(0.12, "melee"), A(AS, 0.05, 1), A(HP, 6.0)]),
               ("Evergreen", "heart_green", [A(HEALR, 0.18), HEAL(0.03, "tick", cooldown=40)]),
               ("One With the Wild", "apple_green", [A(DODGE, 0.05), A(MS, 0.05, 1), A(LUCK, 0.3)])],
    keystones=[("Wild Shape", "bone", [D(0.25, "melee"), A(HP, 0.20, 1), A(NATURE_SP, -0.25, 1)]),
               ("Gaia's Embrace", "potion_green_big", [A(NATURE_SP, 0.30, 1), HEAL(0.02, "tick", cooldown=20), A(ARM, -0.20, 1)]),
               ("Pack Leader", "bone", [A(SUMM, 0.40, 1), A(HP, 0.10, 1), D(-0.15)])]))

# ======================================================================== NECROMANCER (Arcane) ================================================
REGIONS.append(dict(
    key="necromancer", name="Necromancer", start="arcane", color="6b3fa0", blurb="Command the dead: summons, souls, curses and dark magic that grows stronger with every servant.",
    minors=[("Grave Whisper", "skull", [A(GNEC, 0.03, 1)]), ("Dark Pact", "potion_indigo_small", [A(MANA, 15.0)]),
            ("Servile Strength", "bone", [A(SUMM, 0.03, 1)]), ("Soul Siphon", "heart_violet", [A(MREG, 0.03, 1)])],
    entry=("Necromancer's Pact", "skull", [A(GNEC, 0.04, 1), A(SUMM, 0.04, 1)]),
    notables=[("Raise Dead", "skull", [A(SUMM, 0.08, 1), A(HP, 2.0)]),
              ("Soul Harvest", "heart_violet", [HEAL(0.02, "kill"), A(MREG, 0.06, 1)]),
              ("Curse of Frailty", "potion_black", [FX("minecraft:weakness", 5, 0, "hit", 0.3), A(GNEC, 0.05, 1)]),
              ("Bone Armor", "bone", [A(ARM, 2.0), A(TOU, 1.0)]),
              ("Dark Study", "potion_indigo", [A(ELD_SP, 0.06, 1), A(MANA, 30.0)]),
              ("Necrotic Touch", "potion_black_small", [FX("minecraft:wither", 4, 0, "hit", 0.25), D(0.04, "magic")]),
              ("Grave Chill", "void", [A(ICE_SP, 0.05, 1), A(SRES, 0.04, 1)]),
              ("Ghostly Step", "boots_leather", [A(MS, 0.04, 1), A(CMS, 0.10, 1)])],
    majors=[("Legion Master", "skull", [A(SUMM, 0.15, 1), A(GNEC, 0.08, 1)]),
            ("Soul Shield", "heart_violet", [T(-0.08), A(SRES, 0.10, 1)]),
            ("Plague Bearer", "potion_black_big", [FX("minecraft:poison", 6, 1, "hit", 0.3), D(0.08, "poison")]),
            ("Deathly Focus", "potion_indigo", [A(CDR, 0.08, 1), A(CAST, 0.08, 1)]),
            ("Harvester of Souls", "heart_black", [HEAL(0.04, "kill"), A(MANA, 40.0, by="effects/1")])],
    masteries=[("Lich's Mind", "potion_indigo_small", [A(GNEC, 0.12, 1), A(MANA, 80.0)]),
               ("Undying Servants", "bone", [A(SUMM, 0.20, 1), A(HP, 8.0)]),
               ("Soul Reaper", "skull", [D(0.10, "magic"), HEAL(0.03, "kill")]),
               ("Veil of Death", "void", [A(DODGE, 0.05), A(SRES, 0.12, 1)])],
    keystones=[("Army of the Damned", "skull", [A(SUMM, 0.50, 1), A(HP, -0.20, 1), A(MANA, 0.10, 1)]),
               ("Lichdom", "heart_black", [A(GNEC, 0.35, 1), A(MANA, 0.35, 1), A(HEALR, -0.30)]),
               ("Pact of Ash", "potion_black_big", [CONVERT(0.50, "fire", "magic"), A(SP, 0.20, 1), T(0.10, "fire")])]))

# ======================================================================== BLOOD MAGE (Arcane/Might) ===========================================
REGIONS.append(dict(
    key="bloodmage", name="Blood Mage", start="arcane", color="9b1b30", blurb="Spend life, not mana: blood spells, health-cost casting, life drain and sanguine hybrids.",
    minors=[("Crimson Study", "heart_red", [A(BLOOD_SP, 0.03, 1)]), ("Rich Blood", "heart_black", [A(HP, 2.0)]),
            ("Drain", "potion_red", [A(LIFE, 0.005)]), ("Hemomancy", "chili_pepper_red", [A(SP, 0.02, 1)])],
    entry=("Blood Mage's Rite", "heart_red", [A(BLOOD_SP, 0.04, 1), A(HP, 2.0)]),
    notables=[("Sanguine Power", "heart_red", [A(BLOOD_SP, 0.08, 1), A(LIFE, 0.01)]),
              ("Vampiric Touch", "potion_red_big", [HEAL(0.02, "hit", 0.4, cooldown=20), A(BLOOD_SP, 0.04, 1)]),
              ("Crimson Armor", "chestplate_bronze_fur", [A(ARM, 2.0), A(BLOOD_R, 0.10, 1)]),
              ("Ichor Reservoir", "potion_red", [A(MANA, 30.0), A(HP, 4.0)]),
              ("Pain Channel", "heart_violet", [A(SP, 0.04, 1, by="missinghp/0.1")]),
              ("Blood Rush", "boots_gold", [A(MS, 0.05, 1), A(CAST, 0.05, 1)]),
              ("Hexblood", "potion_black", [FX("minecraft:wither", 4, 0, "hit", 0.25), A(BLOOD_SP, 0.04, 1)]),
              ("Transfusion", "heart_green", [A(HEALR, 0.08), A(OVERHEAL, 0.05)])],
    majors=[("Lifetap", "heart_red", [HEAL(0.03, "crit", cooldown=20), A(MREG, 0.12, 1)]),
            ("Blood Barrier", "chestplate_bronze_fur", [T(-0.08, "magic"), A(BLOOD_R, 0.15, 1)]),
            ("Sanguine Focus", "potion_red_big", [A(BLOOD_SP, 0.10, 1), A(CDR, 0.06, 1)]),
            ("Crimson Dance", "boots_leather", [A(DODGE, 0.05), A(MS, 0.05, 1, when="hp<0.6")]),
            ("Vein Opener", "cross_red", [FX("minecraft:wither", 5, 1, "crit", 0.5), D(0.08, "magic")])],
    masteries=[("Hemomancer", "heart_red", [A(BLOOD_SP, 0.15, 1), A(LIFE, 0.02)]),
               ("Crimson Vitality", "heart_black", [A(HP, 10.0), HEAL(0.02, "tick", cooldown=40)]),
               ("Pain is Power", "heart_violet", [A(SP, 0.06, 1, by="missinghp/0.1"), A(ARM, 1.0, by="missinghp/0.1")]),
               ("Sanguine Tide", "potion_red_big", [A(CAST, 0.10, 1), A(CDR, 0.08, 1)])],
    keystones=[("Blood Magic", "heart_black", [RESERVE(0.30), A(SP, 0.35, 1), A(MANA, 0.30, 1)]),
               ("Crimson Covenant", "heart_red", [A(LIFE, 0.08), A(BLOOD_SP, 0.30, 1), A(HP, -0.12, 1)]),
               ("Vampire Lord", "potion_red_big", [HEAL(0.05, "hit", 0.5, cooldown=20), A(MS, 0.08, 1), A(HOLY_R, -0.50, 1)])]))

# ======================================================================== ELEMENTALIST (Arcane) ===============================================
REGIONS.append(dict(
    key="elementalist", name="Elementalist", start="arcane", color="e8772e", blurb="Fire, frost and lightning: elemental spell power, ignition, chill and storm control.",
    minors=[("Spark", "torch", [A(FIRE_SP, 0.03, 1)]), ("Frost Touch", "potion_blue_small", [A(ICE_SP, 0.03, 1)]),
            ("Static Charge", "potion_yellow_big", [A(LIGHT_SP, 0.03, 1)]), ("Attunement", "potion_indigo_small", [A(MANA, 15.0)])],
    entry=("Elementalist's Spark", "torch", [A(SP, 0.03, 1), A(MANA, 20.0)]),
    notables=[("Pyromancy", "torch", [A(FIRE_SP, 0.08, 1), A(FIRE_R, 0.10, 1)]),
              ("Cryomancy", "potion_blue", [A(ICE_SP, 0.08, 1), A(ICE_R, 0.10, 1)]),
              ("Stormcalling", "potion_yellow_big", [A(LIGHT_SP, 0.08, 1), A(LIGHT_R, 0.10, 1)]),
              ("Elemental Resonance", "potion_cyan", [A(SP, 0.05, 1), A(CDR, 0.03, 1)]),
              ("Arcane Focus", "eye_green", [A(CAST, 0.06, 1), A(MREG, 0.05, 1)]),
              ("Ember Skin", "chestplate_bronze_fur", [T(-0.08, "fire"), A(FIRE_R, 0.12, 1)]),
              ("Chill Aura", "void", [FX("minecraft:slowness", 3, 0, "hit", 0.25), A(ICE_SP, 0.04, 1)]),
              ("Conductor", "glove_gold", [A(LIGHT_SP, 0.05, 1), A(MS, 0.03, 1)])],
    majors=[("Wildfire", "chili_pepper_red", [IGNITE(0.25, 4), A(FIRE_SP, 0.10, 1)]),
            ("Permafrost", "potion_cyan_big", [FX("minecraft:slowness", 4, 1, "hit", 0.4), A(ICE_SP, 0.10, 1)]),
            ("Chain Lightning", "potion_yellow_big", [A(LIGHT_SP, 0.10, 1), A(CAST, 0.06, 1)]),
            ("Elemental Mastery", "potion_cyan", [A(SP, 0.08, 1), A(MANA, 50.0)]),
            ("Storm Shield", "potion_gray", [T(-0.08, "magic"), A(SRES, 0.10, 1)])],
    masteries=[("Inferno", "torch", [A(FIRE_SP, 0.16, 1), D(0.06, "fire")]),
               ("Glacier", "potion_cyan_big", [A(ICE_SP, 0.16, 1), A(COLD, 2.0)]),
               ("Tempest", "potion_yellow_big", [A(LIGHT_SP, 0.16, 1), A(CAST, 0.08, 1)]),
               ("Convergence", "potion_cyan", [A(SP, 0.12, 1), A(CDR, 0.08, 1)])],
    keystones=[("Avatar of Flame", "torch", [A(FIRE_SP, 0.45, 1), A(ICE_SP, -0.40, 1), A(ICE_R, -0.30, 1)]),
               ("Heart of Winter", "potion_cyan_big", [A(ICE_SP, 0.45, 1), A(FIRE_SP, -0.40, 1), A(FIRE_R, -0.30, 1)]),
               ("Eye of the Storm", "potion_yellow_big", [A(LIGHT_SP, 0.45, 1), A(CAST, 0.15, 1), A(HP, -0.15, 1)])]))

# ======================================================================== ARCANIST (Arcane) ===================================================
REGIONS.append(dict(
    key="arcanist", name="Arcanist", start="arcane", color="4aa3df", blurb="Pure magic: mana, spell power, cooldowns, cast speed and the eldritch arts.",
    minors=[("Mana Well", "potion_blue_small", [A(MANA, 20.0)]), ("Arcane Study", "eye_green", [A(SP, 0.025, 1)]),
            ("Mind's Edge", "potion_indigo_small", [A(MREG, 0.04, 1)]), ("Quick Hands", "glove_bronze", [A(CAST, 0.03, 1)])],
    entry=("Arcanist's Awakening", "eye_green", [A(MANA, 30.0), A(SP, 0.03, 1)]),
    notables=[("Spell Weaver", "potion_blue", [A(SP, 0.07, 1), A(CAST, 0.04, 1)]),
              ("Deep Reserves", "potion_cyan_big", [A(MANA, 80.0), A(MREG, 0.08, 1)]),
              ("Temporal Flow", "potion_cyan", [A(CDR, 0.06, 1), A(CAST, 0.04, 1)]),
              ("Eldritch Insight", "eye_green", [A(ELD_SP, 0.08, 1), A(ELD_R, 0.10, 1)]),
              ("Evoker's Craft", "glove_gold", [A(EVOC_SP, 0.08, 1), A(SRES, 0.05, 1)]),
              ("Ender Affinity", "void", [A(ENDER_SP, 0.08, 1), A(DODGE, 0.02)]),
              ("Spell Ward", "potion_gray", [T(-0.06, "magic"), A(SRES, 0.06, 1)]),
              ("Efficient Casting", "potion_indigo", [A(MREG, 0.08, 1), A(MANA, 30.0)])],
    majors=[("Arcane Surge", "potion_cyan_big", [A(SP, 0.10, 1, when="hp>0.8"), A(CAST, 0.06, 1)]),
            ("Hasty Chants", "glove_diamond", [A(CAST, 0.12, 1), A(CMS, 0.15, 1)]),
            ("Limitless Mind", "potion_indigo", [A(MANA, 120.0), A(MREG, 0.10, 1)]),
            ("Spell Echo", "eye_green", [A(CDR, 0.10, 1), A(SP, 0.06, 1)]),
            ("Aether Barrier", "potion_gray", [T(-0.10, "magic"), A(SRES, 0.12, 1)])],
    masteries=[("Archmage", "potion_cyan_big", [A(SP, 0.14, 1), A(MANA, 100.0)]),
               ("Chrono Mage", "potion_cyan", [A(CDR, 0.12, 1), A(CAST, 0.10, 1)]),
               ("Void Scholar", "void", [A(ENDER_SP, 0.12, 1), A(ELD_SP, 0.12, 1)]),
               ("Mana Overflow", "potion_blue", [A(MREG, 0.25, 1), A(MANA, 60.0)])],
    keystones=[("Mana Shield", "potion_cyan_big", [T(-0.30), A(MREG, -0.30, 1), A(MANA, 0.20, 1)]),
               ("Overchannel", "eye_green", [A(SP, 0.40, 1), A(CAST, -0.20, 1)]),
               ("Perfect Casting", "potion_cyan", [A(CDR, 0.30, 1), A(CAST, 0.25, 1), A(SP, -0.20, 1)])]))

# ======================================================================== SPELLBLADE (Arcane/Might) ===========================================
REGIONS.append(dict(
    key="spellblade", name="Spellblade", start="arcane", color="8e6bd6", blurb="Steel and sorcery: spell-charged weapons, elemental enchantment, mobility and hybrid scaling.",
    minors=[("Runed Edge", "sword_iron", [D(0.02, "melee")]), ("Channeled Mind", "potion_blue_small", [A(SP, 0.02, 1)]),
            ("Fluid Steps", "boots_leather", [A(MS, 0.015, 1)]), ("Mana-Fed", "potion_indigo_small", [A(MANA, 15.0)])],
    entry=("Spellblade's Union", "sword_iron", [D(0.03, "melee"), A(SP, 0.03, 1)]),
    notables=[("Fire Edge", "sword_gold", [A(FIREDMG, 2.0), A(FIRE_SP, 0.05, 1)]),
              ("Frost Edge", "sword_iron", [A(COLD, 2.0), A(ICE_SP, 0.05, 1)]),
              ("Arc Edge", "sword_bronze", [FX("minecraft:glowing", 3, 0, "hit", 0.3), A(LIGHT_SP, 0.05, 1)]),
              ("Battle Channeling", "glove_gold", [A(CAST, 0.05, 1), A(AS, 0.03, 1)]),
              ("Warded Armor", "chestplate_bronze_fur", [A(ARM, 2.0), A(SRES, 0.06, 1)]),
              ("Spell Strike", "sword_iron", [D(0.06, "melee"), A(SP, 0.04, 1)]),
              ("Blink Step", "boots_gold", [A(MS, 0.04, 1), A(ROLL_D, 0.5)]),
              ("Arcane Reserves", "potion_blue", [A(MANA, 50.0), A(MREG, 0.06, 1)])],
    majors=[("Spellsteel", "sword_gold", [D(0.10, "melee"), A(SP, 0.08, 1)]),
            ("Riposte", "glove_steel", [HEAL(0.02, "block", cooldown=30), D(0.10, "melee", when="worn:shield")]),
            ("Mana Burn", "potion_red", [D(0.10, "magic"), A(MREG, 0.10, 1)]),
            ("Aegis Weave", "potion_gray", [T(-0.08), A(SRES, 0.10, 1)]),
            ("Dancing Blades", "sword_iron", [A(AS, 0.08, 1), A(ROLL_N, 1.0)])],
    masteries=[("Battlemage", "sword_gold", [D(0.12, "melee"), A(SP, 0.12, 1)]),
               ("Runic Armor", "chestplate_bronze_fur", [A(ARM, 0.10, 1), A(SRES, 0.15, 1)]),
               ("Elemental Weapon", "torch", [A(FIREDMG, 3.0), A(COLD, 3.0)]),
               ("Phase Stride", "boots_gold", [A(DODGE, 0.05), A(MS, 0.06, 1)])],
    keystones=[("Arcane Blade", "sword_gold", [CONVERT(0.40, "melee", "magic"), A(SP, 0.30, 1), A(ATK, -0.25, 1)]),
               ("Spell Parry", "glove_steel", [HEAL(0.04, "block", cooldown=20), T(-0.15, when="worn:shield"), A(CAST, -0.15, 1)]),
               ("Transcendent Duelist", "sword_iron", [D(0.20, "melee", when="hp>0.9"), A(SP, 0.20, 1, when="hp>0.9"), T(0.10)])]))

# ======================================================================== RANGER (Finesse) ====================================================
REGIONS.append(dict(
    key="ranger", name="Ranger", start="finesse", color="3e8e5a", blurb="Bows, crossbows and the hunt: draw speed, arrow damage, elemental shots and tracking.",
    minors=[("Steady Aim", "arrow_steel", [A(ARROWD, 0.03, 1)]), ("Strong Draw", "bow_gold", [A(DRAW, 0.03, 1)]),
            ("Light Feet", "boots_leather", [A(MS, 0.015, 1)]), ("Sharp Eye", "eye_green", [CC(0.012)])],
    entry=("Ranger's Mark", "bow_gold", [A(ARROWD, 0.03, 1), A(DRAW, 0.03, 1)]),
    notables=[("Longbow Training", "bow_diamond", [A(ARROWD, 0.07, 1, when="hand:" + W("bow")), A(ARROWV, 0.08, 1)]),
              ("Crossbow Craft", "bow_emerald", [A(ARROWD, 0.07, 1, when="hand:" + W("crossbow")), A(DRAW, 0.06, 1)]),
              ("Quick Nock", "glove_bronze", [A(DRAW, 0.10, 1), A(MS, 0.02, 1)]),
              ("Eagle Eye", "eye_green", [CC(0.03), CD(0.10)]),
              ("Fletcher", "arrow_diamond", [ARROW(0.15), A(ARROWD, 0.04, 1)]),
              ("Swift Hunter", "boots_gold", [A(MS, 0.05, 1), D(0.04, "projectile")]),
              ("Poison Tips", "potion_green_small", [FX("minecraft:poison", 4, 0, "hit", 0.2), D(0.04, "projectile")]),
              ("Hunter's Instinct", "arrow_emerald", [LOOT(0.04, "mobs"), D(0.05, "projectile", target="hp>0.7")])],
    majors=[("Multishot", "arrow_diamond", [PDUP(0.15), D(-0.06, "projectile")]),
            ("Piercing Arrows", "arrow_steel", [A(APIERCE, 2.0), A(PPIERCE, 0.05)]),
            ("Ranged Dodge", "boots_leather", [A(DODGE, 0.04), A(MS, 0.04, 1)]),
            ("Marked Prey", "eye_green", [D(0.12, "projectile", target="debuffs>0"), CC(0.03)]),
            ("Elemental Shots", "arrow_bronze", [IGNITE(0.2, 4), A(COLD, 1.5), D(0.06, "projectile")])],
    masteries=[("Sharpshooter", "bow_diamond", [D(0.12, "projectile"), CD(0.15)]),
               ("Windrunner", "boots_gold", [A(MS, 0.07, 1), A(DODGE, 0.04)]),
               ("Arrowstorm", "arrow_diamond", [A(DRAW, 0.15, 1), PDUP(0.10)]),
               ("Master Tracker", "eye_green", [LOOT(0.06, "mobs"), XP(0.08, "any")])],
    keystones=[("Deadeye", "eye_green", [CC(0.15), CD(0.40), A(DRAW, -0.20, 1)]),
               ("Rain of Arrows", "arrow_diamond", [PDUP(0.40), D(-0.20, "projectile"), A(ARROWV, -0.10, 1)]),
               ("Lone Wolf", "bow_emerald", [D(0.30, "projectile", when="hp>0.8"), A(DODGE, 0.08), NOUSE(W("heavy"))])]))

# ======================================================================== ROGUE (Finesse) =====================================================
REGIONS.append(dict(
    key="rogue", name="Rogue", start="finesse", color="48484d", blurb="Daggers, shadows and critical strikes: speed, evasion, poison and the perfect backstab.",
    minors=[("Quick Fingers", "glove_bronze", [A(AS, 0.025, 1)]), ("Keen Edge", "sword_iron", [CC(0.012)]),
            ("Nimble", "boots_leather", [A(DODGE, 0.01)]), ("Venom Vial", "potion_green_small", [A(CRITD, 0.03)])],
    entry=("Rogue's Edge", "sword_iron", [A(AS, 0.03, 1), CC(0.02)]),
    notables=[("Dagger Dance", "sword_bronze", [D(0.07, "melee", when="hand:" + W("dagger")), A(AS, 0.04, 1)]),
              ("Assassinate", "skull", [CD(0.18), D(0.06, "melee", target="hp>0.8")]),
              ("Shadow Step", "boots_leather", [A(MS, 0.04, 1), A(DODGE, 0.02), A(ROLL_D, 0.5)]),
              ("Lethal Dose", "potion_green", [FX("minecraft:poison", 5, 1, "hit", 0.25), D(0.04, "poison")]),
              ("Cutpurse", "treasure_chest", [LOOT(0.04, "mobs"), A(LUCK, 0.3)]),
              ("Evasion", "boots_gold", [A(DODGE, 0.04), HEAL(0.01, "evade", cooldown=10)]),
              ("Flurry", "glove_gold", [A(AS, 0.06, 1), CC(0.02)]),
              ("Mark of Death", "cross_red", [CC(0.03, target="hp<0.5"), CD(0.10)])],
    majors=[("Backstab", "sword_gold", [CD(0.30), A(CRITC, 0.04)]),
            ("Smoke Veil", "potion_gray", [A(DODGE, 0.06), T(-0.06, "projectile")]),
            ("Deadly Poison", "potion_green_big", [FX("minecraft:poison", 6, 2, "crit", 0.5), D(0.08, "poison")]),
            ("Opportunist", "sword_bronze", [D(0.12, "melee", target="debuffs>0"), CC(0.03)]),
            ("Light as Air", "boots_gold", [A(MS, 0.08, 1), JUMP(0.15), A(ROLL_R, 0.2)])],
    masteries=[("Assassin", "skull", [CD(0.25), CC(0.05)]),
               ("Phantom", "potion_gray", [A(DODGE, 0.08), A(MS, 0.05, 1)]),
               ("Toxicologist", "potion_green_big", [D(0.12, "poison"), FX("minecraft:poison", 6, 1, "hit", 0.3)]),
               ("Blade Virtuoso", "sword_iron", [A(AS, 0.12, 1), D(0.08, "melee", when="hand:" + W("light"))])],
    keystones=[("Shadow Dance", "potion_gray", [A(DODGE, 0.15), A(AS, 0.20, 1), A(HP, -0.20, 1)]),
               ("Death Mark", "skull", [CC(0.20, target="hp>0.9"), CD(0.60, target="hp>0.9"), D(-0.15, "melee", target="hp<0.9")]),
               ("Venom Master", "potion_green_big", [FX("minecraft:poison", 8, 2, "hit", 0.6), D(0.20, "poison"), D(-0.20, "melee")])]))

# ======================================================================== WANDERER (Finesse) ==================================================
REGIONS.append(dict(
    key="wanderer", name="Wanderer", start="finesse", color="d9c36a", blurb="Traveler and explorer: speed, leaps, swimming, rolls, luck, and the freedom to go anywhere.",
    minors=[("Long Stride", "boots_leather", [A(MS, 0.015, 1)]), ("Sure Footing", "boots_bronze", [A(STEP, 0.1)]),
            ("Fortune's Favor", "treasure_chest", [A(LUCK, 0.2)]), ("Curious Mind", "eye_green", [XP(0.03, "any")])],
    entry=("Wanderer's Road", "boots_gold", [A(MS, 0.03, 1), A(LUCK, 0.2)]),
    notables=[("Leaping Heart", "boots_gold", [JUMP(0.12), A(STEP, 0.25)]),
              ("Roll With It", "glove_bronze", [A(ROLL_N, 1.0), A(ROLL_R, 0.15)]),
              ("Swimmer", "potion_blue_small", [A(SWIM, 0.25), A(MS, 0.03, 1, when="underwater")]),
              ("Treasure Hunter", "treasure_chest_gold", [LOOT(0.04, "mobs"), LOOT(0.05, "fishing"), A(LUCK, 0.3)]),
              ("Packed Light", "chicken_leg", [A(MS, 0.03, 1), XP(0.05, "any")]),
              ("Trailblazer", "boots_bronze", [A(MS, 0.05, 1), A(KB, 0.1)]),
              ("Soft Landing", "boots_leather", [T(-0.25, "fall"), JUMP(0.08)]),
              ("Cartographer", "eye_green", [XP(0.08, "any"), A(LUCK, 0.2)])],
    majors=[("Wind at Your Back", "boots_gold", [A(MS, 0.08, 1), A(STEP, 0.2)]),
            ("Dodge Master", "glove_gold", [A(ROLL_N, 1.0), A(ROLL_D, 1.0), A(DODGE, 0.03)]),
            ("Lucky Find", "treasure_chest_gold", [LOOT(0.08, "mobs"), A(LUCK, 0.5)]),
            ("Reach Beyond", "glove_diamond", [A(REACH, 1.0), A("forge:block_reach", 1.0)]),
            ("Second Wind", "heart_green", [A(HP, 6.0), HEAL(0.02, "tick", cooldown=60)])],
    masteries=[("Pathfinder", "boots_gold", [A(MS, 0.08, 1), JUMP(0.12), A(STEP, 0.25)]),
               ("Lorekeeper", "eye_green", [XP(0.12, "any"), A(XPG, 0.10)]),
               ("Fortune Seeker", "treasure_chest_gold", [LOOT(0.10, "mobs"), A(LUCK, 0.6)]),
               ("Free Spirit", "glove_bronze", [A(ROLL_N, 1.0), A(ROLL_R, 0.25), A(DODGE, 0.04)])],
    keystones=[("Nomad's Freedom", "boots_gold", [A(MS, 0.15, 1), JUMP(0.25), A(HP, -0.15, 1)]),
               ("Fortune's Fool", "treasure_chest_gold", [A(LUCK, 2.0), LOOT(0.15, "mobs"), D(-0.12)]),
               ("Windrider", "boots_leather", [A(MS, 0.10, 1), T(-1.0, "fall"), A(ARM, -0.25, 1)])]))

# ======================================================================== BRIDGES (hybrid nodes between adjacent regions) =====================
# order around the circle (clockwise): see tools/build_skilltree.py ORDER.  Each gap has an inner (minor-size) and outer (major) bridge.
BRIDGES = {
    ("spellblade", "warrior"): [("Steel and Spell", "sword_iron", [D(0.04, "melee"), A(SP, 0.04, 1)]),
                                ("Arcane Edge Training", "sword_gold", [D(0.08, "melee", when="hand:" + W("onehand")), A(SP, 0.07, 1), A(CAST, 0.04, 1)])],
    ("warrior", "berserker"): [("Battle Fury", "chili_pepper_red", [D(0.04, "melee"), A(AS, 0.03, 1)]),
                               ("Warrior's Rage", "sword_bronze", [D(0.08, "melee", when="hp<0.7"), CD(0.12), A(HP, 4.0)])],
    ("berserker", "bloodmage"): [("Blood Hunger", "heart_red", [A(LIFE, 0.01), A(BLOOD_SP, 0.03, 1)]),
                                 ("Crimson Warrior", "heart_black", [A(LIFE, 0.02), A(BLOOD_SP, 0.06, 1), D(0.06, "melee", when="hp<0.6")])],
    ("bloodmage", "necromancer"): [("Dark Blood", "heart_violet", [A(BLOOD_SP, 0.03, 1), A(GNEC, 0.03, 1)]),
                                   ("Sanguine Pact", "heart_black", [A(BLOOD_SP, 0.07, 1), A(SUMM, 0.07, 1), HEAL(0.02, "kill")])],
    ("necromancer", "arcanist"): [("Forbidden Knowledge", "potion_indigo_small", [A(GNEC, 0.03, 1), A(SP, 0.03, 1)]),
                                  ("Eldritch Dominion", "eye_green", [A(ELD_SP, 0.08, 1), A(GNEC, 0.06, 1), A(MANA, 40.0)])],
    ("arcanist", "elementalist"): [("Elemental Theory", "potion_cyan", [A(SP, 0.03, 1), A(FIRE_SP, 0.03, 1)]),
                                   ("Prismatic Mind", "potion_cyan_big", [A(SP, 0.07, 1), A(CDR, 0.05, 1), A(MANA, 40.0)])],
    ("elementalist", "druid"): [("Storm and Root", "potion_green", [A(LIGHT_SP, 0.03, 1), A(NATURE_SP, 0.03, 1)]),
                                ("Primal Elements", "potion_green_big", [A(NATURE_SP, 0.07, 1), A(FIRE_SP, 0.05, 1), A(ICE_SP, 0.05, 1)])],
    ("druid", "cleric"): [("Healing Herbs", "potion_green_small", [A(HEALR, 0.05), A(NATURE_SP, 0.03, 1)]),
                          ("Lifebloom", "heart_green", [A(HEALR, 0.12), HEAL(0.02, "tick", cooldown=40), A(NATURE_SP, 0.05, 1)])],
    ("cleric", "paladin"): [("Holy Resolve", "potion_white", [A(HOLY_SP, 0.03, 1), A(HP, 2.0)]),
                            ("Healing Crusade", "potion_yellow_big", [A(HOLY_SP, 0.07, 1), A(HEALR, 0.10), A(ARM, 2.0)])],
    ("paladin", "guardian"): [("Sworn Shield", "glove_gold", [A(ARM, 1.0), A(HOLY_R, 0.05, 1)]),
                              ("Templar's Wall", "chestplate_bronze_fur", [A(ARM, 3.0), T(-0.06), A(HOLY_SP, 0.05, 1)])],
    ("guardian", "wanderer"): [("Hardy Traveler", "boots_bronze", [A(HP, 2.0), A(MS, 0.02, 1)]),
                               ("Pack Mule", "chestplate_fur", [A(ARM, 2.0), A(KB, 0.15), A(MS, 0.04, 1)])],
    ("wanderer", "ranger"): [("Trail Hunter", "boots_leather", [A(MS, 0.02, 1), D(0.03, "projectile")]),
                             ("Wild Hunt", "arrow_bronze", [A(MS, 0.05, 1), D(0.07, "projectile"), LOOT(0.05, "mobs")])],
    ("ranger", "rogue"): [("Silent Shot", "arrow_steel", [CC(0.015), D(0.03, "projectile")]),
                          ("Ambusher", "potion_gray", [CD(0.15), D(0.07, "projectile", target="hp>0.8"), A(DODGE, 0.03)])],
    ("rogue", "spellblade"): [("Shadowed Blade", "sword_iron", [CC(0.015), A(SP, 0.03, 1)]),
                              ("Phantom Edge", "sword_gold", [CD(0.12), A(SP, 0.07, 1), A(AS, 0.05, 1)])],
}

START_ORDER = ["might", "finesse", "arcane", "faith"]
START_INFO = {
    "might": ("Oath of Might", "sword_gold", [A(ATK, 1.0), A(HP, 4.0)]),
    "finesse": ("Oath of Finesse", "boots_gold", [A(AS, 0.04, 1), A(MS, 0.02, 1)]),
    "arcane": ("Oath of the Arcane", "potion_cyan_big", [A(MANA, 40.0), A(SP, 0.04, 1)]),
    "faith": ("Oath of Faith", "heart_yellow", [A(HP, 4.0), A(HEALR, 0.06)]),
}
# clockwise ring order of the 14 regions
ORDER = ["warrior", "berserker", "bloodmage", "necromancer", "arcanist", "elementalist", "druid", "cleric", "paladin", "guardian", "wanderer", "ranger", "rogue", "spellblade"]
