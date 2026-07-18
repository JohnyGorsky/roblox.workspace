# Final Summary — Job #005: roblox-ui + roblox-animation + roblox-avatar skills

**Project**: `roblox.workspace`
**Completed**: 2026-07-18
**Status**: ✅ Completed

## What was produced

Three authoritative shared skills, docs-sourced (same rigor as `roblox-terrain`), each a `SKILL.md`
guide + `reference/` doc, unverified items flagged:

1. **`roblox-ui`** — GUI containers (ScreenGui/SurfaceGui/BillboardGui + `ScreenInsets`), GuiObjects,
   `UDim2` scale positioning, layout (UIListLayout/flex, grid, `UICorner`/`UIStroke`/`UIGradient`),
   **mobile-first scaling** (`UIScale`/`UISizeConstraint`/`UIAspectRatioConstraint`/`TextScaled`,
   `CoreUISafeInsets`), images/decals/9-slice, input (`Activated`, RichText, gamepad), best practices.
   (Named `roblox-ui` to avoid clashing with Defender's `roblox-gui` design-system skill.)
2. **`roblox-animation`** — R6/R15 rigs, Motor6D & bones/skinned meshes, `Animator`+`AnimationTrack`
   playback, creating/publishing animations, `AnimationPriority` blending, `IKControl`/runtime posing,
   default `Animate` script, and custom/Meshy rigging via **Adaptive Animation**.
3. **`roblox-avatar`** — `HumanoidDescription` dressing (classic + layered clothing, accessories),
   scaling, dressing NPCs/players server-side, and **Tools** (Handle, `RequiresHandle`, equip,
   Backpack/StarterPack/StarterGear, giving/removing). (Distinct from the `roblox-chars` Meshy agent.)

## Grounding & currency

- Three research passes over official Creator Docs; exact signatures/enums captured, e.g.
  `Enum.AccessoryType` (20 items), `AnimationPriority` values, `ScreenInsets` values.
- Current 2026 corrections captured: appearance methods now prefer **`...Async`**; `AnimationTrack.Stopped`
  → **`Ended`**, `KeyframeReached` → **`GetMarkerReachedSignal`**; `AnimationController:LoadAnimation`
  deprecated → use a child `Animator`; deprecated text props `FontSize`/`TextColor`/`TextWrap`.

## Files changed (roblox.workspace)

- New: `.claude/skills/roblox-ui/{SKILL.md,reference/ui.md}`,
  `.claude/skills/roblox-animation/{SKILL.md,reference/animation.md}`,
  `.claude/skills/roblox-avatar/{SKILL.md,reference/avatar.md}`, `Jobs/005/*`.

## Verification

- [x] All three skills loaded by the harness (appeared in the skills list as written).
- [x] Sourced from official docs; unverified items flagged in each reference.

## Notes / next
- Not committed (per rule).
- Shared skill set is now: `roblox-dev`, `roblox-terrain`, `roblox-scripting`, `roblox-physics`,
  `roblox-ui`, `roblox-animation`, `roblox-avatar`, `studio-diagnostics`.
- Resume: the deferred **pause & commit**, then Jungle (world generator / boat).
