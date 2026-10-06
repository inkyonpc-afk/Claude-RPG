# PERFORMANCE

_Status: skeleton — filled in during its phase (see ARCHITECTURE.md)._

## Registry size (measured 2026-10-06, tier G, 672 jars)
item=38,026 block=29,349 entity_type=2,873 attribute=451. Block count is dominated by furniture/decor wood-variant mods. Consequences observed:
- **WorldEdit** stalls the Server thread for minutes at start (state-map generation for every block): rejected.
- **Every Compat** caused Forge registry ID mismatches ("did not get ID it asked for"): rejected.
- Watch: startup time (~77 s server "Done" at 672 jars), EMI/JEI load, memory. Phase 14 will profile and prune decor mods if needed.
