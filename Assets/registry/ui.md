# UI templates / prefabs — shared catalog

Reusable GUI prefabs (HUD panels, buttons, shop cards) across all games. See [README](README.md).

| Name | Path (repo / ReplicatedStorage) | Project(s) | Source | Notes |
|------|--------------------------------|------------|--------|-------|
| `Theme` | `roblox.jungle.game/lobby/sync/ReplicatedStorage/UI/Theme.luau` → `ReplicatedStorage.UI.Theme` | jungle (lobby) | Job #065 | **Tokens only, no instances** — colours, fonts, text scale, spacing, radii, strokes, tweens, plus the icon/sound/product-art id maps. The single place a hex value or asset id is written. Client **and** server safe. |
| `Components` | `…/UI/Components.luau` | jungle (lobby) | Job #065 | Builders consuming `Theme`, no game logic: `screen · icon · iconButton · button(4 variants/4 states) · chip · progressBar · panel(X + tap-outside) · row(+flashFail) · toast · confirm · burst · iconBar`. |
| `UISound` | `…/UI/UISound.luau` | jungle (lobby) | Job #065 | 2D interface cues by key; sounds cached, per-cue volumes, 60 ms debounce. World cues stay positional on their own part — do not route those here. |
| `UIBus` | `…/UI/UIBus.luau` | jungle (lobby) | Job #065 | Client-side BindableEvent bus for panel opens. `ReplicatedStorage.OpenPanel` is server→client only, so it cannot carry one client script's request to another's panel. |

> **Adopting these in the game place:** they are lobby-tree only by decision (Job #065 #7) so an unused
> copy can't drift. When the game place is restyled, copy them into `sync/ReplicatedStorage/UI/`
> **byte-identically** and keep the two in step, as with `RankDefs`/`ProfileConfig`.
>
> **Two traps they encode, worth reading before writing new Roblox UI:**
> `AutomaticSize` cannot measure children sized by scale or by a `UIAspectRatioConstraint` — and that
> constraint defaults to `DominantAxis.Width`, so a zero width silently collapses the height too.
> `Components.chip` measures `TextBounds` and sizes from a known height instead.
