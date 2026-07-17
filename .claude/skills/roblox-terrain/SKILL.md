---
name: roblox-terrain
description: Roblox smooth-terrain knowledge + reliable recipes for any game in this workspace — the Terrain voxel API (fill/read/write, occupancy, water, Region3), tested recipes (flat water, island, hills, river channel), and a hard verify-by-read-back discipline. Use before writing ANY code that creates/edits terrain or terrain water, or when reasoning about rivers/lakes/islands/hills. Scripting is for PROCEDURAL terrain; hero terrain is hand-sculpted by the human (see GROUND-RULES §2).
---

# Roblox terrain

Authoritative terrain knowledge so we **stop guessing geometry and stop assuming fills worked**. Full
API in [reference/terrain-api.md](reference/terrain-api.md) — read it for signatures/semantics. This
file is the working discipline + recipes.

## Golden rules (these are why past terrain work failed)

1. **VERIFY every edit — never assume.** After any terrain write, **read it back**
   (`Terrain:ReadVoxels` at representative points) **and** `screen_capture`, and confirm it matches
   intent before reporting done. This is a standing workspace rule (GROUND-RULES §2 / memory).
2. **Compute the geometry first — don't eyeball it.** Write down the cross-section before coding:
   bank-top Y, water Y, riverbed/floor Y, channel width, and **base-slab thickness**. The slab must be
   **thicker than the deepest any carve reaches**, or you punch through to the void.
3. **Overlapping fills OVERWRITE.** A large fill inside a loop erases what earlier iterations placed
   nearby. **Carve everything first, then fill water in a second pass** — never interleave.
4. **Water needs a solid basin** and snaps to the **4-stud grid** — carve/enclose first, then fill
   water; sub-4-stud water is unreliable.
5. **Change one thing at a time.** If something works, make the *smallest* fix — don't rewrite the
   whole method and lose what worked.
6. **Inspect the scene first.** Check for a default `Baseplate`, existing water level, spawn, etc.
   before building (a Baseplate under translucent water reads as "grey broken water").

## Hybrid authoring (who does what — GROUND-RULES §2)

- **Human hand-sculpts hero terrain** in Studio's Terrain Editor — it's faster and better-looking, and
  the *reliable* water/landscape tools live there: **Generate** (biomes + seed), **Import heightmap**,
  **Sea Level** (flat water over a basin), Sculpt/Draw/Paint/Smooth.
- **Claude scripts only *procedural* terrain** (noise fields, repeatable/endless content), computing
  geometry and verifying by read-back. Claude does **not** script hero terrain.

## Recipe: flat water surface as a PART (deterministic — prefer for greybox / precise control)

When you want water that is 100% predictable (no voxel/occupancy surprises), don't use terrain water —
lay a flat translucent Part at the waterline. Grass hides it on land; it shows only in the carved
channel. Simulate buoyancy/current in code (see the game's boat controller).

```lua
local water = Instance.new("Part")
water.Name, water.Anchored, water.CanCollide = "Water", true, false
water.Size = Vector3.new(mapX, 1, mapZ)
water.Position = Vector3.new(0, WATER_Y, 0)
water.Material, water.Transparency = Enum.Material.Glass, 0.3
water.Color = Color3.fromRGB(35, 125, 195)
water.Parent = workspace
```

## Recipe: terrain WATER body (real swimmable water — needs a basin)

```lua
local T = workspace.Terrain
-- 1) solid basin, thick enough that carving can't punch through
T:FillBlock(CFrame.new(0, -30, 0), Vector3.new(600, 100, 1000), Enum.Material.Grass) -- top y=20
-- 2) carve the basin (ALL carving first)
-- ... FillBlock/FillBall Air along the shape ...
-- 3) fill water second (won't be erased), flat top at WATER_Y, inside the basin
-- ... FillBlock Water up to WATER_Y ...
-- 4) VERIFY: ReadVoxels a column + screen_capture before declaring done
```

## Recipe: procedural hills (chunked noise — the official pattern)

```lua
for cx = 0, chunksX do for cz = 0, chunksZ do
    local materials, occupancy = {}, {}      -- size = 16/4 = 4 per axis
    -- fill [x][y][z] 1-based with math.clamp(math.noise(...), 0, 1) and a material
    local corner = Vector3.new(cx*16, 0, cz*16)
    task.synchronize()                        -- WriteVoxels is serial-only
    workspace.Terrain:WriteVoxels(Region3.new(corner, corner + Vector3.new(16,64,16)), 4, materials, occupancy)
end end
```

## Recipe: verify a terrain edit (do this EVERY time)

```lua
local T, res = workspace.Terrain, 4
local region = Region3.new(Vector3.new(px-2, minY, pz-2), Vector3.new(px+2, maxY, pz+2)):ExpandToGrid(res)
local mats, occ = T:ReadVoxels(region, res)
for y = 1, mats.Size.Y do print(mats[1][y][1].Name, occ[1][y][1]) end  -- inspect the column
```
Then `screen_capture` the area. Only report success after both confirm it.

## Don't

- Don't call `FillTerrain`/`SmoothRegion` (not real API), or deprecated `GetCell/SetCell/SetWaterCell`.
- Don't script hero terrain — that's the human's Terrain-Editor job.
- Don't trust a fill worked because the code ran — **read it back**.
