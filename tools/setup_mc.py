"""Set up a Minecraft 1.20.1 + Forge 47.4.10 client install for tools/launch_client.py on Linux (cloud sessions); the Windows machine uses
G:/curseforge/Install instead. Idempotent; every download is sha1-checked against Mojang's metadata.

  python tools/setup_mc.py [--dir .build/mc]
Steps: Forge installer --installClient (patched client jars + Forge libraries), the vanilla 1.20.1 version JSON (the installer does not write
it), every library allowed on Linux, and the asset index plus all asset objects (about 650 MB)."""
import argparse, concurrent.futures as cf, hashlib, json, os, subprocess, urllib.request

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FORGE = "1.20.1-47.4.10"
JAVA = os.environ.get("JAVA17", "/usr/lib/jvm/java-17-openjdk-amd64/bin/java")
ap = argparse.ArgumentParser()
ap.add_argument("--dir", default=os.path.join(ROOT, ".build", "mc"))
a = ap.parse_args()
MC = a.dir
os.makedirs(MC, exist_ok=True)


def fetch(url, path, sha1=None):
    if os.path.isfile(path) and (not sha1 or hashlib.sha1(open(path, "rb").read()).hexdigest() == sha1):
        return 0
    data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ClaudeRPG-setup"}), timeout=120).read()
    if sha1 and hashlib.sha1(data).hexdigest() != sha1:
        raise SystemExit("sha1 mismatch: " + url)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(data)
    return len(data)


# 1. Forge client (runs the installer's processors: binary patches, srg/extra jars)
if not os.path.isfile(os.path.join(MC, "libraries", "net", "minecraftforge", "forge", FORGE, "forge-%s-client.jar" % FORGE)):
    inst = os.path.join(ROOT, ".build", "dl", "forge-%s-installer.jar" % FORGE)
    fetch("https://maven.minecraftforge.net/net/minecraftforge/forge/%s/forge-%s-installer.jar" % (FORGE, FORGE), inst)
    lp = os.path.join(MC, "launcher_profiles.json")
    if not os.path.isfile(lp):
        open(lp, "w").write('{"profiles":{}}')
    r = subprocess.run([JAVA, "-jar", inst, "--installClient", MC], cwd=MC, capture_output=True, text=True)
    print("forge:", (r.stdout.strip().splitlines() or ["?"])[-2:])
# 2. vanilla version JSON
vpath = os.path.join(MC, "versions", "1.20.1", "1.20.1.json")
if not os.path.isfile(vpath):
    man = json.load(urllib.request.urlopen("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json", timeout=60))
    ent = [v for v in man["versions"] if v["id"] == "1.20.1"][0]
    fetch(ent["url"], vpath, ent.get("sha1"))
v = json.load(open(vpath))
fj = json.load(open(os.path.join(MC, "versions", "1.20.1-forge-47.4.10", "1.20.1-forge-47.4.10.json")))


# 3. libraries allowed on Linux (the launcher normally does this)
def allowed(lib):
    ok = not lib.get("rules")
    for r in lib.get("rules", []):
        if r.get("os", {}).get("name", "linux") == "linux":
            ok = r["action"] == "allow"
    return ok


arts = [lib["downloads"]["artifact"] for lib in v["libraries"] + fj["libraries"] if allowed(lib) and lib.get("downloads", {}).get("artifact", {}).get("url")]
with cf.ThreadPoolExecutor(16) as ex:
    got = list(ex.map(lambda art: fetch(art["url"], os.path.join(MC, "libraries", art["path"]), art.get("sha1")), arts))
print("libraries: %d (%d downloaded)" % (len(arts), sum(1 for g in got if g)))
# 4. assets
ai = v["assetIndex"]
ipath = os.path.join(MC, "assets", "indexes", ai["id"] + ".json")
fetch(ai["url"], ipath, ai.get("sha1"))
objs = json.load(open(ipath))["objects"].values()
with cf.ThreadPoolExecutor(32) as ex:
    got = list(ex.map(lambda o: fetch("https://resources.download.minecraft.net/%s/%s" % (o["hash"][:2], o["hash"]),
                                      os.path.join(MC, "assets", "objects", o["hash"][:2], o["hash"]), o["hash"]), objs))
print("assets: %d objects (%d downloaded, %.0f MB)" % (len(got), sum(1 for g in got if g), sum(got) / 1e6))
