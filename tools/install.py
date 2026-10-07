"""Install mods from pack/mods.lock.json into a mods directory.

  python tools/install.py [--cats perf,qol,...] [--status core,std,test] [--server] [--dest DIR] [--only NAME,NAME]
Selected = lock entries whose category/status match, plus the transitive required dependencies.
Prefers the local cached jar or a --cache folder (sha1-verified), falls back to the CDN url. Only jars previously installed by this tool
(tracked in <dest>/.installed.json) are ever removed. --server skips pack/client_only.txt.
"""
import argparse, hashlib, json, os, re, shutil, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor


def norm(n):
    return re.sub(r"\s+", " ", re.sub(r"\s*[\[\(].*?[\]\)]", "", n or "")).strip().lower()


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
ap = argparse.ArgumentParser()
ap.add_argument("--cats", default="")
ap.add_argument("--status", default="core,std,test")
ap.add_argument("--only", default="")
ap.add_argument("--server", action="store_true")
ap.add_argument("--dest", default="")
ap.add_argument("--dry", action="store_true")
ap.add_argument("--cache", default="", help="comma-separated folders to copy sha1-matching jars from before downloading (e.g. mods)")
a = ap.parse_args()

lock = json.load(open(os.path.join(ROOT, "pack", "mods.lock.json"), encoding="utf-8"))
byid = {e["addonID"]: e for e in lock}
cats = set(filter(None, a.cats.split(",")))
status = set(a.status.split(","))
only = {x.strip().lower() for x in a.only.split(",") if x.strip()}
cfile = os.path.join(ROOT, "pack", "client_only.txt")
client_only = set()
if a.server and os.path.isfile(cfile):
    client_only = {norm(l) for l in open(cfile, encoding="utf-8") if l.strip() and not l.startswith("#")}
rej = os.path.join(ROOT, "pack", "rejects.txt")
rejected = set()
if os.path.isfile(rej):
    rejected = {l.split("|")[0].strip().lower() for l in open(rej, encoding="utf-8") if l.strip() and not l.startswith("#")}

sel = {}
stack = []
for e in lock:
    if e["why"] != "candidate" or e["status"] not in status:
        continue
    if cats and e["category"] not in cats:
        continue
    if only and e["name"].lower() not in only:
        continue
    if norm(e["name"]) in rejected:
        continue
    stack.append(e["addonID"])
while stack:
    i = stack.pop()
    if i in sel or i not in byid:
        continue
    sel[i] = byid[i]
    stack.extend(byid[i]["deps"])

if a.server:
    gone = {i for i, e in sel.items() if norm(e["name"]) in client_only}
    changed = True
    while changed:   # drop anything that requires an excluded mod
        changed = False
        for i, e in sel.items():
            if i not in gone and any(d in gone for d in e["deps"]):
                gone.add(i); changed = True
                print("server-excluded (needs client-only dep):", e["name"])
    sel = {i: e for i, e in sel.items() if i not in gone}

dest = a.dest or os.path.join(ROOT, "mods")
os.makedirs(dest, exist_ok=True)
track = os.path.join(dest, ".installed.json")
prev = json.load(open(track)) if os.path.isfile(track) else []
want = {e["fileName"] for e in sel.values()}
for fn in prev:
    if fn not in want and os.path.isfile(os.path.join(dest, fn)):
        if not a.dry:
            os.remove(os.path.join(dest, fn))
        print("removed", fn)


def sha1(p):
    h = hashlib.sha1()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def download(e, out):
    """CDN download, sha1-verified before it replaces anything. edge.forgecdn.net answers 404 for these files (seen 2026-10-07 for every sampled
    file) while mediafilez.forgecdn.net serves the same paths, so it is tried second."""
    urls = [e["url"]] + ([e["url"].replace("://edge.forgecdn.net/", "://mediafilez.forgecdn.net/")] if "://edge.forgecdn.net/" in e["url"] else [])
    err = None
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "ClaudeRPG-packbuilder/0.1"})
            with urllib.request.urlopen(req, timeout=120) as r, open(out + ".part", "wb") as f:
                shutil.copyfileobj(r, f)
            if e["sha1"] and sha1(out + ".part") != e["sha1"]:
                raise ValueError("sha1 mismatch for %s" % u)
            os.replace(out + ".part", out)
            return
        except Exception as ex:   # try the next mirror; report the last error
            err = ex
            if os.path.isfile(out + ".part"):
                os.remove(out + ".part")
    raise RuntimeError("%s: %s" % (e["fileName"], err))


n_copy = 0
todo = []
for e in sorted(sel.values(), key=lambda x: x["name"].lower()):
    out = os.path.join(dest, e["fileName"])
    if os.path.isfile(out) and (not e["sha1"] or sha1(out) == e["sha1"]):
        continue
    if a.dry:
        continue
    src = next((c for c in [e["localJar"]] + [os.path.join(d, e["fileName"]) for d in filter(None, a.cache.split(","))]
                if c and os.path.isfile(c) and (not e["sha1"] or sha1(c) == e["sha1"])), None)
    if src:
        shutil.copyfile(src, out)
        n_copy += 1
    else:
        todo.append((e, out))
with ThreadPoolExecutor(8) as ex:
    list(ex.map(lambda t: download(*t), todo))
n_dl = len(todo)
if not a.dry:
    json.dump(sorted(want), open(track, "w"))
print("selected %d mods -> %s (copied %d, downloaded %d)" % (len(sel), dest, n_copy, n_dl))
