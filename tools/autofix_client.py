"""Boot the test server repeatedly; when it fails on a client-class mixin, add the offending mod to pack/client_only.txt.
Usage: python tools/autofix_client.py <server_test args...>   (e.g. --cats qol --status core,std --fresh --tag x)
"""
import json, os, re, subprocess, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
lock = json.load(open(os.path.join(ROOT, "pack", "mods.lock.json"), encoding="utf-8"))
by_file = {e["fileName"]: e["name"] for e in lock if e["status"] != "core"}   # never auto-exclude core mods
args = sys.argv[1:]
tag = args[args.index("--tag") + 1] if "--tag" in args else "run"
for attempt in range(8):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "server_test.py")] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    res = [l for l in r.stdout.splitlines() if l.startswith("RESULT")]
    print("attempt", attempt, res[-1] if res else r.stdout[-300:])
    if not res or "DONE" in res[-1]:
        break
    log = open(os.path.join(ROOT, ".build", "logs", tag + ".log"), encoding="utf-8", errors="replace").read()
    blocks = re.findall(r"Mod File: [^\n]*?/mods/([^\n/]+\.jar)\n\s*Failure message: [^\n]*has failed to load correctly\n((?:[^\n]*\n){0,6})", log)
    cj = [j for j, body in blocks if "invalid dist" in body or "net.minecraft.client.renderer" in body or "net/minecraft/client/renderer" in body]
    if cj:
        names = [by_file[j] for j in sorted(set(cj)) if j in by_file]
        with open(os.path.join(ROOT, "pack", "client_only.txt"), "a", encoding="utf-8") as f:
            for n in names:
                f.write(re.sub(r"\s*[\[\(].*?[\]\)]", "", n).strip() + "\n")
        print("added to client_only (failed load, client class):", names)
        continue
    if "invalid dist DEDICATED_SERVER" not in log:
        print("failure is not a client-dist mixin; stopping for manual triage")
        break
    scan = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mixin_scan.py"), os.path.join(ROOT, ".build", "server", "mods"),
                           re.findall(r"load class (net/minecraft/client/[\w/$]+) for invalid dist", log)[-1]], capture_output=True, text=True).stdout
    jars = sorted({m.group(1) for l in scan.splitlines() for m in [re.match(r"^(.+?\.jar) ", l)] if m})
    names = [by_file[j] for j in jars if j in by_file]
    if not names:
        print("could not attribute; scan output:", scan[:300]); break
    with open(os.path.join(ROOT, "pack", "client_only.txt"), "a", encoding="utf-8") as f:
        for n in names:
            f.write(re.sub(r"\s*[\[\(].*?[\]\)]", "", n).strip() + "\n")
    print("added to client_only:", names)
