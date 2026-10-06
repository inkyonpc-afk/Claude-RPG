"""Query the registry snapshot. Usage: python tools/ids.py <registry> <regex> [limit]   e.g. python tools/ids.py structure 'yungs|dungeons_arise' 40"""
import json, os, re, sys
r = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pack", "registries_snapshot.json"), encoding="utf-8"))
reg, rx = sys.argv[1], re.compile(sys.argv[2])
lim = int(sys.argv[3]) if len(sys.argv) > 3 else 60
hits = [i for i in r[reg] if rx.search(i)]
print(len(hits), "hits:", " ".join(hits[:lim]))
