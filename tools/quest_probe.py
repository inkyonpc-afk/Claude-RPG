"""FTB Quests runtime probe: checks in a running server what tools/questmap_check.py checks on paper.

  python tools/quest_probe.py --install            write the probe chapter into .build/server's quest folder (never into the shipped config)
  python tools/quest_probe.py --report [--log L]   read the server log + saved team data and print PASS/FAIL per expectation
  python tools/quest_probe.py --remove             delete the probe chapter again
Use with tests/quest_probe.txt (server commands) and a client joined as the non-op AldrethTest. Verified 2026-10-07 on Linux: all PASS.
Probe quests (ids 7A0B0C0D0E0F11xx, last chapter group): a command reward with elevate_perms and one with the old "elevate" key, a
dimension task with the "dimension" key and one with the old "dim" key."""
import argparse, glob, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from questmap_check import parse_snbt  # noqa: E402

SRV = os.path.join(ROOT, ".build", "server")
CHAPTER = os.path.join(SRV, "config", "ftbquests", "quests", "chapters", "99_probe.snbt")


def quest(qid, title, x, task, reward=None):
    out = '\t\t{\n\t\t\tid: "%s"\n\t\t\ttitle: "%s"\n\t\t\tx: %.1fd\n\t\t\ty: 0.0d\n\t\t\ttasks: [{\n\t\t\t\tid: "%s"\n%s\t\t\t}]\n' % (
        qid, title, x, "7A0B0C0D0E0F12" + qid[-2:], "".join("\t\t\t\t%s: %s\n" % kv for kv in task))
    rw = "".join("\t\t\t\t%s: %s\n" % kv for kv in reward) if reward else ""
    out += ('\t\t\trewards: [{\n\t\t\t\tid: "%s"\n%s\t\t\t}]\n' % ("7A0B0C0D0E0F13" + qid[-2:], rw)) if reward else "\t\t\trewards: [ ]\n"
    return out + "\t\t}"


PROBE = "{\n\tid: \"7A0B0C0D0E0F1001\"\n\tfilename: \"99_probe\"\n\ttitle: \"ZZ Probe (test only)\"\n\ticon: \"minecraft:barrier\"\n\torder_index: 99\n" \
        "\tgroup: \"07B3A2C356D6233C\"\n\tquests: [\n" + "\n".join([
            quest("7A0B0C0D0E0F1101", "Probe: give with elevate_perms", 0, [("type", '"checkmark"')],
                  [("type", '"command"'), ("command", '"give {p} minecraft:diamond 1"'), ("elevate_perms", "true"), ("silent", "true"), ("auto", '"enabled"')]),
            quest("7A0B0C0D0E0F1102", "Probe: give with old elevate key", 2, [("type", '"checkmark"')],
                  [("type", '"command"'), ("command", '"give {p} minecraft:gold_ingot 1"'), ("elevate", "true"), ("silent", "true"), ("auto", '"enabled"')]),
            quest("7A0B0C0D0E0F1103", "Probe: dimension key", 4, [("type", '"dimension"'), ("dimension", '"minecraft:the_nether"')]),
            quest("7A0B0C0D0E0F1104", "Probe: old dim key", 6, [("type", '"dimension"'), ("dim", '"minecraft:the_nether"')])]) + "\n\t]\n}\n"


def report(log):
    text = open(log, encoding="utf-8", errors="replace").read()
    inv = re.search(r"AldrethTest has the following entity data: (\[.*\])", text)
    inv = inv.group(1) if inv else ""
    saves = sorted(glob.glob(os.path.join(SRV, "world", "ftbquests", "*.snbt")), key=os.path.getmtime)
    if not saves or not inv:
        sys.exit("no team data or inventory line found (did the client join and the commands run?)")
    data = parse_snbt(open(saves[-1], encoding="utf-8").read())
    done, started = data.get("completed", {}), data.get("started", {})
    titles = {}
    for f in glob.glob(os.path.join(SRV, "config", "ftbquests", "quests", "chapters", "*.snbt")):
        for qd in parse_snbt(open(f, encoding="utf-8").read()).get("quests", []):
            titles[qd["id"]] = qd.get("title", "")
    nether = [qid for qid, t in titles.items() if t in ("The Land Below", "Flame")]
    checks = [("command reward with elevate_perms runs for a non-op player", "minecraft:diamond" in inv),
              ("command reward with the old 'elevate' key does not (key ignored)", "minecraft:gold_ingot" not in inv),
              ("dimension task with the 'dimension' key completes", "7A0B0C0D0E0F1103" in done),
              ("dimension task with the old 'dim' key never completes", "7A0B0C0D0E0F1104" not in done),
              ("real Nether quests start but wait for their dependencies", nether and all(q in started and q not in done for q in nether))]
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    return all(ok for _, ok in checks)


ap = argparse.ArgumentParser()
ap.add_argument("--install", action="store_true")
ap.add_argument("--remove", action="store_true")
ap.add_argument("--report", action="store_true")
ap.add_argument("--log", default=os.path.join(SRV, "logs", "latest.log"))
a = ap.parse_args()
if a.install:
    os.makedirs(os.path.dirname(CHAPTER), exist_ok=True)
    open(CHAPTER, "w", encoding="utf-8").write(PROBE)
    print("probe chapter written:", os.path.relpath(CHAPTER, ROOT))
if a.report:
    sys.exit(0 if report(a.log) else 1)
if a.remove and os.path.isfile(CHAPTER):
    os.remove(CHAPTER)
    print("probe chapter removed")
