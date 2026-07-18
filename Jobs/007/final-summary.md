# Final Summary — Job #007: Shared asset registry (move + populate)

**Project**: `roblox.workspace`
**Completed**: 2026-07-18
**Status**: ✅ Completed (seed populated; expandable)

## What was done

- **Moved the asset registry to a single SHARED workspace catalog:** `roblox.workspace/Assets/registry/`
  (README + models/meshes/images/audio/animations/ui), with a **Project** column so it serves all games
  and we reuse across projects. Removed the per-game Jungle copy.
- **Repointed** the `roblox-assets` skill (guide + description) and `GROUND-RULES.md §4` to the shared registry.
- **Populated from our Roblox inventory** via the Studio MCP (`search_asset` scope `user`), account
  `johnygorsky10` (userId 5025640608):
  - **Models 20, Meshes 20, Audio 20, Images 20, Animations 20** (Decals: 0). All **our own uploads**
    (owned; no third-party scan needed). All are **Roblox Defender** assets (knight/skeleton/zombie/dragon/
    golem, potions, armor, mob SFX + anims, Meshy meshes/textures) — tagged `defender`.

## Important limitation

`search_asset` returns **≤20 results per type with no pagination**, so this is the **first 20 per type** —
the inventory almost certainly has more (Defender is mature). Expand by keyword searches (e.g. `search_asset`
with a query like "dragon", "potion", "armor") to surface the rest. Generic-named meshes (`Mesh_0`,
`Mesh1.0`) and PBR textures (`Material_*`) need identifying/renaming to be reusably searchable.

## Notes / next

- **No Jungle/Last River assets yet** — the boat, crocodiles, jungle props, etc. get logged here as we
  create them (Meshy) per the asset workflow.
- Not committed (per rule).
- Files: `roblox.workspace/Assets/registry/*` (new/moved); `.claude/skills/roblox-assets/SKILL.md`,
  `GROUND-RULES.md` (§4) edited; `roblox.jungle/assets/registry/` removed.
