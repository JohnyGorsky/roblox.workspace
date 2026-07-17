# Roblox physics — authoritative reference

Sourced from official Creator Docs (`create.roblox.com/docs`), current 2026-07. Not-verbatim items
flagged **[unverified]**. Docs rarely print defaults, so "default" is noted only when stated.

## 1. Physics model

**Assembly** = parts joined by a rigid `WeldConstraint` or movable joints (`Motor6D`) → simulated as
**one rigid body**. Assembly joints are active only in `Workspace`. Each assembly has one **root part**
(`AssemblyRootPart`; influence via `RootPriority` -127..127). **Anchoring one part anchors the whole
assembly; anchoring TWO parts SPLITS the assembly and disables the welds between them** (classic
"vehicle fell apart" bug).

**BasePart physics props:** `Anchored`, `CanCollide`, `CanTouch`, `CanQuery`, `Massless` (no mass/inertia
contribution — for decorative welded parts), `CustomPhysicalProperties`, `Mass` (ro), `CenterOfMass` (ro).
**Assembly:** `AssemblyMass` (ro), `AssemblyCenterOfMass` (ro), `AssemblyLinearVelocity` (rw, studs/s),
`AssemblyAngularVelocity` (rw, rad/s). **Methods:** `ApplyImpulse(v)`, `ApplyImpulseAtPosition(v,pos)`,
`ApplyAngularImpulse(v)`, `GetVelocityAtPosition(pos)`, `GetConnectedParts(recursive)`.

**PhysicalProperties:** `Density` 0.0001..100 (**water = 1.0**), `Friction` 0..2, `Elasticity` 0..1,
`FrictionWeight`/`ElasticityWeight` 0..100. `PhysicalProperties.new(material)` or `(d,f,e[,fw,ew])`.

**Collision groups** (`PhysicsService`, **max 32**): `RegisterCollisionGroup(name)`,
`CollisionGroupSetCollidable(a,b,bool)`, set `BasePart.CollisionGroup = name`.

**Workspace:** `Gravity` (default **196.2** studs/s²), `FallenPartsDestroyHeight`, `AirDensity`,
`GetNumAwakeParts()`, `GetPhysicsThrottling()`. **Units:** 1 stud=28cm, 1 RMU=21.952kg; forces are
RMU·stud/s² — **`MaxForce`/`MaxTorque` must scale with `AssemblyMass`**.

## 2. Network ownership

Decides **who simulates** a part — owner gets latency-free physics. Default: server owns all; engine
auto-reassigns unanchored parts to a nearby client. **Server always owns anchored parts.** API (on the
root part, affects the assembly): `SetNetworkOwner(player?)` (nil = server), `SetNetworkOwnershipAuto()`,
`GetNetworkOwner()` **[unverified sig]**. **Vehicle pitfall:** if a passenger sits before the driver,
they own the whole vehicle. Fix: `SetNetworkOwner(driver)` on sit, `SetNetworkOwnershipAuto()` on exit,
and reassign loose cargo to the driver too.

## 3. Attachments

A point+orientation on a part. Constraints connect `Attachment0`(+`Attachment1`). Props: `CFrame`,
`Position`, `Orientation`, **`Axis`** (local X = the "primary axis" many constraints act on),
`SecondaryAxis` (local Y), `World*` variants. **One-attachment** mode = align to a world goal
(`Position`/`CFrame`); **two-attachment** = align the two attachments. Mechanical constraints need both.

## 4. Mover constraints / forces — MODERN (use)

Cross-cutting: **`ActuatorRelativeTo`** = `World`|`Attachment0`|`Attachment1` (frame the vector is in —
`Attachment0` makes a force follow the body's heading). **`ReactionForce/TorqueEnabled`** applies
equal-opposite to Attachment1's body. **`MaxForce`/`MaxTorque`** must beat gravity×mass.
**`Responsiveness`** 5..200 (feel; tune this, not just MaxForce).

- **`VectorForce`** — `Force` (Vector3), `RelativeTo`, **`ApplyAtCenterOfMass`** (true = pure linear;
  false = at Attachment0, induces torque). Constant thrust/hover/propulsion. Does NOT cap velocity.
- **`Torque`** — `Torque` (Vector3), `RelativeTo`. Constant spin authority.
- **`LineForce`** — `Magnitude` along A0→A1, `InverseSquareLaw`, `MaxForce` (only w/ inverse-square).
  Attraction/repulsion.
- **`AngularVelocity`** — `AngularVelocity` (Vector3 target), `MaxTorque`, `RelativeTo`
  (**`Attachment0` is unsupported/unpredictable — use `World` or `Attachment1`**). Spinning wheels/rotors.
- **`LinearVelocity`** — modern `BodyVelocity`. `VelocityConstraintMode` = `Vector`/`Line`/`Plane` with
  `VectorVelocity`/`LineVelocity`+`LineDirection`/`PlaneVelocity`. `ForceLimitsEnabled`+`MaxForce`.
  Maintain a target velocity (cruise/conveyor/speed cap).
- **`AlignPosition`** — modern `BodyPosition`. `Mode` One/Two, `Position` (goal), `RigidityEnabled`
  (ignore limits), `MaxForce`, `MaxVelocity`, `Responsiveness`, `ApplyAtCenterOfMass`. Hover/track a point.
- **`AlignOrientation`** — modern `BodyGyro`. `Mode` One/Two, `CFrame` (goal), **`PrimaryAxisOnly`**
  (correct only primary axis → free yaw, locked roll/pitch), `AlignType`
  (AllAxes/PrimaryAxisParallel/Perpendicular/LookAt), `MaxTorque`, `MaxAngularVelocity`, `Responsiveness`,
  `RigidityEnabled`. **Keep a boat level / facing its heading.**

## 5. Mechanical constraints / joints — MODERN

Powered ones share **`ActuatorType`** = `None`|`Motor` (velocity-driven)|`Servo` (angle/position-driven).

- **`HingeConstraint`** — 1-axis rotation. Motor: `AngularVelocity`, `MotorMaxTorque`,
  `MotorMaxAcceleration`. Servo: `TargetAngle`, `AngularSpeed`, `ServoMaxTorque`, `AngularResponsiveness`.
  `LimitsEnabled`/`LowerAngle`/`UpperAngle`/`Restitution`, `CurrentAngle`. Wheels (motor), steering/doors (servo).
- **`PrismaticConstraint`** — 1-axis slide. Motor `Velocity`/`MotorMaxForce`; Servo `TargetPosition`/`Speed`/
  `ServoMaxForce`; limits. Pistons/elevators/landing gear.
- **`CylindricalConstraint`** — slide + rotate (both actuators). Steer-and-suspend.
- **`BallSocketConstraint`** — free 3-axis rotation; `LimitsEnabled`/`UpperAngle` cone, twist limits,
  `MaxFrictionTorque`. Ragdolls/hitches/pendulums.
- **`UniversalConstraint`** — two perpendicular axes; `MaxAngle` (default 45). Driveshafts.
- **`RodConstraint`** — fixed distance, rotation allowed. **`RopeConstraint`** — max distance (goes
  slack); `Length`, `Restitution`, winch (`WinchEnabled`/`WinchTarget`/`WinchSpeed`/`WinchForce`). Tow/crane.
- **`SpringConstraint`** — `FreeLength`, `Stiffness`, `Damping`, `MaxForce`, `MinLength`/`MaxLength`.
  Vehicle suspension.
- **`WeldConstraint`** — MODERN rigid weld (`Part0`/`Part1`, no C0/C1; keeps current relative pose).
  `Weld` = legacy (C0/C1); `RigidConstraint` = attachment-based successor **[props unverified]**.
- **`Motor6D`** — animatable joint (`Part0/Part1/C0/C1/Transform`); rigs. For **avatars** superseded by
  `AnimationConstraint`; still correct for mechanical rigs (turrets, animated vehicle parts).
- **`NoCollisionConstraint`** — disables collision between `Part0`&`Part1` only (wheels vs chassis).

## 6. Legacy BodyMovers — DEPRECATED → modern replacement

`BodyVelocity`→**LinearVelocity**; `BodyAngularVelocity`→**AngularVelocity**; `BodyForce`→**VectorForce**;
`BodyThrust`→**VectorForce** (ApplyAtCenterOfMass=false); `BodyPosition`→**AlignPosition**;
`BodyGyro`→**AlignOrientation**; `RocketPropulsion`→**AlignPosition+AlignOrientation**. (Old `P`/`D`
tuning ≈ `Responsiveness`/`Damping`.) Deprecated pages sometimes point to other legacy movers — ignore.

## 7. Buoyancy & drag

Terrain water auto-applies buoyancy+drag to unanchored parts; float/sink threshold is **density vs
water = 1.0** (density<1 floats). Exact force curve **[unverified]**. **`BuoyancySensor`** (parent to a
part) only *detects*: `TouchingSurface`, `FullySubmerged` (no force). **Custom buoyancy (recommended for
a boat):** read submersion (BuoyancySensor or raycast to water) → upward **`VectorForce`** (or
**`AlignPosition`** to a hover height) proportional to depth, `ApplyAtCenterOfMass=true`, + **damping**
(force opposing vertical velocity) so it doesn't oscillate, + **`AlignOrientation`** to keep level.
Aerodynamic drag (`Workspace.FluidForces=Experimental` + `EnableFluidForces`) is off by default & beta —
model your own drag as a `VectorForce` opposing velocity.

## 8. Vehicles

**`VehicleSeat`:** `Throttle`/`ThrottleFloat` (1/0/-1), `Steer`/`SteerFloat`, `Occupant`, `Disabled`,
`HeadsUpDisplay`, `MaxSpeed`, `Torque`, `TurnSpeed`, `Sit(humanoid)`. Throttle/Steer auto-reset to 0.
**Grounded/mechanical vehicle:** HingeConstraint motors (wheels), Spring/Cylindrical (suspension), Hinge
servo or AlignOrientation (steering), NoCollisionConstraint (wheels↔body). **Boat/hover/arcade:**
`VectorForce` thrust along hull forward (`RelativeTo=Attachment0`) + `AlignOrientation` (level + steer) +
custom buoyancy + optional `LinearVelocity`/drag for a speed cap. Assign network ownership to the driver.

## 9. CFrame vs physics

Set `CFrame` directly only on **anchored**/deterministic parts (platforms, timed doors, cutscenes).
Setting CFrame on an unanchored simulated part fights the solver (jitter/teleport/desync). Let physics
simulate (constraints/forces on **unanchored** parts) for collision, momentum, buoyancy, responsiveness.
Move a welded group via the **root part's `CFrame`**, never individual welded children.

## 10. Gotchas

- Don't stack two constraints controlling the same DOF (they oscillate) — use `PerAxis`/`PrimaryAxisOnly`/
  `AlignType` so each owns only its axes.
- Tune `MaxForce`/`MaxTorque` until the goal is reachable (beat gravity×`AssemblyMass`), then `Responsiveness`.
- Upright: `AlignOrientation` high `MaxTorque`, moderate `Responsiveness`, `PrimaryAxisOnly` for free yaw.
- `ApplyAtCenterOfMass=true` on thrust/buoyancy to avoid unwanted torque.
- `Massless` on decorative parts; keep COM low for a stable boat.
- Never anchor moving vehicle parts (anchor splits assembly + forces server ownership).
- Monitor `GetNumAwakeParts()`/`GetPhysicsThrottling()`; sleep idle vehicles; fewer well-tuned constraints > many overlapping.

## Sources
`/docs/physics/{assemblies,network-ownership,mover-constraints,mechanical-constraints,units}`,
`/docs/tutorials/use-case-tutorials/physics/create-moving-objects`, and class/datatype pages for each
constraint, `BasePart`, `Workspace`, `Attachment`, `VehicleSeat`, `BuoyancySensor`, `PhysicsService`,
`PhysicalProperties`, `FluidForces`, plus the deprecated Body* pages.
