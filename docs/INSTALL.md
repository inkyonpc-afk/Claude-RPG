# Install

## For players (CurseForge app)
1. Build the export zip (`python tools/export_curseforge.py --version X.Y.Z`) or receive `dist/EmbersOfAldreth-X.Y.Z.zip`.
2. CurseForge app: **Create Custom Profile, Import**, select the zip. It installs Minecraft 1.20.1 + Forge 47.4.10, downloads the CurseForge-hosted mods, resource packs and shader packs, and unpacks `overrides/` (configs, KubeJS scripts, datapacks, the Default Options defaults, plus any bundled jars for mods that are not CurseForge-hosted).
3. Allocate **8 to 10 GB** of RAM. The pack has about 710 mods; expect 2.5 to 4 minutes to reach the title screen and a little longer to enter a first world.
4. First launch: pick a people on the Origins screen, open the quest book (**J**) and the skill tree (**K**).
5. Shaders are **off by default**. To try them: Options, Video Settings, Shader Packs, pick Complementary Reimagined, then (optionally) a preset from `config/aldreth/shader_presets/` (see VISUALS.md).

## Controls added or changed
| Key | Action |
|---|---|
| K | skill tree |
| J | quest book |
| R | combat roll |
| comma, semicolon, period | Spellstone ability, XP scroll, Ars Elemental pouch (moved off defaults that collided) |
| F | Soulslike parry |

A one-time KubeJS script (`kubejs/client_scripts/01_default_keybinds.js`) applies the scheme on first world join; after that every key is yours to rebind (it will not run again; delete `local/aldreth_keys_v1.json` to re-apply). Conflicting defaults (Quark rotation lock, Iris shader keys, several joke/utility binds) are unbound on purpose.

## For developers (rebuild from source)
```
python tools/local_union.py && python tools/jarmeta.py      # index the local jar cache (read-only on other instances)
python tools/resolve.py                                      # candidates.txt (+pinned.json, dep_replaced.txt) -> mods.lock.json
python tools/install.py --status core,std                   # lock -> mods/   (--dry never writes)
python tools/build_tags.py; python tools/build_skilltree.py; python tools/build_origins.py
python tools/build_quests.py; python tools/build_loot.py; python tools/build_traversal.py; python tools/build_sigils.py
python tools/build_art.py; python tools/build_menu_art.py; python tools/build_visuals.py
python tools/tune_apotheosis.py; python tools/tune_structures.py; python tools/tune_mounts.py
python tools/verify.py                                       # release gate: counts, duplicates, dependencies, data
python tools/export_curseforge.py --version X.Y.Z            # dist/EmbersOfAldreth-X.Y.Z.zip
```
Every generator is idempotent; the design sources are `design/` (skill tree, quests, bosses, custom items) and the tuning tools above. Do not hand-edit generated files.

Requirements: Python 3.12 (numpy, Pillow), JDK 17, the Forge 1.20.1-47.4.10 installer (downloaded from maven.minecraftforge.net into `.build/`), and the CurseForge install at `G:\curseforge\Install` for client libraries.

### Test harness
```
python tools/server_test.py --fresh --tag t --cmds "forge tps"            # headless server boot (release set core,std)
python tools/server_test.py --cmds tests/mp_flight.txt --tag mp            # scripted multiplayer checks (see tests/)
python tools/launch_client.py --world NAME --wait 300 --script "j55:key j;j65:shot name"      # offline client + GUI automation
python tools/launch_client.py --join 127.0.0.1:25599 --wait 420            # client joins the test server
python tools/structure_census.py                                           # structure density from a generated world
python tools/stop_server.py                                                # stops only the recorded test-server PID
```
The test client uses an offline identity (`AldrethTest`). Never run `taskkill /IM java.exe`: it would kill your own Minecraft.

## Dedicated server
1. `python tools/install.py --server --dest <serverdir>/mods` (skips `pack/client_only.txt`; 678 jars).
2. Copy `config/`, `defaultconfigs/`, `kubejs/` into the server directory. Datapacks and resource packs ride in `config/paxi/` (inside `config/`).
3. Install Forge 1.20.1-47.4.10, give it 6 to 8 GB (`-Xms2G -Xmx8G -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200` is what the tests use), set `online-mode` as you wish, and accept the Minecraft EULA yourself.
4. Optional: pregenerate before opening the server, for example `chunky radius 2000` then `chunky start`.
5. Admin commands worth knowing: `/skilltree points add <player> <n>`, `/kubejs stages add <player> aldreth_flight` (unlock flying mounts early), `/ftbquests editing_mode`.
6. Players need the full client pack; the join test showed that every channel-registering mod must be on both sides.
