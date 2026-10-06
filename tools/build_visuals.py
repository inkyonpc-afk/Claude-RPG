"""Visual/audio layer: copy the curated resource packs + shader packs from local CurseForge instances (read-only), record their CurseForge
project/file ids in pack/visual_packs.json (the export references them instead of bundling), write Complementary quality presets and the
resource-pack order. Usage: python tools/build_visuals.py [--options]   (--options also rewrites options.txt resourcePacks; client must be closed)"""
import glob, hashlib, json, os, re, shutil, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
INST = os.path.dirname(ROOT)

# lowest priority first (options.txt order); UI theme last so it wins
RESOURCE = ["FreshAnimations_v1.10.4.zip", "FA+All_Extensions-v1.4.zip", "FreshCompats_v1.6.zip", "Fresh mowzie mobs v. 1.2.1.zip",
            "Fancy Crops v1.3.zip", "Better+Lanterns+v1.2(mc-1.20.1).zip", "Just Fancy Torches v2.0.zip",
            "Better_End_Portal_Frame_(1.20).zip", "LowOnFire_1.20.1.zip", "SimplySwordsWhimscape_v1.1.zip", "Medieval_Style_Lootr.zip", "enchant icons 1.20 v1.3.zip",
            "[Compressed] Alternative Rain Sounds 1.20-1.20.1.zip", "More Cave Sounds.zip", "Soft-Weather-1.0-1.20.zip", "Cataclysmic_tunes_V8(Maledictus_update).zip",
            "Visual Titles.zip", "Alex's Titles 2.0.zip", "EclecticTrove-1.20.1-1.3.0.zip", "Better Fitting XP Mana Bar for Iron's Spells 'n Spellbooks.zip",
            "[1.4.1] Enhanced Boss Bars.zip", "EmbellishedStone-1.20.1-1.0.0.zip", "FTBQuestsShapesHeyKatu.zip",
            "STONEBORN+-+1.20-1.20.1+-+V3.2.3.zip", "SBMC-1.20.1-3.10.1.zip", "STONEBORN - 1.4-1.20.1 MeiAdditions.zip", "STONEBORN - Denis' Mod Compats v2.1.zip"]
SHADERS = ["ComplementaryReimagined_r5.9.3.zip", "ComplementaryUnbound_r5.9.3.zip"]
DEFAULT_SHADER = SHADERS[0]

# Complementary quality presets (keys/ranges read from the r5.9.3 shader source)
PRESETS = {
    "performance": dict(SHADOW_QUALITY=0, shadowDistance=96.0, WATER_REFLECT_QUALITY=0, BLOCK_REFLECT_QUALITY=0, LIGHTSHAFT_QUALI_DEFINE=0, SSAO_QUALI_DEFINE=0,
                        FXAA_DEFINE=1, DETAIL_QUALITY=0, CLOUD_QUALITY=1, ANISOTROPIC_FILTER=0),
    "balanced": dict(SHADOW_QUALITY=2, shadowDistance=128.0, WATER_REFLECT_QUALITY=1, BLOCK_REFLECT_QUALITY=1, LIGHTSHAFT_QUALI_DEFINE=1, SSAO_QUALI_DEFINE=2,
                     FXAA_DEFINE=1, DETAIL_QUALITY=2, CLOUD_QUALITY=2, ANISOTROPIC_FILTER=0),
    "high": dict(SHADOW_QUALITY=3, shadowDistance=192.0, WATER_REFLECT_QUALITY=2, BLOCK_REFLECT_QUALITY=3, LIGHTSHAFT_QUALI_DEFINE=2, SSAO_QUALI_DEFINE=2,
                 FXAA_DEFINE=1, DETAIL_QUALITY=3, CLOUD_QUALITY=2, ANISOTROPIC_FILTER=8),
    "ultra": dict(SHADOW_QUALITY=4, shadowDistance=256.0, WATER_REFLECT_QUALITY=2, BLOCK_REFLECT_QUALITY=3, LIGHTSHAFT_QUALI_DEFINE=3, SSAO_QUALI_DEFINE=3,
                  FXAA_DEFINE=1, DETAIL_QUALITY=4, CLOUD_QUALITY=3, ANISOTROPIC_FILTER=16),
}

# index every non-jar addon tracked by local instances: fileName -> (instance, addon record)
index = {}
for mi in glob.glob(os.path.join(INST, "*", "minecraftinstance.json")):
    inst = os.path.basename(os.path.dirname(mi))
    if inst == os.path.basename(ROOT):
        continue
    try:
        d = json.load(open(mi, encoding="utf-8"))
    except Exception:
        continue
    for a in d.get("installedAddons", []):
        f = a.get("installedFile") or {}
        if f.get("fileName"):
            index.setdefault(f["fileName"], (inst, a, f))


def sha1(p):
    h = hashlib.sha1()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def fetch(fn, sub):
    if fn not in index:
        raise SystemExit("not tracked by any local instance: " + fn)
    inst, a, f = index[fn]
    src = os.path.join(INST, inst, sub, fn)
    dst = os.path.join(ROOT, sub, fn)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(src):
        raise SystemExit("unzipped folder pack, not supported: " + src)
    if not os.path.isfile(dst):
        if not os.path.isfile(src):
            raise SystemExit("missing on disk: " + src)
        shutil.copy2(src, dst)
    return {"name": a.get("name"), "fileName": fn, "kind": sub, "projectID": a.get("addonID"), "fileID": f.get("id"), "downloadUrl": f.get("downloadUrl"), "sha1": sha1(dst),
            "from": inst}


out = [fetch(fn, "resourcepacks") for fn in RESOURCE] + [fetch(fn, "shaderpacks") for fn in SHADERS]
json.dump(out, open(os.path.join(ROOT, "pack", "visual_packs.json"), "w", encoding="utf-8"), indent=1)

pdir = os.path.join(ROOT, "config", "aldreth", "shader_presets")
os.makedirs(pdir, exist_ok=True)
for name, opts in PRESETS.items():
    open(os.path.join(pdir, name + ".txt"), "w", encoding="utf-8").write("".join("%s=%s\n" % kv for kv in opts.items()))
for sh in SHADERS:   # default every shader to BALANCED (Oculus reads <pack>.txt next to the zip)
    shutil.copy2(os.path.join(pdir, "balanced.txt"), os.path.join(ROOT, "shaderpacks", sh + ".txt"))

# Oculus: shader selected but OFF by default (performance first); toggle in Video Settings > Shader Packs
op = os.path.join(ROOT, "config", "oculus.properties")
props = {}
if os.path.isfile(op):
    for l in open(op, encoding="utf-8"):
        if "=" in l and not l.startswith("#"):
            k, v = l.rstrip("\n").split("=", 1)
            props[k] = v
props.update({"shaderPack": DEFAULT_SHADER, "enableShaders": "false"})
open(op, "w", encoding="utf-8").write("".join("%s=%s\n" % kv for kv in props.items()))

if "--options" in sys.argv:
    p = os.path.join(ROOT, "options.txt")
    s = open(p, encoding="utf-8").read()
    packs = ["vanilla", "mod_resources"] + ["file/" + fn for fn in RESOURCE]
    line = "resourcePacks:" + json.dumps(packs, ensure_ascii=False, separators=(",", ":"))
    s = re.sub(r"(?m)^resourcePacks:.*$", lambda m: line, s) if re.search(r"(?m)^resourcePacks:", s) else s + line + "\n"
    open(p, "w", encoding="utf-8").write(s)
    print("options.txt resourcePacks:", len(packs))
print("resource packs:", len(RESOURCE), "| shaders:", len(SHADERS), "| presets:", ", ".join(PRESETS))
