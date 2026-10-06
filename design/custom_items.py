"""Aldreth custom items (registered by KubeJS from tools/build_sigils.py). Validators treat these ids as known.
SIGILS: realm key -> (item id, display name, dimensions it unlocks, shapeless ingredients, rune color, lore)."""
EMBER_SHARD = "aldreth:ember_shard"
S = EMBER_SHARD
SIGILS = {
    "flame": ("aldreth:sigil_of_flame", "Sigil of Flame", ["minecraft:the_nether"], [S, "minecraft:flint_and_steel", "minecraft:obsidian", "minecraft:obsidian"], (255, 110, 40),
              "Unseals the Flame Ward: the Nether."),
    "root": ("aldreth:sigil_of_root", "Sigil of Root", ["twilightforest:twilight_forest"], [S, "minecraft:diamond", "#minecraft:saplings", "minecraft:moss_block"], (90, 200, 90),
             "Unseals the Root Ward: the Twilight Forest."),
    "stone": ("aldreth:sigil_of_stone", "Sigil of Stone", ["undergarden:undergarden"], [S, "minecraft:iron_block", "minecraft:cobbled_deepslate", "minecraft:glow_berries"], (150, 170, 190),
              "Unseals the Stone Ward: the Undergarden."),
    "sky": ("aldreth:sigil_of_sky", "Sigil of Sky", ["aether:the_aether"], [S, S, "minecraft:glowstone", "minecraft:feather", "twilightforest:naga_scale"], (120, 200, 255),
            "Unseals the Sky Ward: the Aether."),
    "dream": ("aldreth:sigil_of_dream", "Sigil of Dream", ["blue_skies:everbright", "blue_skies:everdawn"], [S, S, "minecraft:amethyst_shard", "minecraft:diamond", "minecraft:blaze_rod"],
              (200, 130, 255), "Unseals the Dream Ward: Everbright and Everdawn."),
    "echo": ("aldreth:sigil_of_echo", "Sigil of Echo", ["deeperdarker:otherside"], [S, S, S, "minecraft:echo_shard", "minecraft:sculk_catalyst"], (40, 190, 180),
             "Unseals the Echo Ward: the Otherside."),
    "end": ("aldreth:sigil_of_the_end", "Sigil of the End", ["minecraft:the_end"], [S, S, S, S, "minecraft:ender_eye", "minecraft:nether_star"], (230, 220, 160),
            "Unseals the last Ward: the End."),
}
ITEMS = {EMBER_SHARD: "Ember Shard"}
ITEMS.update({v[0]: v[1] for v in SIGILS.values()})
