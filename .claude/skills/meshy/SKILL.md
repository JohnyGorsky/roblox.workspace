---
name: meshy
description: Meshy.ai 3D-asset generation for Roblox in this workspace (user has the Pro plan) — best prompt/settings inputs for game-ready meshes, the generate→remesh→texture pipeline, auto-rigging & the animation library, exporting to Roblox (GLB/FBX, 3D Importer, the DCC "Send to Roblox" Bridge, scale/tri budgets), and API/MCP automation of the whole pipeline. Use when generating models/characters/props via Meshy, rigging/animating them, or automating asset creation. Pairs with the roblox-chars agent (import/rig cleanup) and roblox-assets (registry/scan).
---

# Meshy.ai for Roblox

Full detail in [reference/meshy.md](reference/meshy.md). This is the working guide. Current authoritative Meshy
reference — the older settings in the `roblox-chars` agent defer to this.

## Best settings for game-ready Roblox assets

- **`ai_model: meshy-6`** (or `latest`) + **`model_type: smart-topology`** (clean quad loops, 100–15k faces).
  `lowpoly` only when faceted is the intended *style*.
- **`topology: quad`** for characters you'll rig; `triangle` for engine-direct static props.
- **`target_polycount`** to the Roblox budget: **props 1–3K tris, characters 5–10K tris**. `enable_pbr` on.
- ⚠️ **`art_style`/`symmetry` are deprecated in meshy-6** — steer via **prompt text** (+ "symmetrical").
- **Prompt:** specific, 3–5 descriptors, **one subject**, no plurals, **state limbs**, request **T-pose** for characters.

## Pipeline

**Generate → Remesh (retopo+UV) → Texture** (keep <20 MB). Text-to-3D = Preview then Refine. Retexture reuses geometry.

## Rig & animate

Auto-rig needs a **textured humanoid biped, facing +Z, feet grounded, T-pose**. Output is a **skinned glTF/FBX
(bones) — NOT native R15**. Add animations from the library by `action_id` (3 cr each, ≤10/task).

## Into Roblox

- **Preferred: the DCC Bridge "Send to Roblox"** (one-click GLB → Creator Hub → Toolbox → My Packages, textures
  preserved). Or download GLB/FBX and **Import 3D** in Studio (MeshPart + bones, ≤4 bones/vertex).
- **Check on import:** scale (**1 stud ≈ 0.28 m**), **+Z facing**, freeze transforms, TextureID/SurfaceAppearance,
  tri budget, textures ≤1024². A skinned char imports as a **custom rig** — use `studio-diagnostics` fix scripts +
  `roblox-animation` (Adaptive Animation / HumanoidRigDescription) to get it moving as a Humanoid.
- **Then:** run the mandatory asset **security scan** and **log it in the shared asset registry** (`roblox-assets`).

## The Meshy MCP — connected (`roblox.workspace/.mcp.json`)

Registered in the committed `roblox.workspace/.mcp.json` as server **`meshy`**:
`npx -y @meshy-ai/meshy-mcp-server` with `MESHY_API_KEY` in its `env` (the key is stored there — the repo is
private, single-owner). Needs **Node/npx** (v20 present). **Activate:** restart Claude Code → **approve** the
project-scoped MCP server → verify with `/mcp` or `claude mcp list` ("meshy ✓"). First launch runs `npx` which
downloads the package (brief). Alt (per-machine, off-git):
`claude mcp add --transport stdio --scope user --env MESHY_API_KEY=<key> meshy -- npx -y @meshy-ai/meshy-mcp-server`.
- **Webhooks NOT needed** — the MCP **polls** (`get_task_status`) / SSE-streams; webhooks only matter for a
  server *you* host. Leave Meshy's Webhooks section empty.
- **Gotcha (hit on first setup):** if it won't start with `Cannot find module './db.json'` / MODULE_NOT_FOUND
  (a corrupted npx cache, not Meshy), fix it: `npm cache clean --force` + delete `%LOCALAPPDATA%\npm-cache\_npx`,
  then reload Claude Code. Verified working: key validated, 24 tools registered.
- If the key ever leaks (it's in git history + our chat), rotate it in Meshy → Settings → API and update `.mcp.json`.

## Using the MCP (24 tools) — headless pipeline

`text_to_3d` / `image_to_3d` / `multi_image_to_3d` → poll **`get_task_status`** (or `wait_job_finished`) →
`remesh` → `retexture` → `rig` → `animate` (pick `action_id`s) → **`download_model`** (GLB/FBX) → import into
Studio via the **Studio MCP** (`insert_asset`/`execute_luau`). The DCC "Send to Roblox" is the only non-API
step and it's skippable. Also: `convert`, `resize`, `uv_unwrap`, `list_tasks`, `cancel_task`, **`check_balance`**,
`list_models`, `text_to_image`/`image_to_image`. An agent (e.g. `roblox-chars`) can drive the whole chain.
- The MCP server **enforces cost confirmation** — always present the credits + plan and get the user's OK
  before any generation tool (matches our present-before-use asset policy). Decide **`target_formats`** (e.g.
  `glb`/`fbx` for Roblox) at creation time — it can't be changed after. `check_balance` is free.

## Credits (this account)

~**1,440** available (**830 monthly + 610 permanent**); monthly resets, no rollover. Budget: a rigged+animated
character ≈ **40–50 cr** (preview 20 + refine 10 + rig 5 + animations 3 ea); a textured prop ≈ 15–30 cr. Run
`check_balance` before big batches; **failed tasks refund credits**.

## Credits & license
Pro = 1000 cr/mo (no rollover); a rigged+animated character ≈ 40–50 cr (preview 20 + refine 10 + rig 5 +
animations 3 each). **Pro grants a private/commercial license → safe to publish in Roblox** (don't prompt others' IP).
