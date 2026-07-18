# Meshy.ai for Roblox — reference

Sourced from docs.meshy.ai / meshy.ai / help center / GitHub, current 2026-07. Not-verified items flagged
**[unverified]**. Current model line: **Meshy 6** (2025) + **Smart Topology** (2026 game-dev mode); Meshy 5 legacy.
User has **Pro** ($20/mo, 1000 credits/mo, 10 concurrent, 20 RPS, unlimited downloads, **private/commercial
license**, API + DCC Bridge + MCP + Agent Skill).

## Best inputs (the key choices)

- **`ai_model`:** `meshy-6`/`latest` (cleaner topology — use this), not `meshy-5`.
- **`model_type` / topology mode:** **`smart-topology`** = the game/real-time mode (clean quad edge loops,
  auto-retopo, target **100–15,000 faces**) → **prefer for Roblox**. `lowpoly` = faceted (only when that's the
  *style*). `standard` = heavy hero props only.
- **`topology`:** `quad` (if you'll rig/edit — needed for clean deformation) vs `triangle` (engine-direct).
- **`target_polycount`** (default 30k). Roblox budgets: **props 1K–3K tris, characters 5K–10K tris**.
- **`enable_pbr`** (metallic/roughness/normal), **`hd_texture`** (4K base/2K PBR — meshy-6), **`texture_prompt`**,
  **`pose_mode`** (`a-pose`/`t-pose` — set for clean rigging).
- ⚠️ **`art_style` & `symmetry_mode` are DEPRECATED in meshy-6** — steer style via the **prompt text** and add
  "symmetrical"/"bilateral symmetry" when needed (old guides are stale on this).

**Prompt best practices (text-to-3D):** specific, **3–5 strong descriptors** (object/shape/posture/color/
material/style); **one focal subject** (compose scenes in Roblox); **avoid plurals** (extra/fused limbs);
**state topology** ("two arms, four legs"); request an **A/T-pose** for characters.
**Image-to-3D:** single clean subject on neutral background; `remove_lighting=true` (keep — let Roblox light
it); **Multi-Image-to-3D** (front/side/back) when one view is ambiguous.

## Pipeline

Text-to-3D is two-stage: **Preview** (`mode:preview`) → **Refine** (`mode:refine`, `preview_task_id`).
**Remesh** (5 cr) = auto retopology + fresh UVs to a target polycount (do this before exporting). **Retexture**
(10 cr) re-textures an existing model from a new prompt/image. **Order: Generate → Remesh → Texture** (compact
files, under 20 MB).

## Rigging & animation

**Auto-Rig requirements:** a **textured humanoid biped**, clear limbs, **face +Z**, feet grounded, centered;
**T-pose best for rigging** (A-pose = better shoulders); ≤300k faces via `input_task_id`; ~30s. Skeletons:
Humanoid (widest anim coverage) / Quadruped / Custom. Output: `rigged_character_fbx_url`/`glb_url`.
**Animation library:** ~500+ motions (marketed "600+"), reference by **`action_id`** (range **0–696**), up to
**10 clips/task**, **3 cr each**. Meshy produces a **standard glTF/FBX humanoid skeleton — NOT native Roblox
R15 Motor6D**; Roblox ingests it as a **skinned MeshPart with bones**. **[unverified]** exact bone→R15 joint map.

## Export & Roblox fit

- **GLB** = preferred (single file, textures+scale; what the Bridge uses). **FBX** = rigged/animated assets for
  Studio's Animation Editor. OBJ = static only.
- **Roblox 3D Importer:** right-click Workspace → **Import 3D** (or Asset Manager bulk). Imports as **MeshPart**;
  skinned brings **bones** (max **4 bones/vertex**). Fix TextureID, add **SurfaceAppearance** for full PBR.
- **Constraints:** tris ≤10k (batch) / ≤21k (single) per mesh; textures **≤1024²**, **one material/mesh**;
  **scale 1 stud ≈ 0.28 m**, model **faces +Z / up +Y**, **freeze transforms** (scale 1, rot 0); file **<20 MB**.
- **Roblox DCC Bridge (headline feature):** **"Send to Roblox"** — one-time OAuth, then one-click pushes the
  model **as GLB to Creator Hub** (textures/scale preserved) → appears in Studio **Toolbox → Inventory → My
  Packages**. No download/FBX/broken-texture hassle. Meshy = "only AI 3D tool with a native Roblox Bridge".
- **Animations onto a Roblox rig:** import the skinned FBX/GLB into the Animation Editor; to drive **native R15**
  use **Adaptive Animation / HumanoidRigDescription** retargeting (expect **manual joint mapping** for custom
  skinned chars). Use `studio-diagnostics` Meshy fix scripts (HipHeight, Motor6D reparent/offsets, PrimaryPart,
  anchoring) + `roblox-animation`.

## API & automation

Async REST; **API key** `msy_...` (Pro+), Bearer auth. **Pro: 20 RPS, 10 concurrent.** Endpoints:
`POST /openapi/v2/text-to-3d`, `POST /openapi/v1/image-to-3d`, multi-image, remesh, retexture,
`POST /openapi/v1/rigging`, `POST /openapi/v1/animations` (`action_id`s); `GET /:id` (poll:
**PENDING→IN_PROGRESS→SUCCEEDED/FAILED**, `progress` 0–100) or **SSE `/:id/stream`** or **webhooks**;
**failed tasks refund credits.** Official **Python/Node SDKs** + **API Playground**.
- **Official MCP server:** `@meshy-ai/meshy-mcp-server` — `npx add-mcp @meshy-ai/meshy-mcp-server --env
  MESHY_API_KEY=msy_...` (auto-detects Claude Code). **24 tools** (`text_to_3d`, `image_to_3d`, `remesh`,
  `retexture`, `rig`, `animate`, `convert`, `get_task_status`, `download_model`, `check_balance`, …).
- **Official Agent Skill:** `meshy-3d-agent` (`npx skills add meshy-dev/meshy-3d-agent`) — generate→poll→download
  workflows, calls REST directly. Agent docs: `docs.meshy.ai/llms.txt` / `llms-full.txt`.
- **Fully automatable:** prompt → 3D → remesh → texture → rig → animate → `download_model`. **Only the Bridge
  "Send to Roblox" isn't in the API** — skip it by importing the downloaded GLB/FBX (e.g. via the Studio MCP).

## Credits (docs) & licensing

T2D preview: meshy-6/lowpoly **20**, smart-topology **5**; refine **10**. I2D: meshy-6 **20/30** (no-tex/tex),
smart **5/15**. Remesh **5**, retexture **10**, rig **5**, animate **3**, convert/resize **1**. Pro **1000
cr/mo, no rollover** (~a rigged+animated character run ≈ 40–50 cr). **License:** Free = CC-BY-4.0 (attribution);
**Pro = private/commercial license → safe to publish in Roblox** (you still can't prompt others' IP; Roblox
moderation applies on upload).

## Sources
docs.meshy.ai/{en, api/*, llms.txt}, meshy.ai/{pricing, api, integrations, use-cases/.../roblox-developers,
tutorials/*}, help.meshy.ai (prompts, credits), github.com/meshy-dev/meshy-mcp-server.
