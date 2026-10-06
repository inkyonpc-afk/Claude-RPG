// Embers of Aldreth: dev tool. Logs every key mapping to logs/kubejs/client.log as KEYBIND|name|key|category|context a few seconds after login (after defaults are applied).
ClientEvents.loggedIn(event => {
  try {
    var aldMinecraft = Java.loadClass('net.minecraft.client.Minecraft').getInstance()
    var aldMaps = aldMinecraft.options.keyMappings
    for (var i = 0; i < aldMaps.length; i++) {
      var km = aldMaps[i]
      console.info('KEYBIND|' + km.getName() + '|' + km.saveString() + '|' + km.getCategory() + '|' + km.getKeyConflictContext())
    }
  } catch (e) { console.error('[Aldreth] keybind dump failed: ' + e) }
})
