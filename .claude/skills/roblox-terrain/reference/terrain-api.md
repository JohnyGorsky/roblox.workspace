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
- **`resolution` must be `4`** — the docs state it as the only supported value, for both read and write.
- 🔴 **HARD LIMIT — the docs state it verbatim: "Will throw an error if region is too large. The limit
  is currently 4194304 voxels."** Applies to `ReadVoxels`, `WriteVoxels` and `ReadVoxelChannels`.
  It **throws** — so `pcall(...)` without checking the result turns an oversized region into a **silent
  no-op that looks like success**. Compute `(X/4)*(Y/4)*(Z/4)` before calling, and slab anything bigger.
- **`WriteVoxels` must run in the serial phase** — `task.synchronize()` first if parallel. `ReadVoxels`
  is thread-safe; `WriteVoxels` is not. Array dims must exactly match the grid-aligned region or it errors.
- **Sampling a point/column:** read the smallest grid-aligned region around it and index `[1][y][1]`.
  There is no `GetVoxel`; `GetCell`/`SetCell`/`GetWaterCell`/`SetWaterCell` are **deprecated legacy**.
- **A voxel's world position is its CENTRE.** `wy = base.Y + (yi - 0.5) * 4`, so a *surface* is the top
  voxel's centre **+ 2**. Comparing centres to target surfaces is an off-by-2 bug.

## Channel API (verified — prefer for anything involving water)

```lua
local data = Terrain:ReadVoxelChannels(region: Region3, resolution: number, channelIds: {string}): Dictionary
Terrain:WriteVoxelChannels(region: Region3, resolution: number, channels: Dictionary): ()
```

Channel ids, **confirmed in the official docs sample**: `"SolidMaterial"`, `"SolidOccupancy"`,
`"LiquidOccupancy"`. Returned as parallel 3D arrays under those keys.

- Water becomes an independent **liquid** channel instead of a material competing for the voxel, which
  removes most water-vs-ground fighting.
- **A voxel cannot be both**: the docs' own sample enforces `if solidOccupancy > 1 - EPSILON then
  liquid = 0` with the comment *"Solids cannot contain water"*.

## Other ops

```lua
Terrain:ReplaceMaterial(region, resolution, sourceMaterial, targetMaterial)  -- find & replace material
Terrain:Clear()                                        -- wipe ALL terrain (see warning below)
Terrain:CountCells(): int                              -- non-empty cell count
Terrain:CopyRegion(region: Region3int16) -> TerrainRegion
Terrain:PasteRegion(region: TerrainRegion, corner: Vector3int16, pasteEmptyCells: boolean)
Terrain:WorldToCell(pos) / CellCenterToWorld(x,y,z) / CellCornerToWorld(x,y,z)
```

### Copy / Paste — cell coordinates, verified

- `CopyRegion` takes a **`Region3int16`**, `PasteRegion` a **`Vector3int16`** corner — both in **CELL**
  units (1 cell = 4 studs). Passing a `Region3` fails with *"Unable to cast Region3 to Region3int16"*.
- 🔴 **`Region3int16`'s max corner is INCLUSIVE**, measured: min `(-653,-15,1097)` to max `(-547,5,1203)`
  gives `SizeInCells` **107, 21, 107** = `max - min + 1`. A half-width of 53 cells captures 107 cells.
- ⚠️ **Translation is therefore quantised to 4 studs.** An 18-stud shift cannot be expressed; 16 or 20
  only. Derive offsets **surface-to-surface**, not centre-to-level.
- `pasteEmptyCells = true` → exact paste (empty cells clear existing terrain). `false` → overlay solids.
- **`TerrainRegion` data does NOT replicate between server and client** (stated in the docs). It is,
  however, an `Instance`, which is what makes it the transport for moving terrain **between places** via
  the Studio clipboard.

### ⚠️ `Terrain:Clear()`

Wipes everything, including hand-sculpted hero terrain. Any `Clear()` at server boot will erase the
human's work on every start. If a place mixes sculpted and generated terrain, **remove the blanket
clear** and ship the file with the sculpted zones present and the generated area empty.
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
- **Per-op cap = 4,194,304 voxels, and it THROWS** (documented, not approximate). A `pcall` that ignores
  the result converts this into a silent no-op. Slab big jobs and check every result.
- **`WriteVoxels` serial only** (`ReadVoxels` is thread-safe).
- 🔴 **Land whose surface sits at the water level renders as thin sheets with occupancy holes.** Keep
  every land surface at least ~8 studs clear of `WATER_Y`; never ramp gently *through* the waterline.
- **`Terrain.MaxExtents` is not an emptiness test** — it returns a huge sentinel box when the terrain is
  empty. Probe voxels or use `CountCells()`.
- **Heightmap import**: 1 px = 4 studs, max 4096×4096 `.png`/`.jpg`; optional colormap maps exact RGB
  values to materials (see the colour table in `parts/terrain`). Human/editor path.

## When to use what

- **Smooth Terrain** — large organic landscapes + the only real **swimmable/buoyant water** (waves,
  reflection, `BuoyancySensor`). Cost: 4-stud grid, no hard edges.
- **BaseParts** — precise hard-edged geometry, cheap flat ground, and a **flat water-surface plane**
  (translucent part) when you want deterministic control and simulate buoyancy in code.
- **EditableMesh** — runtime/procedural *mesh* geometry (e.g. stylized low-poly landforms), but there
  is **no official EditableMesh terrain/water workflow**; you'd build/deform meshes yourself.

Sources: `reference/engine/classes/Terrain.md`, `parts/terrain`, `datatypes/Region3.md`,
`studio/terrain-editor`, `scripting/multithreading`, `classes/BuoyancySensor.md`, `classes/EditableMesh.md`.
