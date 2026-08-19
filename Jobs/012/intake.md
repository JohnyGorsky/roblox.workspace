# Job #012: Correct stale Studio UI and lighting knowledge in the skills

**Project**: `roblox.workspace`
**Created**: 2026-08-19 23:15:23
**Status**: Requirements Gathering (intake)

## Requirements / goal

Two pieces of skill knowledge are wrong against the live Studio, caught while writing the tide settings baseline. (1) LIGHTING: the roblox-vfx skill and its reference both describe Lighting.Technology as an existing-but-not-script-settable property with Enum.Technology values Voxel/ShadowMap/Future. In the current Studio the Lighting instance has NO Technology property at all - it is not even readable from Luau - and has been replaced by LightingStyle (Enum.LightingStyle: Realistic=0, Soft=1) plus PrioritizeLightingQuality (bool). MCP-verified: both are READ-ONLY to scripts even under plugin capability, so they are Properties-panel values. Enum.Technology still exists as an enum but no longer maps to a property. Current values in The Last Tide: LightingStyle=Soft, PrioritizeLightingQuality=true. (2) STUDIO MENUS: I told the user to open File > Game Settings, which does not exist in their Studio. Their File menu has Experience Settings and Avatar Settings as separate entries, plus Open Configs and Studio Settings (Alt+S). The ribbon tabs are Home, Avatar, UI, Script, Model, Plugins with no Test tab - playtest is the transport buttons top-left plus the Test menu. The roblox-studio skill has no section on where things live in the Studio UI at all, which is why there was nothing to check against. Fix both, and add a rule that Studio UI locations are verified against the live Studio or a screenshot before being stated.

## Checklist

- [ ] Requirements reviewed (this intake)
- [ ] Implementation plan created & agreed
- [ ] Implementation completed
- [ ] Final summary + changelog written
