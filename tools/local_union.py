"""Build a union index of CurseForge addons installed across local 1.20.1 Forge instances.

Read-only on the other instances. Output: pack/local_union.json (keyed by addonID).
Each entry: name, kind (mods/resourcepacks/shaderpacks), fileId, fileName, downloadUrl, sha1, instances[], jar (abs path of an existing copy).
"""
import json, os, sys

ROOT = r"G:\curseforge\Instances"
OUT = os.path.join(os.path.dirname(__file__), "..", "pack", "local_union.json")
SELF = "Claude RPG"
FOLDERS = {6: "mods", 12: "resourcepacks", 6552: "shaderpacks", 17: "saves"}


def main():
    union = {}
    for inst in sorted(os.listdir(ROOT)):
        if inst == SELF:
            continue
        mi = os.path.join(ROOT, inst, "minecraftinstance.json")
        if not os.path.isfile(mi):
            continue
        try:
            data = json.load(open(mi, encoding="utf-8"))
        except Exception as e:
            print("skip", inst, e)
            continue
        if data.get("gameVersion") != "1.20.1":
            continue
        loader = (data.get("baseModLoader") or {}).get("name", "")
        if not loader.startswith("forge"):
            continue
        for a in data.get("installedAddons") or []:
            f = a.get("installedFile") or {}
            aid = a.get("addonID")
            if not aid or not f:
                continue
            fname = f.get("fileName") or ""
            sub = a.get("modFolderPath") or ""
            jar = os.path.join(sub, a.get("fileNameOnDisk") or fname) if sub else ""
            if not os.path.isfile(jar):
                jar = ""
            sha1 = next((h["value"] for h in f.get("hashes", []) if h.get("algo") == 1 or h.get("type") == 1), "")
            e = union.get(aid)
            kind = os.path.basename(sub).lower() if sub else ""
            rec = dict(name=a.get("name"), kind=kind,
                       fileId=f.get("id"), fileName=fname, downloadUrl=f.get("downloadUrl"),
                       sha1=sha1, jar=jar, addonId=aid, deps=[d["addonId"] for d in f.get("dependencies", []) if d.get("type") == 3], gameVersions=f.get("gameVersion"), instances=[inst])
            if e is None:
                union[aid] = rec
            else:
                e["instances"].append(inst)
                if (f.get("id") or 0) > (e["fileId"] or 0):
                    rec["instances"] = e["instances"]
                    union[aid] = rec
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(union, open(OUT, "w", encoding="utf-8"), indent=0)
    withjar = sum(1 for v in union.values() if v["jar"])
    print("addons:", len(union), "with local jar:", withjar, "->", os.path.relpath(OUT))


if __name__ == "__main__":
    main()
