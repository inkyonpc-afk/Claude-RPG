"""Model L2 Hostility mob scaling for this pack without starting the game.

Formulas from L2 Hostility 2.5.19 (github.com/Minecraft-LightLand/L2Hostility, tag 2.5.19 = commit a799baf):
  mob level   = round(dimBase + biomeBase + round(distanceFactor * blocks from 0,0) + sectionLevel + P * (dimScale + biomeScale) + gauss * dimVar)
                (MobDifficultyCollector.getDifficulty, SectionDifficulty.modifyInstanceInternal)
  P (player)  = adaptive level + dimensionFactor * (dimensions visited - 1)          (PlayerDifficulty.getLevel / getExtraLevel)
  adaptive    = per kill exp += min(adaptive + 10, mob level)^2; level up while exp >= adaptive^2 * killsPerLevel   (DifficultyLevel.grow)
  health      = x (1 + healthFactor * level), damage x (1 + damageFactor * level)    (TraitManager.scale, LHAttackListener; linear unless exponential*)
  P comes from the LOWEST-level player within newPlayerProtectRange of the mob, else the nearest player within 128 blocks (PlayerFinder).
Built-in dimension entries (src/generated/.../l2hostility_config/difficulty): overworld base 0 / scale 1.0 / var 4, nether 20 / 1.2 / 9,
end 40 / 1.5 / 16. Any other dimension uses the config defaults (defaultLevelBase/Scale/Var) unless some mod ships its own entry.
Not modeled: biome bonuses (overworld biomes add 5-20, deep dark 50), per-chunk-section adaptive levels, traits, per-boss health/attack scales.

Usage: python tools/hostility_model.py [--md] | --measured .build/logs/<tag>.log (a tests/l2_curve.txt server run)"""
import os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CFG = os.path.join(ROOT, "config", "l2_configs", "l2hostility-common.toml")
BUILTIN = {"minecraft:overworld": (0, 1.0, 4.0), "minecraft:the_nether": (20, 1.2, 9.0), "minecraft:the_end": (40, 1.5, 16.0)}
# Act plan from docs/PROGRESSION.md: realms first entered in each act (the Iron's Spells pocket dimension also counts once visited).
ACTS = [("I Awakening", ["minecraft:overworld"]),
        ("II A Wider World", ["minecraft:the_nether", "twilightforest:twilight_forest", "undergarden:undergarden"]),
        ("III Beyond the Veil", ["aether:the_aether", "blue_skies:everbright", "blue_skies:everdawn"]),
        ("IV Fallen Kingdoms", ["deeperdarker:otherside"]),
        ("V End of the Age", ["minecraft:the_end"])]


def load_cfg(path=CFG):
    vals = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"\s*(\w+)\s*=\s*([^#\s]+)", line)
        if m:
            v = m.group(2)
            vals[m.group(1)] = v == "true" if v in ("true", "false") else float(v)
    return vals


def dim_params(dim, c):
    return BUILTIN.get(dim, (int(c["defaultLevelBase"]), c["defaultLevelScale"], c["defaultLevelVar"]))


def mob_level(dim, p, c, dist=0):
    base, scale, _ = dim_params(dim, c)
    return max(0, round(base + round(c["distanceFactor"] * dist) + p * scale))


def mult(level, c):
    return 1 + c["healthFactor"] * level, 1 + c["damageFactor"] * level


def adaptive_after(kills, extra, dim, c, start=0, dist=0):
    """Adaptive level after `kills` kills of average mobs in `dim` while the player carries `extra` bonus levels (dimensions)."""
    a, exp = start, 0
    for _ in range(kills):
        lv = mob_level(dim, a + extra, c, dist)
        exp += min(a + 10, lv) ** 2
        while exp >= a * a * c["killsPerLevel"]:
            exp -= a * a * c["killsPerLevel"]
            a += 1
    return a


def report(md=False):
    c = load_cfg()
    out = []
    row = (lambda *x: out.append("| " + " | ".join(str(v) for v in x) + " |")) if md else (lambda *x: out.append("  ".join("%-22s" % v for v in x)))
    out.append("Config: health +%.0f%%/level, damage +%.0f%%/level, +%g levels per 1000 blocks, +%d levels per extra dimension, %d kills per level, death keeps %.0f%%."
               % (c["healthFactor"] * 100, c["damageFactor"] * 100, c["distanceFactor"] * 1000, c["dimensionFactor"], c["killsPerLevel"], c["playerDeathDecay"] * 100))
    out.append("")
    # 1) kills needed: adaptive level after N kills in the overworld near spawn (no dimension bonus)
    if md:
        out += ["Adaptive player level from kills alone (overworld, mobs at the player's own level):", "", "| kills | 100 | 300 | 1000 | 3000 |", "|---|---|---|---|---|"]
    row("overworld adaptive lv", *[adaptive_after(k, 0, "minecraft:overworld", c) for k in (100, 300, 1000, 3000)])
    out.append("")
    # 2) act table: dimensions visited so far add dimensionFactor each; adaptive level assumed from a kill budget per act
    budget = [300, 500, 500, 500, 400]   # assumed hostile kills per act (play-style dependent; see BALANCE.md)
    if md:
        out += ["| Act | dims visited | assumed kills (total) | adaptive | P | newest realm: mob lv / HP x / dmg x | overworld at 0 / 3000 blocks: mob lv / HP x |",
                "|---|---|---|---|---|---|---|"]
    visited, a, kills = 0, 0, 0
    for (name, dims), k in zip(ACTS, budget):
        visited += len(dims)
        extra = int(c["dimensionFactor"]) * (visited - 1)
        a = adaptive_after(k, extra, dims[0] if name.startswith("I ") else dims[0], c, start=a)
        kills += k
        p = a + extra
        realm = dims[-1] if name.startswith("I ") else dims[0]
        lv = mob_level(realm, p, c)
        hp, dmg = mult(lv, c)
        ow0, ow3 = mob_level("minecraft:overworld", p, c), mob_level("minecraft:overworld", p, c, 3000)
        row(name, visited, kills, a, p, "%s %d / %.1f / %.1f" % (realm.split(":")[1], lv, hp, dmg), "%d / %.1f, %d / %.1f" % (ow0, mult(ow0, c)[0], ow3, mult(ow3, c)[0]))
    return "\n".join(out), c


def measured(log):
    """Compare a tests/l2_curve.txt run (player level 0: no player online) with the model's dimension base + distance bonus."""
    c = load_cfg()
    rows, cur = [], None
    for ln in open(log, encoding="utf-8", errors="replace"):
        m = re.search(r"SAMPLE (\S+) (\S+) (-?\d+)", ln)
        if m:
            cur = dict(name=m.group(1), dim=m.group(2), x=int(m.group(3)), lv=[], hp=[])
            if cur["name"] != "end":
                rows.append(cur)
            continue
        if cur is None:
            continue
        m = re.search(r"has the following entity data: (-?\d+)", ln)
        if m:
            cur["lv"].append(int(m.group(1)))
        m = re.search(r"Value of attribute Max Health for (?:entity )?\S+ is ([\d.]+)", ln)
        if m:
            cur["hp"].append(float(m.group(1)))
    out = ["| sample | dimension | blocks from 0,0 | husks | L2 level (mean, range) | model at player level 0 | max health (husk base 20) |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        base = dim_params(r["dim"], c)[0] + round(c["distanceFactor"] * abs(r["x"]))
        lv = ("%.1f (%d-%d)" % (sum(r["lv"]) / len(r["lv"]), min(r["lv"]), max(r["lv"]))) if r["lv"] else "none"
        hp = ("%.0f" % (sum(r["hp"]) / len(r["hp"]))) if r["hp"] else "n/a"
        out.append("| %s | %s | %d | %d | %s | %d | %s |" % (r["name"], r["dim"], r["x"], len(r["lv"]), lv, base, hp))
    return "\n".join(out)


if __name__ == "__main__":
    if "--measured" in sys.argv:
        print(measured(sys.argv[sys.argv.index("--measured") + 1]))
    else:
        text, _ = report("--md" in sys.argv)
        print(text)
