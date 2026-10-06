"""Derive per-tier spread factors from measured censuses (tools/structure_census.py --json).
Model: spacing and separation both scale with the factor f, so structure density scales as 1/f^2. Each generated structure is normalised back to f=1
(count * f_used^2), the tier's base density D1 is pooled over all samples per km2, and f_new = sqrt(D1 / target). Tiers with few samples are blended toward their
prior factor (weight n/(n+10) in log space) because a few km2 is a small, biased sample. Biome-bound ocean decor is excluded (fixed factor).
Each input is census.json[@used_config.json5], the config being the spacing the census world was generated with (default: the server's current copy).
Output: config/aldreth/spacing_calibration.json (read by tune_structures.py).
Usage: python tools/calibrate_spacing.py census1.json[@config1] [census2.json[@config2] ...]"""
import argparse, collections, json, math, os, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import spacing_tiers as ST  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("inputs", nargs="+")
a = ap.parse_args()
DEFAULT_CFG = os.path.join(ROOT, ".build", "server", "config", "sparsestructures.json5")


def load_cfg(path):
    txt = open(path, encoding="utf-8").read()
    used = json.loads(txt[txt.index("{"):])
    by_set = {c["structure"]: c["factor"] for c in used["customSpreadFactors"]}
    by_ns = collections.defaultdict(list)
    for s, f in by_set.items():
        by_ns[s.split(":")[0]].append((s.split(":")[1], f))
    return used.get("spreadFactor", 2), by_set, by_ns


def used_factor(cfg, sid):
    """the factor the census world used for a structure: exact set id, else the set whose name prefixes the path, else the namespace's most common factor."""
    default_used, by_set, by_ns = cfg
    if sid in by_set:
        return by_set[sid]
    ns, path = sid.split(":", 1)
    for name, f in by_ns.get(ns, []):
        if path.startswith(name) or path.startswith(name.rstrip("s")) or name.startswith(path.split("/")[0]):
            return f
    if by_ns.get(ns):
        return collections.Counter(f for _, f in by_ns[ns]).most_common(1)[0][0]
    return default_used


area_total, d1_sum, n = 0.0, collections.defaultdict(float), collections.Counter()
for spec in a.inputs:
    path, _, cfgpath = spec.partition("@")
    cfg = load_cfg(cfgpath or DEFAULT_CFG)
    census = json.load(open(path, encoding="utf-8"))
    area_total += census["area_km2"]
    for sid, cnt in census["structures"].items():
        t = ST.classify(sid)
        f = used_factor(cfg, sid)
        d1_sum[t] += cnt * f * f
        n[t] += cnt
d1 = {t: v / area_total for t, v in d1_sum.items()}

prior = {t: x for t, x, _, _ in ST.TIERS}
prior["default"] = ST.DEFAULT_FACTOR
out, rows = dict(prior), []
for t, target in ST.TARGETS.items():
    if n[t] == 0:
        rows.append((t, 0, None, prior[t], prior[t]))
        continue
    raw = math.sqrt(d1[t] / target)
    w = n[t] / (n[t] + 10.0)
    f = math.exp((1 - w) * math.log(prior[t]) + w * math.log(raw))
    out[t] = round(min(6.0, max(1.0, f)) / 0.05) * 0.05
    rows.append((t, n[t], raw, prior[t], out[t]))
print("%-11s %6s %8s %7s %7s   (area %.2f km2 pooled)" % ("tier", "starts", "raw f", "prior", "final", area_total))
for t, cnt, raw, pr, fin in rows:
    print("%-11s %6d %8s %7.2f %7.2f   D1=%.1f/km2 target=%.1f" % (t, cnt, "%.2f" % raw if raw else "n/a", pr, fin, d1.get(t, 0), ST.TARGETS[t]))
os.makedirs(os.path.join(ROOT, "config", "aldreth"), exist_ok=True)
json.dump({"area_km2": round(area_total, 2), "targets": ST.TARGETS, "factors": {k: round(v, 2) for k, v in out.items()}, "starts": dict(n)},
          open(os.path.join(ROOT, "config", "aldreth", "spacing_calibration.json"), "w", encoding="utf-8"), indent=1)
