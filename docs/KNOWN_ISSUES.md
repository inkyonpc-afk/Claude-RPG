# KNOWN_ISSUES

_Status: skeleton — filled in during its phase (see ARCHITECTURE.md)._

## Fixed / worked-around (compat datapack `config/paxi/datapacks/aldreth_fixes`)
- **Prodigium Dungeons 0.9.2** ships two 0-byte structure files (`glider_tower`, `glider_tower_crystal`) that abort datapack loading ("Not a JSON object: null"). Blocked via pack.mcmeta filter together with their structure_sets.
- **Prodigium Dungeons** also uses Ancient Aether's structure type (`ancient_aether:jigsaw_skylands`) without declaring it: see `pack/extra_deps.txt`.
- **Legendary Monsters 2.2.1** has a common mixin targeting a client class (crashes dedicated servers): rejected.
- **Alshanex's Familiars 1.1.2**, **Born In Configuration**, RPG-Series jewelry (Spell Engine stack): rejected (version/architecture conflicts).
