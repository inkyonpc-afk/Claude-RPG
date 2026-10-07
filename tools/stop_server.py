"""Kill ONLY the test server process recorded in .build/server.pid (never other java processes)."""
import os, subprocess
pid = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".build", "server.pid")
if os.path.isfile(pid):
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", open(pid).read().strip()], capture_output=True)
    else:
        try:
            os.kill(int(open(pid).read().strip()), 9)
        except (ValueError, OSError):
            pass
    print("stopped", open(pid).read().strip())
