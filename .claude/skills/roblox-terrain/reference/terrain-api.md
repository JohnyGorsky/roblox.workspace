# Roblox Terrain API — authoritative reference

Sourced from the official Roblox Creator Docs (`create.roblox.com/docs`), 2026-07. Items not stated
verbatim in the docs are flagged **[practice]** (reliable but undocumented) or **[approx]**.

## Voxel model

- Terrain is a **4×4×4-stud voxel grid**. Each cell has a **material** (`Enum.Material`, incl. `Air`)
  and an **occupancy** float **0..1** (fraction filled). Intermediate occupancy is what smooths the
  surface (marching-cubes style). All voxel/region methods use **`resolution = 4`** (only supported value).
- Water is tracked separately as a **liquid** channel (`LiquidOccupancy`), independent of the solid
  material. A water-only voxel = `SolidMaterial = Air` + `LiquidOccupancy > 0`.

## Fill methods (verbatim signatures)

```lua
Terrain:FillBlock(cframe: CFrame, size: Vector3, material: Enum.Material): ()      -- rotatable box
Terrain:FillBall(center: Vector3, radius: number, material: Enum.Material): ()
Terrain:FillCylinder(cframe: CFrame, height: number, radius: number, material: Enum.Material): ()  -- axis = CFrame up (Y)
Terrain:FillWedge(cframe: CFrame, size: Vector3, material: Enum.Material): ()       -- like a WedgePart
Terrain:FillRegion(region: Region3, resolution: number, material: Enum.Material): ()
```

- **There is NO `Terrain:FillTerrain` and NO `Terrain:SmoothRegion` method.** ("Fill"/"Smooth" are
  Terrain *Editor* tools, not API.)
- **Overlapping fills overwrite the voxels they cover** **[practice]** — a later fill replaces the
  material+occupancy of covered voxels. ⚠️ This is the #1 footgun: a big fill in a loop erases what an
  earlier iteration placed nearby.
- **`Enum.Material.Air` carves/removes** terrain **[practice]** — filling a volume with Air empties it.
- **`Water` stays put** — a static body (the old flowing-water API is deprecated).

## Read / write voxels

```lua
local materials, occupancies = Terrain:ReadVoxels(region: Region3, resolution: number)
Terrain:WriteVoxels(region: Region3, resolution: number, materials, occupancies): ()
```

- Arrays are **1-based `[x][y][z]`** (x outermost). Both have a `.Size` field = voxel dims = `region.Size / 4`.
- `materials[x][y][z]` is an `Enum.Material` (use `.Name`); `occupancies[x][y][z]` is 0..1.
- Build regions grid-aligned: `Region3.new(min, max):ExpandToGrid(4)`.
- **`WriteVoxels` must run in the serial phase** — `task.synchronize()` first if parallel. Array dims
  must exactly match the grid-aligned region or it errors.
- **Sampling a point/column:** read the smallest grid-aligned region around it and index `[1][y][1]`.
  There is no `GetVoxel`; `GetCell`/`SetCell`/`GetWaterCell`/`SetWaterCell` are **deprecated legacy**.
- **Channel API** (read/write water independently): `ReadVoxelChannels` / `WriteVoxelChannels` with
  channel ids `"SolidMaterial"`, `"SolidOccupancy"`, `"LiquidOccupancy"` **[approx — verify names in Studio]**.

## Other ops

```lua
Terrain:ReplaceMaterial(region, resolution, sourceMaterial, targetMaterial)  -- find & replace material
Terrain:Clear()                                        -- wipe all terrain
Terrain:CopyRegion(region: Region3int16) -> TerrainRegion
Terrain:PasteRegion(region: TerrainRegion, corner: Vector3int16, pasteEmptyCells: boolean)
Terrain:WorldToCell(pos) / CellCenterToWorld(x,y,z) / CellCornerToWorld(x,y,z)
```
Deprecated (do NOT use): `GetCell/SetCell/SetCells/GetWaterCell/SetWaterCell`, `AutowedgeCell(s)`,
`ConvertToSmooth`, property `IsSmooth`, enums `WaterDirection`/`WaterForce`.

## Water

Properties on `Terrain`: `WaterColor: Color3`, `WaterReflectance: 0..1`, `WaterTransparency: 0..1`,
`WaterWaveSize: 0..1` (studs), `WaterWaveSpeed: 0..100` (cycles/min).

- Water is a static voxel liquid. **It needs a solid basin** — water next to Air at the sides/bottom
  won't hold; **carve/enclose the basin first, then fill/raise water inside it.**
- Reliable flat water: the **Sea Level** Terrain-Editor tool (fills a selected box to a flat level, or
  evaporates water) — an editor tool (human). From code: `FillBlock`/`FillRegion` with `Water`, or
  `WriteVoxelChannels` `LiquidOccupancy`.
- Buoyancy/drag: terrain water applies buoyancy+drag to unanchored parts (engine behavior; **exact
  force model not in docs** — don't rely on precise numbers). `BuoyancySensor` only *detects*
  (`TouchingSurface`, `FullySubmerged`).

## Editor tools (the human's reliable authoring path)

- **Generate** — biome-based procedural terrain (Water/Mountains/Hills/Plains/Marsh/Canyons/…), with
  size, blending, caves, and a **seed**. The sanctioned quick way to lakes/islands/mountains.
- **Import heightmap** (+ colormap): 1 px = 4 studs, up to 4096×4096 `.png`/`.jpg`. Best for authored
  islands/ranges.
- **Sea Level / Draw / Sculpt / Paint / Smooth / Flatten / Region** brushes.

## Procedural generation from code (official pattern)

Chunked, noise-driven `WriteVoxels` (from the multithreading docs sample). Chunk (e.g. 16 studs),
`math.noise` → occupancy, write serially:

```lua
for x = 0, 3 do for y = 0, 3 do for z = 0, 3 do
    occupancy[x+1][y+1][z+1] = math.clamp(math.noise(xd + 0.25*x, yd + 0.25*y, zd + 0.25*z), 0, 1)
    materials[x+1][y+1][z+1]  = someMaterial
end end end
local corner = Vector3.new(cx*16, cy*16, cz*16)
task.synchronize()
workspace.Terrain:WriteVoxels(Region3.new(corner, corner + Vector3.new(16,16,16)), 4, materials, occupancy)
```
`math.noise` returns ~−1..1 while occupancy is 0..1 — **clamp/remap yourself**.

## Gotchas

- **4-stud grid snapping** — no sub-4-stud detail; thin/shallow water (<4 studs) is unreliable.
- **`resolution` must be 4**; `ExpandToGrid(4)` regions before read/write.
- **Overlapping fills overwrite** (see above) — the erase-your-own-work trap.
- **Water needs a solid basin**; carve first, fill water second.
- **Per-op voxel cap ~4,194,304** **[approx]**; bounded by `Terrain.MaxExtents`. Chunk big jobs.
- **`WriteVoxels` serial only.**

## When to use what

- **Smooth Terrain** — large organic landscapes + the only real **swimmable/buoyant water** (waves,
  reflection, `BuoyancySensor`). Cost: 4-stud grid, no hard edges.
- **BaseParts** — precise hard-edged geometry, cheap flat ground, and a **flat water-surface plane**
  (translucent part) when you want deterministic control and simulate buoyancy in code.
- **EditableMesh** — runtime/procedural *mesh* geometry (e.g. stylized low-poly landforms), but there
  is **no official EditableMesh terrain/water workflow**; you'd build/deform meshes yourself.

Sources: `reference/engine/classes/Terrain.md`, `parts/terrain`, `datatypes/Region3.md`,
`studio/terrain-editor`, `scripting/multithreading`, `classes/BuoyancySensor.md`, `classes/EditableMesh.md`.
