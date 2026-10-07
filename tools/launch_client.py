"""Launch the Forge client directly (offline test identity) in THIS instance folder, bypassing the CurseForge app.

  python tools/launch_client.py [--world NAME] [--wait SECONDS] [--shot NAME,NAME2] [--shot-at S,S2] [--keep] [--tag T]
Reads the Forge version JSON from minecraftinstance.json, builds the classpath from G:/curseforge/Install/libraries,
logs to .build/logs/client_<tag>.log, records the PID in .build/client.pid and kills ONLY that process when done (unless --keep).
Screenshots capture just the game window (tools/shot.ps1)."""
import argparse, json, pathlib, re, subprocess, sys, threading, time, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
INSTALL = pathlib.Path("G:/curseforge/Install")
LIBS = INSTALL / "libraries"
ap = argparse.ArgumentParser()
ap.add_argument("--world", default="")
ap.add_argument("--join", default="", help="host:port of a server to join (multiplayer test)")
ap.add_argument("--wait", type=int, default=180)
ap.add_argument("--shot", default="")
ap.add_argument("--shot-at", default="")
ap.add_argument("--tag", default="client")
ap.add_argument("--keep", action="store_true")
ap.add_argument("--script", default="", help="timed GUI actions: 'SECONDS:click x,y;SECONDS:key o;SECONDS:shot name'")
ap.add_argument("--xmx", default="10G")
ap.add_argument("--size", default="1280x720", help="window client size WxH")
a = ap.parse_args()

prof = json.loads((ROOT / "minecraftinstance.json").read_text(encoding="utf-8-sig"))
forge = json.loads(prof["baseModLoader"]["versionJson"])
base = json.loads((INSTALL / "versions/1.20.1/1.20.1.json").read_text())
natives = ROOT / ".build" / "natives"
natives.mkdir(parents=True, exist_ok=True)


def allowed(e):
    if any(t in e.get("name", "") for t in ["natives-linux", "natives-macos", "natives-windows-arm64", "natives-windows-x86"]):
        return False
    rules = e.get("rules")
    if not rules:
        return True
    ok = False
    for r in rules:
        o = r.get("os", {})
        if o.get("name", "windows") != "windows":
            continue
        if "arch" in o and o["arch"] not in ("x86_64", "amd64"):
            continue
        if "features" in r:
            continue
        ok = r["action"] == "allow"
    return ok


arts = []
for lib in forge["libraries"] + base["libraries"]:
    if not allowed(lib):
        continue
    art = lib.get("downloads", {}).get("artifact")
    if not art:
        continue
    p = LIBS / art["path"]
    if not p.exists():
        sys.exit("missing library: %s" % p)
    arts.append(p)
    if "natives-windows" in lib["name"]:
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():
                if n.endswith(".dll"):
                    (natives / pathlib.Path(n).name).write_bytes(z.read(n))
fv = "1.20.1-47.4.10"
for p in [LIBS / "net/minecraft/client/1.20.1-20230612.114412/client-1.20.1-20230612.114412-extra.jar",
          LIBS / ("net/minecraftforge/forge/%s/forge-%s-client.jar" % (fv, fv)),
          LIBS / ("net/minecraftforge/forge/%s/forge-%s-universal.jar" % (fv, fv))]:
    if not p.exists():
        sys.exit("missing: %s" % p)
    arts.append(p)
cp = ";".join(dict.fromkeys(x.as_posix() for x in arts))
variables = {"library_directory": LIBS.as_posix(), "classpath_separator": ";", "version_name": "forge-47.4.10"}


def rep(v):
    for k, val in variables.items():
        v = v.replace("${%s}" % k, val)
    return v


jvm = ["-Xms2G", "-Xmx" + a.xmx, "-XX:+UseG1GC", "-Djava.library.path=" + natives.as_posix(), "-Dorg.lwjgl.librarypath=" + natives.as_posix()] + \
      [rep(x) for x in forge["arguments"]["jvm"] if isinstance(x, str)] + ["-DlegacyClassPath=" + cp, "-cp", cp]
game = ["--username", "AldrethTest", "--version", "forge-47.4.10", "--gameDir", ROOT.as_posix(), "--assetsDir", (INSTALL / "assets").as_posix(),
        "--assetIndex", base["assetIndex"]["id"], "--uuid", "7044934c487f306d9e0d40257bbf3be1", "--accessToken", "0", "--userType", "legacy",
        "--versionType", "release", "--width", a.size.split("x")[0], "--height", a.size.split("x")[1]]
if a.world:
    game += ["--quickPlaySingleplayer", a.world]
elif a.join:
    game += ["--quickPlayMultiplayer", a.join]
game += [x for x in forge["arguments"]["game"] if isinstance(x, str)]
args = jvm + [forge["mainClass"]] + game
argfile = ROOT / ".build" / "client-args.txt"
argfile.write_text("\n".join('"' + x.replace("\\", "/").replace('"', '\\"') + '"' for x in args), encoding="utf-8")

java = r"C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot\bin\java.exe"
logp = ROOT / ".build" / "logs" / ("client_%s.log" % a.tag)
logp.parent.mkdir(parents=True, exist_ok=True)
t0 = time.time()
p = subprocess.Popen([java, "@" + argfile.as_posix()], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                     errors="replace", creationflags=subprocess.CREATE_NO_WINDOW)
(ROOT / ".build" / "client.pid").write_text(str(p.pid))
marks = {}


def reader():
    with logp.open("w", encoding="utf-8") as f:
        for ln in p.stdout:
            f.write(ln)
            f.flush()
            for k, rx in (("sound", r"Sound engine started"), ("world", r"Preparing spawn area|Loaded \d+ advancements"), ("joined", r"joined the game|logged in with entity"),
                          ("fatal", r"Crash report saved|Mod Loading has failed|Minecraft has crashed")):
                if k not in marks and re.search(rx, ln):
                    marks[k] = round(time.time() - t0)


threading.Thread(target=reader, daemon=True).start()
script = []
for part in [x for x in a.script.split(";") if x.strip()]:
    t, rest = part.split(":", 1)
    verb, _, arg = rest.strip().partition(" ")
    script.append((t.strip(), verb, arg))
si = 0
shots = [s for s in a.shot.split(",") if s]
shot_at = [int(s) for s in a.shot_at.split(",") if s]
done = 0
while p.poll() is None and time.time() - t0 < a.wait:
    if done < len(shots) and done < len(shot_at) and time.time() - t0 >= shot_at[done]:
        out = ROOT / ".build" / "shots" / (shots[done] + ".png")
        out.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["powershell", "-NoProfile", "-File", str(ROOT / "tools" / "shot.ps1"), "-ProcId", str(p.pid), "-Out", str(out)],
                           capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr.strip()[:200], flush=True)
        done += 1
    while si < len(script):
        tt = script[si][0]
        if tt.startswith("j"):
            if "joined" not in marks or time.time() - t0 < marks["joined"] + int(tt[1:]):
                break
        elif time.time() - t0 < int(tt):
            break
        _, verb, arg = script[si]
        si += 1
        if verb == "shot":
            outp = ROOT / ".build" / "shots" / (arg + ".png")
            outp.parent.mkdir(parents=True, exist_ok=True)
            arg = str(outp)
        r = subprocess.run(["powershell", "-NoProfile", "-File", str(ROOT / "tools" / "gui.ps1"), "-ProcId", str(p.pid), "-Action", verb, "-Arg", arg], capture_output=True, text=True)
        print((r.stdout.strip() or r.stderr.strip()[:200]), flush=True)
    if "fatal" in marks and time.time() - t0 - marks["fatal"] > 5:
        break
    time.sleep(2)
status = "RUNNING" if p.poll() is None else "EXITED(%s)" % p.returncode
if "fatal" in marks:
    status = "CRASH"
print("CLIENT %s | markers %s | %.0fs | log %s" % (status, marks, time.time() - t0, logp.relative_to(ROOT)))
if not a.keep and p.poll() is None:
    subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
    print("stopped client pid", p.pid)
