"""Main story: Act IV (Fallen Kingdoms), Act V (End of the Age), Postgame."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from questlib import *
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from custom_items import EMBER_SHARD  # noqa: E402

CHAPTERS = []

# =============================================================== ACT IV ===============================================================
c = Chapter("act4", "Act IV: Fallen Kingdoms", "minecraft:sculk_catalyst", "story", "The Wardens guarded their realms. Others, long ago, lost theirs.", bg="act4")
c.q("otherside", "The Hall of Echoes", "deeperdarker:soul_crystal", "Under the deepest cities there is a door that the Wardens never closed. Beyond it, the Otherside: a mirror of the world, drained of colour and full of listening.", [dim("deeperdarker:otherside")], [xp(250), cache(4)], deps=["act3.act3_end"], shape="diamond", size=1.3)
c.q("city", "A City Under the Stone", "minecraft:sculk_shrieker", "Ancient cities hold the best loot in the old world and the loudest enemy. Sneak, never run, and learn what a heartbeat sounds like.", [struct("minecraft:ancient_city"), adv("deeperdarker:main/find_ancient_city")], [xp(200)], deps=["otherside"])
c.q("shard", "Reinforced Echo", "deeperdarker:reinforced_echo_shard", "The shard is the key to the rest of the Otherside's deeper secrets. Take it from the deepest vault.", [item("deeperdarker:reinforced_echo_shard")], [xp(150)], deps=["city"])
c.q("warden", "The Warden of Echoes", "deeperdarker:warden_carapace",
    ["The fifth Warden did not guard a door: it guarded a silence. The thing that stalks the Otherside is both its jailer and its prisoner.",
     "Do not fight it in the open. Do not fight it twice. Do not breathe loudly."],
    [kill("minecraft:warden"), adv("deeperdarker:main/kill_warden")], [xp(900), points(2), cache(5, "Warden spoils")], deps=["shard"], shape="octagon", size=1.6)
c.q("factory", "The Ancient Factory", "cataclysm:void_forge", "A machine-fortress from a time before the Wardens: arms, cranes and a boss that was never meant to be awake.", [struct("cataclysm:ancient_factory")], [xp(200)], deps=["otherside"])
c.q("harbinger", "The Harbinger", "cataclysm:void_core", "Mechanical and merciless. Its beam sweeps the room; its legs stomp the floor. Move constantly.", [kill("cataclysm:the_harbinger"), adv("cataclysm:kill_harbinger")], [xp(800), cache(5)], deps=["factory"], shape="octagon", size=1.5)
c.q("sunken", "The Sunken City", "minecraft:prismarine_bricks", "A drowned acropolis whose guardians are older than the sea. Bring water breathing and a spear.", [struct("cataclysm:sunken_city")], [xp(200)], deps=["otherside"])
c.q("leviathan", "The Leviathan", "cataclysm:tidal_claws", "Jaws the size of a cottage, patience the size of an ocean. The Leviathan is an exam in positioning.", [kill("cataclysm:the_leviathan"), adv("cataclysm:kill_leviathan")], [xp(850), cache(5)], deps=["sunken"], shape="octagon", size=1.5)
c.q("pyramid", "Cursed Pyramid", "minecraft:sandstone", "Wadjet, then the Ancient Remnant. The desert does not forgive tomb-robbers and neither does its master.", [struct("cataclysm:cursed_pyramid")], [xp(200)], deps=["otherside"])
c.q("remnant", "The Ancient Remnant", "minecraft:chiseled_sandstone", "A sandstone titan with a hundred attacks and no patience. Bring good armor, better timing and a plan for the sandstorm.", [kill("cataclysm:ancient_remnant"), adv("cataclysm:kill_remnant")], [xp(850), cache(5)], deps=["pyramid"], shape="octagon", size=1.5)
c.q("dragon_egg", "A Dragon's Egg", "iceandfire:dragonegg_red", "The old dragons are not gone; they sleep in the mountains. An egg is a long journey: it needs warmth, fire or ice, and attention for days.", [adv("iceandfire:iceandfire/dragon_egg")], [xp(200)], deps=["act3.hippogryph"], shape="hexagon")
c.q("dragon_horn", "A Horn for a Beast", "iceandfire:dragon_horn", "The horn of a fallen dragon commands its kin. Your hatchling listens, if you have earned it.", [adv("iceandfire:iceandfire/dragon_horn")], [xp(200)], deps=["dragon_egg"])
c.q("dragon_staff", "Staff of Command", "iceandfire:dragon_flute", "A dragon is a person, not a vehicle. A staff tells it where to stand, where to guard, whom to fight. The stage of its growth decides what it can do.", [adv("iceandfire:iceandfire/dragon_staff")], [xp(200)], deps=["dragon_horn"])
c.q("fire_dragon", "The Fire Dragon", "iceandfire:dragon_skull_fire", "A mature fire dragon is the hardest thing in the open overworld. It remembers who burns it.", [kill("iceandfire:fire_dragon")], [xp(700), cache(5)], deps=["dragon_staff"], shape="octagon", size=1.5)
c.q("ride", "The Rider", "iceandfire:dragonsteel_fire_ingot", "At stage three, a dragon will carry you. Flight on dragonback is the greatest freedom in this world, and the most carefully fenced: dungeon roofs, boss arenas and the Wardens' cities refuse it.", [adv("iceandfire:iceandfire/dragonarmor")], [xp(300), points(2)], deps=["fire_dragon"], shape="hexagon", size=1.3)
c.q("wyrm", "Wyrmroost Wings", "wyrmroost:dragon_egg", "Drakes, wyverns, and stranger things: Wyrmroost's creatures are smaller than dragons and mean in different ways. Find an egg and raise something unexpected.", [item("wyrmroost:dragon_egg")], [xp(200)], deps=["ride"], optional=True)
c.q("kayra", "Keep Kayra", "minecraft:iron_bars", "Sprawling, haunted, full of bandits and worse. Dungeons Arise's great keeps hold rare gear and rarer secrets.", [struct("dungeons_arise:keep_kayra")], [xp(350), cache(5)], deps=["otherside"])
c.q("shiraz", "Shiraz Palace", "minecraft:gold_block", "A jewel-box of a palace with a bad habit of ambushes.", [struct("dungeons_arise:shiraz_palace")], [xp(350), cache(5)], deps=["otherside"], optional=True)
c.q("heavenly", "The Heavenly Challenger", "minecraft:white_glazed_terracotta", "The sky has its own challengers. Three trials, three towers; each of them taller than the last.", [struct("dungeons_arise:heavenly_challenger")], [xp(300), cache(5)], deps=["act3.aether"], optional=True)
c.q("citadel", "The Black Citadel", "minecraft:crying_obsidian", "A fortress of obsidian and old oaths, big enough to get lost in.", [struct("dungeons_enhanced:black_citadel")], [xp(350), cache(5)], deps=["otherside"])
c.q("keeping", "The Keeping Castle", "minecraft:chain", "Prodigium's great castle: a fortress with a story, a gauntlet, and a ledger of everyone who failed here.", [struct("prodigium_dungeons:keeping_castle")], [xp(350), cache(5)], deps=["otherside"], optional=True)
c.q("apostle", "The Apostle", "goety:nameless_staff", "A priest who forgot what he served. Goety's tallest boss. The tools he drops reshape any necromancer.", [kill("goety:apostle")], [xp(900), points(1), cache(5)], deps=["otherside"], shape="octagon", size=1.5)
c.q("catacombs", "Catacombs", "irons_spellbooks:cultist_helmet", "Under a collapsed keep: an entire catacomb of cultists, wraiths and one very patient king.", [adv("irons_spellbooks:irons_spellbooks/enter_catacombs")], [xp(250)], deps=["otherside"])
c.q("dead_king", "The Dead King", "irons_spellbooks:legendary_spell_book", "Hordes, then the king. Bring a tank, a healer or both. His spellbook is the first truly legendary casting tool.", [kill("irons_spellbooks:dead_king")], [xp(1000), points(2), cache(5, "Dead King spoils")], deps=["catacombs"], shape="octagon", size=1.6)
c.q("mythic", "Mythic", "apotheosis:mythic_material", "Mythic items are the pinnacle of normal drops: five affixes, full-strength bonuses, a name worth saying.", [adv("apotheosis:affix/mythic")], [xp(300), cache(5)], deps=["warden"], optional=True)
c.q("ench60", "A Level 60 Table", "apotheosis:infused_hellshelf", "High-tier shelves multiply your options. Chase rare enchantments, treasure enchantments and the long tail.", [adv("apotheosis:enchanting/60ench")], [xp(300)], deps=["act2.gear30"], optional=True)
c.q("act4_end", "Seven Roads, Three Open", "minecraft:crying_obsidian",
    ["The Warden of Echoes is down, and the Harbinger. The factory's machines speak of one more place: not a realm but an ending, hung in a darkness above everything.",
     "Four Wardens have fallen. Three realms remain. The Ember has grown large enough to see by."],
    [check()], [item_r(EMBER_SHARD, 4), xp(500), points(3), cache(5, "Act IV cache")], deps=["warden", "harbinger", "leviathan", "remnant"], shape="diamond", size=1.3)
CHAPTERS.append(c)

# =============================================================== ACT V ================================================================
c = Chapter("act5", "Act V: The End of the Age", "minecraft:dragon_egg", "story", "The Hollow Crown was never broken. It was split, to be gathered by someone willing to finish what the Wardens started.", bg="act5")
c.q("end", "The End", "minecraft:end_stone", "Every old story ends here. The stronghold portal is open for you now; the thing waiting is no longer asleep.", [dim("end")], [xp(300), cache(5)], deps=["act4.act4_end"], shape="diamond", size=1.3)
c.q("city", "A City at the Edge", "minecraft:purpur_block", "End cities hold shulkers, elytra and the first honest glimpse of what comes next.", [struct("minecraft:end_city"), adv("minecraft:end/find_end_city")], [xp(250)], deps=["end"])
c.q("shell", "Shell of the Ender", "minecraft:shulker_shell", "Shulker shells make the greatest travel storage in the world. They are also very annoying to collect.", [item("minecraft:shulker_shell", 4)], [xp(150)], deps=["city"])
c.q("elytra", "Wings Earned", "minecraft:elytra", "Real, unrestricted wings: the last, quickest, loneliest form of flight. Earned only here, only at this price.", [adv("minecraft:end/elytra")], [xp(500), points(2)], deps=["city"], shape="hexagon", size=1.4)
c.q("guardian", "The Ender Guardian", "cataclysm:void_core", "A construct of the End, stranger than the dragon and less merciful. It guards a vault the Wardens never knew existed.", [kill("cataclysm:ender_guardian"), adv("cataclysm:kill_ender_guardian")], [xp(1000), cache(6)], deps=["city"], shape="octagon", size=1.5)
c.q("wither", "The Withered One", "minecraft:nether_star", "A star made of sorrow. Summon it somewhere you can afford to lose.", [kill("minecraft:wither"), adv("minecraft:nether/summon_wither")], [xp(800), cache(5)], deps=["end"], shape="octagon", size=1.4)
c.q("beacon", "A Light for the Dark", "minecraft:beacon", "Beacons light the way for allies, for ships and for gods. A full pyramid is a statement.", [adv("minecraft:nether/create_full_beacon")], [xp(400)], deps=["wither"])
c.q("dragon", "The Warden of the End", "minecraft:dragon_head",
    ["The last Warden has become the thing it guarded. The Ender Dragon is what happens when duty is left alone for ten thousand years.",
     "Its breath is slow and brutal, its dives merciless. Take the crystals first. Always take the crystals first."],
    [kill("minecraft:ender_dragon"), adv("minecraft:end/kill_dragon")], [xp(2000), points(3), cache(6, "Dragon spoils")], deps=["guardian", "beacon"], shape="octagon", size=1.7)
c.q("egg", "An Egg of Quiet", "minecraft:dragon_egg", "It does not hatch. It does not need to. It sits and hums a note only the Ember can hear.", [item("minecraft:dragon_egg")], [xp(500)], deps=["dragon"])
c.q("pearl", "A Pearl Between Worlds", "gateways:gate_pearl", "Gate pearls open arenas of waves. Beyond the story is the long game: gateways, superbosses, and everything you skipped.", [item("gateways:gate_pearl")], [xp(200)], deps=["dragon"], optional=True)
c.q("wings", "The Last Wings", "icarus:black_dragon_wings", "Wing-gear that is not an elytra: craftable only from End materials, only with Ember-fire. They glide, they hover, they have a stamina bar. This is the fastest way to cross the world.", [item("icarus:black_dragon_wings")], [xp(600)], deps=["elytra"], optional=True, shape="hexagon")
c.q("crown", "The Hollow Crown", "minecraft:beacon",
    ["The Crown was never destroyed. It was split into seven sigils and left with seven Wardens, so that no single hand could hold it. You hold all seven now. They are warm, and they are heavy.",
     "Set them in the ring of a beacon, and the Ember will do the rest."],
    [check()], [xp(1000), points(3), cache(6)], deps=["dragon", "act4.warden", "act3.sun", "act2.ur_ghast"], shape="diamond", size=1.5)
c.q("ending", "End of the Age", "minecraft:nether_star",
    ["The Crown rekindles. The seven realms do not heal at once, but they stop dying. The sky is, for a moment, exactly the colour it should be.",
     "You are no longer an ordinary adventurer. The road still goes on; the Wardens are gone, but their enemies are not. The Postgame begins where the story stops."],
    [check()], [xp(2000), points(5), cache(6, "Ending cache")], deps=["crown"], shape="diamond", size=1.8)
CHAPTERS.append(c)

# =============================================================== POSTGAME ============================================================
c = Chapter("postgame", "Postgame: The Long Dark After", "minecraft:totem_of_undying", "story", "The Crown is whole and the world is still dangerous. This is where legends are measured.", bg="postgame")
c.q("start", "A Quieter World", "minecraft:totem_of_undying", "Peace is just the interval between disasters. The Ember keeps burning; it knows there are things left to do.", [check()], [xp(200)], deps=["act5.ending"], shape="diamond", size=1.3)
c.q("maledictus", "Maledictus", "cataclysm:witherite_ingot", "A cursed warrior in the Cursed Pyramid's deepest vault; strong, fast, hateful. Cataclysm's hardest early superboss.", [kill("cataclysm:maledictus"), adv("cataclysm:kill_maledictus")], [xp(1500), cache(6)], deps=["start"], shape="octagon", size=1.6)
c.q("scylla", "Scylla", "cataclysm:abyssal_egg", "The siren-queen of the abyssal depths. Her storms are the longest in any fight in the game.", [kill("cataclysm:scylla"), adv("cataclysm:kill_scylla")], [xp(1500), cache(6)], deps=["start"], shape="octagon", size=1.6)
c.q("all_cata", "All Cataclysm", "cataclysm:gauntlet_of_guard", "Every boss from the Nether to the sea. A rare completion, and the gear to prove it.", [adv("cataclysm:kill_all_bosses")], [xp(2000), points(2), cache(6)], deps=["maledictus", "scylla"], shape="hexagon", size=1.5)
c.q("lich_bomd", "The Obsidilith", "minecraft:obsidian", "A towering monolith in the End's void, summoned and sealed behind obsidian. Its beams repeat and escalate.", [kill("bosses_of_mass_destruction:obsidilith")], [xp(1200), cache(6)], deps=["start"], optional=True)
c.q("void_blossom", "The Void Blossom", "bosses_of_mass_destruction:void_blossom", "A lotus in a hole in the world. Its petals are spears; its heart is a sapphire.", [kill("bosses_of_mass_destruction:void_blossom")], [xp(1200), cache(6)], deps=["start"], optional=True)
c.q("gauntlet", "The Gauntlet", "minecraft:chain", "A floating fist in a cave of chains. The only thing worse than its punches is the wait between them.", [kill("bosses_of_mass_destruction:gauntlet")], [xp(1200), cache(6)], deps=["start"], optional=True)
c.q("dread", "The Dread Lich", "minecraft:wither_skeleton_skull", "Ice and Fire's dread lich is a siege boss: a wave of wights, a king, and a very large number of ways to die.", [kill("iceandfire:dread_lich")], [xp(1200), cache(6)], deps=["start"], optional=True)
c.q("hydra_if", "The Hydra of Fire and Flood", "minecraft:dragon_head", "Its heads regenerate. Its fire spreads. It is the largest non-dragon beast in the game.", [kill("iceandfire:hydra")], [xp(800), cache(5)], deps=["start"], optional=True)
c.q("ice_dragon", "The Ice Dragon", "iceandfire:dragonsteel_ice_ingot", "The cold sister. Its glaciers are an obstacle; its steel is a reward.", [kill("iceandfire:ice_dragon")], [xp(1000), cache(6)], deps=["start"], optional=True)
c.q("ancient", "Ancient", "apotheosis:ancient_material", "Past mythic lies the rarest tier of loot. Items here are not found, they are inherited: only the most dangerous places drop them.", [adv("apotheosis:affix/ancient")], [xp(2000), points(2), cache(6)], deps=["start"], shape="hexagon")
c.q("ancient_gem", "An Ancient Gem", "apotheosis:gem_fused_slate", "The strongest gems are earned by killing the strongest things.", [adv("apotheosis:affix/ancient_gem")], [xp(1500)], deps=["ancient"], optional=True)
c.q("ench100", "A Level 100 Table", "apotheosis:ender_library", "The final shelves. Enchantments here go beyond max level, with a cost.", [adv("apotheosis:enchanting/100ench")], [xp(1500), points(1)], deps=["ancient"], optional=True)
c.q("heroism", "Hero of the Village", "minecraft:emerald_block", "Protect a village from a raid and the villagers will remember. It is a small honour. It is also, in its way, the biggest.", [adv("minecraft:adventure/hero_of_the_village")], [xp(500), points(1)], deps=["start"], optional=True)
c.q("all_mobs", "Every Last One", "minecraft:wither_skeleton_skull", "Kill every hostile mob in the base game. The modded ones will come eventually.", [adv("minecraft:adventure/kill_all_mobs")], [xp(1000)], deps=["start"], optional=True)
c.q("potions", "A Good Drink", "minecraft:brewing_stand", "Get every potion effect at least once. Many of them are useful, some of them are wonderful.", [adv("minecraft:nether/all_potions")], [xp(800)], deps=["start"], optional=True)
c.q("pearl_arena", "Wave Defense", "gateways:gate_pearl", "Gate pearls summon arenas of enemies in waves. Rewards scale with the arena. Do not attempt the last wave without all your potions.", [item("gateways:gate_pearl", 3)], [xp(600)], deps=["start"], optional=True)
c.q("legend", "Legend", "minecraft:nether_star",
    ["There are builds and then there are legends. Stand in front of the skill tree and count: how many keystones can you put in one character, and what does each one cost you?",
     "That question has no end; that is the point."],
    [check()], [xp(3000), points(5), cache(6, "Legend cache")], deps=["all_cata", "ancient"], shape="diamond", size=1.8)
CHAPTERS.append(c)
