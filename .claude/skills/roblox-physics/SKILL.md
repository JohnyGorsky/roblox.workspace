---
name: roblox-physics
description: Roblox physics knowledge for any game in this workspace — the assembly/mass/network-ownership model, and the full MODERN constraint system (VectorForce, LinearVelocity, AngularVelocity, AlignPosition, AlignOrientation, Torque; Hinge/Prismatic/Cylindrical/BallSocket/Rope/Spring/Weld constraints, Motor6D, NoCollisionConstraint), buoyancy, and vehicles. Use before writing/reviewing ANY physics — boats, vehicles, joints, movers, forces, rigs, buoyancy, network ownership, or "why is my thing jittering/spinning/falling apart".
---

# Roblox physics

Full API + properties in [reference/physics.md](reference/physics.md). This is the working guide.
**Use modern constraints; the `Body*` movers are deprecated** (reference has the mapping).

## Mental model (get this right first)

- Physics simulates **assemblies** (parts joined by `WeldConstraint`/`Motor6D` = one rigid body).
  **Anchoring two parts of one assembly SPLITS it and disables the welds** — the #1 "my vehicle fell
  apart" bug. Never anchor moving vehicle parts.
- **Network ownership** = who simulates (owner = zero-latency). Server owns anchored parts always.
- **Forces are RMU·stud/s²** → `MaxForce`/`MaxTorque` must scale with `AssemblyMass` and beat
  gravity (`Workspace.Gravity` ≈ 196.2). **Tune `MaxForce` until the goal is reachable, then
  `Responsiveness` (5..200) for feel.**

## Pick the right mover (modern)

| Want | Use |
|---|---|
| Constant push/thrust | `VectorForce` (`ApplyAtCenterOfMass=true` for pure linear) |
| Hold/reach a position | `AlignPosition` |
| Hold/reach an orientation (stay upright / face heading) | `AlignOrientation` (`PrimaryAxisOnly` = free yaw) |
| Maintain a target velocity / speed cap | `LinearVelocity` |
| Continuous spin (wheels/rotors) | `AngularVelocity` (**RelativeTo `World`/`Attachment1`, never `Attachment0`**) |
| Constant torque | `Torque` |
| Wheel/steer/door joint | `HingeConstraint` (Motor / Servo) |
| Slider/piston | `PrismaticConstraint` |
| Suspension / springy | `SpringConstraint` |
| Tow / crane / winch | `RopeConstraint` |
| Rigid attach | `WeldConstraint` (animatable rig → `Motor6D`) |
| Stop two parts colliding (wheel vs body) | `NoCollisionConstraint` |

`ActuatorRelativeTo`: `World` = fixed direction; `Attachment0` = follows the body's heading (use for
thrust that should point where the vehicle faces).

## Boat recipe (what we're building — verified pattern)

Hull = root part, unanchored, `Attachment` at COM. Then:
- **Thrust:** `VectorForce`, `RelativeTo=Attachment0` (or World with `hull.CFrame.LookVector`),
  `ApplyAtCenterOfMass=true`, `Force = throttle × mag`.
- **Steer:** `AngularVelocity` about world Y (`RelativeTo=World`) — momentum carries the hull = drift.
- **Upright + heading:** `AlignOrientation` (`PrimaryAxisOnly` to keep level but allow yaw), high `MaxTorque`.
- **Float:** custom buoyancy — `BuoyancySensor` (or raycast to water) → upward `VectorForce` ∝ submersion,
  `ApplyAtCenterOfMass=true`, **+ damping** (force opposing vertical velocity) so it doesn't bob. Don't
  rely on terrain-water auto-buoyancy alone (density<1 floats, but it's hard to tune/keep stable).
  **Two buoyancy traps that make a *moving* boat bounce forever (verified — Jungle):** (1) Apply the
  **damping separately** from the up-only `math.max(spring, 0)` clamp — if damping lives *inside* the
  clamp, it vanishes exactly when the boat rises (spring goes negative → clamped to 0 → no damping on the
  way up), so energy never leaves and it limit-cycles. (2) If you switch buoyancy **off** above some height
  (`pos.Y > WATER_Y + N`) to allow ramp jumps, keep `N` **well above the normal bob amplitude** — a cutoff
  the bob's peak reaches turns the damping off at the top of every cycle → a sustained ~several-stud bounce
  while driving. Give damping enough authority (`FLOAT_D` not << `FLOAT_K`).
- **Speed cap / water drag:** optional `LinearVelocity` or a `VectorForce` opposing velocity.
- **Ownership:** `SetNetworkOwner(driver)` on sit, `SetNetworkOwnershipAuto()` on exit; reassign cargo too.
  **BUT if you compute the vehicle's forces SERVER-side (e.g. a buoyancy loop on the server), it must stay
  SERVER-owned** — see the ownership gotcha below.
- Input via `VehicleSeat` (`ThrottleFloat`/`SteerFloat`; auto-reset to 0). Keep COM low; `Massless` decor.

## Mooring / temporarily holding a moving vehicle (verified — Jungle boat)

To park a vehicle (dock it, moor a boat, freeze a car at a checkpoint) then release it:

- **Do NOT anchor it.** Anchoring a dynamic assembly and later un-anchoring it while a **client-owned
  character is standing on it** makes the physics **explode in a single step** — the engine then
  removes the parts (you see `hull.Parent → nil` with **no `Destroying` event** and no NaN visible next
  frame, because it's gone before your monitor runs). This bit us hard: the boat "just disappeared" on
  untie. The base game's boat never anchored, so it never hit this.
- **Instead hold it with a constraint and keep it dynamic + server-owned:**
  - `AlignPosition` (`OneAttachment`, `MaxForce` > the vehicle's constant forces e.g. river current,
    `MaxVelocity` caps the reel-in speed) — move `.Position` to reel/tow it, **`:Destroy()` it to release**.
    A player standing on it rides along (it's a normal moving platform), and release is instant + safe.
  - Or `RopeConstraint` to a fixed winch point for a true tow/winch feel (distance-only, can swing).
- **When you place a moored vehicle, keep its whole footprint clear of terrain.** A hull edge buried in
  the (invisible, underwater) bank is fine while held but blows up on release. Raycast the ground under
  the *whole* footprint (a grid, not one point) and dock only where the water is deep enough.

## CFrame vs physics

Set `CFrame` directly only on **anchored** parts. On an unanchored simulated part it fights the solver
(jitter/desync). Let constraints/forces drive unanchored parts. Move a welded group via the root part's CFrame.

## Gotchas

- Two constraints on the same DOF fight → oscillation. Use `PerAxis`/`PrimaryAxisOnly`/`AlignType`.
  **Concrete case:** an `AlignPosition` holding a *floating* body bounces because it drives **Y** while
  buoyancy also drives Y. `AlignPosition.MaxForce` is a scalar (no per-axis mask), so hold X/Z only by
  re-aiming the target's Y at the body's **current** Y every frame (zero Y error → zero Y force → buoyancy
  owns the float). Same idea for any hold that should leave one axis to another system.
- **Never anchor a dynamic vehicle to "park" it** and then un-anchor with a rider aboard — it explodes
  (see *Mooring* above). Hold it with a constraint instead.
- `RigidityEnabled=true` ignores force limits (hard lock) — leave false for vehicles.
- `AngularVelocity.RelativeTo=Attachment0` is unsupported.
- Monitor `Workspace:GetNumAwakeParts()`/`GetPhysicsThrottling()`; sleep idle vehicles.
- Client owns their vehicle → still validate movement server-side (see `roblox-scripting` security).
- **Server-computed force on a client-owned body = delayed-feedback instability (verified — Jungle boat).**
  If a server loop computes and applies a force from the body's position/velocity (buoyancy spring-damper,
  station-keeping, etc.), the body MUST be server-owned. If a `VehicleSeat` hands ownership to the driver
  on sit, the server then reads that body's state via **lagged replication** and applies a force one
  round-trip late → the spring pumps energy instead of removing it → the vehicle **bounces higher and
  higher while driven** (was rock-stable while server-owned/idle). Fix: re-grab `SetNetworkOwner(nil)`
  whenever a client holds it (the seat only hands over once on sit, so a per-frame `if GetNetworkOwner() ~=
  nil then SetNetworkOwner(nil)` check settles instantly and doesn't thrash) — or move the force
  computation onto the owner (client). Diagnose by logging `GetNetworkOwner()` in the force loop.
