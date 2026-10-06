"""Mount tuning (flight is slow early, fast late; tamed mounts never grief). Patches TOML keys in place; fails loudly if a key is missing.
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
}
for rel, kv in PATCH.items():
    p = os.path.join(ROOT, rel)
    s = open(p, encoding="utf-8").read()
    for k, v in kv.items():
        rx = re.compile(r'(?m)^(\s*"%s"\s*=\s*)(.*)$' % re.escape(k))
        if not rx.search(s):
            raise SystemExit("%s: key not found: %s" % (rel, k))
        s = rx.sub(lambda m: m.group(1) + v, s, count=1)
    open(p, "w", encoding="utf-8").write(s)
    print("patched", rel, len(kv), "keys")
