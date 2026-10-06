# Visuals

## Identity
Name **Embers of Aldreth**. Palette: ember orange and gold on deep indigo. Generated art (Pillow/numpy; `tools/build_menu_art.py`, `tools/build_art.py`):
- **Title screen:** custom panorama (aurora over a broken crown-moon, floating islands, lit tower, forest line), logo "EMBERS OF ALDRETH", tagline, 23 custom splash texts, pack icon.
- **Quest book:** 29 chapters with themed procedural backgrounds (embers, peaks, trees, clouds, rings, runes, blades, gems, waves, stars).
- **Skill tree:** PST textures plus per-region colors; custom region icons pending (PST ships 80 icons).

## Resource packs
- **Always on (Paxi):** `aldreth_core`: panorama, logo, splashes, quest art.
- **Curated stack** (`tools/build_visuals.py`; copies from the local CurseForge cache, records project/file ids in `pack/visual_packs.json`; the export references them on CurseForge instead of bundling). Lowest to highest priority:
  - *Animation:* Fresh Animations 1.10.4 + Extensions + Fresh Compats + Fresh Mowzie's Mobs (through EMF/ETF).
  - *World detail:* Fancy Crops, Better Lanterns, Just Fancy Torches, Shiny Trims, Better End Portal Frame, Low On Fire, Simply Swords Whimscape, Medieval Style Lootr, Enchant Icons.
  - *Audio:* Alternative Rain Sounds, More Cave Sounds, Soft Weather, Cataclysmic Tunes (boss themes).
  - *Presentation:* Visual Traveler's Titles + Alex's Titles, Eclectic Trove (Legendary Tooltips frames), Better XP/Mana bar for Iron's Spells, Enhanced Boss Bars, Embellished Stone (advancement plaques), FTB Quests Extra Shapes.
  - *UI theme:* none on purpose. The STONEBORN UI pack was tried and dropped: it replaces the title panorama with a wooden-table scene and overrides our brand. Our own panorama, logo and quest art carry the identity.
- Players can reorder or disable any of these in Options > Resource Packs. Order lives in `options.txt` (`build_visuals.py --options`).

## Shaders
- **Stack:** Oculus 1.8.0 + Embeddium (the last working pair). Shader packs: Complementary Reimagined r5.9.3 (default) and Complementary Unbound r5.9.3.
- **Off by default:** `config/oculus.properties` has `enableShaders=false` with Reimagined preselected, so turning shaders on is one click in Video Settings > Shader Packs. The shader toggle key is unbound by default.
- **Presets** live in `config/aldreth/shader_presets/`:

| Preset | Shadows | Shadow dist | Reflections (water/block) | Light shafts | SSAO | Detail | Clouds | AF | Target |
|---|---|---|---|---|---|---|---|---|---|
| performance | 0 | 96 | 0 / 0 | 0 | off | 0 | 1 | 0 | GTX 1060-class, 60 fps |
| **balanced** (default) | 2 | 128 | 1 / 1 | 1 | 2 | 2 | 2 | 0 | RTX 3060-class |
| high | 3 | 192 | 2 / 3 | 2 | 2 | 3 | 2 | 8x | RTX 4070-class |
| ultra | 4 | 256 | 2 / 3 | 3 | 3 | 4 | 3 | 16x | screenshots |

- **Switch preset:** copy the preset file over `shaderpacks/ComplementaryReimagined_r5.9.3.zip.txt` (or run `python tools/build_visuals.py`, which resets both packs to balanced), then reload shaders in game.

## HUD and polish
Legendary Tooltips (rarity borders), Item Borders, Overflowing Bars, Blessfulled damage indicators, boss bars, Traveler's Titles, advancement plaques, Xaero's minimap/world map, FancyMenu + Drippy Loading Screen (custom layouts pending), AmbientSounds, Sound Physics, Presence Footsteps, Better Third Person, Particular, Falling Leaves, camera overhaul.

## Status
- **Implemented:** title panorama and logo, quest backgrounds, the resource-pack stack, shader presets, and the FancyMenu editor overlay (hidden for players; Ctrl+Alt+C toggles it).
- **Follow-ups:** FancyMenu button and loading-screen layouts, per-region skill icons.
