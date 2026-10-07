// DEV ONLY (tools/dev_scripts): logs the client FPS string every 5 s as FPSPROBE lines in logs/kubejs/client.log.
// Copied into kubejs/client_scripts for measurement runs and removed afterwards; never shipped.
var aldProbeN = 0
ClientEvents.tick(event => {
  aldProbeN++
  if (aldProbeN % 100 != 0) return
  var mcp = Java.loadClass('net.minecraft.client.Minecraft').getInstance()
  console.info('FPSPROBE|' + aldProbeN + '|' + mcp.fpsString + '|inWorld=' + (mcp.level != null))
})
