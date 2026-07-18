---
name: roblox-optimization
description: Roblox performance optimization for any game in this workspace (mobile-first) — profiling (MicroProfiler, Performance analytics, GetRealPhysicsFPS), Instance Streaming for a long world, rendering (mesh instancing, LOD/SLIM, shadows, draw calls), physics (adaptive stepping, collision fidelity, awake parts), scripting (Parallel Luau, native, spread-across-frames), and memory (connection/instance leaks, pooling, textures). Use when the game runs slow, before shipping a phase, or when reasoning about mobile perf/streaming/memory.
---

# Roblox performance optimization (mobile-first)

Full detail + checklist in [reference/optimization.md](reference/optimization.md). This is the working guide.
Budget: **16.67 ms/frame**. Our games are mobile-first — optimize for low-end devices.

## Profile first (don't guess)

**MicroProfiler** (on-device via the web UI) — is the bottleneck **orange (CPU/Jobs)** or **blue/red (GPU)**?
Watch `ProcessPackets`, `physicsStepped`, `updateInvalidatedFastClusters`, `RenderView`. Keep `LuaHeap`/
`InstanceCount` **flat** (growth = leak). `GetRealPhysicsFPS()`/`GetNumAwakeParts()` for the boat.
**Performance analytics** P90 memory + OOM by device.

## The big levers (in order)

1. **Instance Streaming** (long world): `StreamingEnabled`, low `StreamingTargetRadius`, `Opportunistic`
   stream-out, boat/mechanisms `Atomic`, minimal `Persistent`, `RequestStreamAroundAsync` ahead of the boat.
2. **Mesh instancing:** reuse one asset id (duplicate, don't re-import) so NPC crowds/props batch. Biggest render win.
3. **Physics:** anchor static parts; `PhysicsSteppingMethod = Adaptive`; `CollisionFidelity = Box`/`Hull`;
   single stable boat owner.
4. **Shadows/lighting:** `CastShadow=false` on clutter; Voxel lighting on mobile; don't stack post-effects.
5. **Memory:** `Disconnect()` every connection; `Debris:AddItem` transient VFX; **pool NPCs**; textures ≤512²; dedupe.
6. **Scripting:** signals over polling; **chunk procedural generation across frames** (`task.wait`) or run it in
   **Parallel Luau (Actors)**; `--!native` hot server loops.

## NPCs (many crocs/animals)

Animate **client-side**, `AnimationController` for simple ones, disable unused Humanoid states, **pool** them,
LOD distant ones to slow/sleep (see `roblox-ai`).

## Verify
MicroProfiler on the **Device Emulator** / a real phone; confirm flat memory and P90/OOM by device before shipping a phase.
