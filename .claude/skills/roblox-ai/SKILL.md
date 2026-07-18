---
name: roblox-ai
description: Roblox NPC AI & pathfinding for any game in this workspace — PathfindingService (CreatePath/ComputeAsync/waypoints/costs/modifiers/links), moving Humanoid & Humanoid-less NPCs, detection/aggro (magnitude → radius overlap → line-of-sight raycast), the idle/patrol/chase/attack behavior loop, chasing/leading a MOVING target, spawning/pooling via CollectionService, and server-authoritative perf. Use before building/reviewing enemy or NPC behavior, pathfinding, mob spawning, or aggro/attack logic.
---

# Roblox NPC AI & pathfinding

Full API in [reference/ai.md](reference/ai.md). This is the working guide. **All AI runs server-side.**

## Pathfinding recipe

```lua
local path = PathfindingService:CreatePath({ AgentRadius=2, AgentHeight=5, AgentCanJump=true,
    Costs = { Water = 20 } })                       -- high cost = avoid; math.huge = impassable
local ok = pcall(function() path:ComputeAsync(npcPos, targetPos) end)
if ok and path.Status == Enum.PathStatus.Success then
    for _, wp in path:GetWaypoints() do
        humanoid:MoveTo(wp.Position); humanoid.MoveToFinished:Wait()
        if wp.Action == Enum.PathWaypointAction.Jump then humanoid.Jump = true end
    end
end
```
- **Reuse the `Path`** (re-ComputeAsync each tick); **`pcall` + check `Status == Success`**.
- **Limits:** start↔finish ≤ 3000 studs, ~20000-node budget. **Deprecated:** `FindPathAsync` (use `CreatePath`+`ComputeAsync`).
- `AgentJumpHeight`/`AgentMaxSlope`/`AgentWalkableClimb` are **not** valid keys — use the Humanoid's props.
- Recompute on an **interval** + on `Path.Blocked` (only if the blockage is ahead). **Stagger** recomputes across NPCs.

## Detection (cheap → expensive)

`(target-npc).Magnitude` gate → `workspace:GetPartBoundsInRadius(pos, r, OverlapParams)` sweep → one
`workspace:Raycast(origin, target-origin, RaycastParams)` LoS check (`RaycastParams.IgnoreWater` per animal).

## Behavior loop (build it yourself — no FSM API)

**Idle/Patrol** (wander or sleep) → **Chase** (radius+LoS → path + follow, re-path on interval/block) →
**Attack** (in range+LoS → stop, play anim, **damage server-side**, cooldown via `os.clock()`) → back to Chase.

## Chasing a MOVING target (the boat) — Last River crocs

- **Track cheaply:** `Humanoid:MoveTo(location, boatPart)` — the 2nd arg re-bases the goal to the boat's
  part, so it follows between recomputes. Re-issue `MoveTo` before the ~8s `MoveToFinished` timeout.
- **Lead/predict:** aim at `targetPos + boat.AssemblyLinearVelocity * leadTime` to intercept, not trail.
- **Amphibious:** `Costs` (materials) + `PathfindingModifier` no-go zones so crocs prefer water; a
  `PathfindingLink` labeled `"BoardBoat"` models climbing aboard (handle its `Action=Custom` waypoint).

## NPCs without a Humanoid (swarm perf)

`AnimationController` + child `Animator` = animation only (no `MoveTo`). Move via constraints
(`LinearVelocity`/`AlignOrientation` — see `roblox-physics`) or `PivotTo` each step. Much cheaper than
Humanoids for many simple enemies; you reimplement movement.

## Spawning / pooling / perf

- **`CollectionService`** tags: `GetTagged(tag)` (global AI tick over all live enemies),
  `GetInstanceAddedSignal`/`RemovedSignal` (spawn/cleanup). Disconnect connections + clear tags on death.
- **Object pool** (your code): reuse pre-built rigs (`PivotTo` + re-enable) instead of Destroy+Clone.
- **Perf:** cap active full-AI NPCs, LOD distant ones to slow/sleep, cheap checks before rays, animate
  NPCs client-side, throttle+stagger pathfinding. Never trust the client for aggro/damage.
