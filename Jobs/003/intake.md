# Job #003: Build roblox-terrain skill + adopt hybrid terrain authoring

**Project**: `roblox.workspace`
**Created**: 2026-07-18
**Status**: In progress

## Why (root-cause of the terrain struggle in Jungle P1)

Scripted terrain sculpting for the Jungle river failed ~5 times. Honest root causes:

1. **Guessed geometry instead of computing it** — slab 42 thick but carved with radius-40 ball →
   punched through to the void; round carve bowl wider than the rectangular water fill → dry gaps.
   Never worked out the cross-section (bank height / water level / carve depth / widths) first.
2. **Reported "done" from assumption** — claimed the water was fixed 3× without reading it back. One
   voxel read instantly exposed "all grass, no water." (→ now a standing rule.)
3. **Didn't inspect the existing scene** — the "grey water" was the default **Baseplate** under
   translucent water the whole time; a quick look would have caught it.
4. **Changed everything at once** — a working terrain-water version got wholesale-rewritten
   (balls → aligned boxes) and broke; no controlled one-variable iteration.
5. **Tool + knowledge gap** — scripted terrain *water* is finicky (occupancy, FillBall vs FillBlock,
   overlapping-material overwrite, water rendering) and I worked from approximate API knowledge, not
   an authoritative reference. Scripting overlapping primitives is a poor way to author a precise shape.

## Decisions

- **Hybrid terrain authoring** (recorded in GROUND-RULES §2): the **human hand-sculpts hero terrain**
  in Studio (rivers, islands, set-pieces); **Claude scripts only *procedural* terrain**, computing
  geometry (never guessing) and **verifying by voxel read-back + screenshot**.
- **Build a shared `roblox-terrain` skill** grounded in the official Creator Docs (not memory).

## Deliverables

1. `roblox.workspace/.claude/skills/roblox-terrain/` — authoritative Terrain API reference (fill ops,
   occupancy, read/write voxels, water, Region3) + **tested recipes** (flat water body, island, hills,
   river/channel) + the verify discipline + when to use terrain vs parts vs meshes.
2. GROUND-RULES §2 updated (done).
3. Jungle P1 follow-up: the river becomes **hand-sculpted by the user**; Claude focuses P1 on the
   boat/physics/systems. (Update the P1 plan accordingly.)

## Notes

- Terrain API reference sourced via a research pass over official docs (in progress).
- Not committed (per the rule).
