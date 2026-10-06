# Changelog

## 2026-10-06 — Phase 0: baseline architecture
- Chose Forge 1.20.1 / 47.4.10 after ecosystem research (RESEARCH.md).
- Built `tools/local_union.py` (index of 1,319 CurseForge addons across local 1.20.1 Forge instances, read-only) and `tools/resolve.py`.
- Candidate pool `pack/candidates.txt` (resolves to ~817 incl. dependencies; to be tiered/cut by testing).

## 2026-10-06: Phases 1-3, 10, 11 (first pass)
- **Base:** 666-jar server boot clean (Done in ~78 s, 20 TPS); client enters a world with 720 mods (~150 s to world, ~230 s to interactive).
- **Compat fixes (evidence-driven):** AzureLib 3.1.17, OPAC 0.32.7, Drippy 3.1.5, ETF 7.1 + EMF 3.2.4 (Oculus compat), KubeJS Iron's Spells 6.5-3.14, Miner's Delight 1.4.5, Iron's RPG Tweaks 2.2.3. Rejected: Spell Engine stack, Legendary Monsters, Alshanex's Familiars, Cataclysm: Spellbooks, Chipped, WorldEdit, Every Compat, Healing Campfire, Subtle Effects, Despawn Tweaks (TxniLib), FTB Quests Optimizer, Born In Configuration.
- **Skill tree:** 620 custom nodes (14 regions, 42 keystones, 28 bridges, 4 Oaths), loads with zero PST errors. Economy: 100 points, 8-700 XP each.
- **Races:** 8 original Origins races; default (flight-granting) origins removed.
- **Weapon taxonomy:** 21 classes tagged `aldreth:weapons/*` (~1,000 items).
- **Quests:** 29 chapters, 491 quests across 5 groups, every ID registry-validated; chapter art generated.
- **Tooling:** resolve/install/server_test/autofix/ddmin/launch_client (GUI-automated), build_skilltree/origins/quests/tags/art, registry dump via KubeJS.
