# Roblox NPC AI & pathfinding — reference

Sourced from official Creator Docs, current 2026-07. Not-verbatim items flagged **[unverified]**.
Run AI **server-side** (authoritative).

## PathfindingService

`PathfindingService:CreatePath(agentParams) → Path` (reuse the Path; re-`ComputeAsync` each tick).
**Verified agent keys:** `AgentRadius`(2), `AgentHeight`(5), `AgentCanJump`(true), `AgentCanClimb`(false),
`WaypointSpacing`(4; `math.huge` = only turning points), **`Costs`** (map `Enum.Material` names /
`PathfindingModifier` / `PathfindingLink` labels → cost; default 1; high = avoid; `math.huge` = impassable).
⚠️ **`AgentJumpHeight`/`AgentMaxSlope`/`AgentWalkableClimb` are NOT valid keys [unverified/legacy]** — jump/
slope come from the Humanoid's `JumpHeight`/`JumpPower`/`MaxSlopeAngle` + `AgentCanJump`/`AgentCanClimb`.

`Path:ComputeAsync(start, finish)` — yields; **`pcall` it and check `path.Status == Enum.PathStatus.Success`**
(else `NoPath`; other statuses deprecated). `Path:GetWaypoints()` → `{PathWaypoint}` each with `Position`,
`Action` (`Walk`/`Jump`/`Custom`), `Label`. `Path.Blocked(idx)` / `Unblocked(idx)` — **recompute only if the
blockage is ahead** (`idx >= nextWaypointIndex`), then disconnect + recompute.

**Costs targeting** (make a croc prefer water / land animals avoid it): set `Costs = {Water = 20, ...}`; or
a **`PathfindingModifier`** (`Label`, `PassThrough`) on an anchored non-colliding region for no-go zones; or
a **`PathfindingLink`** (`Attachment0/1`, `IsBidirectional`, `Label`) for a discrete custom traversal (e.g.
`"BoardBoat"`) → produces `Action=Custom` waypoints you handle in code.

**Limits:** straight-line start↔finish ≤ **3,000 studs**; ~**20,000-node** budget; Y within ±65,536.
**Deprecated:** `FindPathAsync`, `ComputeRawPathAsync`, `ComputeSmoothPathAsync` — use `CreatePath`+`ComputeAsync`.

## Moving Humanoid NPCs

- **`Humanoid:MoveTo(location, part?)`** — the optional `part` **re-bases the goal to a moving part → pass
  the boat's part to chase it** between recomputes. `Humanoid:Move(dir, relativeToCamera)` = lower-level.
- **`Humanoid.MoveToFinished(reached)`** — **times out ~8s** (`reached=false`); on long chases re-issue
  `MoveTo` every ~6s so it doesn't stall. `WalkSpeed`, `Jump=true`, `ChangeState(Enum.HumanoidStateType.Jumping)`.
- **Follow loop:** for each waypoint `MoveTo(wp.Position)` → wait `MoveToFinished`; if
  `wp.Action == Enum.PathWaypointAction.Jump` trigger a jump.

## NPCs without a Humanoid (perf)

`AnimationController` + child `Animator` = **animation only** (no MoveTo/WalkSpeed). Move manually via
constraints (`LinearVelocity`/`AlignPosition`/`AlignOrientation` — see `roblox-physics`) or `PivotTo`/CFrame
each step toward each waypoint. **Big CPU win for swarms of simple enemies** (Humanoids are expensive), at
the cost of reimplementing movement.

## Detection / aggro (cheap → expensive)

1. **Magnitude:** `(targetPos - npcPos).Magnitude` vs aggro/attack ranges (gate first).
2. **Radius sweep:** `workspace:GetPartBoundsInRadius(pos, radius, OverlapParams)` (or `InBox`) → candidates
   (filter to players/boat via `OverlapParams`).
3. **Line-of-sight raycast:** `workspace:Raycast(origin, target-origin, RaycastParams)` — **direction
   magnitude = ray length**; visible if no solid hit before the target. `RaycastParams`:
   `FilterDescendantsInstances`, `FilterType` (Include/Exclude), **`IgnoreWater`** (set per animal),
   `CollisionGroup`, `RespectCanCollide`. Also `Blockcast`/`Spherecast` for fat bodies.
Pick nearest candidate, confirm with one LoS ray, then chase — don't spam rays per frame.

## Behavior FSM (built from primitives — no built-in API)

**Idle/Patrol** (no target: wander via periodic MoveTo, or sleep) → **Chase** (radius+LoS: ComputeAsync,
follow waypoints, **recompute on interval 0.3–1.0s + on Blocked-ahead**) → **Attack** (in range+LoS: stop,
play attack anim, **damage server-side**, cooldown via `os.clock()`) → back to Chase when out of range.

## Attacking a MOVING target (boat + players)

- **Lead/predict:** aim at `targetPos + targetVelocity * leadTime` (velocity from last 2 samples or the
  boat's `AssemblyLinearVelocity`) so the croc intercepts, not trails.
- **Track cheaply:** `MoveTo(loc, boatPart)`. Re-path on cadence + on `Path.Blocked`. Water/terrain `Costs`
  + a `PathfindingLink "BoardBoat"` to model climbing aboard.

## Spawning, grouping, pooling

- **`CollectionService`:** `AddTag`/`RemoveTag`/`HasTag`, `GetTagged(tag)` (enumerate live enemies for a
  global tick), `GetInstanceAddedSignal`/`GetInstanceRemovedSignal` (wire spawn/cleanup).
- **Object pooling** (your own code — no built-in): keep pre-built rigs; on spawn pull one + `PivotTo` +
  enable AI; on death reset + return to pool (don't Destroy+Clone). Disconnect all connections + clear tags on death.

## Performance

Server-authoritative; **throttle & stagger** ComputeAsync (never per-frame); **cap active full-AI NPCs**,
LOD distant ones to slow ticks/sleep; cheap checks before rays; drop Humanoids for swarms; animate NPCs
client-side; reuse `Path` objects.

## Sources
characters/pathfinding, classes/{PathfindingService,Path,PathfindingModifier,PathfindingLink,Humanoid,
AnimationController,WorldRoot,CollectionService}, enums/{PathStatus,PathWaypointAction},
datatypes/RaycastParams, mechanics/raycasting.
