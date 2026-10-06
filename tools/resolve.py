"""Resolve pack/candidates.txt against pack/local_union.json -> pack/mods.lock.json.

Match: case-insensitive; exact bracket-stripped name first, then unique prefix. Dependency closure uses CurseForge
required deps (type 3) recorded in the union. Statuses core/std/test are installed; skip is not.
Usage: python tools/resolve.py [--no-test]
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.join(HERE, "..", "pack")
union = json.load(open(os.path.join(PACK, "local_union.json"), encoding="utf-8"))
no_test = "--no-test" in sys.argv


def norm(s):
    s = re.sub(r"\s*[\[\(].*?[\]\)]", "", s or "")
    return re.sub(r"\s+", " ", s).strip().lower()


mods = {k: v for k, v in union.items() if v["kind"] == "mods"}
by_name = {}
for k, v in mods.items():
    by_name.setdefault(norm(v["name"]), []).append(k)

FABRIC = re.compile(r"fabric|quilt", re.I)
cands, report = [], []
for line in open(os.path.join(PACK, "candidates.txt"), encoding="utf-8"):
    line = line.rstrip("\n")
    if not line.strip() or line.startswith("#"):
        continue
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 3:
        continue
    cands.append(dict(cat=parts[0], name=parts[1], status=parts[2], note=parts[3] if len(parts) > 3 else ""))

selected = {}   # addonID(str) -> dict(reason, cat, status)
unmatched, ambiguous, external = [], [], []
for c in cands:
    if c["status"] == "skip" or (no_test and c["status"] == "test"):
        continue
    if c["cat"] == "ext":
        external.append(c)
        continue
    frag = None
    if "::" in c["name"]:
        c["name"], frag = [x.strip() for x in c["name"].split("::", 1)]
    n = norm(c["name"])
    hits = by_name.get(n)
    if not hits:
        hits = [k for nn, ks in by_name.items() if nn.startswith(n) for k in ks]
    if not hits:
        unmatched.append(c)
        continue
    if frag:
        hits = [h for h in hits if frag.lower() in mods[h]["fileName"].lower()]
    if len(hits) > 1:
        # prefer a forge-looking build
        forge = [h for h in hits if not FABRIC.search(mods[h]["fileName"])]
        if len(forge) == 1:
            hits = forge
        else:
            ambiguous.append((c, [mods[h]["name"] + " :: " + mods[h]["fileName"] for h in hits]))
            continue
    selected[hits[0]] = dict(cat=c["cat"], status=c["status"], why="candidate")

# dependency closure
queue, missing_deps = list(selected), {}
while queue:
    k = queue.pop()
    for d in mods[k]["deps"]:
        d = str(d)
        if d not in mods:
            missing_deps.setdefault(d, []).append(mods[k]["name"])
            continue
        if d not in selected:
            selected[d] = dict(cat="lib", status="dep", why="dependency of " + mods[k]["name"])
            queue.append(d)

lock = []
for k, s in sorted(selected.items(), key=lambda kv: (kv[1]["cat"], mods[kv[0]]["name"].lower())):
    m = mods[k]
    lock.append(dict(addonID=int(k), name=m["name"], fileId=m["fileId"], fileName=m["fileName"], sha1=m["sha1"],
                     url=m["downloadUrl"], localJar=m["jar"], category=s["cat"], status=s["status"], why=s["why"]))
json.dump(lock, open(os.path.join(PACK, "mods.lock.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

fab = [l["name"] + " :: " + l["fileName"] for l in lock if FABRIC.search(l["fileName"])]
out = []
out.append("selected mods: %d  (candidates %d, deps %d)" % (len(lock), sum(1 for l in lock if l["why"] == "candidate"), sum(1 for l in lock if l["why"] != "candidate")))
out.append("external (Modrinth) to resolve: " + ", ".join(c["name"] for c in external))
out.append("unmatched (%d): " % len(unmatched) + "; ".join(c["name"] for c in unmatched))
out.append("ambiguous (%d):" % len(ambiguous))
for c, h in ambiguous:
    out.append("  %s -> %s" % (c["name"], h))
out.append("fabric/quilt-looking files selected (%d): %s" % (len(fab), "; ".join(fab)))
out.append("deps missing from cache: %s" % missing_deps)
text = "\n".join(out)
open(os.path.join(PACK, "resolve_report.txt"), "w", encoding="utf-8").write(text)
print(text)
