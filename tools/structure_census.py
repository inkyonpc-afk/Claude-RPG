"""Structure census: count structure starts in a generated world's region files (all dimensions found), grouped by tier from tools/tune_structures.py.
Reads chunk NBT directly (zlib/gzip/uncompressed chunks; no external deps). Reports starts per structure, per namespace and per tier, plus density
per 1000x1000 blocks of generated area, so spacing can be judged from data instead of /locate probes.
Usage: python tools/structure_census.py [world_dir] [--top 25] [--json out.json]"""
import argparse, collections, glob, gzip, json, os, re, struct, sys, zlib

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ap = argparse.ArgumentParser()
ap.add_argument("world", nargs="?", default=os.path.join(ROOT, ".build", "server", "world"))
ap.add_argument("--top", type=int, default=25)
ap.add_argument("--json", default="")
a = ap.parse_args()

# ---- minimal NBT reader (only what chunks need)
TAGS = {}


def rd(buf, pos, t):
    if t == 1: return struct.unpack_from(">b", buf, pos)[0], pos + 1
    if t == 2: return struct.unpack_from(">h", buf, pos)[0], pos + 2
    if t == 3: return struct.unpack_from(">i", buf, pos)[0], pos + 4
    if t == 4: return struct.unpack_from(">q", buf, pos)[0], pos + 8
    if t == 5: return struct.unpack_from(">f", buf, pos)[0], pos + 4
    if t == 6: return struct.unpack_from(">d", buf, pos)[0], pos + 8
    if t == 7:
        n = struct.unpack_from(">i", buf, pos)[0]; return None, pos + 4 + n
    if t == 8:
        n = struct.unpack_from(">H", buf, pos)[0]; return buf[pos + 2:pos + 2 + n].decode("utf-8", "replace"), pos + 2 + n
    if t == 9:
        it = buf[pos]; n = struct.unpack_from(">i", buf, pos + 1)[0]; pos += 5; out = []
        for _ in range(n):
            v, pos = rd(buf, pos, it); out.append(v)
        return out, pos
    if t == 10:
        d = {}
        while True:
            it = buf[pos]; pos += 1
            if it == 0: return d, pos
            n = struct.unpack_from(">H", buf, pos)[0]; k = buf[pos + 2:pos + 2 + n].decode("utf-8", "replace"); pos += 2 + n
            d[k], pos = rd(buf, pos, it)
    if t == 11:
        n = struct.unpack_from(">i", buf, pos)[0]; return None, pos + 4 + 4 * n
    if t == 12:
        n = struct.unpack_from(">i", buf, pos)[0]; return None, pos + 4 + 8 * n
    raise ValueError("bad tag %d" % t)


def chunk_nbt(raw, comp):
    data = zlib.decompress(raw) if comp == 2 else gzip.decompress(raw) if comp == 1 else raw
    if data[0] != 10: return None
    n = struct.unpack_from(">H", data, 1)[0]
    d, _ = rd(data, 3 + n, 10)
    return d


def region_chunks(path):
    with open(path, "rb") as f:
        head = f.read(4096)
        for i in range(1024):
            off = int.from_bytes(head[i * 4:i * 4 + 3], "big")
            if not off: continue
            f.seek(off * 4096)
            ln, comp = struct.unpack(">iB", f.read(5))
            try:
                nbt = chunk_nbt(f.read(ln - 1), comp)
            except Exception:
                continue
            if nbt: yield nbt


# ---- tiers from tune_structures.py (same regex table; first match wins)
src = open(os.path.join(ROOT, "tools", "tune_structures.py"), encoding="utf-8").read().split("assign, counts")[0].replace('os.path.dirname(os.path.abspath(__file__)), ".."', '"' + ROOT.replace("\\", "/") + '"')
ns = {}
exec(src, ns)
TIERS, DEFAULT = ns["TIERS"], ns["DEFAULT"]
reg = json.load(open(os.path.join(ROOT, "pack", "registries_snapshot.json"), encoding="utf-8"))
struct_to_set = {}   # a structure's tier is judged by its structure_set when known, else by its own id
for s in reg["structure_set"]:
    struct_to_set[s] = s


def tier_of(sid):
    for tier, f, why, rx in TIERS:
        if re.search(rx, sid):
            return tier
    return "default"


starts = collections.Counter()
area = 0
dims = {}
for rdir in glob.glob(os.path.join(a.world, "**", "region"), recursive=True):
    rel = os.path.relpath(rdir, a.world).replace("\\", "/")
    dim = {"region": "overworld", "DIM-1/region": "the_nether", "DIM1/region": "the_end"}.get(rel, rel.replace("dimensions/", "").replace("/region", ""))
    seen, chunks = set(), 0
    for mca in glob.glob(os.path.join(rdir, "*.mca")):
        for nbt in region_chunks(mca):
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
