"""The Wide Road (part 1): traversal, mounts, flight."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from questlib import *

CHAPTERS = []

# =============================================================== TRAVERSAL ========================================================
c = Chapter("traversal", "The Many Roads", "minecraft:leather_boots", "road", "Every way of crossing the world, and why you will keep using the old ones.", bg="traversal")
c.q("intro", "A World Worth Crossing", "minecraft:compass",
    ["You can sprint, roll, climb, glide, grapple, ride, sail, blink, recall and, eventually, fly. None of them replaces the others: horses win on roads, boats win on rivers, a grapple wins in a dungeon, a recall wins when you are late.",
     "Flight is the last thing you earn and the most fenced: it should be a reward, not a skip."],
    [check()], [xp(20)], shape="diamond", size=1.3)
c.q("roll", "Roll and Sprint", "minecraft:leather_boots", "The first movement skills cost nothing. Rolls grant a moment of safety and a good chunk of distance.", [check()], [xp(20)], deps=["intro"])
c.q("jump", "Jump and Climb", "minecraft:ladder", "Step height, jump height and better climbing add up. The Wanderer branch takes all three further.", [check()], [xp(20)], deps=["intro"])
c.q("waystone", "A Waystone Home", "waystones:waystone", "Link places you have visited. Cross-world travel is quick but only goes to the places you have already earned.", [item("waystones:waystone")], [xp(30)], deps=["roll"])
c.q("scroll", "Return Scrolls", "waystones:return_scroll", "A scroll to bring you back to the last waystone you used. A pocket-sized insurance policy.", [item("waystones:return_scroll")], [xp(40)], deps=["waystone"])
c.q("sharestone", "A Sharestone", "waystones:sharestone", "Sharestones connect in pairs: bind two points for a private shortcut.", [item("waystones:sharestone")], [xp(60)], deps=["waystone"], optional=True)
c.q("portstone", "Portstone", "waystones:portstone", "Portstones carry you from anywhere to a waystone you know. Use them to save time on the way back from an adventure.", [item("waystones:portstone")], [xp(80)], deps=["scroll"], optional=True)
c.q("glide", "Paraglider", "paraglider:paraglider", "Glide with stamina; stamina is spirit. A good glider lets you jump off a mountain and keep your dignity.", [item("paraglider:paraglider")], [xp(50)], deps=["jump"])
c.q("hook", "Grapple", "rehooked:wood_hook", "Hooks and chains: stronger materials, longer reach, harder swings. Better in a dungeon than on a mountain.", [item("rehooked:wood_hook")], [xp(50)], deps=["jump"])
c.q("hook2", "A Real Hook", "rehooked:diamond_hook", "Diamond, ender and blaze hooks carry more weight, more speed and more risk.", [item("rehooked:diamond_hook")], [xp(120)], deps=["hook"], optional=True)
c.q("bottle", "Cloud in a Bottle", "artifacts:cloud_in_a_bottle", "A double jump with real height. It is the cheapest extra dimension of movement.", [item("artifacts:cloud_in_a_bottle")], [xp(60)], deps=["jump"])
c.q("blink", "Blink", "ars_nouveau:glyph_blink", "Short teleports in combat: the best defence against a boss you cannot read yet.", [item("ars_nouveau:glyph_blink")], [xp(60)], deps=["roll"])
c.q("boat", "A Boat, a River", "minecraft:oak_boat", "Boats do not need to be fast. They need to be quiet and cheap and exactly where you need them.", [item("minecraft:oak_boat")], [xp(20)], deps=["intro"])
c.q("ship", "A Ship", "smallships:oak_cog", "A real vessel: cargo hold, cannons, sails. Oceans become routes.", [item("smallships:oak_cog")], [xp(80)], deps=["boat"])
c.q("cart", "A Cart", "astikorcarts:supply_cart", "A cart behind a mount carries more than a horse alone. It is a base on wheels.", [item("astikorcarts:supply_cart")], [xp(60)], deps=["boat"], optional=True)
c.q("recall", "Potion of Recall", "simplerecall:recall_potion", "A one-shot trip home, brewed from rare ingredients. Do not waste it.", [item("simplerecall:recall_potion")], [xp(80)], deps=["scroll"], optional=True)
c.q("loader", "Chunk Loaders", "chunkloaders:basic_chunk_loader", "Keep a base running while you are away. Small areas, big convenience.", [item("chunkloaders:basic_chunk_loader")], [xp(80)], deps=["waystone"], optional=True)
c.q("fence", "Know the Fences", "minecraft:iron_bars", ["Boss arenas, great dungeons and the Wardens' cities refuse flying mounts and flight gear: you will be dismounted at the door. Cliffs and rooftops are not a shortcut here.", "Climb in, fight through, leave by the front. It is the way the old keepers designed it."], [check()], [xp(40)], deps=["intro"])
c.q("master", "Wayfarer", "minecraft:elytra", "Ride, glide, grapple, swim and blink. You can cross anywhere; the world is smaller and better.", [check()], [xp(300), points(2)], deps=["glide", "hook", "ship", "blink", "bottle"], shape="diamond", size=1.4)
CHAPTERS.append(c)

# =============================================================== LAND AND SEA MOUNTS ==============================================
c = Chapter("mounts", "The Stable: Mounts of Aldreth", "minecraft:saddle", "road", "A mount is a partner: they have strengths, they have limits, and you will find a use for every one.", bg="mounts")
c.q("intro", "A Place in the Saddle", "minecraft:saddle",
    ["Every mount has a niche: a horse for roads, a chocobo for forests, a tusklin for hills, a ship for rivers, a hippogryph for mountains, a dragon for everything the others cannot reach.",
     "Mounts can be tamed, equipped and named. Some breed; some are found as eggs; some are earned from bosses. Do not expect every mount to feel the same."],
    [check()], [xp(20)], shape="diamond", size=1.3)
c.q("horse", "A Horse", "minecraft:saddle", "The default mount. Cheap, fast enough, carries a chest, wears armor. Tame one, saddle it, learn the controls.", [adv("minecraft:husbandry/tame_an_animal"), item("minecraft:saddle")], [xp(40)], deps=["intro"])
c.q("armor", "Horse Armor", "minecraft:diamond_horse_armor", "A little protection turns a horse into a real war mount.", [item("minecraft:iron_horse_armor")], [xp(40)], deps=["horse"])
c.q("donkey", "Pack Animals", "minecraft:chest", "Donkeys and mules carry chests. Not fast, but they never complain.", [item("minecraft:chest", 4)], [xp(25)], deps=["horse"], optional=True)
c.q("llama", "A Llama Caravan", "minecraft:lead", "Llamas follow a leader and carry a lot. A long road is easier with a string of them.", [item("minecraft:lead")], [xp(25)], deps=["horse"], optional=True)
c.q("chocobo", "A Chocobo", "chocobos:chocobo_egg", "Fast, nimble, a good jumper and happy to carry two. They hatch from nests and need greens.", [item("chocobos:chocobo_egg")], [xp(80)], deps=["horse"])
c.q("chocobo_armor", "Chocobo Barding", "chocobos:iron_chocobo_armor", "Armor for the bird who cannot afford to be hit.", [item("chocobos:iron_chocobo_armor")], [xp(60)], deps=["chocobo"], optional=True)
c.q("tusk", "Tusklin and Elephant", "alexsmobs:vine_lasso", "A vine lasso pulls a wild animal to you: tusklin, elephants and bison are strong and slow. Great on rough ground.", [item("alexsmobs:vine_lasso")], [xp(60)], deps=["chocobo"], optional=True)
c.q("camel", "Desert Mounts", "blue_skies:camel_saddle", "Camels cross sand without tiring. Crystal camels in the Blue Skies cross anything.", [item("blue_skies:camel_saddle")], [xp(70)], deps=["chocobo"], optional=True)
c.q("raptor", "Raptor Rider", "alexscaves:heavy_bone", "Vallumraptors are the fastest land mount in the deep caves; they are small, mean and loyal.", [kill("alexscaves:vallumraptor")], [xp(120)], deps=["chocobo"], optional=True)
c.q("rex", "A T. Rex", "minecraft:bone_block", "Unusual Prehistory's big predator: rideable, huge and not tame by default. For people who like to be noticed.", [kill("unusualprehistory:rex")], [xp(300), cache(4)], deps=["raptor"], optional=True, shape="hexagon")
c.q("felsteed", "The Felsteed", "minecraft:soul_lantern", "A night-black horse from a darker world: faster than any horse, harder to keep.", [kill("born_in_chaos_v1:lord_pumpkinhead")], [xp(250), cache(4)], deps=["horse"], optional=True)
c.q("board", "Straddleboard", "alexsmobs:straddle_saddle", "A surfboard saddled to a hover: crosses water and ice at speed. A fun mount, not a fast one.", [item("alexsmobs:straddle_saddle")], [xp(100)], deps=["horse"], optional=True)
c.q("sea", "Out on the Water", "smallships:oak_cog", "Boats, cogs, galleys: you can cross an ocean and carry a base across it.", [item("smallships:oak_cog")], [xp(60)], deps=["horse"])
c.q("galley", "A Galley", "smallships:acacia_galley", "A sea-going ship with oars and sails. Faster than a cog, more fragile.", [item("smallships:acacia_galley")], [xp(100)], deps=["sea"], optional=True)
c.q("strider", "Lava Strider", "minecraft:warped_fungus_on_a_stick", "A strider carries you across lava. It is a mount for exactly one place and that place is the Nether.", [item("minecraft:warped_fungus_on_a_stick")], [xp(40)], deps=["intro"], optional=True)
c.q("stable", "A Stable", "minecraft:hay_block", "A good stable keeps mounts safe. Build one with fences, a trough and a roof.", [item("minecraft:hay_block", 4)], [xp(50)], deps=["horse"], optional=True)
c.q("master", "Master of the Stable", "minecraft:golden_horse_armor", "Tame or earn five different mounts. A stable that has everything is a stable you do not need.", [check()], [xp(300), points(1)], deps=["chocobo", "sea", "armor"], shape="hexagon", size=1.3)
CHAPTERS.append(c)

# =============================================================== FLYING MOUNTS =====================================================
c = Chapter("flying", "The Sky Is a Reward", "iceandfire:hippogryph_egg", "road", "Flight is earned, rationed and fenced. That is what makes it joyful.", bg="flying")
c.q("intro", "The Order of Flight", "minecraft:feather",
    ["Flight comes in steps. First the Aether's gentle flyers, confined to the Aether. Then the overworld hippogryph, slow and honest. Then dragons, which take real work. Last, wings: the End's gift.",
     "Every step is limited: boss arenas refuse fliers, dungeons dismount you at the door, and dragons need to grow up. Flight should feel like a reward, not a bypass."],
    [check()], [xp(20)], shape="diamond", size=1.3)
c.q("aether", "Sky Pigs", "minecraft:saddle", "A flying pig, saddled, in a realm made of clouds. This flight stays in the Aether.", [adv("aether:mount_phyg")], [xp(100)], deps=["intro"])
c.q("moa", "The Moa", "aether:blue_moa_egg", "Tall, fast and a good jumper. Not flight, but a series of soaring leaps.", [adv("aether:incubate_moa")], [xp(80)], deps=["aether"], optional=True)
c.q("cow", "Flying Cow", "aether:holystone", "Cows with wings: a placid, charming mount for the Aether's islands.", [kill("aether:flying_cow")], [xp(40)], deps=["aether"], optional=True)
c.q("whale", "Aerwhale", "deep_aether:aerwhale_saddle", "A flying whale for the Aether's skies. Slow, steady and enormous.", [item("deep_aether:aerwhale_saddle")], [xp(180)], deps=["aether"], optional=True)
c.q("hippogryph", "Hippogryph", "iceandfire:hippogryph_egg", "A real flying mount for the overworld: slow, honest, limited. It tires, it cannot enter dungeons, and it will not land in boss arenas.", [item("iceandfire:hippogryph_egg")], [xp(200)], deps=["aether"], shape="hexagon")
c.q("amphithere", "Amphithere", "iceandfire:amphithere_feather", "A feathered serpent: fast in the air, uncomfortable on the ground. A hunter's mount.", [kill("iceandfire:amphithere")], [xp(250)], deps=["hippogryph"], optional=True)
c.q("subter", "Subterranodon", "alexscaves:heavy_bone", "A cave-flier. Perfect for deep caverns and surprisingly agile in the open.", [kill("alexscaves:subterranodon")], [xp(200)], deps=["hippogryph"], optional=True)
c.q("wyvern", "A Wyvern", "wyrmroost:dragon_egg", "Wyrmroost's wyverns and drakes: a family of small flyers, each with its own role and temperament.", [item("wyrmroost:dragon_egg")], [xp(250)], deps=["hippogryph"], optional=True)
c.q("hatchling", "A Dragon Hatchling", "iceandfire:dragonegg_red", "A dragon takes five stages to grow up. Early on it is a pet; late on, a mount.", [adv("iceandfire:iceandfire/dragon_egg")], [xp(300)], deps=["hippogryph"], shape="hexagon")
c.q("stage", "Stage Three", "iceandfire:dragon_flute", "At stage three your dragon is large enough to carry you. At stage five it is large enough to carry a village.", [adv("iceandfire:iceandfire/dragon_staff")], [xp(400)], deps=["hatchling"])
c.q("dragon", "A Dragon Rider", "iceandfire:dragonsteel_fire_ingot", "You are riding a dragon. It does what you tell it, within limits: it will not fight you, and you will not fly through a boss arena.", [adv("iceandfire:iceandfire/dragonarmor")], [xp(600), points(2), cache(5)], deps=["stage"], shape="octagon", size=1.5)
c.q("elytra", "Elytra", "minecraft:elytra", "End-city wings: the unrestricted, human kind of flight.", [adv("minecraft:end/elytra")], [xp(500)], deps=["dragon"], optional=True)
c.q("wings", "Dragon Wings", "icarus:black_dragon_wings", "Crafted from End materials, with a stamina bar and a rule: no flying inside the Wardens' places.", [item("icarus:black_dragon_wings")], [xp(600)], deps=["dragon"], optional=True, shape="hexagon")
c.q("fences", "The Fenced Places", "minecraft:iron_bars", "Boss arenas, mega-dungeons and Warden cities dismount you. A dragon cannot carry you over a wall that the Wardens made to be climbed.", [check()], [xp(50)], deps=["intro"])
c.q("legendary", "Sky-Walker", "minecraft:nether_star", "Ride a dragon, glide on wings, soar on a Wyrmroost wyvern. The sky is a road.", [check()], [xp(1000), points(3), cache(6)], deps=["dragon", "wings", "wyvern"], shape="diamond", size=1.6)
CHAPTERS.append(c)
