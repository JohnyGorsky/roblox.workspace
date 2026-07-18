# GROUND-RULES.md — authoritative rules for the Roblox workspace

These rules are **authoritative** and apply to every game and every job. When a ground rule
conflicts with anything else, the ground rule wins. Claude must follow these without being reminded.

## 1. Standing rules (non-negotiable)

- **Claude never commits.** Claude makes file changes only; the **user is the only one who commits**
  (and pushes). Never run `git commit`/`git push`, never stage with intent to commit, even if a task
  seems to imply it.
- **Always ask via the wizard.** When Claude needs a decision or clarification, ask through the
  interactive **AskUserQuestion** interface — not as a plain-text list of questions.
- **Job-first, always.** Every change starts as an explicit job — even small ones. No ad-hoc
  changes. Describe the work, I open the job (`intake`), and we proceed through the lifecycle. See §5.
- **Every job declares its project** (`workspace` / `defender` / `jungle`) and touches only that one.

## 2. Human ↔ Claude division of labour

**Claude does (in code / on disk, and now in Studio directly via the Roblox Studio MCP):**
- Write and edit Luau, module structure, definitions, and configuration.
- Scaffold and maintain jobs (intake → plan → summary → changelog).
- **Drive the live Studio session via MCP** — read the tree (`search_game_tree`/`inspect_instance`),
  read/edit scripts, run Luau (`execute_luau`), read console output, trigger playtests, capture the
  viewport. This replaces most Command Bar handoffs.
- Generate Meshy.ai prompts + rigging/export checklists.
- Consult the knowledge skills before guessing at APIs, balance, or design.
- **Script *procedural* terrain only** (via the `roblox-terrain` skill) — compute the geometry, never
  eyeball it, and **verify by voxel read-back + screenshot**. Hand-sculpting hero terrain is not Claude's job.

**Human does (in Roblox Studio / external tools):**
- **Hand-sculpt hero/handcrafted terrain** (rivers, islands, set-pieces) with Studio's terrain tools —
  faster and better-looking than scripting it. Claude codes gameplay against what you build.
- Keep **Studio open with the target place loaded** (MCP has no connectivity otherwise), and choose
  which place is active.
- Press **Play** and judge gameplay *feel* — the human is still the one who decides if it's fun/right.
- Import Meshy.ai models, publish animations, and supply asset IDs.
- Source icons/sounds and provide their IDs.
- Review diffs and **commit**.

When work needs a human action, Claude states it explicitly and waits — it does not pretend a
Studio-side step is done.

> **Studio MCP is live** (workspace Job 002, 2026-07-17). Registered via committed
> `roblox.workspace/.mcp.json`. Claude works in Studio directly; MCP writes execute arbitrary Luau in
> the open place, so Claude Code's tool-permission prompts gate them — Claude still describes any
> non-trivial or hard-to-reverse Studio change before applying it. **Always verify terrain/scene edits**
> by reading them back (`Terrain:ReadVoxels` / `inspect_instance`) **and** `screen_capture` before
> reporting done — never assume a `Fill`/edit worked. The Command Bar `studio-diagnostics` flow remains
> the **fallback** when MCP isn't connected (Studio closed, or exports too big for a tool call).

## 3. Building GUIs

- Each game owns its **design system** (colors, fonts, sizes, tokens) as a per-game skill (e.g.
  Defender's `roblox-gui`). Build UI to that game's system — never invent ad-hoc styling.
- Use the game's GUI builder agent/skill where one exists.
- New GUIs match the existing look of that game; if a token is missing, ask (via the wizard) rather
  than guessing brand values.

## 4. Generating models & assets

- **3D models / characters / enemies** — Meshy.ai text-to-3D:
  https://www.meshy.ai/workspace?model-tab=text-to-3d — use the `roblox-chars` agent for generation
  settings, prompt templates, rigging, export, and import fixes.
- **Icons** (UI, items) — Flaticon: https://www.flaticon.com/search?word=sword
- **Sound effects** — Pixabay: https://pixabay.com/sound-effects/search/purchase/
- Claude produces prompts/checklists and the integration code; the **human** does the actual
  generation, publishing, and import in Studio, then supplies IDs.

**Claude can also source assets directly via the Studio MCP — always present candidates for approval
before using them:**
- **Creator Store search** (`search_asset`) — find existing **models, meshes, images/decals, and
  audio** already on Roblox (free or paid), then `insert_asset`. Good for props, kits, SFX, music.
- **AI generation in Studio** — `generate_mesh`, `generate_material`, `generate_procedural_model`.
- **Upload** — `upload_image`/`store_image` for images the human made (e.g. **ChatGPT-generated art**,
  **Flaticon** icons) — hand Claude the file/ID and Claude wires it in.
- Human-preferred external sources stay: **Pixabay** (sound), **Flaticon** (icons), **ChatGPT (paid)**
  for design/art, **Meshy.ai** for custom 3D. Claude proposes → **human approves** → Claude integrates.
  Respect each source's license/attribution; Roblox moderates uploaded images/audio.

**Asset policy (mandatory — full workflow in the `roblox-assets` skill):**
- **Our assets first.** Search our own inventory + the game's **asset registry** before any public search.
- **Present before use.** Claude shows candidate assets (name/id/type/source/license) and **only uses one
  after the human approves it** — never insert into the live game or use an asset unverified.
- **Scan every inserted asset for scripts and delete any not needed.** Inserted Models can hide backdoor
  `Script`/`LocalScript`/`ModuleScript`s — scan (`GetDescendants` → `IsA("LuaSourceContainer")`) in
  isolation, delete anything Claude didn't author, and **never Play before scanning**.
- **Maintain the asset registry** — each game's `Assets/registry/` (markdown per asset type) lists what we
  created vs used, with ids/source/license/location, so we reuse before re-sourcing.

## 5. Job discipline

- Lifecycle: `intake.md` (what we plan) → `implementation-plan.md` (investigate, answer questions,
  list what's needed from the human, agree the approach) → implement → `final-summary.md` (what was
  implemented) + `changelog.md` (short, player-facing release note).
- **Implementation does not start until the implementation plan is agreed.**
- Scaffold with `python tools/job.py new --project <name> "Title" "Requirements"`.
- `changelog.md` is player-facing marketing copy (3–6 short bullets, one emoji per line, no code/file
  names). The technical detail lives in `final-summary.md`.

## 6. Always-use skills

Before doing the matching work, Claude **must** consult the relevant skill rather than guessing:

- Any Luau / Roblox API / security / performance question → **`roblox-dev`** skill.
- Working inside a game → that game's **`<game>-project`** skill (architecture, sync rules, standards).
- Building/restyling UI → that game's GUI design skill.
- Adding content (enemy/weapon/quest/consumable) → that game's matching content skill.
- Setting or checking stats → that game's balance skill.
- Inspecting/fixing the live Studio session → **`studio-diagnostics`** skill.
- Meshy.ai model work → **`roblox-chars`** agent.
