"""The Wide Road (part 2): structures, dimensions, bosses, secrets."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from questlib import *

CHAPTERS = []

# =============================================================== STRUCTURES: small and medium ======================================
c = Chapter("ruins", "Ruins, Towers and Camps", "minecraft:mossy_stone_bricks", "road", "Common places hold common things: supplies, a story, a little luck.", bg="structures")
c.q("intro", "A World That Remembers", "minecraft:map", ["Structures come in tiers. Camps and ruins hold supplies; towers and forts hold decent gear; dungeons and castles hold real treasure; mega-dungeons and boss fortresses hold legends.", "The harder a place is to reach, the better its loot. A chest in a hovel will not give you endgame gear."], [check()], [xp(20)], shape="diamond", size=1.3)
c.q("village", "A Village", "minecraft:bell", "Safe harbour, trading, a bed. Villages are the first places of rest.", [struct("minecraft:village_plains")], [xp(30)], deps=["intro"])
c.q("pillager", "Pillager Outpost", "minecraft:crossbow", "Hard to approach, rewarding to clear.", [struct("minecraft:pillager_outpost")], [xp(60)], deps=["village"])
c.q("mineshaft", "An Old Mineshaft", "minecraft:rail", "Cobwebs, spawners, and iron. Take a torch for every exit.", [struct("minecraft:mineshaft")], [xp(40)], deps=["intro"])
c.q("ruin", "Ruined Portal", "minecraft:crying_obsidian", "A half-built gate in a field. Loot, obsidian, and a place to rest.", [struct("minecraft:ruined_portal")], [xp(30)], deps=["intro"])
c.q("temple", "Abandoned Temple", "minecraft:mossy_stone_bricks", "A temple pulled into the earth by roots. Smaller than you expect, more dangerous than you hope.", [struct("dungeons_arise:abandoned_temple")], [xp(60)], deps=["intro"])
c.q("tower", "Bandit Towers", "minecraft:crossbow", "A tall camp of cutthroats. Bring a shield.", [struct("dungeons_arise:bandit_towers")], [xp(70)], deps=["pillager"])
c.q("illager", "Illager Fort", "minecraft:iron_axe", "Walls, banners and a heavy door: the Illagers do not hide.", [struct("dungeons_arise:illager_fort")], [xp(80)], deps=["tower"])
c.q("lighthouse", "A Lighthouse", "minecraft:lantern", "A light on a cliff; a keeper who has been gone a long while.", [struct("dungeons_arise:lighthouse")], [xp(40)], deps=["intro"], optional=True)
c.q("monastery", "Monastery", "minecraft:bell", "Silent monks, quiet corridors and a library of old books.", [struct("dungeons_arise:monastery")], [xp(80), cache(2)], deps=["temple"], optional=True)
c.q("dungeon", "A Dungeon", "minecraft:spawner", "Rooms of spawners and loot, a classic.", [struct("betterdungeons:skeleton_dungeon")], [xp(60)], deps=["intro"])
c.q("desert", "Desert Temple", "minecraft:sandstone", "Deep in the desert, a trap and a chest.", [struct("minecraft:desert_pyramid")], [xp(60)], deps=["dungeon"])
c.q("jungle", "Jungle Temple", "minecraft:mossy_cobblestone", "Arrows, levers and a secret room.", [struct("minecraft:jungle_pyramid")], [xp(60)], deps=["dungeon"], optional=True)
c.q("monument", "Ocean Monument", "minecraft:prismarine", "A sea-temple with guardians that hate air. Bring water breathing.", [struct("minecraft:monument")], [xp(120), cache(2)], deps=["desert"])
c.q("shipwreck", "A Shipwreck", "minecraft:oak_boat", "A hull on a reef. Treasure maps and rot.", [struct("minecraft:shipwreck")], [xp(40)], deps=["intro"], optional=True)
c.q("ruins", "Ancient Ruins", "minecraft:mossy_cobblestone", "A ruin from before the Crown's fall. Some holds a staircase down.", [struct("minecraft:ocean_ruin_cold")], [xp(40)], deps=["intro"], optional=True)
c.q("master", "Explorer", "minecraft:map", "Visit ten different structures. You do not need to clear them all: just remember where the good ones are.", [check()], [xp(150), points(1)], deps=["monument", "illager", "desert"], shape="hexagon")
CHAPTERS.append(c)

# =============================================================== STRUCTURES: grand =================================================
c = Chapter("grand", "Castles, Citadels and Legends", "minecraft:crying_obsidian", "road", "Rare, huge and dangerous. Plan a trip.", bg="structures")
c.q("intro", "Places of Legend", "minecraft:crying_obsidian", ["The greatest structures are rare, far apart and heavily defended. Their loot is rarer too. Pack food, potions, a waystone and a plan."], [check()], [xp(30)], shape="diamond", size=1.3)
c.q("castle", "A Castle", "minecraft:iron_door", "A fortress of walls and guards.", [struct("dungeons_enhanced:castle")], [xp(150), cache(3)], deps=["intro"])
c.q("mansion", "Woodland Mansion", "minecraft:totem_of_undying", "Illagers, a maze, and a totem at the end.", [struct("minecraft:mansion")], [xp(200), cache(3)], deps=["castle"])
c.q("stronghold", "A Stronghold", "minecraft:ender_eye", "Silverfish halls, libraries and a gateway. The road to the End begins here.", [struct("betterstrongholds:stronghold")], [xp(200)], deps=["castle"])
c.q("kayra", "Keep Kayra", "minecraft:iron_bars", "A sprawling, haunted keep.", [struct("dungeons_arise:keep_kayra")], [xp(300), cache(4)], deps=["mansion"])
c.q("shiraz", "Shiraz Palace", "minecraft:gold_block", "A palace of traps and coin.", [struct("dungeons_arise:shiraz_palace")], [xp(300), cache(4)], deps=["kayra"], optional=True)
c.q("citadel", "The Black Citadel", "minecraft:crying_obsidian", "An obsidian fortress.", [struct("dungeons_enhanced:black_citadel")], [xp(350), cache(4)], deps=["kayra"])
c.q("tower_undead", "Tower of the Undead", "minecraft:wither_skeleton_skull", "A tower of corpses and necromancers.", [struct("dungeons_enhanced:tower_of_the_undead")], [xp(250), cache(4)], deps=["mansion"], optional=True)
c.q("coliseum", "The Coliseum", "minecraft:iron_sword", "A gladiators' arena, enormous and loud.", [struct("dungeons_arise:coliseum")], [xp(300), cache(4)], deps=["kayra"], optional=True)
c.q("citadel_ruin", "A Ruined Citadel", "minecraft:blackstone", "Cataclysm's Nether fortress, guarded by Ignis' kin.", [struct("cataclysm:ruined_citadel")], [xp(300), cache(4)], deps=["castle"], optional=True)
c.q("acropolis", "The Acropolis", "minecraft:chiseled_quartz_block", "A sunken marble city.", [struct("cataclysm:acropolis")], [xp(300), cache(4)], deps=["castle"], optional=True)
c.q("catacombs", "The Great Crypt", "minecraft:sculk", "A crypt as large as a village. The dead outnumber you.", [struct("dungeons_enhanced:deep_crypt")], [xp(250), cache(4)], deps=["castle"], optional=True)
c.q("keeping", "The Keeping Castle", "minecraft:chain", "Prodigium's great castle.", [struct("prodigium_dungeons:keeping_castle")], [xp(350), cache(5)], deps=["citadel"], optional=True)
c.q("master", "Delver of Legends", "minecraft:nether_star", "Clear three of the great structures. The loot is excellent; the memories are better.", [check()], [xp(300), points(2)], deps=["kayra", "citadel", "mansion"], shape="hexagon", size=1.3)
CHAPTERS.append(c)

# =============================================================== DIMENSIONS =======================================================
c = Chapter("dimensions", "The Seven Realms and More", "minecraft:ender_pearl", "road", "Seven realms bound to a Crown; a few more the Crown never knew.", bg="dimensions")
c.q("intro", "A Map of Doors", "minecraft:filled_map", ["Aldreth has seven Warden-realms: Root (Twilight Forest), Stone (Undergarden), Sky (Aether), Dream (Blue Skies), Flame (Nether), Echo (Otherside) and the End.", "The order matters: each realm unlocks the materials, bosses and mounts of the next. You can visit early, but you will not come back unchanged."], [check()], [xp(20)], shape="diamond", size=1.3)
from custom_items import SIGILS, EMBER_SHARD  # noqa: E402  (design/custom_items.py)
c.q("shards", "Ember Shards", EMBER_SHARD, ["Every Warden-realm is sealed. A Sigil opens one, and every Sigil is crafted around Ember Shards: splinters of the Crown that burn in your palm.", "Shards come from the story's turning points (the end of each Act) and, now and then, from a fallen boss. Spend them in order: the realms open in the order the Wardens fell."], [item(EMBER_SHARD)], [xp(30)], deps=["intro"], shape="hexagon")
for _k, (_id, _name, _dims, _ing, _col, _lore) in SIGILS.items():
    c.q("sig_" + _k, _name, _id, "%s Craft it (shapeless) from %d Ember Shard%s and the realm's offerings; crafting it unlocks the portal for you." % (_lore, _ing.count(EMBER_SHARD), "" if _ing.count(EMBER_SHARD) == 1 else "s"), [item(_id)], [xp(40)], deps=["shards"])
c.q("nether", "Flame", "minecraft:netherrack", "The Nether is the realm of the Warden of Flame. Bring fire resistance and a good bow.", [dim("nether")], [xp(80)], deps=["sig_flame", "intro"])
c.q("twilight", "Root", "twilightforest:twilight_portal_miniature_structure", "A forest under a sky that never ends its sunset.", [dim("twilightforest:twilight_forest")], [xp(120)], deps=["sig_root", "intro"])
c.q("undergarden", "Stone", "minecraft:deepslate", "A cold, humid second world under the first.", [dim("undergarden:undergarden")], [xp(120)], deps=["sig_stone", "twilight"])
c.q("aether", "Sky", "aether:aether_portal_frame", "A country on clouds.", [dim("aether:the_aether")], [xp(150)], deps=["sig_sky", "twilight"])
c.q("everbright", "Dream, Bright", "blue_skies:zeal_lighter", "A world of noon.", [dim("blue_skies:everbright")], [xp(150)], deps=["sig_dream", "aether"])
c.q("everdawn", "Dream, Dark", "blue_skies:pyrope_gem", "A world of dusk.", [dim("blue_skies:everdawn")], [xp(150)], deps=["everbright"])
c.q("otherside", "Echo", "deeperdarker:soul_crystal", "A mirror of the world, drained of colour and full of listening.", [dim("deeperdarker:otherside")], [xp(200)], deps=["sig_echo", "aether", "undergarden"])
c.q("end", "The End", "minecraft:end_stone", "A final island, a final dragon.", [dim("end")], [xp(250)], deps=["sig_end", "otherside"])
c.q("pocket", "A Pocket World", "irons_spellbooks:arcane_essence", "Iron's Spells' pocket dimension: a private room tucked into the Veil. Few people find the door.", [dim("irons_spellbooks:pocket_dimension")], [xp(100)], deps=["intro"], optional=True, shape="hexagon")
c.q("caves", "Beneath the Surface", "alexscaves:uranium", "Alex's Caves hides whole biomes under the earth: candy, acid, abyss, forlorn. Pick a biome, descend.", [struct("alexscaves:ocean_trench")], [xp(120)], deps=["intro"], optional=True)
c.q("gate", "Gate Pearls", "gateways:gate_pearl", "A gate pearl opens a wave arena in the open world. Postgame challenge, with prizes.", [item("gateways:gate_pearl")], [xp(150)], deps=["end"], optional=True)
c.q("master", "Realm-Walker", "minecraft:nether_star", "Visit every Warden realm. The seven doors are open to you.", [check()], [xp(600), points(2), cache(5)], deps=["nether", "twilight", "undergarden", "aether", "everbright", "everdawn", "otherside", "end"], shape="diamond", size=1.5)
CHAPTERS.append(c)

# =============================================================== BOSS COMPENDIUM ==================================================
c = Chapter("bosses", "The Compendium of Bosses", "minecraft:wither_skeleton_skull", "road", "Fifty-odd bosses. Each drops something nobody else does.", bg="bosses")
c.q("intro", "A Record of Kills", "minecraft:writable_book", ["Bosses drop unique weapons, armor, spells, relics, trophies and crafting materials. They never drop generic diamonds.", "Defeat each once; defeat them again with a different build."], [check()], [xp(30)], shape="diamond", size=1.3)
from bosses import BOSSES  # noqa: E402  (design/bosses.py)
prev = ["intro"]
for key, name, icon, ent, xpv, tier in BOSSES:
    c.q("b_" + key, name, icon, "Defeat %s. Its drops are unique to it; no other source will give you them." % name, [kill(ent)], [xp(xpv), cache(tier)], deps=["intro"], optional=True, shape="octagon" if tier >= 5 else "circle", size=1.2 if tier >= 5 else 1.0)
c.q("slayer", "Slayer", "minecraft:diamond_sword", "Defeat ten bosses. You are a dangerous person.", [check()], [xp(500), points(2)], deps=["b_naga", "b_lich", "b_hydra", "b_sunspirit", "b_ignis"], shape="hexagon")
c.q("legend", "Boss Slayer, Legendary", "minecraft:nether_star", "Defeat twenty-five bosses. The Wardens would have asked for your help.", [check()], [xp(1500), points(3)], deps=["slayer", "b_harbinger", "b_leviathan", "b_dragon"], shape="diamond", size=1.5)
CHAPTERS.append(c)

# =============================================================== SECRETS ==========================================================
c = Chapter("secrets", "Secrets and Curiosities", "minecraft:ender_eye", "road", "Not everything is on the map.", bg="secrets")
c.q("intro", "Whispers", "minecraft:ender_eye", ["Some places do not show on maps and some quests are not in the book. If you find something strange, follow it."], [check()], [xp(20)], shape="diamond")
c.q("trial", "Trial Chambers", "minecraft:copper_block", "Spawners on a timer, a key and a vault. Bring friends.", [struct("minecraft:ancient_city")], [xp(120)], deps=["intro"], optional=True)
c.q("archaeology", "Dig Sites", "minecraft:brush", "Dusty ruins hold pots, potsherds and quiet secrets.", [struct("minecraft:desert_pyramid")], [xp(60)], deps=["intro"], optional=True)
c.q("lore", "A Lorekeeper", "minecraft:writable_book", "Read the in-game guides: the Emberbound Codex, the Aether's lore, Blue Skies' journal.", [check()], [xp(80)], deps=["intro"], optional=True)
c.q("pearl", "A Gate Pearl", "gateways:gate_pearl", "Gates open arenas of waves at the cost of a pearl.", [item("gateways:gate_pearl")], [xp(120)], deps=["intro"], optional=True)
c.q("hidden", "The Hidden Kingdom", "minecraft:nether_star", "There is a place the Wardens never named. You will not find it by walking.", [check()], [xp(500), points(1)], deps=["lore"], optional=True, shape="diamond", size=1.3)
CHAPTERS.append(c)
