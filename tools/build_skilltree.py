"""Generate the Aldreth passive skill tree datapack (Passive Skill Tree 0.7.6) + docs/SKILL_TREE.md, validating IDs against the registry snapshot.

Output: config/paxi/datapacks/aldreth_core/data/aldreth/{skills/*.json, skill_trees/aldreth.json}; pack.mcmeta filter hides PST's default trees.
Usage: python tools/build_skilltree.py
"""
import json, math, os, re, sys, collections

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "design"))
from skilltree_lib import *            # noqa
import skilltree_content as C          # noqa

REG = json.load(open(os.path.join(ROOT, "pack", "registries_snapshot.json"), encoding="utf-8"))
ATTR, EFFECT, ITEM = set(REG["attribute"]), set(REG["mob_effect"]), set(REG["item"])
FAMILY = {"warrior": ["might"], "berserker": ["might"], "spellblade": ["arcane", "might"], "bloodmage": ["arcane"], "necromancer": ["arcane"], "arcanist": ["arcane"],
          "elementalist": ["arcane"], "druid": ["faith"], "cleric": ["faith"], "paladin": ["faith"], "guardian": ["faith"], "wanderer": ["finesse"], "ranger": ["finesse"], "rogue": ["finesse"]}
KIND = {"m": "minor", "E": "entry", "N": "notable", "M": "major", "S": "mastery", "K": "keystone"}
HALF = 9.6   # extreme node angle offset within a region wedge (degrees)
nodes, order, text = {}, [], {}
errors, warnings = [], []


def polar(r, deg):
    a = math.radians(deg)
    return r * math.cos(a), r * math.sin(a)


def link(a, b):
    if a == b:
        return
    nodes[a]["directConnections"] = sorted(set(nodes[a]["directConnections"]) | {b})
    nodes[b]["directConnections"] = sorted(set(nodes[b]["directConnections"]) | {a})


def add(nid, title, kind, icon, bonuses, x, y, start=False, color=""):
    j, tx = node_json(nid, title, kind, I_(icon), bonuses, x, y, [], start, color)
    nodes[nid] = j
    order.append(nid)
    text[nid] = (title, kind, tx)


def I_(icon):
    return "skilltree:textures/icons/%s.png" % icon


reg_idx = {r["key"]: r for r in C.REGIONS}
assert len(C.ORDER) == len(C.REGIONS) == 14
rings_by_region = {}
for i, key in enumerate(C.ORDER):
    R = reg_idx[key]
    center = i * 360.0 / len(C.ORDER)
    ring_ids = []
    counters = collections.Counter()
    pools = {"N": list(R["notables"]), "M": list(R["majors"]), "S": list(R["masteries"]), "K": list(R["keystones"])}
    minor_seen = collections.Counter()
    for r, (n, types) in enumerate(zip(RING_SIZES, RING_TYPES)):
        radius = RING_R0 + RING_STEP * r
        ids = []
        for j, ch in enumerate(types.split()):
            ang = center + (0 if n == 1 else (-HALF + 2 * HALF * j / (n - 1)))
            x, y = polar(radius, ang)
            nid = "aldreth:%s_%d_%d" % (key, r, j)
            if ch == "m":
                k = counters["m"] % len(R["minors"])
                title, icon, bon = R["minors"][k]
                minor_seen[title] += 1
                if minor_seen[title] > 1:
                    title += " " + ["", "II", "III", "IV", "V", "VI", "VII", "VIII"][minor_seen[title] - 1]
                counters["m"] += 1
            elif ch == "E":
                title, icon, bon = R["entry"]
            else:
                title, icon, bon = pools[ch][counters[ch]]
                counters[ch] += 1
            add(nid, title, KIND[ch], icon, bon, x, y, color="")
            ids.append(nid)
        ring_ids.append(ids)
    rings_by_region[key] = ring_ids
    # intra-region wiring: every node linked to nearest in the next ring; lateral links on web rings
    for r in range(len(ring_ids) - 1):
        a, b = ring_ids[r], ring_ids[r + 1]
        for j, nid in enumerate(b):
            pj = round(j * (len(a) - 1) / max(1, len(b) - 1)) if len(a) > 1 else 0
            link(nid, a[pj])
        for j, nid in enumerate(a):
            cj = round(j * (len(b) - 1) / max(1, len(a) - 1)) if len(a) > 1 else 0
            link(nid, b[cj])
    for r in (0, 2, 4, 6):
        for j in range(len(ring_ids[r]) - 1):
            link(ring_ids[r][j], ring_ids[r][j + 1])

# bridges between adjacent regions
for i, key in enumerate(C.ORDER):
    nxt = C.ORDER[(i + 1) % len(C.ORDER)]
    pair = (key, nxt)
    if pair not in C.BRIDGES:
        errors.append("missing bridge content for %s" % (pair,))
        continue
    (t_in, ic_in, b_in), (t_out, ic_out, b_out) = C.BRIDGES[pair]
    mid = (i * 360.0 / 14) + (360.0 / 14) / 2
    for tag, ring, (t, ic, b), kind in (("a", 3, (t_in, ic_in, b_in), "bridge"), ("b", 5, (t_out, ic_out, b_out), "bridge")):
        x, y = polar(RING_R0 + RING_STEP * ring, mid)
        nid = "aldreth:bridge_%s_%s_%s" % (key, nxt, tag)
        add(nid, t, kind, ic, b, x, y)
        link(nid, rings_by_region[key][ring][-1])
        link(nid, rings_by_region[nxt][ring][0])

# starts
starts = {}
for s in C.START_ORDER:
    members = [k for k, f in FAMILY.items() if f[0] == s or s in f]
    angs = [C.ORDER.index(k) * 360.0 / 14 for k in members]
    cx = sum(math.cos(math.radians(a)) for a in angs); cy = sum(math.sin(math.radians(a)) for a in angs)
    ang = math.degrees(math.atan2(cy, cx))
    x, y = polar(95.0, ang)
    title, icon, bon = C.START_INFO[s]
    nid = "aldreth:start_%s" % s
    add(nid, title, "start", icon, bon, x, y, start=True)
    starts[s] = nid
    for k in members:
        link(nid, rings_by_region[k][0][1])   # region entry (ring 0, middle)

# ---- validation ---------------------------------------------------------------------------------------------------------
def walk(o, nid):
    if isinstance(o, dict):
        t = o.get("type", "")
        if t == "skilltree:attribute" and o["attribute"] not in ATTR:
            errors.append("%s: unknown attribute %s" % (nid, o["attribute"]))
        if t in ("skilltree:inflict_effect", "skilltree:has_effect") and o.get("effect") not in EFFECT:
            errors.append("%s: unknown effect %s" % (nid, o.get("effect")))
        for v in o.values():
            walk(v, nid)
    elif isinstance(o, list):
        for x in o:
            walk(x, nid)


for nid, n in nodes.items():
    walk(n["bonuses"], nid)
    for c in n["directConnections"]:
        if c not in nodes:
            errors.append("%s: dangling connection %s" % (nid, c))
    if not n["directConnections"]:
        errors.append("%s: isolated" % nid)
# connectivity from any start
seen, stack = set(), [starts[s] for s in starts]
while stack:
    a = stack.pop()
    if a in seen:
        continue
    seen.add(a)
    stack.extend(nodes[a]["directConnections"])
if len(seen) != len(nodes):
    errors.append("unreachable nodes: %d" % (len(nodes) - len(seen)))
kcount = collections.Counter(v[1] for v in text.values())

# ---- output -------------------------------------------------------------------------------------------------------------
pack = os.path.join(ROOT, "config", "paxi", "datapacks", "aldreth_core")
sk_dir = os.path.join(pack, "data", "aldreth", "skills")
tr_dir = os.path.join(pack, "data", "aldreth", "skill_trees")
for d in (sk_dir, tr_dir):
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
for nid, n in nodes.items():
    json.dump(n, open(os.path.join(sk_dir, nid.split(":")[1] + ".json"), "w", encoding="utf-8"), indent=1)
json.dump({"id": "aldreth:aldreth", "skillIds": order}, open(os.path.join(tr_dir, "aldreth.json"), "w"), indent=1)
mc = {"pack": {"pack_format": 15, "description": "Embers of Aldreth core data (weapon taxonomy tags, skill tree, races, loot)"},
      "filter": {"block": [{"namespace": "skilltree", "path": "skill_trees/.*"}]}}
json.dump(mc, open(os.path.join(pack, "pack.mcmeta"), "w"), indent=2)

# docs
L = ["# Skill tree: the Constellation of Embers", "",
     "_Generated by `tools/build_skilltree.py` from `design/skilltree_content.py`. Do not edit by hand._", "",
     "**%d nodes** in 14 regions around 4 starting Oaths (Might, Finesse, the Arcane, Faith): %s." % (len(nodes), ", ".join("%d %s" % (v, k) for k, v in sorted(kcount.items()))), "",
     "Design rules: minor nodes are small and thematic; notables pair two effects; majors and masteries add conditions (low health, weapon class, shield, effects); **keystones are build-defining with a real trade-off**. Bridge nodes between neighbouring regions enable hybrids (Spellblade, Battlemage, Blood Knight, Druid-Cleric…).",
     "Weapon-class conditions use the `aldreth:weapons/<class>` item tags (see WEAPON_CLASSES.md). Respec with the Amnesia Scroll.", "",
     "Starting Oaths connect to: " + "; ".join("%s -> %s" % (s, ", ".join(sorted(k for k, f in FAMILY.items() if s in f))) for s in C.START_ORDER), ""]
for key in C.ORDER:
    R = reg_idx[key]
    L += ["## %s" % R["name"], "", "_%s_" % R["blurb"], ""]
    for kind in ("entry", "notable", "major", "mastery", "keystone"):
        items = [(nid, text[nid]) for nid in order if nid.startswith("aldreth:%s_" % key) and text[nid][1] == kind]
        if not items:
            continue
        L.append("**%ss**" % kind.capitalize() + ("" if kind == "entry" else "s")[0:0])
        for nid, (t, k, tx) in items:
            L.append("- *%s*: %s" % (t, "; ".join(tx)))
        L.append("")
L += ["## Bridges", ""]
for nid in order:
    if nid.startswith("aldreth:bridge_"):
        t, k, tx = text[nid]
        L.append("- *%s* (%s): %s" % (t, nid.split(":")[1].replace("bridge_", "").replace("_", "-"), "; ".join(tx)))
open(os.path.join(ROOT, "docs", "SKILL_TREE.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("nodes:", len(nodes), dict(kcount), "| errors:", len(errors))
for e in errors[:40]:
    print("ERR", e)
sys.exit(1 if errors else 0)
