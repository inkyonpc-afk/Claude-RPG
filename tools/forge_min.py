"""Report the minimum Forge versions required by installed mods. Usage: python tools/forge_min.py [modsdir]"""
import zipfile, glob, re, collections, os, sys, tomllib
d0 = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".build", "server", "mods")
need = collections.defaultdict(list)
for j in glob.glob(os.path.join(d0, "*.jar")):
    try:
        z = zipfile.ZipFile(j)
        d = tomllib.loads(z.read("META-INF/mods.toml").decode("utf-8", "replace"))
    except Exception:
        continue
    deps = d.get("dependencies")
    for owner, lst in (deps.items() if isinstance(deps, dict) else []):
        for dd in lst:
            if dd.get("modId") == "forge":
                m = re.match(r"[\[\(]([\d\.]+)", dd.get("versionRange", ""))
                if m:
                    need[m.group(1)].append(os.path.basename(j))
key = lambda v: tuple(int(x) for x in v.split(".") if x.isdigit())
for v in sorted(need, key=key)[-8:]:
    print(v, len(need[v]), need[v][:4])
