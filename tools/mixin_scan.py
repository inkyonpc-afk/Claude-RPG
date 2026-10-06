"""Find common/server mixins whose bytecode references client-only classes (cause of 'invalid dist DEDICATED_SERVER' crashes).
Usage: python tools/mixin_scan.py [modsdir] [needle]"""
import zipfile, glob, json, re, sys, os
d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".build", "server", "mods")
needle = (sys.argv[2] if len(sys.argv) > 2 else "net/minecraft/client/player/LocalPlayer").encode()
for j in sorted(glob.glob(os.path.join(d, "*.jar"))):
    try:
        z = zipfile.ZipFile(j)
    except Exception:
        continue
    names = set(z.namelist())
    for n in names:
        if n.endswith(".json") and "mixin" in n.lower() and "/" not in n:
            try:
                cfg = json.loads(re.sub(r"^\s*//.*$", "", z.read(n).decode("utf-8", "replace"), flags=re.M))
            except Exception:
                continue
            pkg = cfg.get("package", "").replace(".", "/")
            for m in cfg.get("mixins", []) + cfg.get("server", []):
                p = "%s/%s.class" % (pkg, m.replace(".", "/"))
                if p in names and needle in z.read(p):
                    print(os.path.basename(j), n, m)
