"""Launch the Forge client directly (offline test identity) in THIS instance folder, bypassing the CurseForge app.

  python tools/launch_client.py [--world NAME] [--wait SECONDS] [--shot NAME,NAME2] [--shot-at S,S2] [--keep] [--tag T]
Reads the Forge version JSON from minecraftinstance.json, builds the classpath from G:/curseforge/Install/libraries,
logs to .build/logs/client_<tag>.log, records the PID in .build/client.pid and kills ONLY that process when done (unless --keep).
Screenshots capture just the game window (tools/shot.ps1).
Linux (cloud sessions): reads the Forge JSON from <install>/versions (default .build/mc, set up by the Forge installer's --installClient),
runs the client on its own Xvfb display, and drives it with xdotool / ImageMagick `import`. Without a window manager there is no title bar,
so click coordinates are the game's own pixels (Windows coordinates include the title bar)."""
import argparse, json, os, pathlib, re, signal, subprocess, sys, threading, time, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIN = os.name == "nt"
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
ap.add_argument("--install", default="", help="launcher folder with libraries/assets/versions (default G:/curseforge/Install; Linux .build/mc)")
ap.add_argument("--gamedir", default="", help="game directory (default: this instance)")
ap.add_argument("--display", default=":99", help="Linux: X display to start Xvfb on")
a = ap.parse_args()
INSTALL = pathlib.Path(a.install) if a.install else (pathlib.Path("G:/curseforge/Install") if WIN else ROOT / ".build" / "mc")
LIBS = INSTALL / "libraries"
GAMEDIR = pathlib.Path(a.gamedir).resolve() if a.gamedir else ROOT
OSNAME, SEP = ("windows", ";") if WIN else ("linux", ":")

if WIN:
    prof = json.loads((ROOT / "minecraftinstance.json").read_text(encoding="utf-8-sig"))
    forge = json.loads(prof["baseModLoader"]["versionJson"])
else:
    forge = json.loads((INSTALL / "versions/1.20.1-forge-47.4.10/1.20.1-forge-47.4.10.json").read_text())
base = json.loads((INSTALL / "versions/1.20.1/1.20.1.json").read_text())
natives = ROOT / ".build" / "natives"
natives.mkdir(parents=True, exist_ok=True)


def allowed(e):
    skip = ["natives-linux", "natives-macos", "natives-windows-arm64", "natives-windows-x86"] if WIN else \
        ["natives-windows", "natives-macos", "natives-linux-arm64", "natives-linux-arm32"]
    if any(t in e.get("name", "") for t in skip):
        return False
    rules = e.get("rules")
    if not rules:
        return True
    ok = False
    for r in rules:
        o = r.get("os", {})
        if o.get("name", OSNAME) != OSNAME:
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
    if "natives-" + OSNAME in lib["name"]:
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():
                if n.endswith(".dll" if WIN else ".so"):
                    (natives / pathlib.Path(n).name).write_bytes(z.read(n))
fv = "1.20.1-47.4.10"
for p in [LIBS / "net/minecraft/client/1.20.1-20230612.114412/client-1.20.1-20230612.114412-extra.jar",
          LIBS / ("net/minecraftforge/forge/%s/forge-%s-client.jar" % (fv, fv)),
          LIBS / ("net/minecraftforge/forge/%s/forge-%s-universal.jar" % (fv, fv))]:
    if not p.exists():
        sys.exit("missing: %s" % p)
    arts.append(p)
cp = SEP.join(dict.fromkeys(x.as_posix() for x in arts))
variables = {"library_directory": LIBS.as_posix(), "classpath_separator": SEP, "version_name": "forge-47.4.10"}


def rep(v):
    for k, val in variables.items():
        v = v.replace("${%s}" % k, val)
    return v


jvm = ["-Xms2G", "-Xmx" + a.xmx, "-XX:+UseG1GC", "-Djava.library.path=" + natives.as_posix(), "-Dorg.lwjgl.librarypath=" + natives.as_posix()] + \
      [rep(x) for x in forge["arguments"]["jvm"] if isinstance(x, str)] + ["-DlegacyClassPath=" + cp, "-cp", cp]
game = ["--username", "AldrethTest", "--version", "forge-47.4.10", "--gameDir", GAMEDIR.as_posix(), "--assetsDir", (INSTALL / "assets").as_posix(),
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

logp = ROOT / ".build" / "logs" / ("client_%s.log" % a.tag)
logp.parent.mkdir(parents=True, exist_ok=True)
xvfb = None
if WIN:
    java = r"C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot\bin\java.exe"
    env, extra = None, {"creationflags": subprocess.CREATE_NO_WINDOW}
else:
    java = os.environ.get("JAVA17", "/usr/lib/jvm/java-17-openjdk-amd64/bin/java")
    env, extra = dict(os.environ, DISPLAY=a.display, LIBGL_ALWAYS_SOFTWARE="1"), {}
    if subprocess.run(["xdpyinfo", "-display", a.display], capture_output=True).returncode != 0:
        xvfb = subprocess.Popen(["Xvfb", a.display, "-screen", "0", a.size + "x24", "-nolisten", "tcp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
t0 = time.time()
p = subprocess.Popen([java, "@" + argfile.as_posix()], cwd=GAMEDIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                     errors="replace", env=env, **extra)
(ROOT / ".build" / "client.pid").write_text(str(p.pid))
XKEYS = {"{ESC}": "Escape", "{ENTER}": "Return", "{TAB}": "Tab", "{BACKSPACE}": "BackSpace", "{UP}": "Up", "{DOWN}": "Down", "{LEFT}": "Left",
         "{RIGHT}": "Right", "{PGUP}": "Prior", "{PGDN}": "Next", "{HOME}": "Home", "{END}": "End", " ": "space"}


def gui(verb, arg):
    """Run one GUI action; Windows uses tools/gui.ps1, Linux xdotool / ImageMagick on the Xvfb display."""
    if WIN:
        r = subprocess.run(["powershell", "-NoProfile", "-File", str(ROOT / "tools" / "gui.ps1"), "-ProcId", str(p.pid), "-Action", verb, "-Arg", arg],
                           capture_output=True, text=True)
        return r.stdout.strip() or r.stderr.strip()[:200]
    xd = lambda *args: subprocess.run(["xdotool"] + list(args), env=env, capture_output=True, text=True)
    if verb == "shot":
        r = subprocess.run(["import", "-display", a.display, "-window", "root", arg], capture_output=True, text=True)
        return "shot %s %s" % (arg, r.stderr.strip()[:120])
    if verb == "click":
        x, y = arg.split(",")[:2]
        xd("mousemove", x, y); time.sleep(0.15)
        xd("mousedown", "1"); time.sleep(0.22); xd("mouseup", "1")
        return "click %s,%s" % (x, y)
    if verb == "move":
        x, y = arg.split(",")[:2]
        xd("mousemove", x, y)
        return "move %s,%s" % (x, y)
    if verb == "scroll":
        x, y, delta = (int(v) for v in arg.split(","))
        xd("mousemove", str(x), str(y)); time.sleep(0.1)
        for _ in range(max(1, abs(delta) // 120)):
            xd("click", "4" if delta > 0 else "5")
        return "scroll %s" % arg
    if verb == "key":
        for tok in re.findall(r"\{[A-Z0-9]+\}|.", arg):
            name = XKEYS.get(tok) or (tok[1:-1] if tok.startswith("{") else tok)
            xd("key", name); time.sleep(0.12)
        return "key %s" % arg
    return "unknown action %s" % verb
marks = {}


def reader():
    with logp.open("w", encoding="utf-8") as f:
        for ln in p.stdout:
            f.write(ln)
            f.flush()
            for k, rx in (("sound", r"Sound engine started"), ("world", r"Preparing spawn area|Loaded \d+ advancements"), ("joined", r"joined the game|logged in with entity|\[FTB Quests/\]: Read \d+ bytes"),
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
        if WIN:
            r = subprocess.run(["powershell", "-NoProfile", "-File", str(ROOT / "tools" / "shot.ps1"), "-ProcId", str(p.pid), "-Out", str(out)],
                               capture_output=True, text=True)
            print(r.stdout.strip() or r.stderr.strip()[:200], flush=True)
        else:
            print(gui("shot", str(out)), flush=True)
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
        print(gui(verb, arg), flush=True)
    if "fatal" in marks and time.time() - t0 - marks["fatal"] > 5:
        break
    time.sleep(2)
status = "RUNNING" if p.poll() is None else "EXITED(%s)" % p.returncode
if "fatal" in marks:
    status = "CRASH"
print("CLIENT %s | markers %s | %.0fs | log %s" % (status, marks, time.time() - t0, logp.relative_to(ROOT)))
if not a.keep and p.poll() is None:
    if WIN:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
    else:
        p.send_signal(signal.SIGTERM)
        try:
            p.wait(timeout=20)
        except subprocess.TimeoutExpired:
            p.kill()
    print("stopped client pid", p.pid)
if xvfb and not a.keep:
    xvfb.terminate()
