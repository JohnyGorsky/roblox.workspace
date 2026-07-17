# GROUND-RULES.md — authoritative rules for the Roblox workspace

These rules are **authoritative** and apply to every game and every job. When a ground rule
conflicts with anything else, the ground rule wins. Claude must follow these without being reminded.

## 1. Standing rules (non-negotiable)

- **Claude never commits.** Claude makes file changes only; the **user is the only one who commits**
  (and pushes). Never run `git commit`/`git push`, never stage with intent to commit, even if a task
  seems to imply it.
- **Always ask via the wizard.** When Claude needs a decision or clarification, ask through the
  interactive **AskUserQuestion** interface — not as a plain-text list of questions.
- **We only work through jobs.** No ad-hoc changes. See §5.
- **Every job declares its project** (`workspace` / `defender` / `jungle`) and touches only that one.

## 2. Human ↔ Claude division of labour

**Claude does (in code / on disk):**
- Write and edit Luau, module structure, definitions, and configuration.
- Scaffold and maintain jobs (intake → plan → summary → changelog).
- Produce Studio Command Bar scripts (export/diagnose/fix) for the human to paste.
- Generate Meshy.ai prompts + rigging/export checklists.
- Consult the knowledge skills before guessing at APIs, balance, or design.

**Human does (in Roblox Studio / external tools):**
- Run Studio, press Play, and observe in-game behavior (Claude has no runtime).
- Paste Command Bar scripts and report the Output back.
- Import Meshy.ai models, publish animations, and supply asset IDs.
- Do the manual **Studio copies** for services that don't auto-sync.
- Source icons/sounds and provide their IDs.
- Review diffs and **commit**.

When work needs a human action, Claude states it explicitly and waits — it does not pretend a
Studio-side step is done.

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
