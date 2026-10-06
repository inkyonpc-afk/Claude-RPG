"""Shared jar metadata reader."""
import io, json, re, zipfile
try:
    import tomllib
except ImportError:
    tomllib = None
SKIP = {"minecraft", "forge", "neoforge", "java", "fml", "mixinextras"}
def parse_toml(txt):
    try:
        return tomllib.loads(txt)
    except Exception:
        # tolerant fallback: regex for modId lines and mandatory deps
        d = {"mods": [], "dependencies": {}}
        for m in re.finditer(r'^\s*modId\s*=\s*"([^"]+)"', txt, re.M):
            d["mods"].append({"modId": m.group(1)})
        return d


def read_jar(z, depth=0):
    modids, req, kind = [], [], "none"
    names = z.namelist()
    if "META-INF/mods.toml" in names:
        kind = "forge"
        data = parse_toml(z.read("META-INF/mods.toml").decode("utf-8", "replace"))
        mods = [m["modId"] for m in data.get("mods", []) if isinstance(m, dict) and "modId" in m]
        modids += mods
        dmap = data.get("dependencies") or {}
        if isinstance(dmap, list):
            dmap = {"x": dmap}
        for owner, deps in dmap.items():
            for dd in deps if isinstance(deps, list) else []:
                if isinstance(dd, dict) and dd.get("mandatory", False) in (True, "true") and dd.get("side", "BOTH") != "CLIENT_DISABLED":
                    req.append(dd.get("modId"))
    elif "META-INF/neoforge.mods.toml" in names:
        kind = "neoforge"
    elif "fabric.mod.json" in names:
        kind = "fabric"
        try:
            j = json.loads(z.read("fabric.mod.json").decode("utf-8", "replace"))
            modids.append(j.get("id"))
        except Exception:
            pass
    if depth < 2:
        for n in names:
            if n.startswith("META-INF/jarjar/") and n.endswith(".jar"):
                try:
                    sub = zipfile.ZipFile(io.BytesIO(z.read(n)))
                    m2, _, _ = read_jar(sub, depth + 1)
                    modids += m2
                except Exception:
                    pass
    return modids, req, kind




def read(path):
    z = zipfile.ZipFile(path)
    modids, req, kind = read_jar(z)
    own = set(modids)
    return sorted(set(modids)), sorted({r for r in req if r and r not in SKIP and r not in own}), kind
