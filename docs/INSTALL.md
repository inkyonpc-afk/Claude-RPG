# Install

## For players (CurseForge app)
1. Build the export zip (`python tools/export_curseforge.py --version X.Y.Z`) or receive `dist/EmbersOfAldreth-X.Y.Z.zip`.
2. CurseForge app -> Create Custom Profile -> Import -> select the zip. It installs Minecraft 1.20.1 + Forge 47.4.10, downloads CurseForge-hosted mods, and unpacks `overrides/` (configs, KubeJS, datapacks, resource packs, bundled jars for mods not hosted on CurseForge).
3. Allocate **8-10 GB RAM** (the pack has ~720 mods; startup to world takes about 2-4 minutes on a fast machine).
4. First launch: choose a people (Origins screen), open the quest book (`J`) and skill tree (`U`).

## Controls added or changed
`U` skill tree, `J` quest book (see `options.txt`); Combat Roll key under Controls; Iron's Spells quick-cast keys. Conflicts are audited via `kubejs/client_scripts/00_dump_keybinds.js` (dev tool).

## For developers (rebuild from source)
```
python tools/local_union.py && python tools/jarmeta.py      # index local jar cache (read-only on other instances)
python tools/resolve.py                                      # candidates.txt (+pinned.json) -> mods.lock.json
python tools/install.py --status core,std                   # lock -> mods/
python tools/build_tags.py; build_skilltree.py; build_origins.py; build_loot.py; build_quests.py; build_art.py; build_menu_art.py; build_traversal.py
python tools/server_test.py --status core,std --fresh --tag t   # headless server boot test (needs Forge installer in .build)
python tools/launch_client.py --world NAME --wait 300 --script "j75:key u;j85:shot name"   # offline client test with GUI automation
```
Requirements: Python 3.12 (numpy, Pillow), JDK 17, Forge 1.20.1-47.4.10 installer (downloaded from maven.minecraftforge.net into `.build/`), the CurseForge install at `G:\curseforge\Install` for client libraries.

## Dedicated server
`python tools/install.py --server --dest <serverdir>/mods`, copy `config/ defaultconfigs/ kubejs/` and the datapack folder `config/paxi/datapacks`, set `online-mode` as you wish, allocate 6-8 GB, accept the EULA yourself.
