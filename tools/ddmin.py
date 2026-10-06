"""Delta-debug a failing category: find which candidate mod(s) in CAT cause a boot failure matching MARKER.
Usage: python tools/bisect.py CAT BASECATS [MARKER]
Temporarily uses pack/rejects.txt to disable candidates (removed at the end)."""
import json, os, re, subprocess, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
cat, base = sys.argv[1], sys.argv[2]
marker = sys.argv[3] if len(sys.argv) > 3 else "did not get ID"
lock = json.load(open(os.path.join(ROOT, "pack", "mods.lock.json"), encoding="utf-8"))
names = [e["name"] for e in lock if e["category"] == cat and e["why"] == "candidate" and e["status"] in ("core", "std")]
norm = lambda n: re.sub(r"\s+", " ", re.sub(r"\s*[\[\(].*?[\]\)]", "", n or "")).strip().lower()
rej = os.path.join(ROOT, "pack", "rejects.txt")
out = open(os.path.join(ROOT, ".build", "bisect_%s.out" % cat), "w")


def log(*a):
    print(*a, file=out, flush=True)


def fails(subset):
    off = [n for n in names if n not in subset]
    open(rej, "w", encoding="utf-8").write("\n".join(norm(n) for n in off) + "\n")
    lk = os.path.join(ROOT, ".build", "server_test.lock")
    if os.path.isfile(lk):
        os.remove(lk)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "server_test.py"), "--cats", base + "," + cat, "--status", "core,std", "--fresh",
                        "--tag", "bisect", "--timeout", "600"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    res = [l for l in r.stdout.splitlines() if l.startswith("RESULT")]
    logt = open(os.path.join(ROOT, ".build", "logs", "bisect.log"), encoding="utf-8", errors="replace").read()
    bad = marker in logt
    log("test %d mods -> %s | marker=%s" % (len(subset), res[-1] if res else "?", bad))
    return bad


try:
    cur = list(names)
    log("start with %d mods; full set fails: %s" % (len(cur), fails(cur)))
    while len(cur) > 1:
        h = len(cur) // 2
        a, b = cur[:h], cur[h:]
        if fails(a):
            cur = a
        elif fails(b):
            cur = b
        else:
            log("interaction between halves; remaining %d mods: %s" % (len(cur), cur))
            break
    log("CULPRIT(S): %s" % cur)
finally:
    if os.path.isfile(rej):
        os.remove(rej)
    log("FINISHED")
