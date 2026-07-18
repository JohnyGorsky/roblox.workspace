# Roblox GUI / UI — reference (mobile-first)

Sourced from official Creator Docs, current 2026-07. Not-verbatim-on-fetched-page items flagged
**[unverified]** (real API — confirm on the class reference before quoting exactly).

## 1. Containers

Author GUIs in **`StarterGui`**; at spawn they clone into `Players.LocalPlayer.PlayerGui` (operate on
PlayerGui at runtime).
- **`ScreenGui`** — 2D on-screen. `Enabled`, `DisplayOrder` (Z across ScreenGuis), `ResetOnSpawn`,
  `IgnoreGuiInset`, **`ScreenInsets`** (`Enum.ScreenInsets`: `None`0 / `DeviceSafeInsets`1 /
  **`CoreUISafeInsets`2** / `TopbarSafeInsets`3), `ClipToDeviceSafeArea`.
- **`SurfaceGui`** — GUI on a 3D part face. `Adornee`, `Face`, `SizingMode`, `PixelsPerStud`,
  `CanvasSize`, `LightInfluence`, `Brightness`, `AlwaysOnTop`, `MaxDistance`, `ClipsDescendants`.
- **`BillboardGui`** — GUI in 3D that faces the camera. `Adornee`, `Size`, `StudsOffset(WorldSpace)`,
  `ExtentsOffset(WorldSpace)`, `AlwaysOnTop`, `MaxDistance`, `Active`.
- **`GuiService`** — `GetGuiInset()` → two Vector2 (top-left, bottom-right pixel insets); `SelectedObject`,
  `GuiNavigationEnabled`, `AutoSelectGuiEnabled`, `AddSelectionParent/Tuple`, `RemoveSelectionGroup`, `Select`.

## 2. GuiObjects

`Frame`, `TextLabel`/`TextButton`/`TextBox`, `ImageLabel`/`ImageButton`, `ScrollingFrame`,
`ViewportFrame`, `CanvasGroup`, `VideoFrame`.
Common props: `Size`, `Position` (UDim2), `AnchorPoint`, `AutomaticSize`, `BackgroundColor3`,
`BackgroundTransparency`, `Rotation`, `ClipsDescendants`, `AbsoluteSize`. Also `Visible`, `ZIndex`,
`Active`, `Selectable`, `LayoutOrder`, `NextSelection*` **[unverified — real, confirm on class ref]**.
- **Text props:** `Text`, `TextColor3`, `TextTransparency`, `TextSize`, `TextScaled`, `TextWrapped`,
  `TextTruncate`, `TextXAlignment`/`TextYAlignment`, `FontFace`, `RichText`, `LineHeight`,
  `MaxVisibleGraphemes`, `TextStroke*`. **Deprecated: `FontSize`, `TextColor`, `TextWrap`** — use
  `TextSize`/`TextColor3`/`TextWrapped`. `TextBox`: `PlaceholderText`, `FocusLost` event.
- **`ScrollingFrame`:** `CanvasSize`, `CanvasPosition`, `AutomaticCanvasSize`, `ScrollBarThickness`, scrollbar images.
- **`ViewportFrame`:** `CurrentCamera`; parent 3D objects as children (duplicate if it must also be in world).
- **`CanvasGroup`:** flattens descendants → `GroupTransparency` / `GroupColor3` applied to the whole group.
- **`VideoFrame`:** `Video`, `Playing`, `Looped`, `TimePosition`, `Volume`.

## 3. Position & size

**`UDim2.new(scaleX, offsetX, scaleY, offsetY)`** — final = Scale×container + Offset px. **Prefer Scale**
for Position+Size (adapts to every screen); reserve Offset for fixed-pixel things (thin borders, padding).
**`AnchorPoint`** (0–1 per axis) = origin for position/scale; center = AnchorPoint `(0.5,0.5)` + Position
`{0.5,0,0.5,0}`. `AbsoluteSize`/`AbsolutePosition` = resolved pixels (read-only).

## 4. Layout & modifiers

- **`UIListLayout`:** `FillDirection`, `SortOrder`, `HorizontalAlignment`/`VerticalAlignment`, `Padding`,
  `Wraps`, `HorizontalFlex`/`VerticalFlex`. **Flexbox:** flex enum `None/Fill/SpaceBetween/SpaceAround/
  SpaceEvenly`; per-child **`UIFlexItem`** (`FlexMode` Fill/Grow/Shrink/Custom/None). Use flex sparingly (perf cost).
- **`UIGridLayout`** (`CellSize`, `FillDirection`, `FillDirectionMaxCells`, `SortOrder`; `CellPadding`
  **[unverified]**), **`UITableLayout`**, **`UIPageLayout`** **[unverified — confirm on class ref]**, **`UIPadding`**.
- **Appearance:** `UICorner` (`CornerRadius`), `UIStroke` (`Thickness`/`Color`/`ApplyStrokeMode`),
  `UIGradient` (`Color`/`Transparency`/`Rotation`), `UIShadow` **[unverified]**.
- **Constraints/scale:** `UIAspectRatioConstraint` (`AspectRatio`), `UISizeConstraint` (`MinSize`/`MaxSize`),
  `UITextSizeConstraint` (`MinTextSize`/`MaxTextSize`), `UIScale` (`Scale` multiplier on AbsoluteSize).

## 5. Scaling & MOBILE (priority)

**Rule: position/size by Scale, not Offset.** Toolkit:
- **`UIScale`** — one multiplier to scale a whole UI branch (drive off screen `AbsoluteSize`).
- **`UISizeConstraint`** (`MinSize`/`MaxSize`) — stop elements getting unusably small on phones / huge on tablets.
- **`UIAspectRatioConstraint`** — keep buttons/panels/icons from distorting across aspect ratios (portrait/landscape).
- **`TextScaled` + `UITextSizeConstraint`** — text auto-fits its box but stays legible.
- **Safe area:** `ScreenGui.ScreenInsets = CoreUISafeInsets` for any interactive HUD/menu (nothing under
  notches/top-bar); `None` only for full-bleed non-interactive backgrounds; `GuiService:GetGuiInset()` for manual math.
- Cross-platform input: the docs steer toward the **Input Action System** + **Style Queries**
  (`@PreferredInputTouch`) and a "Small" display-size category. **Test on real devices.**
- ⚠️ **No official tap-target pixel minimum exists** — don't cite a hard number as Roblox guidance; size by
  Scale + aspect ratio, clamp with UISizeConstraint, verify by testing.

## 6. Images / decals / textures

- **`ImageLabel`/`ImageButton`:** `Image` (`rbxassetid://…`) / `ImageContent`, `ImageColor3`,
  `ImageTransparency`, `ImageRectOffset`/`ImageRectSize` (sprite-sheet), `ScaleType` (`Stretch`/`Slice`/
  `Tile`; `Fit`/`Crop` **[unverified]**), `ResampleMode` (`Enum.ResamplerMode`; `Pixelated` for crisp pixel-art),
  `SliceCenter`/`SliceScale`, `TileSize`.
- **9-slice:** `ScaleType=Slice` + `SliceCenter` (Rect) → resolution-independent panels/buttons that stretch cleanly.
- **`Decal`** (3D part face): `Texture`, `Face`, `Color3`, `Transparency`, `ZIndex` — fits the face, no tiling.
- **`Texture`** (3D part face): tiles/repeats; `StudsPerTileU`/`V`, `OffsetStudsU`/`V`.

## 7. Input & interaction

- **`GuiButton.Activated`** — the cross-input event (mouse click AND touch tap); prefer it. `SecondaryActivated`
  too. (`MouseButton1Click`/`TouchTap` real but **[unverified]** on fetched page.)
- **`RichText`** (`RichText=true`): tags `<b> <i> <u> <s> <font ...> <stroke ...> <br/> <uppercase> <mark ...>`;
  close in reverse order.
- **Gamepad:** `GuiService.SelectedObject`, `GuiNavigationEnabled`, per-object `Selectable`/`NextSelection*`.
- `UserInputService`/`ContextActionService` exist (touch/gamepad/keyboard) **[member names unverified on fetched pages]**;
  new work favors the Input Action System.

## 8. Best practices

Scale over Offset; clamp with `UISizeConstraint`, lock proportions with `UIAspectRatioConstraint`; use
`CanvasGroup` to fade/tint a whole panel; flex sparingly; reuse component templates (clone a styled Frame +
layout objects); `TextScaled`+`UITextSizeConstraint` + contrast for legibility; `CoreUISafeInsets`; test on
devices. Frameworks: engine-native is the baseline; roblox-react / Fusion exist **[unverified — not in fetched UI docs]**.

## Sources
ui/{on-screen-containers,position-and-size,frames,labels,buttons,text-input,scrolling-frames,viewport-frames,
list-flex-layouts,grid-table-layouts,appearance-modifiers,size-modifiers,9-slice,rich-text},
production/publishing/adaptive-design, projects/cross-platform, classes/{SurfaceGui,BillboardGui,CanvasGroup,
VideoFrame,GuiService,TextLabel,ImageLabel,Decal,Texture}, enums/ScreenInsets.
