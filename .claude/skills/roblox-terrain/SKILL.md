---
name: roblox-terrain
description: Roblox smooth-terrain knowledge + hard-won recipes for any game in this workspace — the voxel/occupancy model, the channel API (solid vs LIQUID water), region limits that THROW, read-modify-write editing, water without shelf artifacts, moving terrain between places, joining hand-sculpted terrain to generated terrain, and a verify-by-read-back-and-screenshot discipline. Use before writing ANY code that creates or edits terrain or terrain water, or when reasoning about rivers, lakes, islands, hills, coastlines, valleys or seams.
---

# Roblox terrain

Authoritative terrain knowledge so we **stop guessing geometry and stop assuming writes worked**.
Signatures + limits: [reference/terrain-api.md](reference/terrain-api.md). This file is the working
discipline, the failure catalogue, and the recipes.

---

## 0. The five facts behind most terrain bugs

1. **Voxels are 4×4×4 studs; `resolution` must be exactly `4`.** Every write is quantised to that grid.
   **A voxel's world Y is its CENTRE** — a voxel reported at `y = 18` occupies **16…20**. But its
   *top face* and **the surface you can stand on are not the same height** — see §3, which was measured
   and is not what this skill said before. Off-by-2 here is the most common analysis error.
2. **`ReadVoxels` / `WriteVoxels` / `ReadVoxelChannels` THROW above 4,194,304 voxels.** Wrapped in a
   `pcall` whose result you ignore, that becomes a **silent no-op**: the script reports success and
   does nothing. Slab your regions and **always check the pcall result**.
3. **Occupancy is fractional (0…1), not boolean.** The surface is where occupancy crosses ~0.5, so a
   land surface that lands *on* the water plane renders as thin hole-riddled sheets (§4).
4. **`CopyRegion`/`PasteRegion` take `Region3int16`/`Vector3int16` in CELL coordinates** — not studs,
   not `Region3`. Passing a `Region3` errors *"Unable to cast Region3 to Region3int16"*. **All
   translation is therefore quantised to 4 studs**: an 18-stud offset is impossible, 16 or 20 only.
5. **Overlapping writes overwrite.** Carve everything, *then* place water. Never interleave.

---

## 1. Who does what (GROUND-RULES §2)

- **Human hand-sculpts hero terrain** in the Terrain Editor, where the reliable tools live: **Generate**
  (biomes + seed), **Import** heightmap/colormap, **Sea Level** (Create/Evaporate), Sculpt / Draw /
  Paint / Smooth / Flatten.
- **Claude scripts PROCEDURAL terrain only** — noise fields, computed channels, valleys, seams —
  computing the geometry and verifying by read-back.

**A computed channel or valley IS procedural work and is in scope.** Out of scope is eyeballing hero
shapes.

> ⚠️ **"I removed terrain so I can't put it back" is WRONG** — I have said this and been corrected.
> You cannot recover the *original voxels*, but you can **fill new terrain**, and shaping a bank,
> valley or riverbed is exactly that. If the original is genuinely needed, re-copy it from a place that
> still has it (§6).

---

## 1b. 🔴 BOUND THE EDIT — the rule that matters most

**Before writing terrain, state the maximum extent of the change and make the code physically unable to
exceed it.** A profile that "blends back to the surroundings" is *not* a bound — it will happily cut a
mountain in half if the mountain happens to be inside its radius.

Two guards, both cheap, both mandatory on any edit near hand-sculpted terrain:

```lua
local MAX_DX = 110        -- studs either side of the feature's centreline (channel 75 + bank 35)
local MAX_Y  = 40         -- never modify a voxel above this
if math.abs(dx) > MAX_DX then continue end
if wy > MAX_Y then continue end          -- <-- this one alone prevents wrecking hillsides
```

**Real incident (Job #071).** A river valley was shaped out to **225 studs** either side of the channel,
blending toward a reference height sampled at 300. Where the hillside rose steeply *inside* that band
but the reference column beyond it sat lower, the profile treated the mountain as terrain to cut down —
flattening a **~400-stud-wide plateau to exactly `BANK_MIN`** and leaving 22 floating rock columns
sheared off at the cut edge. The river needed ~40 studs of bank. A `MAX_Y` guard would have stopped it
dead, because the river never needs to touch anything above ~25.

**Corollaries**

- **A blend target sampled far away is dangerous**: it says nothing about what lies between. Either
  clamp the profile to `min(profile, existingHeight)` outside the channel, or refuse to touch columns
  whose existing surface is already above the target.
- **Never let a "shape the valley" pass double as a "flatten the surroundings" pass.**
- Prefer editing a small band well and leaving the rest alone over one big elegant profile.

## 2. Verify EVERY edit — never assume

After any terrain write: **read it back** at representative points **and** `screen_capture`, then
confirm it matches intent before reporting done (GROUND-RULES §2 / memory).

Measure the thing you are claiming, not a proxy:

- Claiming a depth? Print bed Y, surface Y **and** the difference.
- Claiming a width? Print min/max X of the water, not a voxel count.
- Claiming "clean"? Count the *violations* and print the first few **with coordinates** — that is what
  exposes a false positive in your own test.

⚠️ **`screen_capture` with `camera_position` leaves the camera `Scriptable` and locks the user's
navigation — restore `CameraType = Custom` afterwards** (memory: `screen-capture-locks-camera`).

### 🔴 Your PROBE region silently clips what you measure

A `ReadVoxels` region with a Y ceiling of 40 reports **every taller column as 40** — it cannot see
above its own box. Job #071: a bank was diagnosed as "a 28-stud cliff topping out at 40", a grading
pass was written against that, and the real ground was **76–104**. Re-probing with the ceiling at 60
made the same columns read 60; only a ceiling of 200 showed the truth.

**Size probe regions to the terrain's true range, not to the feature you are thinking about** — and if
a measurement returns suspiciously many columns at exactly your region's ceiling, that is the tell.

### 🔴 Verify in a SEPARATE call, not right after the write

Re-reading immediately after `WriteVoxels` **in the same script** can return pre-write data. Job #071:
a repair reported *"45 columns fixed"* and its own verification printed a byte-identical histogram —
the write had not applied at all. Only a fresh `execute_luau` call revealed it.

If a verification result is *exactly* the same as the pre-fix numbers, suspect a stale read or a no-op
write before you believe the fix worked.

### Don't invent pass/fail thresholds

"More than 20,000 voxels means intact" is a made-up number that will report false failures. State the
measurement and what it means; only assert pass/fail against a threshold you can justify.

---

## 3. Coordinate arithmetic that is easy to get wrong

With `RES = 4` and `base = region.CFrame.Position - region.Size/2`:

```lua
local wx = base.X + (xi - 0.5) * RES   -- world CENTRE of voxel xi
local wy = base.Y + (yi - 0.5) * RES
local wz = base.Z + (zi - 0.5) * RES
```

### 🔴 The surface you can STAND ON is `centre + occupancy × RES`, not `centre + RES/2`

This skill previously said *"surface height = topmost solid voxel centre + RES/2"*. **Measured against 73
columns of a real sculpt (Tide job 027), that rule is wrong by up to a full `RES/2`:**

| Candidate rule | Mean abs. error | Worst |
|---|---|---|
`centre + RES/2` — what this skill used to say | **1.657 studs** | 2.000 |
**`centre + occupancy × RES`** | **0.087 studs** | 0.973 |

Two details, both load-bearing:

- take the topmost **NON-EMPTY** voxel, not the topmost one over 0.5 — the partial cell is what shapes the
  surface;
- multiply occupancy by the **full** `RES`, not half of it.

**The useful corollary:** substitute the voxel arithmetic and it collapses to

```
collision surface  =  sculpt target height + RES/2      -- i.e. +2 studs
```

So terrain **stands 2 studs higher than the height you asked for**. A plateau sculpted at 16 is walked on at
18. Verified both ways: a column targeted at 9.98 measured 11.982.

⚠️ **Anything comparing a raycast against a designed height must add `RES/2` first.** Tide job 027 saw this
as *"worst error 2.0 studs"* against a tolerance of exactly 2 — a passing check that a 1.9 tolerance would
have failed, which is a test agreeing with a bug rather than testing anything. Once converted, the same
check reported **0.0** and the tolerance could go to 0.6.

- A voxel's *top face* is still `centre + RES/2`. That is a different quantity from its surface, and
  conflating the two is the off-by-2.
- `Region3:ExpandToGrid(4)` before every read/write. Cell coords = studs ÷ 4.

---

## 4. Water — the channel API, and the shelf artifact

### Prefer `ReadVoxelChannels` / `WriteVoxelChannels`

They separate **`SolidMaterial`**, **`SolidOccupancy`** and **`LiquidOccupancy`**, so water stops being
a *material* competing with ground for the same voxel.

> **A voxel cannot be both.** Where `SolidOccupancy` ≈ 1, `LiquidOccupancy` must be 0.

The older `ReadVoxels`/`WriteVoxels` treat water as `Enum.Material.Water` and still work — most existing
code in this workspace uses them — but new water work should prefer channels.

> 🔴 **The legacy API CANNOT repair a solid+liquid voxel, and fails silently when you try.**
> A voxel can hold partial solid *and* water at once (e.g. `Mud 0.5` floating on water). `ReadVoxels`
> exposes only one material per voxel, so it reports `Mud 0.5` and **hides the water underneath** — a
> read-modify-write through it cannot express "no solid, full liquid" and the write does nothing.
>
> Job #071: hand-sculpting left a thin partial-mud lid over the river. Two legacy repair passes each
> reported success and changed nothing. `ReadVoxelChannels`/`WriteVoxelChannels` fixed it in one go —
> 508 solid voxels dissolved, 451 liquid set to full — because they can address `SolidOccupancy` and
> `LiquidOccupancy` independently.
>
> **If terrain and water are tangled in the same voxels, reach for channels immediately.**

### 🔴 The shelf artifact — never let land sit at the waterline

**Land whose surface lands on, or within a few studs of, the water surface renders as thin flat sheets
riddled with holes** — a waffle of partial occupancy that reads as broken sandbars floating in the river.

**Rule: no land surface may exist between the water level and about `WATER_Y + 8`.** A bank must start
clear of the water and rise from there. A gentle ramp passing *through* the waterline produces the
artifact along its entire length.

```lua
local BANK_MIN = WATER_Y + 8      -- hard floor for land beside water
h = BANK_MIN + smoothstep(u) * (hRef - BANK_MIN)
```

#### 🔴 A gentle shore cannot avoid it AT ALL. Only a discontinuity can.

The rule above works for a bank that never crosses the waterline. When land *has* to meet water — an island,
a beach — no continuous profile can comply: **to get from `+10` to `−4` continuously you must pass through
the band, and whatever column lands in there is a sheet.** Steepening the ramp only reduces the count.

Measured on Tide's first island: a 60° face still produced **335 offending columns**, plainly visible as flat
sheets lying on the sea. Job 024's earlier "240 of a 400-column shoreline" was read as a floor to live with;
it is actually a floor for the *wrong shape*.

**The fix is to generate nothing in the band at all** — jump straight from the last dry height to the first
wet one:

```lua
if r <= rb then
    return beachTop                     -- lowest DRY land, e.g. +8  (surface +10)
elseif r <= ro then
    return faceBottom + ...             -- highest WET land, e.g. -6 (surface -4)
end                                     -- nothing is ever generated between them
```

That took the same island to **exactly 0** offending columns, because no column's surface can land in a band
no column targets. The renderer bridges the two adjacent columns with a **~72° face**, which a Humanoid still
walks up (`MaxSlopeAngle` defaults to 89).

⚠️ The cost is that the coastline becomes a low bluff rather than a beach. If you need somewhere walkable,
give **one arc** a gentle run and accept the artifact only there — small, and exactly where jetty or dock art
will cover it.

### 🔴 Never write "remove land that is low AND surrounded by water"

That criterion is a **runaway**. With a gentle bank, a ring around *all* the water qualifies; drowning
it moves the shore outward and a fresh ring qualifies next pass. Measured in Job #071: it widened a
148-stud river to **204** across four passes and was still not converging.

Find genuine islands by **connectivity** (is this land joined to the main shore?), not by
neighbour-fraction. Better still, fix the **bank profile** so bars never form.

---

## 5. Recipe: read-modify-write (the workhorse)

For any edit that must preserve its surroundings — carving a channel, shaping a valley, blending a seam.

```lua
local RES = 4
local region = Region3.new(minV, maxV):ExpandToGrid(RES)
-- ① SIZE CHECK FIRST: (X/4)*(Y/4)*(Z/4) must be < 4,194,304
local ok, mats, occ = pcall(function() return Terrain:ReadVoxels(region, RES) end)
if not ok then error("ReadVoxels failed: " .. tostring(mats)) end   -- never swallow this

local base = region.CFrame.Position - region.Size/2
for xi = 1, #mats do for zi = 1, #mats[1][1] do
    local h = targetSurface(wx, wz)          -- the computed profile
    for yi = 1, #mats[1] do
        local wy = base.Y + (yi - 0.5) * RES
        -- wy <= h  -> FILL if currently empty (keeps existing material where already solid)
        -- wy >  h  -> CARVE to Air
    end
end end
Terrain:WriteVoxels(region, RES, mats, occ)
```

**Blend shoulders to a SAMPLED height, not a constant.** Pick a reference column well outside anything
you have touched and interpolate toward `H[refColumn]`. A fixed cap height builds walls wherever the
real hillside happens to be lower.

---

## 6. Recipe: moving terrain between PLACES

Terrain is voxels, not instances — there is no Explorer copy-paste, and `ReadVoxels` → `WriteVoxels`
across places is impossible (the array is far too large to pass through a tool call).

1. **Source place:** `local tr = Terrain:CopyRegion(Region3int16.new(minCell, maxCell)); tr.Parent = workspace`
2. **Human** copies that `TerrainRegion` in Explorer and pastes it into the target place.
3. **Target place:** `Terrain:PasteRegion(tr, cornerCell, true)`, then delete the helper.

- 🔴 **`Region3int16`'s max corner is INCLUSIVE.** Measured: `CopyRegion` over min `(-653,-15,1097)` to max
  `(-547,5,1203)` returns `SizeInCells` **107, 21, 107** — that is `max - min + 1`, not `max - min`. So a
  half-width of 53 cells captures 107 cells, and the paste corner is `destinationCentreCell - halfCells`.
- `pasteEmptyCells = true` makes the paste **exact** (empty cells clear existing terrain); `false`
  overlays solid cells only.
- **To UNDO a sculpt, paste a clean patch over it** rather than computing what the surroundings should look
  like: copy an equal-sized region of untouched terrain from far enough away that the boxes cannot overlap,
  verify it really is clean, then paste it with `pasteEmptyCells = true`. The result then matches its
  surroundings by construction instead of by your arithmetic about seabed depth and water occupancy.
- **`TerrainRegion` does not replicate between server and client.**
- ⚠️ Offsets are cells → **multiples of 4 studs only**, and must be derived **surface-to-surface**.
  Worked example: source top water voxel spans −8…−4 (centre −6), target water level 12 → the offset is
  **+16**, not +18. Comparing the *centre* to the *level* gives the wrong, unrepresentable answer.

---

## 7. Recipe: joining HAND-SCULPTED terrain to GENERATED terrain

The pattern that worked (Job #071):

1. **Seed-lock the junction.** If the generator's shape is seed-derived, force a fixed centre/width in a
   band beside the sculpted zone and blend to the seeded shape over several hundred studs — otherwise
   the hand-sculpt lines up for exactly one seed. **Verify by evaluating across ≥5 seeds and asserting
   the spread at the junction is 0.**
2. **Protect the sculpted zone**: clamp the generator's chunk region to the boundary. **Clamp, not
   skip** — if the boundary isn't a multiple of the chunk length, skipping leaves a hole.
3. **Delete any blanket `Terrain:Clear()` at boot.** It erases hand-sculpted work on every server start.
   Ship the place with the sculpted zones present and the generated corridor empty.
4. **Generate the sculpted zone's base with the same generator**, sculpt on top, and leave the voxels
   nearest the seam untouched — the seam then matches **by construction rather than by eye**.
5. Suppress generator features (forks, branching) inside the locked band, or the channel can split
   right where it meets terrain built for a single mouth.

---

## 8. Don't

- Don't call `FillTerrain`/`SmoothRegion` (not real API) or `GetCell`/`SetCell`/`SetWaterCell`
  (removed legacy).
- Don't `pcall` a terrain read/write and ignore the result — that is how a size violation becomes a
  silent no-op that reports success.
- Don't pass `Region3` to `CopyRegion`, or studs to `PasteRegion`.
- Don't script hero terrain (§1) — but **do** script computed channels, valleys and seams.
- Don't trust `Terrain.MaxExtents` as "is there terrain?" — it returns a huge sentinel box when empty.
  Probe voxels or use `CountCells()`.
- Don't iterate a morphological rule over terrain without proving it converges (§4).
