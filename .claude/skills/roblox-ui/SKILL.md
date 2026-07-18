---
name: roblox-ui
description: Roblox GUI/UI engineering for any game in this workspace — ScreenGui/SurfaceGui/BillboardGui containers, GuiObjects, UDim2 scale positioning, layout (UIListLayout/flex, grid, constraints), MOBILE-FIRST scaling (UIScale/UISizeConstraint/UIAspectRatioConstraint/TextScaled, safe-area insets), images/decals/9-slice, input (Activated, RichText, gamepad), and best practices. Use before building/reviewing ANY UI/HUD/menu. This is generic UI engineering — a game's specific visual design system (colors/fonts) is a separate per-game skill (e.g. Defender's roblox-gui).
---

# Roblox UI (mobile-first)

Full API in [reference/ui.md](reference/ui.md). This is the working guide. This skill = generic UI
*engineering*; a game's *visual design system* (its colors/fonts/tokens) is a separate per-game skill.

## Mobile-first — the non-negotiables (our games are mobile-first)

1. **Position & size by Scale, not Offset** (`UDim2` scale) so layouts hold on every screen. Offset only
   for things that must stay a fixed pixel size (thin borders/padding).
2. **Lock proportions + clamp size:** `UIAspectRatioConstraint` (no distortion across portrait/landscape) +
   `UISizeConstraint` (`MinSize`/`MaxSize`, never unusably small/huge). One global `UIScale` knob helps.
3. **Text:** `TextScaled` + `UITextSizeConstraint` (`MinTextSize`/`MaxTextSize`) — fits its box, stays legible.
4. **Safe area:** `ScreenGui.ScreenInsets = CoreUISafeInsets` for any interactive HUD/menu (keep off notches
   + top bar). `None` only for full-bleed non-interactive backgrounds.
5. **Touch-first input:** use **`GuiButton.Activated`** (fires for mouse click AND touch tap) — never
   mouse-only events for core actions. Favor the Input Action System for cross-platform input.
6. ⚠️ **No official tap-target pixel size exists** — size by Scale + aspect ratio and **test on real devices**;
   don't hardcode a "minimum px" as if it were official.

## Building blocks

- Containers: `ScreenGui` (author in StarterGui → clones to PlayerGui), `SurfaceGui` (on a part),
  `BillboardGui` (3D, faces camera). `GuiService:GetGuiInset()` for manual inset math.
- GuiObjects: `Frame`, `TextLabel/Button/Box`, `ImageLabel/Button`, `ScrollingFrame`, `ViewportFrame`,
  `CanvasGroup`, `VideoFrame`. **Center** with `AnchorPoint (0.5,0.5)` + `Position {0.5,0,0.5,0}`.
- Layout: `UIListLayout` (+ flex: `HorizontalFlex`/`VerticalFlex`, `UIFlexItem` — use sparingly, perf cost),
  `UIGridLayout`, `UIPadding`; modifiers `UICorner`/`UIStroke`/`UIGradient`.
- Deprecated text props to avoid: `FontSize`, `TextColor`, `TextWrap` → use `TextSize`/`TextColor3`/`TextWrapped`.

## Images

`ImageLabel`/`ImageButton` with `Image = rbxassetid://…`. **9-slice** (`ScaleType=Slice` + `SliceCenter`)
for panels/buttons that stretch cleanly at any size. `ResamplerMode.Pixelated` for crisp pixel art. On 3D
parts: `Decal` (fits a face) vs `Texture` (tiles; `StudsPerTileU/V`).

## Best practices

Reuse component templates (clone a styled Frame + a layout object) over bespoke instances; `CanvasGroup`
(`GroupTransparency`/`GroupColor3`) to fade/tint a whole panel as one; `RichText` for inline styling;
contrast + `TextScaled` for legibility. Build UI on the client; drive authoritative state from the server
(see `roblox-scripting`).
