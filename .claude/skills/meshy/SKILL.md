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

## Automate (Pro API + MCP)

The whole pipeline (prompt → 3D → remesh → texture → rig → animate → `download_model`) is scriptable via the
REST API (key `msy_…`, Pro 20 RPS/10 concurrent, poll or SSE/webhook) — and there's an **official MCP server**
(`@meshy-ai/meshy-mcp-server`, 24 tools) + **Agent Skill** (`meshy-3d-agent`). Install the Meshy MCP alongside
the Studio MCP and an agent can run generation headless, then hand the downloaded GLB/FBX to Studio for import
(the Bridge's "Send to Roblox" is the only non-API step — skippable). *Setting up the Meshy MCP is a candidate
follow-up job.*

## Credits & license
Pro = 1000 cr/mo (no rollover); a rigged+animated character ≈ 40–50 cr (preview 20 + refine 10 + rig 5 +
animations 3 each). **Pro grants a private/commercial license → safe to publish in Roblox** (don't prompt others' IP).
