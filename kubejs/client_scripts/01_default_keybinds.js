// Embers of Aldreth: one-time default control scheme (options.txt is not honored for mod keys in this setup).
// Applies once per instance (flag: local/aldreth_keys_v1.json) so players can rebind freely afterwards.
// Core keys: K skill tree, J quest book, R combat roll. Conflicting optional keys are moved or unbound.
ClientEvents.loggedIn(event => {
  try {
    var flag = 'local/aldreth_keys_v1.json'
    if (JsonIO.read(flag) != null) return
    var Input = Java.loadClass('com.mojang.blaze3d.platform.InputConstants')
    var KeyMapping = Java.loadClass('net.minecraft.client.KeyMapping')
    var aldMc = Java.loadClass('net.minecraft.client.Minecraft').getInstance()
    var want = {
      'key.display_skill_tree': 'key.keyboard.k',
      'key.ftbquests.quests': 'key.keyboard.j',
      'keybinds.combatroll.roll': 'key.keyboard.r',
      // moved off K
      'key.spellstoneAbility': 'key.keyboard.comma',
      'key.craftingtweaks.compress_one': 'key.keyboard.unknown',
      'key.craftingtweaks.compress_stack': 'key.keyboard.unknown',
      'key.craftingtweaks.compress_all': 'key.keyboard.unknown',
      'key.goety.lich.laugh': 'key.keyboard.unknown',
      'quark.keybind.lock_rotation': 'key.keyboard.unknown',
      'iris.keybind.toggleShaders': 'key.keyboard.unknown',
      'iris.keybind.shaderPackSelection': 'key.keyboard.unknown',
      'iris.keybind.reload': 'key.keyboard.unknown',
      // moved off J
      'key.xpScroll': 'key.keyboard.semicolon',
      'key.toastcontrol.clear': 'key.keyboard.unknown',
      'key.ars_elemental.open_pouch': 'key.keyboard.period',
      'key.goety.witch.brewCircle': 'key.keyboard.unknown',
      // moved off R (roll keeps R)
      'key.dragon_fireAttack': 'key.keyboard.unknown',
      'key.structure_gel.open_building_tool_gui': 'key.keyboard.unknown',
      'key.golemoverhaul.netherite_golem_summon': 'key.keyboard.unknown',
      'key.soulsweapons.parry': 'key.keyboard.f',
      'key.block_factorys_bosses.dodge_roll': 'key.keyboard.unknown'
    }
    var maps = aldMc.options.keyMappings
    var n = 0
    for (var i = 0; i < maps.length; i++) {
      var km = maps[i]
      var nm = String(km.getName())
      if (want[nm] !== undefined) { km.setKey(Input.getKey(want[nm])); n++ }
    }
    KeyMapping.resetMapping()
    aldMc.options.save()
    JsonIO.write(flag, { applied: true, count: n })
    console.info('[Aldreth] default keybinds applied: ' + n)
  } catch (e) { console.error('[Aldreth] default keybinds failed: ' + e) }
})
