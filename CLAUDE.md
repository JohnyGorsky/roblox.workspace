# CLAUDE.md — Roblox multi-game workspace

Authoritative guidance for Claude Code across all Roblox games developed here.

## What this workspace is

A VS Code **multi-root workspace** holding several sibling Roblox game repos plus this shared,
**authoritative** layer:

- **`roblox.workspace/`** (this repo) — shared skills, agents, tooling, and **ground rules** that
  apply to *every* game. The single source of truth for how we work.
- **`roblox.defender/`** — the Roblox Defender game (its own repo).
- **`roblox.jungle/`** — the Roblox Jungle game (its own repo).

Always work with the multi-root workspace open (`roblox.workspace.code-workspace`), with
`roblox.workspace` as the primary directory.

## How configuration loads (important)

The game folders are **siblings** of this one, each its own git repo. Verified behavior when the
multi-root workspace is open:

- ✅ **Skills** and **agents** load from *this* layer **and** from every game folder at once.
- ❌ **`CLAUDE.md`** and **`settings.json`** load **only** from this workspace (primary) dir — a
  game's own `CLAUDE.md` does **not** auto-load.

Consequences (do not fight these):

1. **Per-game context lives in a `<game>-project` skill**, not in the game's `CLAUDE.md`. That skill
   is the **source of truth** for the game's architecture, rules, and standards; the game's
   `CLAUDE.md` is a thin pointer to it. Read the `<game>-project` skill before doing game work.
2. **Every game-specific skill names its game** in its description, because all games' skills are
   live simultaneously. Pick the skill that matches the project you're working on.
3. Shared config (permissions, ground rules, tooling) lives here because this is the layer that
   always loads.

## Ground rules

Read **[GROUND-RULES.md](GROUND-RULES.md)** — it is authoritative and covers how we build GUIs, how
we generate models/assets, the human↔Claude division of labour, job discipline, and the
never-commit / always-ask-via-wizard rules. When a ground rule and anything else conflict, the
ground rule wins.

## Jobs — the only way we work

All real work flows through **jobs**. Never build ad-hoc.

- Every job declares its target **project** (`workspace`, `defender`, or `jungle`) on the first line
  of its `intake.md`. A job never spans two projects.
- Job lifecycle: `intake.md` → `implementation-plan.md` → (`final-summary.md` + `changelog.md`).
- Scaffold jobs with the shared tool: `python tools/job.py new --project <name> "Title" "Requirements"`.
- Each game keeps its own `Jobs/` (worked jobs) and `Planned/` (one file per queued idea). Promoting
  a planned item = turn it into a new job intake.

## Shared skills & agents (this layer)

- **`roblox-dev`** skill — generic Luau/Roblox engine knowledge (official Creator Docs). Consult it
  before writing/reviewing any Luau or reasoning about Roblox APIs.
- **`studio-diagnostics`** skill — generic Studio Command Bar export/diagnose/fix scripts.
- **`roblox-chars`** agent — generic Meshy.ai model generation, rigging, and import technique.
- **`roblox`** agent — generic Roblox dev + job-workflow driver.

Game-specific skills/agents (content builders, design systems, `<game>-project`) live in each game's
own `.claude/`.
