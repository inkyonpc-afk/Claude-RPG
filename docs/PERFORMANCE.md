# Performance

Measured on the build machine (Ryzen 9 5900X, RTX 4070, 32 GB RAM, NVMe/SSD, Java 17, Forge 47.4.10). Everything below is a measurement unless marked **not measured**.

## Scale
| Item | Value |
|---|---|
| Shipping jars (client) | 710 (`tools/verify.py`: one mod id per jar, all mandatory dependencies present) |
| Dedicated server jars | 670 to 678 (client-only list excluded) |
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

## Recommended settings
- **Client:** 8 to 10 GB heap (`-Xms2G -Xmx8G -XX:+UseG1GC` used in tests). The process also holds about 4 GB outside the heap (textures, native buffers), so budget 12 GB of free RAM.
- **Server:** 6 to 8 GB heap with `-XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200`.
- **Pregenerate** before opening a server: `chunky radius 2000` then `chunky start` (about 70 to 80 minutes for 62,500 chunks at the measured average).
- **Shaders** are off by default; the four presets in VISUALS.md trade shadow distance, reflections and clouds. **Shader and in-world FPS were not measured.**

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
Client FPS (vanilla and with shaders), client memory growth over a long session, TPS with several players and many tamed mounts, and `/spark profiler` hot spots during combat-heavy boss fights.
