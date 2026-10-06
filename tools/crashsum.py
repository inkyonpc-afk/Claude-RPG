"""Summarise the newest FML crash report: which mods failed to load and why. Usage: python tools/crashsum.py [report]"""
import os, re, sys
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".build", "server", "crash-reports")
f = sys.argv[1] if len(sys.argv) > 1 else os.path.join(d, sorted(os.listdir(d), key=lambda x: os.path.getmtime(os.path.join(d, x)))[-1])
t = open(f, encoding="utf-8", errors="replace").read()
print(os.path.basename(f), "|", re.search(r"Description: (.*)", t).group(1))
for m in re.finditer(r"Mod File: [^\n]*?/mods/([^\n/]+)\n\s*Failure message: ([^\n]*)\n((?:\t\t[^\n]*\n){0,3})", t):
    print("-", m.group(1), "::", m.group(2).strip()[:200], "|", " / ".join(x.strip() for x in m.group(3).splitlines())[:240])
for m in re.finditer(r"Caused by 0: ([^\n]+)", t):
    print("  cause:", m.group(1)[:240])
