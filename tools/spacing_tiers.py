"""Structure tiers: one classification shared by tune_structures.py (writes spacing), structure_census.py (measures density) and calibrate_spacing.py
(derives factors from measurements). Classification works on structure_set ids and structure ids alike because the rules are namespace/name based.
FORCE is checked first (decor and sub-structures that a namespace rule would put in the wrong tier); then TIERS, first match wins."""
import json, os, re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DEFAULT_FACTOR = 1.8

# target density per km2 (1 km2 = 1000x1000 blocks) in the overworld: the pacing design (see WORLDGEN.md)
TARGETS = {"boss": 0.4, "great": 0.5, "settlement": 1.5, "vanilla": 3.0, "dungeon": 4.0, "clutter": 12.0, "default": 3.0}

# (tier, fallback factor, meaning, regex on id) - fallback factors are used until config/aldreth/spacing_calibration.json exists
TIERS = [
    ("realm", 1.0, "dimension-designed layouts (Twilight Forest, Aether family, Blue Skies, Undergarden, Otherside, End); untouched",
     r"^(twilightforest|aether|aether_redux|ancient_aether|deep_aether|lost_aether_content|blue_skies|undergarden|deeperdarker|nullscape|endrem|betterendisland):|^minecraft:(end_cities|strongholds)$"),
    ("boss", 2.0, "boss arenas and quest targets: rare, but findable with a map and a plan",
     r"^(cataclysm|soulsweapons|ender_dragon_loot|bosses_of_mass_destruction|block_factorys_bosses|mowziesmobs|iceandfire|eeeabsmobs|illagerinvasion|undead_revamp2):"),
    ("settlement", 1.3, "villages and towns: rest stops, traders, bounties",
     r"(village|town|tidal|hamlet|settlement)|^(towns_and_towers|medieval_buildings):houses|^towns_and_towers:"),
    ("great", 2.5, "mega-dungeons: an expedition each",
     r"^(dungeons_arise|dungeons_arise_seven_seas|prodigium_dungeons|irons_spellbooks|goety|betterstrongholds|betterfortresses|betteroceanmonuments|betterdeserttemples|betterjungletemples|betterwitchhuts):"),
    ("vanilla", 1.5, "vanilla structures (mansions, monuments, ruins, wrecks, ruined portals) and their replacements", r"^(minecraft|bettermineshafts|trials):"),
    ("dungeon", 2.0, "medium dungeons, towers and camps: the bread and butter of exploration",
     r"^(dungeons_enhanced|dungeons_plus|born_in_chaos_v1|explorify|repurposed_structures|dungeoncrawl|ati_structures|structory|structory_towers|valhelsia_structures|hopo|betterarcheology|formationsnether|bygonenether|incendium|nova_structures):"),
    ("ocean_decor", 4.5, "biome-bound sea decor (arches, spirals, sunken villages, rafts, wrecks): fixed factor, excluded from calibration because it is biome-restricted and very prolific",
     r"(?!)"),
    ("clutter", 2.6, "small ruins, wells, cabins and decor: spaced so discoveries feel deliberate",
     r"^(mvs|mns|mss|mes|supplementaries|twigs|wabi_sabi_structures|additionalstructures|philipsruins|red|underground_rooms|farmers_structures|meadow|beautify|verdantvibes|species|friendsandfoes|splendid_slimes|tameablebeasts|paraglider|biomeswevegone|terralith|alexscaves|apotheosis):"),
]

# measured (census 2026-10-06): these were wrongly captured by namespace rules
FORCE = [
    ("ocean_decor", r"^aquamirae:surface|^underwater_village:|^formationsoverworld:(raft|rafts)|wreckage_ocean"),
    ("clutter", r"^terrariastructures:|^valhelsia_structures:(deep_spawner|spawner_room|big_trees)|^buriedwrecks:"),
    ("dungeon", r"^aquamirae:(outpost|shelter|ship)|^betterdungeons:"),
]


def classify(sid):
    for tier, rx in FORCE:
        if re.search(rx, sid):
            return tier
    for tier, _, _, rx in TIERS:
        if re.search(rx, sid):
            return tier
    return "default"


def factors():
    """tier -> spread factor: calibrated values when available, else the fallbacks above."""
    f = {t: x for t, x, _, _ in TIERS}
    f["default"] = DEFAULT_FACTOR
    p = os.path.join(ROOT, "config", "aldreth", "spacing_calibration.json")
    if os.path.isfile(p):
        f.update(json.load(open(p, encoding="utf-8")).get("factors", {}))
    return f
