"""Mount, fast-travel and mob-safety tuning (flight is slow early, fast late; tamed mounts never grief; waystone travel costs XP, which also buys skill points). Patches TOML keys in place; fails loudly if a key is missing.
Usage: python tools/tune_mounts.py"""
import os, re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PATCH = {
    "config/iceandfire-common.toml": {
        "Dragon Griefing": "1",                      # wild dragons break weak blocks only (structures and bases survive)
        "Tamed Dragon Griefing": "false",            # tamed dragons never grief (multiplayer bases)
        "Hippogryph Flight Speed Modifier": "0.75",  # Act III's first overworld flyer is slow and honest
        "Amphithere Flight Speed": "1.5",            # fast but below a grown dragon
        "Dragon Moved Wrongly Error Fix": "true",    # dedicated-server log spam / rubber-banding fix
    },
    "config/l2_configs/l2hostility-common.toml": {   # safety-only changes; scaling numbers stay at defaults until play-tested
        "newPlayerProtectRange": "160",              # no hostility scaling near a new player (spawn area stays gentle)
        "maxTraitCount": "6",                        # cap stacked mob traits (default 9)
    },
    "config/waystones-common.toml": {                # 1 level per 1000 blocks, capped at 5; +3 levels across dimensions
        "maximumBaseXpCost": "5.0",
        "waystoneXpCostMultiplier": "1.0",
        "globalWaystoneXpCostMultiplier": "1.0",
        "inventoryButtonXpCostMultiplier": "1.0",
        "warpStoneXpCostMultiplier": "0.5",          # portable tools pay half: you earned them
        "portstoneXpCostMultiplier": "0.5",
        "sharestoneXpCostMultiplier": "0.5",
        "warpPlateXpCostMultiplier": "0.0",          # player-built local networks stay free
        "dimensionalWarpXpCost": "3",
    },
}
for rel, kv in PATCH.items():
    p = os.path.join(ROOT, rel)
    s = open(p, encoding="utf-8").read()
    for k, v in kv.items():
        rx = re.compile(r'(?m)^(\s*"?%s"?\s*=\s*)(.*)$' % re.escape(k))
        if not rx.search(s):
            raise SystemExit("%s: key not found: %s" % (rel, k))
        s = rx.sub(lambda m: m.group(1) + v, s, count=1)
    open(p, "w", encoding="utf-8").write(s)
    print("patched", rel, len(kv), "keys")
