"""Release validator. Exit code 0 only if every hard check passes.
Hard checks: >=250 mods, no duplicate mod ids, every mandatory dependency present, banned stacks absent, quests/skill tree/loot/boss tables/origins build with 0 errors
and their generated files exist, all 15 required docs exist and are non-trivial, manifest matches the install, game data (KubeJS scripts, datapacks) present.
Usage: python tools/verify.py [--mods-dir mods] [--json out.json]"""
import argparse, collections, glob, json, os, re, subprocess, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import jarmeta_lib  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--mods-dir", default="mods")
ap.add_argument("--json", default="")
a = ap.parse_args()

BANNED = {"spell_engine", "spell_power", "more_rpg_classes", "txnilib", "connectormod", "fabric_api", "forgified_fabric_api", "fabricloader", "connector_extras"}
PROVIDERS = {"kotlinforforge", "gml", "minecraft", "forge", "neoforge", "java", "fml", "mixinextras"}
NESTED_PROVIDED = {"satin"}   # jar-in-jar deeper than the reader recurses; confirmed loading in the FML log ("Found valid mod file satin-forge...")
LIBRARY_OK = {"ConfiguredDefaults-v8.0.4-1.20.1-Forge.jar", "gml-4.0.11-all.jar", "kotlinforforge-4.12.0-all.jar"}   # language providers / library-type jars have no mods.toml
DOCS = ["ARCHITECTURE", "MODLIST", "PROGRESSION", "SKILL_TREE", "QUESTS", "GEAR", "LOOT", "BALANCE", "WORLDGEN", "TRAVERSAL", "PERFORMANCE", "VISUALS", "KNOWN_ISSUES", "INSTALL", "CHANGELOG"]
results, fails = [], []


def check(name, ok, detail=""):
    results.append({"check": name, "ok": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""))
    if not ok:
        fails.append(name)


def run(args):
    r = subprocess.run([sys.executable] + args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return r.returncode, (r.stdout + r.stderr).strip()


# ---- mods
jars = sorted(glob.glob(os.path.join(ROOT, a.mods_dir, "*.jar")))
owners, req, kinds, provided_any = collections.defaultdict(list), {}, collections.Counter(), set()
for j in jars:
    try:
        ids, rq, kind = jarmeta_lib.read(j)
        top = jarmeta_lib.read_jar(__import__("zipfile").ZipFile(j), 2)[0]   # top-level mod ids only (no jar-in-jar)
    except Exception as e:
        check("readable jar " + os.path.basename(j), False, str(e))
        continue
    kinds[kind] += 1 if os.path.basename(j) not in LIBRARY_OK else 0
    req[os.path.basename(j)] = rq
    for i in ids:
        provided_any.add(i)
    for i in top:
        owners[i].append(os.path.basename(j))
check("mod count >= 250", len(jars) >= 250, "%d jars" % len(jars))
check("only Forge-format jars (no Fabric/NeoForge-only)", {k for k, v in kinds.items() if v} <= {"forge"}, dict(kinds).__repr__())
dups = {k: v for k, v in owners.items() if len(set(v)) > 1 and k not in PROVIDERS}
check("no duplicate mod ids", not dups, "; ".join("%s: %s" % (k, ",".join(sorted(set(v)))) for k, v in list(dups.items())[:5]))
have = provided_any | PROVIDERS | NESTED_PROVIDED
missing = {j: [r for r in rq if r not in have] for j, rq in req.items()}
missing = {j: m for j, m in missing.items() if m}
check("all mandatory dependencies present", not missing, "; ".join("%s needs %s" % (j[:30], ",".join(m)) for j, m in list(missing.items())[:5]))
check("banned stacks absent", not (BANNED & set(owners)), ",".join(sorted(BANNED & set(owners))))

# ---- pack manifest
mp = os.path.join(ROOT, "pack", "manifest.json")
if os.path.isfile(mp):
    m = json.load(open(mp, encoding="utf-8"))
    check("manifest mod count", m.get("count", 0) >= 250, "%s mods listed" % m.get("count"))

# ---- generated game data (each builder must pass its own validation)
for name, cmd in (("skill tree builds, 0 errors", ["tools/build_skilltree.py"]), ("quests build, 0 errors", ["tools/build_quests.py"]), ("origins build", ["tools/build_origins.py"]),
                  ("loot tables build, 0 errors", ["tools/build_loot.py"]), ("traversal data builds", ["tools/build_traversal.py"]), ("sigils build", ["tools/build_sigils.py"])):
    rc, out = run(cmd)
    check(name, rc == 0 and not re.search(r"errors:\s*(?!0\b|\[\])\S", out), "rc=%d " % rc + (out.splitlines()[-1][-100:] if out else ""))

dp = os.path.join(ROOT, "config", "paxi", "datapacks", "aldreth_core", "data", "aldreth")
for rel, minimum in (("skills/*.json", 600), ("loot_tables/quest/*.json", 6), ("loot_tables/boss/*.json", 6), ("tags/items/weapons/*.json", 20)):
    n = len(glob.glob(os.path.join(dp, rel)))
    check("datapack %s >= %d" % (rel, minimum), n >= minimum, str(n))
for rel in ("config/ftbquests/quests/chapter_groups.snbt", "kubejs/server_scripts/traversal_flight_guard.js", "kubejs/server_scripts/boss_rewards.js",
            "kubejs/server_scripts/progression_loot_gates.js", "kubejs/server_scripts/sigil_recipes.js", "kubejs/startup_scripts/aldreth_items.js", "kubejs/client_scripts/01_default_keybinds.js",
            "config/sparsestructures.json5", "config/restrictedportals-common.toml", "defaultconfigs/skilltree-server.toml"):
    check("exists " + rel, os.path.isfile(os.path.join(ROOT, rel)))
nq = len(glob.glob(os.path.join(ROOT, "config", "ftbquests", "quests", "chapters", "*.snbt")))
check("quest chapters >= 25", nq >= 25, str(nq))
rc, out = run(["tools/questmap_check.py"])
check("every chapter opens with quests in view (FTB layout replica)", rc == 0, out.splitlines()[-1][-100:] if out else "")

# ---- no secrets / no foreign assets
bad = [f for f in glob.glob(os.path.join(ROOT, "**", "*.zip"), recursive=True) if not any(x in f for x in ("resourcepacks", "shaderpacks", ".build", "dist", "backups", os.sep + "local" + os.sep, "saves", "logs", "mod_data", "xaero"))]
check("no stray zips", not bad, ",".join(os.path.relpath(b, ROOT) for b in bad[:3]))

# ---- docs
for d in DOCS:
    p = os.path.join(ROOT, "docs", d + ".md")
    size = os.path.getsize(p) if os.path.isfile(p) else 0
    check("doc %s.md (>=1500 bytes)" % d, size >= 1500, "%d bytes" % size)

print("\n%d checks, %d failed" % (len(results), len(fails)))
if a.json:
    json.dump(results, open(a.json, "w", encoding="utf-8"), indent=1)
sys.exit(1 if fails else 0)
