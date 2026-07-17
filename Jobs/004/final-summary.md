# Final Summary — Job #004: roblox-scripting + roblox-physics skills

**Project**: `roblox.workspace`
**Completed**: 2026-07-18
**Status**: ✅ Completed

## What was produced

Two authoritative shared skills, docs-sourced (same rigor as `roblox-terrain`), each `SKILL.md` guide +
`reference/` doc, with unverified items flagged:

1. **`roblox-scripting`** — client-server security & exploit-hardening (validate every remote arg;
   nothing secret in ReplicatedStorage; suspicion-scoring), modern Luau (New Type Solver GA, `task.*`,
   string interpolation, if-expressions, generalized iteration, `buffer`), best-practice patterns
   (modules, OOP, connection/leak discipline, attributes), Parallel Luau, performance, and DataStore
   rules (UpdateAsync, session locking, pcall+backoff, limits). Complements `roblox-dev`.
2. **`roblox-physics`** — assembly/mass/network-ownership model, the full MODERN constraint system
   (VectorForce/LinearVelocity/AngularVelocity/AlignPosition/AlignOrientation/Torque; Hinge/Prismatic/
   Cylindrical/BallSocket/Rope/Spring/Weld, Motor6D, NoCollisionConstraint), the deprecated Body*→modern
   mapping, buoyancy (BuoyancySensor + custom force), and a verified boat recipe.

## Grounding & payoff

- Sourced from official Creator Docs via two research passes (exact signatures/ranges captured; e.g.
  `Density` 0.0001..100, water=1.0; `Responsiveness` 5..200; `Gravity` 196.2).
- The physics skill **validated and corrected the earlier boat work**: `AngularVelocity.RelativeTo=
  Attachment0` is unsupported (World was right); `AlignOrientation`+`PrimaryAxisOnly` for upright;
  the VehicleSeat network-ownership pitfall; custom buoyancy needs damping. The boat controller should
  be revisited against this recipe.

## Files changed (roblox.workspace)

- New: `.claude/skills/roblox-scripting/{SKILL.md,reference/luau-scripting.md}`,
  `.claude/skills/roblox-physics/{SKILL.md,reference/physics.md}`, `Jobs/004/*`.

## Verification

- [x] Both skills loaded by the harness (appeared in the skills list after writing).
- [x] Sourced from official docs; unverified items explicitly flagged in each reference.

## Notes / next
- Not committed (per rule).
- Shared skill set is now: `roblox-dev`, `roblox-terrain`, `roblox-scripting`, `roblox-physics`,
  `studio-diagnostics`.
- Resume: the deferred **pause & commit** checkpoint, then Jungle (world generator / boat feel).
