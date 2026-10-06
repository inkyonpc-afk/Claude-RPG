"""Main story, Act II (A Wider World) and Act III (Beyond the Veil)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from questlib import *

CHAPTERS = []

# =============================================================== ACT II ===============================================================
c = Chapter("act2", "Act II: A Wider World", "minecraft:ender_pearl", "story", "The tablet named seven Wardens. The first of them kept a forest where it is always dusk.", bg="act2")
c.q("portal", "Where the Sun Forgot", "twilightforest:twilight_portal_miniature_structure",
    ["The Root Ward is not far: a pool ringed with flowers, a gemstone dropped in, and the world tilts. Beyond is a forest under a sky that never finishes its sunset.",
     "Things are very large there and very old. Bring armor, food and patience."],
    [dim("twilightforest:twilight_forest")], [xp(120), cache(2)], deps=["act1.act1_end"], shape="diamond", size=1.3)
c.q("hollow", "Hollow Hill", "minecraft:mossy_cobblestone", "Burrows in the hillsides hold treasure and things that guard it. Start with the small ones.", [struct("twilightforest:small_hollow_hill")], [xp(60)], deps=["portal"])
c.q("ironwood", "Ironwood", "twilightforest:ironwood_ingot", "A tree that remembers iron. The first honest material of the Twilight.", [item("twilightforest:ironwood_ingot", 4)], [xp(50)], deps=["hollow"])
c.q("naga", "The Courtyard Serpent", "twilightforest:naga_scale",
    ["The Naga coils through a courtyard of broken stone. It is the Root Warden's first mistake: the oldest, tiredest guardian, still doing its duty.",
     "Strafe, don't retreat; the tail hits harder than the head."],
    [struct("twilightforest:naga_courtyard"), kill("twilightforest:naga")], [xp(200), points(1), cache(2)], deps=["ironwood"], shape="octagon", size=1.4)
c.q("scales", "Serpent Scale", "twilightforest:naga_chestplate", "Naga scales make armor that remembers how to turn a blow. It is worth the several fights it takes.", [item("twilightforest:naga_scale", 6)], [xp(70)], deps=["naga"])
c.q("labyrinth", "Down the Labyrinth", "minecraft:oak_trapdoor", "A maze under the hills, built to be forgotten. The Minoshroom waits at its heart, and the cheese is not worth the trouble.", [struct("twilightforest:labyrinth")], [xp(80)], deps=["scales"])
c.q("minoshroom", "The Minoshroom", "twilightforest:minoshroom_trophy", "Half bull, half toadstool, entirely angry. Its axe is the first great weapon you will earn from a Warden's guards.", [kill("twilightforest:minoshroom")], [xp(220), cache(3)], deps=["labyrinth"], shape="octagon", size=1.4)
c.q("lichtower", "A Tower That Hums", "minecraft:purple_stained_glass", "The Lich keeps a tower of floors and spawners, each stronger than the last. Make your way up; the stairs are the easy part.", [struct("twilightforest:lich_tower")], [xp(100)], deps=["minoshroom"])
c.q("lich", "King of the Dead Hours", "twilightforest:lich_trophy",
    ["The Lich clones itself, fires bolts, and steals any hope you had of a clean fight. Its scepters are the first in a family of great magical weapons.",
     "Kill the clones. Reflect the bolts. Do not stand still."],
    [kill("twilightforest:lich"), adv("twilightforest:progress_lich")], [xp(300), points(2), cache(3, "Lich spoils")], deps=["lichtower"], shape="octagon", size=1.5)
c.q("knightmetal", "Knightmetal", "twilightforest:knightmetal_ingot", "The Knight Phantoms kept their armor when they lost everything else. It is a good metal: green-black, heavy, and a little too loyal.", [item("twilightforest:knightmetal_ingot", 6)], [xp(80)], deps=["lich"])
c.q("hydra", "The Hydra's Lair", "twilightforest:hydra_trophy", "Three heads, then four, then seven. Burn the stumps. The lair is a volcano of fire and bad decisions.", [struct("twilightforest:hydra_lair"), kill("twilightforest:hydra")], [xp(350), cache(4)], deps=["knightmetal"], shape="octagon", size=1.5)
c.q("nether", "The Land Below", "minecraft:netherrack",
    ["The Seven Wardens bound seven realms, and the Nether is the one that never forgave them. It burns, but not for the Warden's reasons.",
     "Bring fire resistance, a good bow, and a route back: Waystones will not follow you through the portal."],
    [dim("nether")], [xp(100)], deps=["scales"], shape="diamond")
c.q("fortress", "Brick and Cinder", "minecraft:nether_bricks", "Fortresses guard blaze spawners and little else. Take the rods; leave the wither skeletons their dignity.", [struct("minecraft:fortress")], [xp(80), item_r("minecraft:blaze_rod", 4)], deps=["nether"])
c.q("bastion", "Gold and Pigs", "minecraft:gilded_blackstone", "Piglins build bastions to hold their gold and their grudges. Wear something gold, and bring a lot of arrows.", [struct("minecraft:bastion_remnant")], [xp(90)], deps=["nether"])
c.q("debris", "Ancient Debris", "minecraft:ancient_debris", "Netherite is not mined so much as persuaded. Dig low, listen to the lava, and come home.", [item("minecraft:ancient_debris", 4)], [xp(80)], deps=["fortress"])
c.q("netherite", "A Heavier Metal", "minecraft:netherite_ingot", "Netherite is a plateau, not a summit. The gear beyond it makes it look like an apprenticeship.", [item("minecraft:netherite_ingot")], [xp(150), cache(3)], deps=["debris", "bastion"], shape="hexagon")
c.q("ur_ghast", "The Tower Beyond Twilight", "twilightforest:ur_ghast_trophy", "The Ur-Ghast floats in a tower of bad ideas. It weeps; it is in pain. The kind thing is to make it stop.", [kill("twilightforest:ur_ghast"), adv("twilightforest:progress_ur_ghast")], [xp(400), points(2), cache(4, "Ur-Ghast spoils")], deps=["hydra", "netherite"], shape="octagon", size=1.5)
c.q("undergarden", "Beneath the Roots", "minecraft:deepslate", "A second world sits under the first. The Undergarden is cold, humid and full of things that evolved without sunlight.", [dim("undergarden:undergarden")], [xp(120)], deps=["scales"], shape="diamond")
c.q("cloggrum", "Cloggrum", "undergarden:cloggrum_ingot", "Wet metal, strange alloy. Surprisingly good armor.", [item("undergarden:cloggrum_ingot", 8)], [xp(80)], deps=["undergarden"])
c.q("guardian", "The Forgotten Guardian", "undergarden:forgotten_ingot", "Something was left to guard a gate and never told when to stop. It has not stopped.", [kill("undergarden:forgotten_guardian")], [xp(350), cache(4)], deps=["cloggrum"], shape="octagon", size=1.5)
c.q("cart", "Wheels", "astikorcarts:animal_cart", "A cart behind a horse changes everything: more cargo, same mount. Plows and supply wagons come next.", [item("astikorcarts:animal_cart")], [xp(60)], deps=["portal"], optional=True)
c.q("chocobo", "A Very Fast Bird", "chocobos:chocobo_nest", "Chocobos are the best land mount you can get before the sky opens: fast, quick to jump, willing to carry a second rider. They need nests, greens, and a good reputation.", [item("chocobos:chocobo_nest")], [xp(90), item_r("chocobos:leather_chocobo_armor")], deps=["portal"])
c.q("tusk", "Giants of the Plains", "alexsmobs:vine_lasso", "Elephants and tusklin are mounts for people who prefer arrival to speed. Lasso one, saddle it, and ride; they plow through anything.", [item("alexsmobs:vine_lasso")], [xp(80)], deps=["chocobo"], optional=True)
c.q("sea", "Out on the Water", "smallships:oak_cog", "A cog is a floating base: cargo, cannons and a very large number of ways to sink. Seas are not obstacles any more; they are roads.", [item("smallships:oak_cog")], [xp(80)], deps=["cart"])
c.q("iron_book", "Iron-Bound", "irons_spellbooks:iron_spell_book", "More slots, more spells, more ways to be wrong in public. Upgrade your book as you learn what you actually use.", [item("irons_spellbooks:iron_spell_book")], [xp(80)], deps=["act1.book"], optional=True)
c.q("gear30", "A Level 30 Table", "apotheosis:hellshelf", "Hellshelves, seashelves and endshelves raise the ceiling of your enchanting table. Climb: the real enchantments live above level 30.", [adv("apotheosis:enchanting/30ench")], [xp(120)], deps=["fortress"], optional=True)
c.q("rare", "A Rare Find", "apotheosis:rare_material", "Rare gear carries three affixes and a real identity. It will not replace itself in ten minutes: invest in it.", [adv("apotheosis:affix/rare")], [xp(120), cache(3)], deps=["gear30"], optional=True)
c.q("act2_end", "The Veil Has Edges", "minecraft:nether_star",
    ["Five Wardens remain. Each held a realm: Sky, Dream, Echo, Flame, End. The Root Ward's last words, torn from the Ur-Ghast's ruin, give a direction: up.",
     "Past the clouds is a country built on islands, and the first of its gates is guarded by a sleeping thing. The Ember does not like the sky; it has been there before."],
    [check()], [xp(200), points(2), cache(3, "Act II cache")], deps=["ur_ghast", "guardian"], shape="diamond", size=1.3)
CHAPTERS.append(c)

# =============================================================== ACT III ==============================================================
c = Chapter("act3", "Act III: Beyond the Veil", "minecraft:feather", "story", "Above the weather: sky islands, dream-realms and the first true flight.", bg="act3")
c.q("aether", "A Country in the Clouds", "aether:aether_portal_frame", "Glowstone, water and a sky-blue light: the Aether is a realm of floating islands, gentle fauna and dangerous architecture. Keep a slowfall potion close.", [dim("aether:the_aether")], [xp(200), cache(3)], deps=["act2.act2_end"], shape="diamond", size=1.3)
c.q("zanite", "Zanite", "aether:zanite_gemstone", "The Aether's tools are made from gemstones, not metal. Holystone, zanite, gravitite: each is a tier of lightness.", [item("aether:zanite_gemstone", 8)], [xp(80)], deps=["aether"])
c.q("moa", "Moa", "aether:blue_moa_egg", "The Moa is a tall, fast, gentle bird that can jump higher than any horse. It is the first sky-mount: not flight, but close to it. Incubate an egg.", [adv("aether:incubate_moa")], [xp(120)], deps=["zanite"])
c.q("phyg", "A Saddle for a Pig", "minecraft:saddle", "Flying pigs: the Aether's joke and its best ride. Saddle a phyg and you can glide above any island. Remember: this flight stays in the Aether.", [adv("aether:mount_phyg")], [xp(140)], deps=["moa"], shape="hexagon")
c.q("bronze", "The Bronze Dungeon", "aether:bronze_dungeon_key", "Stone and slider; chests and traps. Bronze is the first of three dungeons whose keys you must earn.", [adv("aether:bronze_dungeon")], [xp(150), cache(3)], deps=["zanite"])
c.q("slider", "The Slider", "aether:bronze_dungeon_key", "A cube of stone that wants to hit you. It remembers every attack you tried last time; do not repeat yourself.", [kill("aether:slider")], [xp(300), points(1), cache(4)], deps=["bronze"], shape="octagon", size=1.5)
c.q("silver", "The Silver Dungeon", "aether:silver_dungeon_key", "A pyramid of puzzles and angels. The Valkyrie Queen is the third stage of the Aether, and she dislikes visitors.", [struct("aether:silver_dungeon")], [xp(180)], deps=["slider"])
c.q("valkyrie", "The Valkyrie Queen", "aether:valkyrie_lance", "A duel, not a boss fight. She is quick, accurate and fair; the lance she drops is the first truly legendary weapon in this campaign.", [kill("aether:valkyrie_queen")], [xp(450), points(2), cache(4, "Valkyrie spoils")], deps=["silver"], shape="octagon", size=1.5)
c.q("gold", "The Gold Dungeon", "aether:gold_dungeon_key", "Sun on the water, fire in the air. The last Aether dungeon belongs to the Sun Spirit, who is angry at the world.", [struct("aether:gold_dungeon")], [xp(200)], deps=["valkyrie"])
c.q("sun", "The Sun Spirit", "aether:victory_medal", "A boss of fire and fury at the roof of the sky. Beat him and the Aether is yours; the Warden of Sky has no more to say.", [kill("aether:sun_spirit")], [xp(600), points(2), cache(5, "Sun Spirit spoils")], deps=["gold"], shape="octagon", size=1.6)
c.q("whale", "Whale-Rider", "deep_aether:aerwhale_saddle", "Aerwhales drift through the clouds like cathedrals. A saddle, patience and a lot of fruit, and you ride the sky like a ship.", [item("deep_aether:aerwhale_saddle")], [xp(180)], deps=["phyg"], optional=True)
c.q("hippogryph", "Hippogryph", "iceandfire:hippogryph_egg", "A real flying mount for the overworld: slow, honest, limited. It cannot enter dungeons and it tires. Even so, the first time you land on a mountaintop you will want to stay.", [item("iceandfire:hippogryph_egg")], [xp(200)], deps=["sun"], shape="hexagon")
c.q("wing", "Wings of the First Flight", "alexsmobs:straddle_saddle", "The Straddleboard, the aerwhale, the hippogryph: you have three ways into the sky now. The Wardens' structures are built to keep fliers out. Respect that; or break it, and learn why.", [check()], [xp(150), points(1)], deps=["hippogryph"], shape="diamond")
c.q("everbright", "A Dream of Light", "blue_skies:zeal_lighter", "Blue Skies is two realms: Everbright, where it is always noon, and Everdawn, where it never finishes midnight. Both are beautiful, both have teeth.", [dim("blue_skies:everbright")], [xp(200)], deps=["aether"], shape="diamond")
c.q("summoner", "The Summoner", "blue_skies:diopside_gem", "A dungeon of nature, a Summoner who does not fight alone. Bring a ranged weapon and a friend.", [kill("blue_skies:summoner")], [xp(350), cache(4)], deps=["everbright"], shape="octagon", size=1.4)
c.q("crusher", "The Starlit Crusher", "blue_skies:horizonite_ingot", "A giant of crystal and rock. The Everbright's last stand.", [kill("blue_skies:starlit_crusher")], [xp(500), points(1), cache(5)], deps=["summoner"], shape="octagon", size=1.5)
c.q("everdawn", "Under Forever Moon", "blue_skies:pyrope_gem", "Everdawn's dungeons are poison and webs. Antidotes first, adventure second.", [dim("blue_skies:everdawn")], [xp(200)], deps=["everbright"])
c.q("arachnarch", "The Arachnarch", "blue_skies:falsite_ingot", "A spider the size of a cottage. Fight on the edges of its web and bring something to clear the poison.", [kill("blue_skies:arachnarch")], [xp(500), cache(5)], deps=["everdawn"], shape="octagon", size=1.5)
c.q("caves", "A Mouth in the Earth", "alexscaves:uranium", "Alex's Caves hides entire worlds under the surface: candy caverns, acid pits, abyssal trenches. Pick a biome and descend.", [struct("alexscaves:ocean_trench")], [xp(150)], deps=["act2.act2_end"], optional=True)
c.q("raptor", "Subterranodon", "alexscaves:heavy_bone", "A cave flier you can ride. Short flights, strong dives: a mount built for caverns, and a clue to what the underground will give you later.", [kill("alexscaves:subterranodon")], [xp(200)], deps=["caves"], optional=True)
c.q("fire", "Fire and Forge", "cataclysm:infernal_forge", "Ignitium is the first of Cataclysm's metals. Its gear is magnificent and its source is a creature that does not forgive.", [struct("cataclysm:burning_arena")], [xp(200)], deps=["act2.netherite"], optional=True)
c.q("ignis", "Ignis", "cataclysm:ignitium_ingot", "The Fallen Knight of the Nether: a duel against someone better than you. Take a shield, take a potion of resistance, take your time.", [kill("cataclysm:ignis"), adv("cataclysm:kill_ignis")], [xp(700), points(2), cache(5, "Ignis spoils")], deps=["fire"], shape="octagon", size=1.6)
c.q("epic", "Epic", "apotheosis:epic_material", "Your gear has entered the middle of the rarity ladder. Epic items have four affixes and often a named bonus. Think about what you would give them up for.", [adv("apotheosis:affix/epic")], [xp(250)], deps=["aether"], optional=True)
c.q("act3_end", "What the Sky Remembers", "minecraft:elytra",
    ["The Sun Spirit's flame and the Crusher's stone both carry the same sigil. The Wardens did not just guard realms; they guarded one another. Two have fallen. The Crown's pieces ring like a bell when you hold them close.",
     "Below, a darker place calls: a city at the bottom of the dark, a hall of echoes. And the Ember has begun to speak in whispers."],
    [check()], [xp(300), points(3), cache(4, "Act III cache")], deps=["sun", "crusher", "arachnarch"], shape="diamond", size=1.3)
CHAPTERS.append(c)
