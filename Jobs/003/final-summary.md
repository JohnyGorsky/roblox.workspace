# Final Summary — Job #003: roblox-terrain skill + hybrid terrain authoring

**Project**: `roblox.workspace`
**Completed**: 2026-07-18
**Status**: ✅ Completed

## What was produced

After scripted terrain sculpting failed repeatedly in Jungle P1, we diagnosed the causes and built a
reliable foundation:

1. **`roblox-terrain` skill** (shared, in `roblox.workspace/.claude/skills/roblox-terrain/`):
   - `SKILL.md` — golden rules (verify-by-read-back, compute geometry first, carve-then-fill,
     water-needs-a-basin, change-one-thing, inspect-scene-first), the hybrid authoring split, and
     tested recipes (flat water Part, terrain water basin, procedural noise hills, a verify snippet).
   - `reference/terrain-api.md` — authoritative Terrain API (fill/read/write, occupancy, water props,
     Region3, channels, editor tools, gotchas), sourced from official Creator Docs with unverified
     items flagged.
2. **Hybrid terrain authoring** recorded in `GROUND-RULES.md §2`: human hand-sculpts hero terrain in
   Studio's Terrain Editor; Claude scripts only *procedural* terrain and verifies by read-back.
3. **Jungle P1 plan** updated: the river/island is now hand-sculpted by the user; Claude focuses P1 on
   the boat physics/systems (optionally a flat water Part for a deterministic greybox surface).

## Root causes captured (the "why")

Guessing geometry (punch-through, gaps), reporting "done" without read-back, missing the default
Baseplate, rewriting the whole method at once, and a real API-knowledge gap — the terrain reference
confirms the mechanisms (overlapping fills overwrite; water needs a basin; 4-stud grid snap).

## Files changed (roblox.workspace)

- New: `.claude/skills/roblox-terrain/SKILL.md`, `.../reference/terrain-api.md`, `Jobs/003/*`.
- Edited: `GROUND-RULES.md` (§2 hybrid terrain + verify rule earlier this session).
- Memory: `verify-studio-terrain-edits` added.

## Verification

- [x] Terrain API sourced from official docs (research pass), unverified items flagged.
- [x] `roblox-terrain` skill loaded by the harness (appeared in the skills list after writing).
- [ ] Real test of the recipes happens next time terrain is scripted (procedural) — apply the verify discipline.

## Notes / next

- Not committed (per rule).
- Jungle: user hand-sculpts the river when ready; Claude resumes P1 on the boat once there's water to float on.
