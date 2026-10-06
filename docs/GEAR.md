# Gear

## Lifecycle
base equipment -> rarity -> affixes -> enchantments -> reforging -> sockets -> gems -> accessory slots -> boss materials -> endgame enhancement. Not every item needs every layer; the aim is that a found item can be **invested in** instead of replaced ten minutes later.

## Systems and who provides them
| Layer | Mod | Notes |
|---|---|---|
| Rarity + affixes | **Apotheosis 7.4.8** (+ Apotheotic Additions, Apothic Attributes, Apothic Curios) | Common, Uncommon, Rare, Epic, Mythic, Ancient; affix count by rarity; names and set bonuses |
| Salvage / reforge / augment | Apotheosis tables | materials by rarity (`apotheosis:*_material`); sigils for socketing/rebirth/unnaming |
| Sockets + gems | Apotheosis gems (core/overworld/end sets) | gem cutting for purity; ancient gems from top bosses |
| Enchanting | Apotheosis shelves + Majrusz's Enchantments, Allurement | table ceiling 30/60/100 by shelf tier; treasure shelf; library |
| Item growth | Lukas' Weapon Leveling (+ Better Combat compat), Ancient Reforging | favourite weapons level with use |
| Weapons | Simply Swords, Epic Knights (Magistu's Armory), Marium's Soulslike Weaponry, Celestisynth, Age of Weapons, Too Many Bows, Better Crossbows, Dreadsteel, Immersive Armors, boss weapons | 21 weapon classes tagged `aldreth:weapons/*` (see WEAPON_CLASSES.md) |
| Combat feel | Better Combat (+ Apothic/Particle compat) + Combat Roll | weapon-class attack animations; rolls; stagger |
| Accessories | Curios, Artifacts, Relics, Enigmatic Legacy, Majrusz's Accessories, Apothic Curios | limited slots; skill tree adds slots |
| Magic gear | Iron's Spells (books, staffs, armor, runes, upgrade orbs), Ars Nouveau, Goety | schools scale with spell-power attributes |
| Armor | vanilla tiers, Twilight/Aether/Undergarden/Blue Skies/Cataclysm sets, Epic Knights, Iron's mage armors | set bonuses via Armor Set Bonuses |

## Rarity and acts
Act I common-rare, II rare-epic, III epic-mythic, IV mythic, V+ ancient only from top bosses and vaults. Dimension bands live in `config/apotheosis/adventure.cfg` (tools/tune_apotheosis.py): overworld common-rare, Nether uncommon-epic, Twilight/Undergarden uncommon-epic, Aether rare-epic, Blue Skies rare-mythic, Otherside epic-mythic, End rare-mythic.

## Uniques
Hand-authored boss and relic drops (Simply Swords uniques, Cataclysm, Soulslike Weaponry, Celestisynth, Ice and Fire dragon-steel, Aether lances, Twilight scepters) are excluded from random loot and come only from bosses and structure vaults.

## Tooltips
Legendary Tooltips draws a border per rarity; Equipment Compare and Tool Stats help decisions; Enchantment Descriptions explains each enchant.
