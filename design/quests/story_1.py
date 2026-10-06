"""Main story, Prologue and Act I."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from questlib import *
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from custom_items import EMBER_SHARD  # noqa: E402

CHAPTERS = []

# =============================================================== PROLOGUE ==============================================================
c = Chapter("prologue", "Prologue: The Ember Wakes", "minecraft:blaze_powder", "story", "You wake beside a cold hearth with a shard of crown-glass burning in your palm.", bg="prologue")
c.q("spark", "A Spark in the Ash", "minecraft:flint_and_steel",
    ["The fire is out. The world is quiet in the wrong way, like a bell that has just stopped ringing.",
     "In your hand: a sliver of crown-glass, warm as a living thing. The old tales called it an Ember. They said the Hollow Crown shattered and the pieces went looking for someone stubborn enough to carry them."],
    [check()], [xp(10)], shape="diamond", size=1.2)
c.q("blood", "Remember Your Blood", "minecraft:player_head",
    ["Every people of Aldreth carries a gift and a burden. Open the origin screen and choose the blood you were born to. There is no wrong answer, only different roads.",
     "Elf, dwarf, orc, halfling, hexblood, scaleborn, wisp-touched or plain Emberborn human: the Ember does not care."],
    [check()], [xp(15)], deps=["spark"])
c.q("constellation", "The Constellation of Embers", "minecraft:enchanted_book",
    ["Press the skill tree key (K by default). Four Oaths hang at the heart of the sky: Might, Finesse, the Arcane and Faith. Choose one to begin. The Constellation is large; you will never fill it. Choose what you are, not what you could be.",
     "Spend experience to light your first star. Later you may unlearn a path with an Amnesia Scroll, at a small cost."],
    [check()], [xp(20), points(1)], deps=["blood"], shape="hexagon")
c.q("tools", "First Tools", "minecraft:crafting_table",
    "A table, a pick, a place to sleep. Every legend started with someone bad at all three.", [item("minecraft:crafting_table")], [xp(15), item_r("minecraft:torch", 8)], deps=["spark"])
c.q("roll", "Roll With It", "minecraft:leather_boots",
    ["You can dodge-roll. Press the roll key (see Controls) to tumble out of danger; rolling grants brief invulnerability but costs a recharge.",
     "Heavy armor and heavy weapons make rolls slower, a good reason to choose your kit carefully."],
    [check()], [xp(15)], deps=["tools"])
c.q("hunger", "Something Hot", "minecraft:bread",
    "Hunger is the oldest enemy. Bake bread or cook meat; many foods give small lasting boons while you stay fed.", [item("minecraft:bread", 3)], [xp(15), item_r("minecraft:cooked_beef", 4)], deps=["tools"])
c.q("blade", "A Blade for the Road", "minecraft:stone_sword",
    ["Swords, axes, spears, hammers, daggers: the world is full of weapons and each class fights differently. Combat is directional and has weight, so learn the swing before the swing learns you.",
     "Your first choice of weapon will matter less than you think. Your tenth will matter more."],
    [item("minecraft:stone_sword")], [xp(20)], deps=["tools"])
c.q("first_blood", "First Blood", "minecraft:zombie_head",
    "Night brings the hollow things up out of the earth. Put three of them back.", [kill("minecraft:zombie", 3)], [xp(30), item_r("minecraft:iron_ingot", 4)], deps=["blade"])
c.q("shelter", "Four Walls", "minecraft:red_bed",
    "A bed sets your spawn and skips the night. A roof keeps you alive until you can afford to be brave.", [item("minecraft:red_bed")], [xp(20)], deps=["hunger", "roll"])
c.q("waystone", "Mark the Road", "waystones:waystone",
    ["Waystones remember where you have been. Build one at home and others will answer as you find them in the wild, letting you travel between the places you have marked."],
    [item("waystones:waystone")], [xp(30)], deps=["shelter", "first_blood"], shape="hexagon")
c.q("village", "Smoke on the Horizon", "minecraft:bell",
    "Chimney smoke means people. Find a village and listen to what the traders say: there are old ruins beyond the hills, and strange lights over them.", [struct("minecraft:village_plains")], [xp(40), item_r("minecraft:emerald", 3)], deps=["waystone"])
c.q("road_calls", "The Road Calls", "minecraft:compass",
    ["You have a hearth, a blade, a name and a direction. The Ember in your palm is pulling west, toward a ruin the traders will not name.",
     "Take what you can carry. Everything past this point has teeth."],
    [check()], [xp(100), points(2), cache(1, "Prologue supply cache")], deps=["village"], shape="diamond", size=1.3)
CHAPTERS.append(c)

# =============================================================== ACT I ================================================================
c = Chapter("act1", "Act I: The Awakening", "minecraft:iron_sword", "story", "The Ember wants fuel. The old ruins are full of it, and so are the things that guard them.", bg="act1")
c.q("descent", "Into the Dark", "minecraft:iron_pickaxe",
    "Every kingdom is built on what somebody dug up. Find a mineshaft, take what is useful, and remember where the exits are.", [struct("minecraft:mineshaft")], [xp(40)], deps=["prologue.road_calls"], shape="diamond")
c.q("iron", "A Crack in the Stone", "minecraft:iron_ingot",
    "Iron is the first honest metal: heavy, plentiful, unromantic. You will need a lot of it.", [item("minecraft:iron_ingot", 16)], [xp(30)], deps=["descent"])
c.q("forge", "A Proper Forge", "minecraft:blast_furnace",
    "A blast furnace doubles smelting speed. Rarer metals will want it.", [item("minecraft:blast_furnace")], [xp(30)], deps=["iron"])
c.q("armor", "Iron Shell", "minecraft:iron_chestplate",
    "Armor is not cowardice. It is the decision to still be standing when the second blow lands.", [item("minecraft:iron_chestplate")], [xp(40), item_r("minecraft:shield")], deps=["forge"])
c.q("ruin", "The Ruin That Hums", "minecraft:mossy_stone_bricks",
    ["West of the village the traders pointed to: a temple half-swallowed by roots, still humming a note too low to hear.",
     "Structures hold better loot the harder they are to reach, and the rarer they are. Small ruins give supplies; dungeons give gear; the great fortresses give legends."],
    [struct("dungeons_arise:abandoned_temple")], [xp(60), cache(1)], deps=["armor"], shape="hexagon")
c.q("dungeon", "Down the Stairs", "minecraft:spawner",
    "Skeletons, spiders, zombies: three old rooms, three old grudges. Break a dungeon and see what the dark was hoarding.", [struct("betterdungeons:small_dungeon")], [xp(50)], deps=["armor"])
c.q("bandits", "The Bandit Towers", "minecraft:crossbow",
    "Somebody has been robbing the caravans. Their towers are tall and badly defended.", [struct("dungeons_arise:bandit_towers"), kill("minecraft:pillager", 5)], [xp(60), item_r("minecraft:arrow", 32)], deps=["ruin"])
c.q("salvage", "Nothing Wasted", "apotheosis:salvaging_table",
    ["Gear you cannot use is not worthless. Apotheosis lets you break items down into rarity-tinted materials: common, uncommon, rare, and beyond.",
     "Those materials are your currency for everything that follows: reforging, socketing, augmenting."],
    [item("apotheosis:salvaging_table")], [xp(40), item_r("apotheosis:common_material", 8)], deps=["dungeon"])
c.q("gem", "A Glimmer of Power", "apotheosis:gem",
    ["Gems are the first gift of the dungeons: small, socketable, strangely heavy. Each carries a bonus keyed to the kind of item it sits in. Find a socketed item; the sigil of socketing opens more slots."],
    [item("apotheosis:gem")], [xp(50)], deps=["salvage"])
c.q("socket", "Set in Stone", "apotheosis:sigil_of_socketing",
    "A socket is a promise. Fill it with something you believe in.", [item("apotheosis:sigil_of_socketing")], [xp(50)], deps=["gem"])
c.q("enchant", "The Table Hums", "minecraft:enchanting_table",
    "Your first enchantment will be small and a little disappointing. Your hundredth will redefine your build. Shelves around the table raise the ceiling; bring many.", [item("minecraft:enchanting_table")], [xp(40)], deps=["armor"])
c.q("enchanted", "Something Extra", "minecraft:enchanted_book",
    "Enchant an item. Read the description: every enchantment here explains itself.", [adv("minecraft:story/enchant_item")], [xp(60), item_r("apotheosis:hellshelf", 4)], deps=["enchant"])
c.q("scroll", "A Whisper on Paper", "irons_spellbooks:scroll",
    ["Magic is not a different game; it is a different grip. Scrolls hold a single spell each. Cast one to learn what the school feels like.",
     "Spells use mana and have cooldowns. Your skill tree and gear decide how much of each you have."],
    [item("irons_spellbooks:scroll")], [xp(40)], deps=["ruin"])
c.q("inscribe", "Ink and Intention", "irons_spellbooks:inscription_table",
    "An inscription table writes spells onto spellbooks. A book holds many spells at once; a scroll only one.", [item("irons_spellbooks:inscription_table")], [xp(40)], deps=["scroll"])
c.q("book", "A Book of Your Own", "irons_spellbooks:copper_spell_book",
    "Spellbooks are your focus. Tier decides slots, and each rarity of book unlocks more. Copper is where everyone begins.", [item("irons_spellbooks:copper_spell_book")], [xp(50)], deps=["inscribe"])
c.q("anvil", "The Arcane Anvil", "irons_spellbooks:arcane_anvil",
    "Spells can be upgraded: the Arcane Anvil merges scrolls and imbues weapons, and is the beginning of spellblade work.", [item("irons_spellbooks:arcane_anvil")], [xp(50)], deps=["book"])
c.q("friend", "A Friend with Hooves", "minecraft:saddle",
    ["Horses are the oldest mount and the first good one. Find a wild horse, tame it, and ride. They carry a chest, wear armor, and will not abandon you in a fight.",
     "Much faster, stranger and far larger mounts wait for you later. Keep your first horse. It earned the right."],
    [adv("minecraft:husbandry/tame_an_animal"), item("minecraft:saddle")], [xp(60), item_r("minecraft:golden_carrot", 8)], deps=["prologue.village"])
c.q("glider", "A Leaf for the Wind", "paraglider:paraglider",
    "Gliding spends stamina but costs nothing else. Cliffs become runways; chasms become shortcuts. Stamina grows with spirit orbs found in shrines.", [item("paraglider:paraglider")], [xp(60)], deps=["friend"])
c.q("hook", "A Hook and a Prayer", "rehooked:wood_hook",
    "Hooks and chains: swing, climb, cross gaps. Better hooks use better chains and stronger materials.", [item("rehooked:wood_hook")], [xp(50)], deps=["glider"])
c.q("keep", "The Quiet Keep", "minecraft:iron_door",
    "Old castles are earned: the walls are thick, the guards have not slept in years. This keep stands near the ruined portal north of the village.", [struct("dungeons_enhanced:castle")], [xp(80), cache(2)], deps=["bandits"], shape="hexagon")
c.q("hollow_knight", "The Wrought Chamber", "minecraft:iron_block",
    ["There is a vault under the hills that was sealed from the inside. The thing within does not sleep; it waits to be asked politely.",
     "Ferrous Wroughtnaut is a test: big hits, long windups, a pattern you can learn. Roll, wait, strike. If it falls, the dungeons will start to feel small."],
    [kill("mowziesmobs:ferrous_wroughtnaut", 1)], [xp(250), points(2), cache(2, "Wroughtnaut spoils")], deps=["keep", "anvil"], shape="octagon", size=1.5)
c.q("shield", "Shield Wall", "minecraft:shield",
    "Block with a raised shield at the right moment and the enemy staggers. Shields are a build of their own: Guardian and Paladin nodes love them.", [item("minecraft:shield")], [xp(30)], deps=["armor"], optional=True)
c.q("bow", "From a Distance", "minecraft:bow",
    "Bows reward patience: draw speed, arrow damage and crit chance all scale in the Ranger branch.", [item("minecraft:bow")], [xp(30)], deps=["prologue.tools"], optional=True)
c.q("act1_end", "What the Ember Wants", "minecraft:blaze_powder",
    ["The Wroughtnaut's chamber holds a tablet in a language that predates the Crown. You can read it, which is odd: Seven Wardens bound seven realms to the Crown, and the realms are waking.",
     "Westward is a forest where it is always dusk. The tablet calls it the Root Ward. The Ember in your palm burns hot at the name."],
    [check()], [item_r(EMBER_SHARD, 3), xp(150), points(2)], deps=["hollow_knight"], shape="diamond", size=1.3)
CHAPTERS.append(c)
