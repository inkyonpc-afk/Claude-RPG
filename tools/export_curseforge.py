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
# resource/shader packs tracked on CurseForge are referenced, not bundled
vis = json.load(open(os.path.join(ROOT, "pack", "visual_packs.json"), encoding="utf-8")) if os.path.isfile(os.path.join(ROOT, "pack", "visual_packs.json")) else []
vis_cf = {v["fileName"] for v in vis if v.get("projectID") and v.get("fileID")}
files += [{"projectID": v["projectID"], "fileID": v["fileID"], "required": True} for v in vis if v["fileName"] in vis_cf]
manifest = {"minecraft": {"version": "1.20.1", "modLoaders": [{"id": "forge-47.4.10", "primary": True}]}, "manifestType": "minecraftModpack", "manifestVersion": 1,
            "name": "Embers of Aldreth", "version": a.version, "author": "Claude + Connor", "overrides": "overrides", "files": files}
os.makedirs(os.path.join(ROOT, a.out), exist_ok=True)
zp = os.path.join(ROOT, a.out, "EmbersOfAldreth-%s.zip" % a.version)
INCLUDE_DIRS = ["config", "defaultconfigs", "kubejs", "mod_data", "resourcepacks", "shaderpacks", "datapacks"]
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
                full = os.path.join(dp, f)
                z.write(full, "overrides/" + os.path.relpath(full, ROOT).replace("\\", "/"))
    # options travel as Default Options defaults: applied on first launch only, so updates never clobber a player's settings
    if os.path.isfile(os.path.join(ROOT, "options.txt")):
        keep = [l for l in open(os.path.join(ROOT, "options.txt"), encoding="utf-8").read().splitlines() if not l.startswith(("lastServer:", "fullscreen", "overrideWidth", "overrideHeight"))]
        z.writestr("overrides/config/defaultoptions/options.txt", "\n".join(keep) + "\n")
    for fn in extra:   # jars without a CurseForge id travel inside the pack (personal/friends distribution)
        z.write(os.path.join(mods_dir, fn), "overrides/mods/" + fn)
print("exported", zp, "| CurseForge-hosted mods:", len(files), "| bundled jars:", len(extra), "| size MB: %.1f" % (os.path.getsize(zp) / 1e6))
