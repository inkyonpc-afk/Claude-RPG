"""Pin a Modrinth build into pack/pinned.json (replace a cached mod or add a new one).

  python tools/pin.py SLUG [--replaces "Cached Name"] [--cat magic] [--status std] [--version SUBSTR] [--name "Display"]
Downloads the jar to .build/cache/, reads mods.toml for modids/requires, records url+sha1. resolve.py merges pins.
"""
import argparse, hashlib, io, json, os, sys, urllib.parse, urllib.request, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
UA = {"User-Agent": "ClaudeRPG-packbuilder/0.1"}
ap = argparse.ArgumentParser()
ap.add_argument("slug"); ap.add_argument("--replaces", default=""); ap.add_argument("--cat", default="misc")
ap.add_argument("--status", default="std"); ap.add_argument("--version", default=""); ap.add_argument("--name", default="")
ap.add_argument("--loader", default="forge"); ap.add_argument("--mc", default="1.20.1")
a = ap.parse_args()


def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40))


q = urllib.parse.urlencode({"loaders": json.dumps([a.loader]), "game_versions": json.dumps([a.mc])})
vers = get("https://api.modrinth.com/v2/project/%s/version?%s" % (a.slug, q))
if a.version:
    vers = [v for v in vers if a.version in v["version_number"]]
if not vers:
    sys.exit("no %s/%s version for %s" % (a.loader, a.mc, a.slug))
rel = [v for v in vers if v["version_type"] == "release"] or vers
v = rel[0]
f = next((x for x in v["files"] if x.get("primary")), v["files"][0])
os.makedirs(os.path.join(ROOT, ".build", "cache"), exist_ok=True)
dst = os.path.join(ROOT, ".build", "cache", f["filename"])
if not os.path.isfile(dst):
    data = urllib.request.urlopen(urllib.request.Request(f["url"], headers=UA), timeout=120).read()
    open(dst, "wb").write(data)
sha1 = hashlib.sha1(open(dst, "rb").read()).hexdigest()
if sha1 != f["hashes"]["sha1"]:
    sys.exit("sha1 mismatch")
import jarmeta_lib
modids, req, kind = jarmeta_lib.read(dst)
proj = get("https://api.modrinth.com/v2/project/" + a.slug)
entry = dict(name=a.name or a.replaces or proj["title"], replaces=a.replaces, category=a.cat, status=a.status,
             fileName=f["filename"], url=f["url"], sha1=sha1, localJar=dst, modids=modids, requires=req, loader=kind,
             source="modrinth:" + a.slug, version=v["version_number"], published=v["date_published"][:10], license=proj.get("license", {}).get("id", ""))
pf = os.path.join(ROOT, "pack", "pinned.json")
pins = json.load(open(pf, encoding="utf-8")) if os.path.isfile(pf) else []
pins = [p for p in pins if p["source"] != entry["source"]]
pins.append(entry)
json.dump(pins, open(pf, "w", encoding="utf-8"), indent=1)
print("pinned %s -> %s [%s] modids=%s requires=%s" % (entry["name"], f["filename"], kind, modids, req))
