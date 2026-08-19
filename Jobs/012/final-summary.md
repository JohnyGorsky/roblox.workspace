# Final Summary — Job #012

**Project**: `roblox.workspace`
**Completed**: 2026-08-19 23:17:21
**Status**: ✅ Completed

## What was implemented

Corrected two stale facts and closed the gap that let them go unchallenged. LIGHTING: Lighting.Technology no longer exists on the Lighting instance - it is not even readable from Luau - and is replaced by LightingStyle (Enum.LightingStyle: Realistic=0 high-quality/mobile-expensive, Soft=1 cheaper and the new-place default) plus PrioritizeLightingQuality (bool, trades shadow range against view distance under load). MCP-verified that BOTH are read-only to scripts even under the plugin capability, so no script can configure or repair them. Enum.Technology still exists with all six values but no property consumes it. Three places in roblox-vfx said otherwise and now say this, including the mobile/perf line that named Future as the heaviest Technology. STUDIO UI: the roblox-studio skill had no section on where anything lives in the Studio interface, which is exactly why a wrong menu path went unchallenged - I told the user File > Game Settings and their Studio has no such entry. Added a verified section: Game Settings is gone, split into File > Experience Settings (max players, per-place config) and File > Avatar Settings (avatar type, its own entry, NOT nested inside Experience Settings), plus Open Configs and the separate File > Studio Settings for Studio's own preferences; menu bar and ribbon tabs recorded; no Test ribbon tab, playtest is the transport buttons plus the Test menu. The section opens with a verify-before-you-instruct rule and closes with the list of settings a script cannot touch (MaxPlayers/PreferredPlayers, LightingStyle/PrioritizeLightingQuality, anything on the Creator Hub) plus the technique that caught this: read the property, try assigning its own value back, and report writability - which turns a guess into a fact. Every claim is dated 2026-08-19 with a re-verify-after-Studio-update warning, since this UI moves often. The tide settings baseline and job 004 checklist were corrected in the same pass.

### Files changed

- `.claude/skills/roblox-vfx/SKILL.md`
- `.claude/skills/roblox-vfx/reference/vfx.md`
- `.claude/skills/roblox-studio/SKILL.md`

## Verification

- [x] `LightingStyle` / `PrioritizeLightingQuality` read from the live place: `Soft` / `true`
- [x] Write attempt on each refused: "The current thread cannot write" — read-only confirmed, not assumed
- [x] `Lighting.Technology` confirmed **unreadable** from Luau (not merely non-settable)
- [x] `Enum.LightingStyle` = Realistic(0), Soft(1); `Enum.Technology` still lists all six values
- [x] Studio UI claims cross-checked against the user's own screenshots, not memory
- [x] No remaining "set Lighting.Technology" or "Game Settings" instruction in the skills or tide docs
- [ ] Whether `ShadowSoftness` still needs a specific lighting path — **flagged as re-verify, untested**
