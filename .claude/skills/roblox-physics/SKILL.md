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
- **Speed cap / water drag:** optional `LinearVelocity` or a `VectorForce` opposing velocity.
- **Ownership:** `SetNetworkOwner(driver)` on sit, `SetNetworkOwnershipAuto()` on exit; reassign cargo too.
- Input via `VehicleSeat` (`ThrottleFloat`/`SteerFloat`; auto-reset to 0). Keep COM low; `Massless` decor.

## CFrame vs physics

Set `CFrame` directly only on **anchored** parts. On an unanchored simulated part it fights the solver
(jitter/desync). Let constraints/forces drive unanchored parts. Move a welded group via the root part's CFrame.

## Gotchas

- Two constraints on the same DOF fight → oscillation. Use `PerAxis`/`PrimaryAxisOnly`/`AlignType`.
- `RigidityEnabled=true` ignores force limits (hard lock) — leave false for vehicles.
- `AngularVelocity.RelativeTo=Attachment0` is unsupported.
- Monitor `Workspace:GetNumAwakeParts()`/`GetPhysicsThrottling()`; sleep idle vehicles.
- Client owns their vehicle → still validate movement server-side (see `roblox-scripting` security).
