"""List JSON key strings of PST serializer classes via javap. Usage: python tools/pst_keys.py ClassNameSubstr ..."""
import glob, os, re, subprocess, sys, zipfile
JP = r"C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot\bin\javap.exe"
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
jar = glob.glob(os.path.join(root, ".build", "server", "mods", "PassiveSkillTree*.jar"))[0]
z = zipfile.ZipFile(jar)
tmp = os.path.join(root, ".build", "pst", "cls")
os.makedirs(tmp, exist_ok=True)
for q in sys.argv[1:]:
    for n in z.namelist():
        if n.endswith(".class") and q in n.split("/")[-1] and "Serializer" in n:
            p = os.path.join(tmp, n.replace("/", "_"))
            open(p, "wb").write(z.read(n))
            out = subprocess.run([JP, "-c", "-constants", "-p", p], capture_output=True, text=True).stdout
            strs = sorted(set(re.findall(r'// String (.+)', out)))
            print(n.split("/")[-1], strs)
