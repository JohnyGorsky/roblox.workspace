# Shared asset registry (workspace)

The **single, cross-project catalog** of every asset we own/use — so we **reuse across all games**
(Defender, Jungle/Last River, future). Lives in the workspace (shared layer), not per game. One file per
asset type. See the `roblox-assets` skill for the full workflow (our-assets-first → present for approval
→ scan for scripts → store → **log here**).

## Rules
- **Grep this before sourcing anything new** — we may already own it.
- Every asset we add to any game gets a row here.
- `Project` column = which game(s) use it, or `shared` if reusable / `inventory` if owned-but-unused.
- Third-party inserts must be **script-scanned** before use.

## Files
- [models.md](models.md) · [meshes.md](meshes.md) · [images.md](images.md) · [audio.md](audio.md) ·
  [animations.md](animations.md) · [ui.md](ui.md)

## Row format
`| Name | rbxassetid / path | Type | Project(s) | Ours-created / Source | License | Stored at | Scanned? | Notes |`
