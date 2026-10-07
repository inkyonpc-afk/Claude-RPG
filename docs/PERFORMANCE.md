# Performance

Measured on the build machine (Ryzen 9 5900X, RTX 4070, 32 GB RAM, NVMe/SSD, Java 17, Forge 47.4.10). Everything below is a measurement unless marked **not measured**.

## Scale
| Item | Value |
|---|---|
| Shipping jars (client) | 705 (`tools/verify.py`: one mod id per jar, all mandatory dependencies present) |
| Dedicated server jars | 665 to 678 (client-only list excluded) |
| Mods reported by Forge (incl. nested libraries) | 753 |
| Registries (KubeJS dump) | items about 38,000; blocks about 29,000; entity types about 2,900; attributes about 450 |
| Quests / skills / bosses | 499 / 620 / 39 |

The block count is dominated by furniture and decor wood-variant mods, which is also what makes registry-sensitive mods dangerous here (see Rejected for performance).

## Startup
| Phase | Time |
|---|---|
| Dedicated server, jars to "Done" | 135 to 161 s total (the server's own "Done" is reported about 60 s after mod loading ends, spawn-area preparation included) |
| Client, launch to title screen | about 150 s (ModernFix reports "Game took 150 seconds to start") |
| Client, title screen to interactive world | about 50 to 75 s after the join message |
| Client first run end to end | about 4 minutes |

Startup is dominated by mod construction and registry work for 710 mods, plus EMI/JEI recipe indexing (a one-time cost per launch). ModernFix, FerriteCore, Embeddium, ImmediatelyFast and Entity Culling are installed and active.

## Server throughput (fresh world, spark 1.10.53)
- **Pregeneration, 1000-block radius (16,129 chunks) in 18 min 54 s**: average about 14 chunks per second, peaks near 33, slowest stretches about 3 to 5 chunks per second around structure-dense and ocean areas.
- **TPS stayed at 20.0** for the whole run (spark 5 s / 10 s / 1 min / 5 min averages all 20; the 15-minute average dipped to 18.8 only because it included startup).
- **Tick durations during pregeneration:** median 2.8 to 3.2 ms, 95th percentile 6 to 11 ms, maximum about 52 ms. Idle: median 1.4 ms, maximum 5.6 ms.
- **CPU:** 15 % of the machine, 13 % process.
- **Memory:** 6.8 of 8 GB heap used (84 %) while pregenerating; give a real server 6 to 8 GB.
- **One player on the dedicated server:** overall mean tick 1.2 to 17 ms in the multiplayer tests (high end while scripted entity tests ran), 20 TPS.

## Client memory and frame rate (measured; the most important finding)
Test: singleplayer world, 1280x720, render distance 12, view idle at the saved position, vsync off, FPS read from the game every 5 s by a dev-only probe (`tools/dev_scripts/03_fps_probe.js`).

| Heap | Result |
|---|---|
| **8 GB** | **Unplayable.** FPS is 40 to 80 for the first 25 s, then collapses to 0 to 8 FPS; in 13 minutes the game ran only 1,400 ticks (should be about 15,000). Cause: the live heap is about 8.7 GB, so the JVM spends nearly all its CPU in garbage collection (thread dumps: every G1 thread at 88 s of CPU in 348 s). |
| **10 GB** | **Fine.** Steady state 300 to 390 FPS with shaders off; Balanced shaders 160 to 260 FPS; High shaders 195 to 260 FPS (all measured, RTX 4070). Live heap after a forced GC is 8.1 to 8.9 GB, so 10 GB leaves little slack. |
| **12 GB** | Comfortable margin (recommended). |

- **Why so much:** the class histogram shows 1.86 million block states (with 5.7 million baked-model keys and 6.5 million baked quads), 3.2 million EMI item stacks, 35 million hash-map nodes. That is the cost of about 29,000 registered blocks and 31,000 items across about 700 mods; there is no single hog.
- **Pack settings:** `config/memorysettings.json` now warns below 9 GB and above 16 GB (the old 8.5 GB maximum made the 10 GB default raise a blocking dialog). The test harness defaults to 10 GB.
- **After joining a world** the client spends one to two minutes in background work (EMI recipe baking, JEI indexing, Easy NPC variant registration): expect a slow first minute even at 10 GB.
- **Measured levers:**
  - ModernFix `mixin.perf.dynamic_resources=true` lowered the old-generation live set by about 1.6 GB with identical FPS; not enabled because its compatibility could not be verified for every mod.
  - Pruning four cosmetic decor mods (about 2,400 blocks: More Beautiful Torches and the Diagonal Walls/Fences/Windows suite) saved about 0.6 GB and is applied.
- **Startup:** client title screen in 144 to 183 s (varies run to run).

## Recommended settings
- **Client: 10 GB minimum, 12 GB recommended** (`-Xms2G -XX:+UseG1GC`). The process also holds about 4 GB outside the heap, so budget 16 GB of free system RAM. Do not run it on 8 GB.
- **Server:** 6 to 8 GB heap with `-XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200`.
- **Pregenerate** before opening a server: `chunky radius 2000` then `chunky start` (about 70 to 80 minutes for 62,500 chunks at the measured average).
- **Shaders** are off by default (Balanced costs about 40 % of the shaders-off frame rate on this GPU but is still well above 150 FPS).

## Rejected for performance or stability (evidence in KNOWN_ISSUES.md)
- **WorldEdit:** stalled the server thread for minutes at startup building block-state maps for ~29k blocks.
- **Every Compat:** caused Forge registry ID mismatches.
- **Shiny Trims resource pack:** disables ImmediatelyFast HUD batching and font-atlas resizing.
- **IceAndFire Community Edition:** alone, it produced the same registry ID mismatch on client and server.

## Levers if a machine struggles
1. Lower the client's render distance and simulation distance (the server tests used 6).
2. Drop the cosmetic resource packs first (`options.txt`, Options, Resource Packs): Fresh Animations is the heaviest.
3. Prune low-value decor mods: each furniture/decor mod adds hundreds of blocks and models. Cuts should come from `pack/candidates.txt` (set to `skip`), then `tools/resolve.py` and `tools/install.py`; re-run `tools/verify.py`.
4. Reduce structure density by raising tier factors in `tools/spacing_tiers.py` (WORLDGEN.md).

## Not measured (open)
Client memory growth beyond about 10 minutes, FPS on lower-end GPUs, TPS with several players and many tamed mounts, and `/spark profiler` hot spots during combat-heavy boss fights. FPS above was measured idle, not in combat.
