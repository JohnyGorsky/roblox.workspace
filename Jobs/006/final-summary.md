# Final Summary — Job #006: roblox-vfx + roblox-studio + roblox-assets + game-design skills

**Project**: `roblox.workspace`
**Completed**: 2026-07-18
**Status**: ✅ Completed

## What was produced

Four authoritative shared skills (docs/web-sourced, each `SKILL.md` + `reference/`, unverified flagged) +
policy/registry deliverables:

1. **`roblox-vfx`** — ParticleEmitter/Beam/Trail, legacy Fire/Smoke/Sparkles/Explosion, lights,
   Lighting service (day/night, fog), Atmosphere/Sky, post-processing, shadows + `Enum.Technology`,
   mobile perf caps. Captured gotchas (Beam has no Emit/Clear; Trail `WidthScale` is a NumberSequence;
   Atmosphere `Decay` is Color3; `Lighting.Technology` set in Studio not script; particle Rate 400/100).
2. **`roblox-studio`** — the built-in Studio MCP tool set + our verify/playtest discipline, Assistant/
   agentic tools, editors, new Luau type solver, testing (Device Emulator for mobile), and 2025-2026
   features worth using (texture streaming, SLIM, custom matchmaking, 120-stud lights).
3. **`roblox-assets`** — asset types & storage, licensing, the **security script-scan**, and the operative
   workflow: **our-assets-first → present for approval → scan & delete scripts → store → log in registry.**
4. **`game-design`** — core loops, retention/onboarding, replayability patterns, economy/difficulty
   balance, fair monetization, and the 2026 discovery algorithm / live-ops.

Also:
- **`GROUND-RULES.md §4`** strengthened with the mandatory asset policy (our-assets-first, present-before-use,
  scan-for-scripts, maintain registry).
- **Asset registry scaffolded** for Jungle: `roblox.jungle/assets/registry/` (README + `_TEMPLATE`-style
  per-type files: models, meshes, images, audio, animations, ui) — the fast reuse catalog.

## Grounding & corrections captured

- Sourced from official docs / newsroom / DevForum; unverified items flagged.
- Current-2026 corrections: **Engagement-Based/Premium Payouts deprecated 2025-07-24 → Creator Rewards**;
  Roblox publishes **no official retention benchmarks** (third-party only); discovery window widened to 28
  days; `Lighting.Technology` deprecated as script-settable; deprecated `InsertService:GetFreeModels`.

## Files changed (roblox.workspace + roblox.jungle)

- New skills: `.claude/skills/{roblox-vfx,roblox-studio,roblox-assets,game-design}/{SKILL.md,reference/*.md}`.
- Edited: `GROUND-RULES.md` (§4 asset policy). New job: `Jobs/006/*`.
- Jungle: `assets/registry/{README,models,meshes,images,audio,animations,ui}.md`.

## Verification
- [x] All four skills loaded by the harness (appeared in the skills list as written).
- [x] Sourced from official docs/web; unverified flagged.

## Notes / next
- Not committed (per rule).
- Shared skill set is now **12**: roblox-dev, roblox-terrain, roblox-scripting, roblox-physics, roblox-ui,
  roblox-animation, roblox-avatar, roblox-vfx, roblox-studio, roblox-assets, game-design, studio-diagnostics.
- Resume: the deferred **pause & commit**, then Jungle (world generator / boat).
