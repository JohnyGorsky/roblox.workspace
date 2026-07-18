---
name: roblox-animation
description: Roblox animation, rigging, skeletons & joints for any game in this workspace — R6/R15 rigs, Motor6D joints, bones/skinned meshes, the Animator + AnimationTrack playback API, creating/publishing animations, AnimationPriority blending, IKControl & runtime posing, default Humanoid animations, and custom/Meshy-import rigging (Adaptive Animation). Use before writing/reviewing any animation, rig setup, joint/Motor6D work, or importing/animating custom characters.
---

# Roblox animation & rigging

Full API in [reference/animation.md](reference/animation.md). This is the working guide.

## Core model

- A **rig** = Model + `Humanoid` (or `AnimationController`) + root part + parts joined by **`Motor6D`**
  (segmented) or **`Bone`** (skinned mesh). Both expose a **`Transform`** CFrame the animation system drives.
- Play via an **`Animator`** (child of the Humanoid): `Animator:LoadAnimation(animation) → AnimationTrack`.
  **Never** use the deprecated `Humanoid:LoadAnimation`.
- `Animation.AnimationId` = the published `rbxassetid://`.

## Playback quick rules

- `track:Play(fadeTime, weight, speed)` / `:Stop(fadeTime)` / `:AdjustSpeed` / `:AdjustWeight`.
- **Priority** decides who wins on shared joints: `Idle<Movement<Action<Action2/3/4<Core(1000)`.
  Action anims must outrank Movement/Idle to be seen.
- Use **`Ended`** (not deprecated `Stopped`) and **`GetMarkerReachedSignal(name)`** (not `KeyframeReached`).
- **Cache/reuse tracks**; don't reload the same Animation. Play NPC anims **client-side** (they replicate
  via the Animator — don't double-play on server + client).

## Making animations

Studio **Animation Editor** → keyframe the rig → Save (KeyframeSequence) → **Publish to Roblox** → assign
the returned asset id to `Animation.AnimationId`. External Blender/Maya anims import via the 3D Importer.

## Custom / Meshy-imported characters (important for this workspace)

- Segmented import: add `Motor6D`s (Part0=parent, Part1=child, C0/C1), chained from the root part.
- Odd-proportioned custom humanoids: use **Adaptive Animation** — import as "Custom", create
  `HumanoidRigDescription` + `DigitsRigDescription`, map ≥15 joints + a T-pose → it can play **any R15
  animation set** (the clean path for Meshy humanoids). Pair with the `roblox-chars` agent for import and
  `studio-diagnostics` for Motor6D/HipHeight fix scripts.

## Runtime posing / IK

`IKControl` (Type Transform/Position/Rotation/LookAt; Target/ChainRoot/EndEffector/Pole/Weight) layers on
top of animation. Or write `Motor6D.Transform`/`Bone.Transform` each frame in `RunService.PreSimulation`.
`AnimationConstraint` = newer spring-driven animatable joint (Motor6D remains valid, not deprecated).

## Default character anims

Edit the `Animate` LocalScript's `AnimationId`s (states: run/walk/jump/idle/fall/swim/swimidle/climb),
or set `HumanoidDescription.{Idle,Walk,Run,Jump,Fall,Swim,Climb}Animation`.
