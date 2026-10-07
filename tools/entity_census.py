"""Entity census: counts stored entities by type in a world's entities/*.mca (all dimensions), to spot runaway spawning.
Usage: python tools/entity_census.py <world_dir> [--top 20]"""
import argparse, collections, glob, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtlite import region_chunks  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("world")
ap.add_argument("--top", type=int, default=20)
a = ap.parse_args()
total = collections.Counter()
for d in glob.glob(os.path.join(a.world, "**", "entities"), recursive=True):
    dim = os.path.relpath(d, a.world).replace("\\", "/")
    c = collections.Counter()
    for mca in glob.glob(os.path.join(d, "*.mca")):
        for nbt in region_chunks(mca):
            for e in nbt.get("Entities") or []:
                c[e.get("id")] += 1
    if c:
        print("%s: %d entities, %d types" % (dim, sum(c.values()), len(c)))
        total.update(c)
print("TOTAL %d entities" % sum(total.values()))
for k, v in total.most_common(a.top):
    print("%6d  %s" % (v, k))
