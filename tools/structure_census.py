"""Structure census: count structure starts in a generated world's region files (all dimensions found), grouped by tier from tools/tune_structures.py.
Reads chunk NBT directly (zlib/gzip/uncompressed chunks; no external deps). Reports starts per structure, per namespace and per tier, plus density
per 1000x1000 blocks of generated area, so spacing can be judged from data instead of /locate probes.
Usage: python tools/structure_census.py [world_dir] [--top 25] [--json out.json]"""
import argparse, collections, glob, json, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ap = argparse.ArgumentParser()
ap.add_argument("world", nargs="?", default=os.path.join(ROOT, ".build", "server", "world"))
ap.add_argument("--top", type=int, default=25)
ap.add_argument("--outside", type=int, default=0, help="ignore chunks within this many blocks of the origin (skip an earlier, differently-configured pregen)")
ap.add_argument("--json", default="")
a = ap.parse_args()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtlite import region_chunks  # noqa: E402
sys.path.insert(0, os.path.join(ROOT, "tools"))
import spacing_tiers as ST  # noqa: E402  (shared tier rules)
reg = json.load(open(os.path.join(ROOT, "pack", "registries_snapshot.json"), encoding="utf-8"))
tier_of = ST.classify

starts = collections.Counter()
area = 0
dims = {}
for rdir in glob.glob(os.path.join(a.world, "**", "region"), recursive=True):
    rel = os.path.relpath(rdir, a.world).replace("\\", "/")
    dim = {"region": "overworld", "DIM-1/region": "the_nether", "DIM1/region": "the_end"}.get(rel, rel.replace("dimensions/", "").replace("/region", ""))
    seen, chunks = set(), 0
    for mca in glob.glob(os.path.join(rdir, "*.mca")):
        for nbt in region_chunks(mca):
            if a.outside and abs(nbt.get("xPos", 9999) * 16) < a.outside and abs(nbt.get("zPos", 9999) * 16) < a.outside:
                continue
            chunks += 1
            st = (nbt.get("structures") or {}).get("starts") or {}
            for sid, v in st.items():
                if isinstance(v, dict) and v.get("id") != "INVALID" and v.get("ChunkX") is not None:
                    key = (sid, v["ChunkX"], v["ChunkZ"])
                    if key not in seen:   # a start is referenced from every chunk it touches; count once
                        seen.add(key)
                        starts[(dim, sid)] += 1
    dims[dim] = chunks
    area_km2 = chunks * 256 / 1e6
    dims[dim] = (chunks, area_km2)

print("dimension chunks area_km2 (1 km2 = 1000x1000 blocks):", {k: (v[0], round(v[1], 2)) for k, v in dims.items()})
ow = [(sid, n) for (d, sid), n in starts.items() if d == "overworld"]
ow_area = dims.get("overworld", (0, 0))[1] or 1
bytier, byns = collections.Counter(), collections.Counter()
for sid, n in ow:
    bytier[tier_of(sid)] += n
    byns[sid.split(":")[0]] += n
print("\nOVERWORLD starts per km2 by tier (area %.2f km2):" % ow_area)
for t, n in sorted(bytier.items(), key=lambda x: -x[1]):
    print("  %-11s %5d starts  %6.2f /km2" % (t, n, n / ow_area))
print("\nTop namespaces:", ", ".join("%s %d" % kv for kv in byns.most_common(a.top)))
print("\nTop structures:", ", ".join("%s %d" % kv for kv in sorted(ow, key=lambda x: -x[1])[:a.top]))
print("\nDistinct overworld structures generated: %d of %d registered" % (len({s for s, _ in ow}), len(reg["structure"])))
for d in dims:
    if d != "overworld":
        sub = [(sid, n) for (dd, sid), n in starts.items() if dd == d]
        print("%s: %d starts of %d kinds" % (d, sum(n for _, n in sub), len({s for s, _ in sub})))
if a.json:
    json.dump({"area_km2": ow_area, "by_tier": bytier, "by_namespace": byns, "structures": dict(ow)}, open(a.json, "w"), indent=1)
