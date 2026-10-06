"""Export a CurseForge-format modpack zip: manifest.json (project/file ids for CurseForge-hosted mods) + overrides/ (configs, kubejs, datapack and resource-pack
folders, options, plus the jars that have no CurseForge id, i.e. Modrinth pins).
Usage: python tools/export_curseforge.py [--version 0.1.0] [--out dist]"""
import argparse, json, os, shutil, sys, zipfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ap = argparse.ArgumentParser()
ap.add_argument("--version", default="0.1.0")
ap.add_argument("--out", default="dist")
ap.add_argument("--status", default="core,std")
a = ap.parse_args()
lock = json.load(open(os.path.join(ROOT, "pack", "mods.lock.json"), encoding="utf-8"))
status = set(a.status.split(","))
sys.path.insert(0, os.path.join(ROOT, "tools"))
rej = os.path.join(ROOT, "pack", "rejects.txt")

# resolve the same selection install.py would use (client install)
import subprocess
subprocess.run([sys.executable, os.path.join(ROOT, "tools", "install.py"), "--dry", "--status", a.status], capture_output=True)
mods_dir = os.path.join(ROOT, "mods")
installed = {f for f in os.listdir(mods_dir) if f.endswith(".jar")}
files, extra = [], []
for e in lock:
    if e["fileName"] not in installed:
        continue
    if e["addonID"] > 0 and e.get("fileId"):
        files.append({"projectID": e["addonID"], "fileID": e["fileId"], "required": True})
    else:
        extra.append(e["fileName"])
extra_entries = {e["fileName"]: e for e in lock if e["fileName"] in extra}
# resource/shader packs tracked on CurseForge are referenced, not bundled
vis = json.load(open(os.path.join(ROOT, "pack", "visual_packs.json"), encoding="utf-8")) if os.path.isfile(os.path.join(ROOT, "pack", "visual_packs.json")) else []
vis_cf = {v["fileName"] for v in vis if v.get("projectID") and v.get("fileID")}
files += [{"projectID": v["projectID"], "fileID": v["fileID"], "required": True} for v in vis if v["fileName"] in vis_cf]
# Jars without a CurseForge id: bundle only when the jar's own declared license allows redistribution; anything else is downloaded by the player
import re, zipfile as _zf
REDIST = re.compile(r"MIT|LGPL|GPL|GNU|Apache|BSD|MPL|Mozilla|CC0|Unlicense|ISC|Zlib", re.I)


def jar_license(path):
    try:
        t = _zf.ZipFile(path).read("META-INF/mods.toml").decode("utf-8", "replace")
        m = re.search(r'^\s*license\s*=\s*"([^"]*)"', t, re.M)
        return m.group(1) if m else ""
    except Exception:
        return ""


bundled, external = [], []
for fn in extra:
    lic = jar_license(os.path.join(mods_dir, fn))
    (bundled if REDIST.search(lic) else external).append((fn, lic))
extra = [fn for fn, _ in bundled]
FETCH_SCRIPT = '''"""Downloads mods whose license does not allow redistribution inside this pack. Run once from the instance folder: python fetch_extra_mods.py
Each file comes from its author's own page and is verified against the sha1 below."""
import hashlib, json, os, urllib.request
here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(here, "mods"), exist_ok=True)
for e in json.load(open(os.path.join(here, "EXTRA_DOWNLOADS.json"), encoding="utf-8")):
    out = os.path.join(here, "mods", e["fileName"])
    if os.path.isfile(out):
        continue
    data = urllib.request.urlopen(urllib.request.Request(e["url"], headers={"User-Agent": "EmbersOfAldreth-fetch"}), timeout=60).read()
    if e["sha1"] and hashlib.sha1(data).hexdigest() != e["sha1"]:
        raise SystemExit("checksum mismatch: " + e["fileName"])
    open(out, "wb").write(data)
    print("downloaded", e["fileName"], "(" + e["license"] + ")")
'''
manifest = {"minecraft": {"version": "1.20.1", "modLoaders": [{"id": "forge-47.4.10", "primary": True}]}, "manifestType": "minecraftModpack", "manifestVersion": 1,
            "name": "Embers of Aldreth", "version": a.version, "author": "Claude + Connor", "overrides": "overrides", "files": files}
os.makedirs(os.path.join(ROOT, a.out), exist_ok=True)
zp = os.path.join(ROOT, a.out, "EmbersOfAldreth-%s.zip" % a.version)
INCLUDE_DIRS = ["config", "defaultconfigs", "kubejs", "resourcepacks", "shaderpacks", "datapacks"]   # mod_data is a regenerated cache (GML mappings): never shipped
EXCLUDE_PARTS = ("exported", "__pycache__", "local", "crash_assistant", "backups")
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    z.writestr("manifest.json", json.dumps(manifest, indent=1))
    z.writestr("modlist.html", "<ul>" + "".join("<li>%s</li>" % e["name"] for e in lock if e["fileName"] in installed) + "</ul>")
    for d in INCLUDE_DIRS:
        base = os.path.join(ROOT, d)
        for dp, dn, fn in os.walk(base):
            dn[:] = [x for x in dn if x not in EXCLUDE_PARTS]
            for f in fn:
                if f in vis_cf and d in ("resourcepacks", "shaderpacks"):
                    continue
                if f.endswith(".db") or f == "player-volumes.properties":   # per-player / runtime state
                    continue
                full = os.path.join(dp, f)
                z.write(full, "overrides/" + os.path.relpath(full, ROOT).replace("\\", "/"))
    # options travel as Default Options defaults: applied on first launch only, so updates never clobber a player's settings
    if os.path.isfile(os.path.join(ROOT, "options.txt")):
        keep = [l for l in open(os.path.join(ROOT, "options.txt"), encoding="utf-8").read().splitlines() if not l.startswith(("lastServer:", "fullscreen", "overrideWidth", "overrideHeight"))]
        z.writestr("overrides/config/defaultoptions/options.txt", "\n".join(keep) + "\n")
    for fn in extra:   # redistributable jars without a CurseForge id travel inside the pack
        z.write(os.path.join(mods_dir, fn), "overrides/mods/" + fn)
    # provenance + the download path for jars whose license does not allow redistribution
    third_party = ["# Bundled third-party jars", "",
                   "Every jar below was published by its author under the license shown (read from the jar's own mods.toml) and is redistributed unmodified. "
                   "See each project's page for source and full license text.", "", "| Jar | License | Source |", "|---|---|---|"]
    third_party += ["| %s | %s | %s |" % (fn, lic, (extra_entries[fn].get("url") or "")[:90]) for fn, lic in bundled]
    z.writestr("overrides/THIRD_PARTY.md", "\n".join(third_party) + "\n")
    if external:
        z.writestr("overrides/EXTRA_DOWNLOADS.json", json.dumps([{"fileName": fn, "license": lic, "url": extra_entries[fn]["url"], "sha1": extra_entries[fn]["sha1"]} for fn, lic in external], indent=1))
        z.writestr("overrides/fetch_extra_mods.py", FETCH_SCRIPT)
print("exported", zp, "| CurseForge-hosted mods:", len(files), "| bundled jars:", len(extra), "| external downloads:", len(external), "| size MB: %.1f" % (os.path.getsize(zp) / 1e6))
