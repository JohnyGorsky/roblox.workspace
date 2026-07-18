# Roblox performance optimization — reference

Sourced from official Creator Docs, current 2026-07. Not-verbatim items flagged **[unverified]**.
Frame budget: **16.67 ms = 60 FPS** (server heartbeat also capped 60).

## Profiling

- **MicroProfiler** (`Ctrl+F6`; mobile via in-game Settings → web UI at shown IP:port, `/90` for more frames).
  Frame colors: **orange = CPU (Jobs)**, **blue/red = GPU/render** bottleneck. Custom scopes:
  `debug.profilebegin/profileend`. Watch scopes: `ProcessPackets` (network), `physicsStepped`→`worldStep`,
  `updateInvalidatedFastClusters` (Humanoid/size-change rebuilds), `RenderView`, `computeLightingPerform`.
- **Developer Console** (`F9`): logs, memory (`LuaHeap`/`InstanceCount` must be **flat over time** — growth = leak).
- **`Stats`** service (`DataReceiveKbps`, `InstanceCount`, `GetTotalMemoryUsageMb`), `Workspace:GetRealPhysicsFPS()`,
  `GetNumAwakeParts()`. Overlays `Shift+Ctrl+F1..F5`, `Shift+F2` (draw calls).
- **Performance analytics** (≥100 DAU): P90/P50/P10 client/server frame rate, memory %, **OOM exits by device** —
  the low-end truth source. Plus the Studio **Device Emulator**.

## Instance Streaming (mandatory for a long world)

On `Workspace` (**set in Studio, not script**): `StreamingEnabled`; `StreamingMinRadius` (64),
`StreamingTargetRadius` (1024 — **lower for mobile**); `StreamingIntegrityMode = PauseOutsideLoadedArea`
(so a fast boat can't outrun the stream); `StreamOutBehavior = Opportunistic`; `ModelStreamingBehavior = Improved`.
**`Model.ModelStreamingMode`:** **`Atomic`** for the boat/mechanisms (never half-loaded), **minimize `Persistent`**.
`Player:RequestStreamAroundAsync(pos)` **before teleport and ahead of the boat's path** (hide pop-in).
`LevelOfDetail = SLIM` + `EnableSLIMAvatars`.

## Rendering

- **Instancing = the #1 mobile lever:** the engine batches meshes sharing an identical `MeshContent` **and**
  `SurfaceAppearance`/texture. **Duplicate one imported mesh; don't bulk-import copies** (different ids break
  instancing). Applies to NPC crowds + repeated props.
- **`MeshPart.RenderFidelity = Automatic`** (or `Performance`); avoid `Precise` at scale.
- **Shadows:** `BasePart.CastShadow = false` on small/distant parts; `Light.Shadows` off where unneeded;
  **Voxel** lighting cheapest, `Future` heaviest (test on-device).
- **Occlusion culling** (auto since 2025) + **texture streaming** (auto, all platforms 2026) — no API; design
  occluders (hull/walls). Watch **overdraw** (stacked transparency) and draw calls (`Shift+F2`).

## Physics

Anchor all static parts (biggest win). **`Workspace.PhysicsSteppingMethod = Adaptive`** (buckets islands to
240/120/60 Hz — up to ~2.5×). `CollisionFidelity = Box`/`Hull` (avoid `PreciseConvexDecomposition`). Reduce
awake parts (`GetNumAwakeParts`), disable `CanCollide`/`CanTouch`/`CanQuery` when unneeded. **Single stable
network owner for the boat** (no ownership thrash).

## Scripting

Signals > polling; limit high-freq `RunService` events; **spread heavy work across frames with `task.wait()`**;
**Parallel Luau (Actors)** for procedural gen / bulk raycasts (`task.desynchronize`/`synchronize`,
`ConnectParallel`, `SharedTable`); `--!native` for hot server numeric loops; no per-frame allocations;
**disconnect connections**.

## Memory

Leaks = undisconnected connections, un-destroyed characters, growing tables. Fixes: track + `Disconnect()`
all connections; `Workspace.PlayerCharacterDestroyBehavior`; **`Debris:AddItem(inst, life)`** for transient
VFX; **pool NPCs** (not Destroy+Clone); textures **≤512²** (1024² = 4× memory); dedupe assets; load audio
on-demand. NPCs: `Humanoid:SetStateEnabled(false, ...)` unused states, **animate client-side**,
`AnimationController` for simple NPCs, avoid needless size/scale changes.

## Mobile checklist

- Streaming: low TargetRadius, `Opportunistic`, `Improved`, boat `Atomic`, minimal `Persistent`, `RequestStreamAround` ahead.
- Rendering: shared-id instancing; `RenderFidelity Automatic`; `LevelOfDetail SLIM`+`EnableSLIMAvatars`;
  `CastShadow` off clutter; Voxel lighting; watch draw calls/overdraw.
- Physics: anchor static; `Adaptive`; Box/Hull; single boat owner; watch `GetRealPhysicsFPS`/`GetNumAwakeParts`.
- Scripting: signals not polling; chunk gen with `task.wait`; Actors for procedural; `--!native` hot loops.
- Memory: disconnect all; `Debris` VFX; pool NPCs; client-side NPC anim; textures ≤512²; dedupe.
- Loading: `ContentProvider:PreloadAsync` **only** loading-screen/spawn assets (never whole Workspace).
- Verify: MicroProfiler on-device (orange vs blue/red vs 16.67ms); flat `LuaHeap`/`InstanceCount`; P90 memory/OOM by device.

## Sources
performance-optimization/{improve,identify}, studio/microprofiler, workspace/streaming,
physics/adaptive-timestepping, scripting/multithreading, luau/native-code-gen,
production/analytics/performance, parts/meshes, classes/Stats.
