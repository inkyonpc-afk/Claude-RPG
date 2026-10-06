"""Headless Forge server validation.

  python tools/server_test.py [--cats ...] [--status ...] [--cmds file|"cmd;cmd"] [--timeout 900] [--fresh] [--keep-mods]
Syncs config/defaultconfigs/kubejs/global datapacks from the instance, installs the selected mod tier with --server,
boots, waits for 'Done', runs commands, stops, then copies the log to .build/logs/<tag>.log and prints a summary.
"""
import argparse, os, shutil, subprocess, sys, threading, time, re, json

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRV = os.path.join(ROOT, ".build", "server")
JAVA = r"C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot\bin\java.exe"
ap = argparse.ArgumentParser()
ap.add_argument("--cats", default="")
ap.add_argument("--status", default="core,std,test")
ap.add_argument("--cmds", default="forge tps")
ap.add_argument("--timeout", type=int, default=900)
ap.add_argument("--fresh", action="store_true", help="delete world first")
ap.add_argument("--no-install", action="store_true")
ap.add_argument("--tag", default="run")
ap.add_argument("--xmx", default="6G")
ap.add_argument("--seed", default="-8310405263479215")
a = ap.parse_args()

lockf = os.path.join(ROOT, ".build", "server_test.lock")
if os.path.isfile(lockf):
    old = open(lockf).read().strip()
    alive = subprocess.run(["tasklist", "/FI", "PID eq " + old], capture_output=True, text=True).stdout
    if old and (" " + old + " ") in alive:
        sys.exit("RESULT BUSY | another server_test (pid %s) is running" % old)
open(lockf, "w").write(str(os.getpid()))

if not a.no_install:
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "install.py"), "--server", "--dest", os.path.join(SRV, "mods"),
                        "--cats", a.cats, "--status", a.status], capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-500:])

for d in ("config", "defaultconfigs", "kubejs"):
    s, t = os.path.join(ROOT, d), os.path.join(SRV, d)
    if os.path.isdir(s):
        shutil.copytree(s, t, dirs_exist_ok=True)
# optional datapack sources (paxi-style global packs)
open(os.path.join(SRV, "eula.txt"), "w").write("eula=true\n")  # user-approved for local test server (2026-10-06)
props = {"online-mode": "false", "server-ip": "127.0.0.1", "server-port": "25599", "view-distance": "6", "simulation-distance": "6",
         "level-seed": a.seed, "motd": "EmbersOfAldreth test", "spawn-protection": "0", "enable-command-block": "true",
         "max-tick-time": "-1", "level-name": "world"}
open(os.path.join(SRV, "server.properties"), "w").write("\n".join("%s=%s" % kv for kv in props.items()) + "\n")
open(os.path.join(SRV, "user_jvm_args.txt"), "w").write("-Xms2G\n-Xmx%s\n-XX:+UseG1GC\n-XX:+ParallelRefProcEnabled\n-XX:MaxGCPauseMillis=200\n" % a.xmx)
if a.fresh and os.path.isdir(os.path.join(SRV, "world")):
    shutil.rmtree(os.path.join(SRV, "world"))
shutil.rmtree(os.path.join(SRV, "logs"), ignore_errors=True)

args_file = None
for dp, dn, fn in os.walk(os.path.join(SRV, "libraries", "net", "minecraftforge", "forge")):
    if "win_args.txt" in fn:
        args_file = os.path.relpath(os.path.join(dp, "win_args.txt"), SRV).replace("\\", "/")
cmd = [JAVA, "@user_jvm_args.txt", "@" + args_file, "nogui"]
t0 = time.time()
p = subprocess.Popen(cmd, cwd=SRV, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
open(os.path.join(ROOT, ".build", "server.pid"), "w").write(str(p.pid))
lines, done_at, fatal_at = [], [None], [None]


def reader():
    for ln in p.stdout:
        lines.append(ln.rstrip("\n"))
        if done_at[0] is None and re.search(r"Done \(\d", ln):
            done_at[0] = time.time()
        if fatal_at[0] is None and re.search(r"Crash report saved to|Failed to start the minecraft server|Mod Loading has failed|Encountered an unexpected exception", ln):
            fatal_at[0] = time.time()


th = threading.Thread(target=reader, daemon=True)
th.start()
while p.poll() is None and done_at[0] is None and time.time() - t0 < a.timeout and not (fatal_at[0] and time.time() - fatal_at[0] > 8):
    time.sleep(1)

result = "BOOT_FAIL"
if done_at[0]:
    result = "DONE"
    cmds = a.cmds
    if os.path.isfile(cmds):
        cmds = ";".join(l.strip() for l in open(cmds) if l.strip() and not l.startswith("#"))
    for c in [x.strip() for x in cmds.split(";") if x.strip()]:
        if c.startswith("wait "):
            time.sleep(float(c.split()[1]))
            continue
        try:
            p.stdin.write(c + "\n"); p.stdin.flush()
        except Exception:
            break
        time.sleep(2)
    time.sleep(2)
    try:
        p.stdin.write("stop\n"); p.stdin.flush()
    except Exception:
        pass
    try:
        p.wait(timeout=120)
    except subprocess.TimeoutExpired:
        p.kill(); result = "STOP_HANG"
else:
    if p.poll() is None:
        p.kill(); result = "BOOT_FAIL" if fatal_at[0] else "TIMEOUT"
th.join(timeout=5)

os.makedirs(os.path.join(ROOT, ".build", "logs"), exist_ok=True)
out = os.path.join(ROOT, ".build", "logs", a.tag + ".log")
open(out, "w", encoding="utf-8").write("\n".join(lines))
mods = len([f for f in os.listdir(os.path.join(SRV, "mods")) if f.endswith(".jar")]) if os.path.isdir(os.path.join(SRV, "mods")) else 0
boot = (done_at[0] - t0) if done_at[0] else None
print("RESULT %s | jars %d | boot %s | log %s" % (result, mods, ("%.0fs" % boot) if boot else "n/a", os.path.relpath(out, ROOT)))
cr = os.path.join(SRV, "crash-reports")
if os.path.isdir(cr):
    newest = sorted(os.listdir(cr))[-1:] 
    if newest:
        print("crash report:", newest[0])
