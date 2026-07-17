# Job #001: Workspace & multi-game project setup

**Project**: `roblox.workspace` (authoritative shared layer)
**Created**: 2026-07-17
**Status**: Requirements Gathering (intake)
**Scope**: `roblox.workspace` + conventions inherited by every game

## Goal

Stand up a clean, repeatable structure for developing multiple Roblox games (`roblox.defender`
today, `roblox.jungle` next, more later) from a single VS Code multi-root workspace, where:

- **`roblox.workspace`** holds the **authoritative, shared** layer — the skills, agents, workflows
  and ground rules that apply to *every* game (how we build GUIs, how we generate models, how we
  run jobs, and the division of labour between the human and Claude).
- **Each game folder** holds only what is specific to that game — its description/vision, its
  planned work, and its jobs.
- **All real work flows through *jobs*.** Nothing gets built ad-hoc; every change is a job with a
  fixed lifecycle so the intent, the plan, the result, and the release note are always on record.

## Confirmed environment facts (from setup investigation, 2026-07-17)

The three folders are **siblings** under `c:\Dati\Work\`, each its own git repo. We always open the
**multi-root workspace** (`roblox.workspace` is the primary dir). Verified empirically in this setup:

- ✅ **Skills** auto-load from the primary dir **and** from every game folder simultaneously.
- ✅ **Agents** auto-load the same way.
- ❌ **`CLAUDE.md`** loads **only** from the primary (workspace) dir — a game's `CLAUDE.md` does *not*
  auto-load in multi-root mode, and we can't force all games' CLAUDE.md on at once without conflict.
- ❌ **Workflows** and **`settings.json`** load only from the workspace (primary) dir.

**Consequences that shape the design:**
1. Per-game context must travel as a **skill** (skills load from game folders), not as `CLAUDE.md`.
   → each game gets a `<game>-project` skill holding its architecture/rules/standards.
2. Both games' skills are live at once → every game-specific skill must name its game in the
   description so the model self-selects the right one.
3. Shared/authoritative config lives in `roblox.workspace/.claude` because that's the one place that
   always loads.

## The structure we are establishing

### A. Workspace layer — `roblox.workspace/` (authoritative, shared by all games)

```
roblox.workspace/
  .claude/
    skills/            # shared, game-agnostic skills (engine knowledge, Studio utilities, …)
    agents/            # shared agents (generic dev + job driver, model/char generation)
    workflows/         # shared job / process workflows
    settings.json      # shared permissions + env
  GROUND-RULES.md      # authoritative ground rules: how we make GUIs, how we generate models,
                       # "what I (human) do vs what you (Claude) do", job discipline
  CLAUDE.md            # workspace overview + how the shared/per-game split works
  Jobs/                # workspace-level jobs (tooling/setup work like THIS one)
```

Candidate **shared skills/agents** (to be split out of Defender in this job):
- `roblox-dev` skill — generic Luau/engine knowledge only (Defender's project rules stripped out).
- `studio-diagnostics` skill — genericized Studio command-bar utilities.
- `roblox-chars` agent — generic Meshy.ai model generation + rigging technique.
- generic dev / job-driver agent — the workflow driver, minus Defender specifics.

### B. Per-game layer — `roblox.<game>/` (specific to one game)

```
roblox.<game>/
  .claude/
    skills/            # game-specific skills (content builders, design system, <game>-project)
    agents/            # game-specific agents
  <GAME>.md            # THE one description file — what the game is + current & planned mechanics
  CLAUDE.md            # kept for solo-open + documentation (mirrors the <game>-project skill)
  Planned/             # backlog: things we intend to turn into jobs (drafts, ideas, queued work)
  Jobs/                # the actual worked jobs (see lifecycle below)
```

Three mandatory per-game artifacts (as you specified):
1. **One description file** (`<GAME>.md`) — the game's vision: what it is, current mechanics,
   planned mechanics.
2. **`Planned/` folder** — where we park what we plan before it becomes a job.
3. **`Jobs/` folder** — where we do the work. *We only work through jobs.*

### C. Job lifecycle (every job, every game, and the workspace itself)

Each job is a numbered folder `Jobs/NNN/` progressing through fixed files.

**Every job must declare which project it targets** — `workspace`, `defender`, or `jungle`. This is
the first line of `intake.md` (a `**Project**:` field) and it is non-negotiable: it decides which
folder the job lives in, which skills/rules apply, and which codebase gets touched. A job never spans
more than one project; cross-cutting work is split into one job per project.

| Stage | File | Purpose |
|-------|------|---------|
| 1. Intake | `intake.md` | What we plan to do — the requirement/goal in plain terms. |
| 2. Plan | `implementation-plan.md` | Answer open questions, do investigations, decide the approach, and **list what is needed from the human**. |
| 3. Done — result | `final-summary.md` | What was actually implemented (files changed, incl. auto-sync vs manual-copy where relevant). |
| 4. Done — release | `changelog.md` | Short, **player-facing** release note (the "release file"). |

Rule: a job does not start implementation until its `implementation-plan.md` is agreed.

### D. Always-use skills / ground rules

Part of this job is to declare the **mandatory** skills and rules that must always be applied:
- Which shared skills are *always* consulted (e.g. `roblox-dev` before touching Luau/APIs;
  the GUI design skill before building any UI; the relevant `<game>-project` skill before game work).
- The authoritative **ground rules** in `GROUND-RULES.md`: GUI conventions, model-generation
  workflow, and the human/Claude division of labour.

## Scope of THIS job (001)

1. Create the `roblox.workspace/.claude` skeleton (`skills/`, `agents/`, `workflows/`, `settings.json`).
2. Write `roblox.workspace/CLAUDE.md` (workspace overview + split explanation) and
   `GROUND-RULES.md` (authoritative rules + human/Claude division of labour).
3. Migrate the clearly-generic pieces out of Defender into the workspace shared layer.
4. Split the "welded" skills (e.g. `roblox-dev`): generic half → shared; Defender-specific half →
   a new `defender-project` skill.
5. Establish the per-game layout in `roblox.defender` (description file, `Planned/`, `Jobs/` already
   present) and scaffold the same in `roblox.jungle` from the Defender template.
6. Provide a shared, **game-agnostic** job scaffolding tool (the current `job_manager.py` is
   Defender-specific; generalize it or replace it).
7. Declare the always-use skills and finalize the ground rules.

## Open questions (to resolve in `implementation-plan.md`)

- [ ] Description file name: `<GAME>.md` (e.g. `DEFENDER.md`) vs a fixed `GAME.md` vs `DESCRIPTION.md`?
- [ ] `Planned/` format — free-form notes, or one draft-intake file per planned item?
- [ ] Job tooling — generalize `job_manager.py` into the workspace, or go script-free / manual folders?
- [ ] Do we keep per-game `CLAUDE.md` in sync with the `<game>-project` skill, or make one the source
      of truth and generate the other?
- [ ] How far to genericize `studio-diagnostics` / `roblox-chars` now vs. later.
- [ ] Git: shared layer committed to the `roblox.workspace` repo (confirmed) — anything else?

## Checklist

- [ ] Requirements reviewed (this intake)
- [ ] Implementation plan created & agreed
- [ ] Workspace shared layer built
- [ ] Defender split done
- [ ] Jungle scaffolded
- [ ] Ground rules + always-use skills declared
- [ ] Final summary + changelog written
