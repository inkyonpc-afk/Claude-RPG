import json,urllib.request,urllib.parse,sys
UA={'User-Agent':'ClaudeRPG-packbuilder/0.1 (connorhalljames@gmail.com)'}
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
slugs="""irons-spells-n-spellbooks apotheosis apothic-attributes apothic-enchanting apothic-spawners passive-skill-tree pufferfish-skills projectmmo better-combat epic-fight simply-swords epic-knights ars-nouveau l_enders-cataclysm mowzies-mobs twilight-forest blue-skies the-undergarden aether alexs-mobs alexs-caves ice-and-fire-dragons ice-and-fire-ce when-dungeons-arise ftb-quests waystones terralith tectonic curios artifacts relics lootr sophisticated-backpacks tetra silent-gear farmers-delight supplementaries kubejs lootjs fancymenu legendary-tooltips combat-roll iris oculus embeddium sodium jei emi xaero-lunar xaeros-minimap yungs-better-dungeons integrated-dungeons-and-structures repurposed-structures towns-and-towers dungeon-crawl dragonmounts-legacy dragon-mounts-2 mythic-mounts creeper-overhaul ad-astra born-in-chaos graveyard-mod deeper-and-darker bosses-of-mass-destruction cataclysm-spellbooks iron-spell-books-addon goblin-traders eidolon-repraised create better-third-person epic-fight-iron-spells-compat tough-as-nails ftb-teams bettercombat-sword-addon wizards rpg-series spell-engine jewelry-rpg paladins-and-priests archers rogues-and-warriors""".split()
out={}
for s in slugs:
    try:
        p=get('https://api.modrinth.com/v2/project/'+s)
    except Exception as e:
        out[s]=None; print(s,'NOTFOUND'); continue
    f=get('https://api.modrinth.com/v2/project/%s/version?%s'%(s,urllib.parse.urlencode({'loaders':json.dumps(['forge']),'game_versions':json.dumps(['1.20.1'])})))
    n=get('https://api.modrinth.com/v2/project/%s/version?%s'%(s,urllib.parse.urlencode({'loaders':json.dumps(['neoforge']),'game_versions':json.dumps(['1.21.1'])})))
    print('%-34s F1.20.1:%-3d NF1.21.1:%-3d dl=%d'%(s,len(f),len(n),p['downloads']))
