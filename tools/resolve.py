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
jm = json.load(open(os.path.join(PACK, "jarmeta.json"), encoding="utf-8"))
provider = {}
for k, m in jm.items():
    if m["loader"] != "forge":
        continue
    for mid in m["modids"]:
        provider.setdefault(mid, k)
ALIAS = {"kotlinforforge": "kotlin for forge", "gml": "groovymodloader"}   # language providers have no mods.toml
for mid, nm in ALIAS.items():
    for k, v in union.items():
        if v["kind"] == "mods" and re.sub(r"\s*[\[\(].*?[\]\)]", "", v["name"] or "").strip().lower() == nm:
            provider[mid] = k
unmet = {}


def deps_of(k):
    ds = [str(d) for d in mods[k]["deps"] if str(d) in mods]
    for mid in jm.get(k, {}).get("requires", []):
        pk = provider.get(mid)
        if pk is None:
            unmet.setdefault(mid, set()).add(mods[k]["name"])
        elif pk != k:
            ds.append(pk)
    return sorted(set(ds))

by_name = {}
for k, v in mods.items():
    by_name.setdefault(norm(v["name"]), []).append(k)

pf = os.path.join(PACK, "pinned.json")
pins = json.load(open(pf, encoding="utf-8")) if os.path.isfile(pf) else []
new_pins = []
for i, pn in enumerate(pins):
    if pn.get("replaces"):
        tgt = by_name.get(norm(pn["replaces"])) or [k for nn, ks in by_name.items() if nn.startswith(norm(pn["replaces"])) for k in ks]
        if len(tgt) != 1:
            print("PIN replace target not unique/found:", pn["replaces"], tgt); continue
        k = tgt[0]
        mods[k].update(fileName=pn["fileName"], downloadUrl=pn["url"], sha1=pn["sha1"], jar=pn["localJar"], deps=[])
        jm[k] = dict(modids=pn["modids"], requires=pn["requires"], loader=pn["loader"])
        for mid in pn["modids"]:
            provider[mid] = k
    else:
        k = str(-(i + 1))
        mods[k] = dict(name=pn["name"], kind="mods", fileName=pn["fileName"], downloadUrl=pn["url"], sha1=pn["sha1"], jar=pn["localJar"], deps=[])
        jm[k] = dict(modids=pn["modids"], requires=pn["requires"], loader=pn["loader"])
        for mid in pn["modids"]:
            provider.setdefault(mid, k)
        new_pins.append((k, pn))

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

for k, pn in new_pins:
    if pn["status"] != "skip" and not (no_test and pn["status"] == "test"):
        selected[k] = dict(cat=pn["category"], status=pn["status"], why="candidate")

# dependency closure
queue, missing_deps = list(selected), {}
while queue:
    k = queue.pop()
    for d in deps_of(k):
        if d not in selected:
            selected[d] = dict(cat="lib", status="dep", why="dependency of " + mods[k]["name"])
            queue.append(d)

BANNED = {"spell_engine", "spell_power", "more_rpg_classes", "txnilib", "connectormod", "fabric_api", "forgified_fabric_api", "fabricloader", "connector_extras"}
banned_hits = [(mods[k]["name"], selected[k]["why"]) for k in selected if BANNED & set(jm.get(k, {}).get("modids", []))]
needing = [(mods[k]["name"], sorted(mods[b]["name"] for b in deps_of(k) if b in selected and BANNED & set(jm.get(b, {}).get("modids", [])))) for k in selected if k in jm and any(BANNED & set(jm.get(b, {}).get("modids", [])) for b in deps_of(k))]
if banned_hits:
    print("mods requiring banned libs:", needing)
if banned_hits:
    print("BANNED MODS SELECTED:", banned_hits)
    sys.exit(2)
lock = []
for k, s in sorted(selected.items(), key=lambda kv: (kv[1]["cat"], mods[kv[0]]["name"].lower())):
    m = mods[k]
    lock.append(dict(addonID=int(k), name=m["name"], fileId=m.get("fileId"), fileName=m["fileName"], sha1=m["sha1"],
                     url=m["downloadUrl"], localJar=m["jar"], category=s["cat"], status=s["status"], why=s["why"], deps=[int(d) for d in deps_of(k)]))
json.dump(lock, open(os.path.join(PACK, "mods.lock.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

fab = [l["name"] + " :: " + l["fileName"] for l in lock if FABRIC.search(l["fileName"])]
out = []
out.append("selected mods: %d  (candidates %d, deps %d)" % (len(lock), sum(1 for l in lock if l["why"] == "candidate"), sum(1 for l in lock if l["why"] != "candidate")))
pinned_src = {p["source"] for p in pins}
out.append("external lines without a pin: " + ", ".join(c["name"] for c in external if "modrinth:" + c["name"] not in pinned_src))
out.append("unmatched (%d): " % len(unmatched) + "; ".join(c["name"] for c in unmatched))
out.append("ambiguous (%d):" % len(ambiguous))
for c, h in ambiguous:
    out.append("  %s -> %s" % (c["name"], h))
out.append("fabric/quilt-looking files selected (%d): %s" % (len(fab), "; ".join(fab)))
out.append("unmet required modids (not provided by any cached forge jar): %s" % {k: sorted(v) for k, v in sorted(unmet.items())})
text = "\n".join(out)
open(os.path.join(PACK, "resolve_report.txt"), "w", encoding="utf-8").write(text)
print(text)
