// Embers of Aldreth: dev tool. Dumps registry IDs so tools/verify.py can validate quests, skill tree and loot references.
// Output: kubejs/exported/registries.json (git-ignored; regenerated on every server load).
ServerEvents.loaded(event => {
  const BR = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
  const Registries = Java.loadClass('net.minecraft.core.registries.Registries')
  const out = {}
  const builtin = {
    item: BR.ITEM, block: BR.BLOCK, entity_type: BR.ENTITY_TYPE, attribute: BR.ATTRIBUTE,
    mob_effect: BR.MOB_EFFECT, enchantment: BR.ENCHANTMENT, particle_type: BR.PARTICLE_TYPE, sound_event: BR.SOUND_EVENT,
    loot_pool_entry: BR.LOOT_POOL_ENTRY_TYPE, loot_function: BR.LOOT_FUNCTION_TYPE, loot_condition: BR.LOOT_CONDITION_TYPE
  }
  Object.keys(builtin).forEach(k => {
    out[k] = []
    builtin[k].keySet().forEach(id => out[k].push(String(id)))
    out[k].sort()
  })
  const ra = event.server.registryAccess()
  const dyn = { structure: Registries.STRUCTURE, structure_set: Registries.STRUCTURE_SET, biome: Registries.BIOME, damage_type: Registries.DAMAGE_TYPE }
  Object.keys(dyn).forEach(k => {
    out[k] = []
    try { ra.registryOrThrow(dyn[k]).keySet().forEach(id => out[k].push(String(id))) } catch (e) { out[k + '_error'] = String(e) }
    out[k].sort()
  })
  out.advancement = []
  try { event.server.getAdvancements().getAllAdvancements().forEach(a => out.advancement.push(String(a.getId()))) } catch (e) { out.advancement_error = String(e) }
  out.advancement.sort()
  out.loot_table = []
  try { event.server.getLootData().getKeys(Java.loadClass('net.minecraft.world.level.storage.loot.LootDataType').TABLE).forEach(id => out.loot_table.push(String(id))) } catch (e) { out.loot_table_error = String(e) }
  out.loot_table.sort()
  out.dimension = []
  event.server.levelKeys().forEach(key => out.dimension.push(String(key.location())))
  out.dimension.sort()
  JsonIO.write('kubejs/exported/registries.json', out)
  console.info('[Aldreth] registry dump written: ' + Object.keys(out).map(k => k + '=' + (out[k].length || 0)).join(' '))
})
