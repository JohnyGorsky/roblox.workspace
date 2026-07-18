# Roblox animation, rigging, skeletons & joints — reference

Sourced from official Creator Docs, current 2026-07. Not-verbatim items flagged **[unverified]**.

## 1. Rigs

A rig = a `Model` with body parts joined by joints + a `Humanoid` + a root part.
- **R6** (6 parts, legacy, no layered clothing) vs **R15** (15 parts, required for avatars/layered
  accessories/Adaptive Animation). Root = **`HumanoidRootPart`** (invisible; LowerTorso→HRP via a
  Motor6D named "Root").
- **`Motor6D`** joins two parts animatably: `Part0`, `Part1`, `C0`, `C1` (offsets), and **`Transform`**
  (CFrame the animation system writes each frame). `Active`/`Enabled` inherited.
- **Rig Builder** (Avatar tab → Character) inserts a ready R6/R15 rig.
- **Animatable custom model needs:** Humanoid (or AnimationController), a root/primary part, Motor6Ds
  chained from root, and an **`Animator`**.

## 2. Skeleton / skinning

`Bone` instances (inherit `Attachment`) deform a single **skinned `MeshPart`** — smooth organic
characters. Key prop **`Transform`** (CFrame pose offset), + read-only `TransformedCFrame`/`WorldCFrame`.
Skin weights are authored in Blender/Maya and baked into the MeshPart on import (3D Importer).
**Bone.Transform** for skinned meshes; **Motor6D.Transform** for segmented rigs. (`SkinningEnabled`
property **[unverified]** — workflow is import-driven, not a scripted toggle.)

## 3. Playing animations

- **`Animation`** instance: `AnimationId` (`rbxassetid://…`).
- **`Animator`** (child of Humanoid or AnimationController — the modern object):
  `LoadAnimation(animation) → AnimationTrack`, `GetPlayingAnimationTracks()`, `AnimationPlayed` event.
  Access: `humanoid:WaitForChild("Animator")`.
- **`AnimationController`** for non-Humanoid rigs — but its own `LoadAnimation` is **deprecated**; parent
  an `Animator` under it and use `Animator:LoadAnimation`.
- **Deprecated:** `Humanoid:LoadAnimation` — use the Animator.
- **`AnimationTrack`:** `Play(fadeTime, weight, speed)`, `Stop(fadeTime)`, `AdjustSpeed(speed)`,
  `AdjustWeight(weight, fadeTime)`, `GetMarkerReachedSignal(name)`; props `Looped`, `Priority`,
  `IsPlaying`, `Length`, `Speed`, `TimePosition`, `WeightCurrent/Target`; events **`Ended`**, `DidLoop`.
  **Deprecated events:** `Stopped` (use **`Ended`** — fires after fade-out), `KeyframeReached`
  (use **`GetMarkerReachedSignal`**).

## 4. Creating animations

**Animation Editor** (Avatar tab): select rig → scrub timeline → move/rotate parts (keyframes appear) →
easing per keyframe (Linear/Constant/CubicV2/Elastic/Bounce; In/Out/InOut). Data model:
`KeyframeSequence` → `Keyframe`s → `Pose`s (CFrame per part). **Save** (AnimSaves folder) → **Publish to
Roblox** → get an asset id → set on `Animation.AnimationId`. (Rename final keyframe "End" for default
char anims.) External Blender/Maya anims import via the 3D Importer then publish.

## 5. Priority & blending

**`Enum.AnimationPriority`:** `Idle`(0) < `Movement`(1) < `Action`(2) < `Action2`(3) < `Action3`(4) <
`Action4`(5) < `Core`(1000). Higher overrides lower on the same joints. Equal priority blends by weight
(`Play` weight / `AdjustWeight`, with `fadeTime`).

## 6. IK & runtime posing

**`IKControl`:** `Type` (`Enum.IKControlType`: Transform0/Position1/Rotation2/LookAt3), `Target`,
`ChainRoot`, `EndEffector`, `EndEffectorOffset`, `Offset`, `Pole`, `Weight`, `Priority`, `SmoothTime`,
`Enabled`; methods `GetChainCount/Length`, `GetNode*CFrame`. Layers on top of animations.
**Manual posing:** write `Motor6D.Transform` (or `Bone.Transform`) as a CFrame each frame in
`RunService.PreSimulation` (legacy Stepped/Heartbeat also work).
**`AnimationConstraint`** (newer, spring-driven animatable joint): `LinearStrength`/`AngularStrength`,
`LinearDamping`/`AngularDamping`, `MaxForce`/`MaxTorque`, `IsKinematic`, `Transform`. (Claim that it
*supersedes* Motor6D via "AvatarJointUpgrade" is **[unverified]** — Motor6D shows no deprecation.)

## 7. Default humanoid animations

Every default character has an **`Animate`** LocalScript driving states `run/walk/jump/idle/fall/swim/
swimidle/climb`; replace by editing its `AnimationId` values. `Humanoid.Animator` plays them.
`HumanoidDescription` anim fields: `Idle/Walk/Run/Jump/Fall/Swim/ClimbAnimation` (asset ids).

## 8. Custom / imported rigs (incl. Meshy)

- Segmented import: add `Motor6D`s (Part0=parent, Part1=child, set C0/C1), chain from root.
- Skinned import: Bones + weights arrive on the MeshPart; add Humanoid/AnimationController + Animator.
- **Adaptive Animation** (recommended for odd-proportioned custom/Meshy humanoids): import as "Custom",
  use the Adaptive Animation tool to create `HumanoidRigDescription` + `DigitsRigDescription`, map ≥15
  joints to the standard R15 skeleton + a T-pose → the character can play **any R15 animation set**.
- Common import bugs: missing/mis-parented Motor6Ds, no HumanoidRootPart/primary part, wrong C0/C1 —
  see the `studio-diagnostics` skill's Meshy fix scripts (HipHeight, Motor6D reparent/offsets, anchoring).
- Play NPC animations **client-side** (replicates cheaply via the Animator).

## 9. Gotchas

- `Animator:LoadAnimation` (never deprecated `Humanoid:LoadAnimation`/`AnimationController:LoadAnimation`).
- `Ended` not `Stopped`; `GetMarkerReachedSignal` not `KeyframeReached`.
- Set `Priority` so Action outranks Movement/Idle or it won't show.
- Cache/reuse AnimationTracks; don't reload the same Animation. `PreferLodEnabled`/throttling help at distance.
- Animations replicate through the Animator — don't double-play on server + client (prefer client for NPCs).
- R6≠R15 joint structure; a track authored for one won't map to the other.

## Sources
art/modeling/rigging, studio/rig-builder, animation/{using,editor,inverse-kinematics},
characters/adaptive-animation, classes/{Motor6D,JointInstance,Bone,Animator,AnimationController,
AnimationTrack,Animation,IKControl,AnimationConstraint}, enums/{AnimationPriority,IKControlType}.
