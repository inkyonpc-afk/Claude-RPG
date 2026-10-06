"""Bucket problems in a Minecraft/Forge log. Usage: python tools/logscan.py <log> [--top N]"""
import re, sys, collections
path = sys.argv[1]
top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 25
B = collections.OrderedDict([
    ("missing-dependency", r"Missing or unsupported mandatory dependencies|requires .* (?:or above|version)|Mod ID: '[^']+', Requested by"),
    ("mixin", r"Mixin apply failed|InvalidMixinException|MixinApplyError|Critical injection failure|Mixin transformation"),
    ("crash", r"Exception in thread|Encountered an unexpected exception|Crash report|java\.lang\.(?:Error|NoSuchMethod|NoClassDef|ClassCast|NoSuchField)"),
    ("client-class-on-server", r"Attempted to load class .* for invalid dist|invalid dist DEDICATED_SERVER|net\.minecraft\.client"),
    ("datapack/recipe", r"Parsing error loading recipe|Couldn't parse data file|Failed to load .* (?:recipe|tag|advancement|loot)|Couldn't load loot table|Unknown (?:recipe|item|block) "),
    ("kubejs", r"KubeJS|kubejs.*(?:error|Error)|Error in 'ServerEvents|Error occurred while handling"),
    ("worldgen", r"Failed to (?:place|generate)|Feature placement|Unknown (?:biome|structure)|Missing registry"),
    ("registry", r"Registry .* (?:not found|missing)|Unknown registry|Missing .* registry"),
    ("config", r"config.*(?:corrupt|invalid|Failed)|Configuration file .* is not correct"),
])
cnt = collections.Counter(); ex = {}
sev = re.compile(r"\[(?:ERROR|FATAL)\]|/ERROR\]|/FATAL\]|Exception")
for ln in open(path, encoding="utf-8", errors="replace"):
    if not sev.search(ln):
        continue
    key = "other"
    for k, rx in B.items():
        if re.search(rx, ln):
            key = k; break
    short = re.sub(r"\d+", "#", ln.strip())[:160]
    cnt[(key, short)] += 1
    ex.setdefault((key, short), ln.strip()[:300])
by = collections.Counter()
for (k, s), n in cnt.items():
    by[k] += n
print("== buckets:", dict(by))
for (k, s), n in cnt.most_common(top):
    print("%4d [%s] %s" % (n, k, ex[(k, s)]))
