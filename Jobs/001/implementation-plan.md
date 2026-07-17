# Implementation Plan — Job #001: Workspace & multi-game project setup

**Project**: `roblox.workspace`
**Created**: 2026-07-17
**Status**: Planning (awaiting go-ahead)

## Decisions locked (via wizard)

1. **Description file** → fixed **`GAME.md`** in each game root (predictable path for tooling).
2. **`Planned/` backlog** → **one draft file per item**; promoting an item = convert it into a new
   `Jobs/NNN/intake.md`.
3. **Job scaffolding** → **shared generic script** in the workspace, driven by a `--project` flag.
4. **Game context** → the **`<game>-project` skill is the source of truth**; each game's `CLAUDE.md`
   becomes a thin pointer to it.

## Analysis

- We always open the multi-root workspace, so only the workspace layer's `CLAUDE.md`/`settings.json`
  load, while skills + agents load from every folder. That's why game context lives in a skill and
  the shared layer lives in `roblox.workspace/.claude`.
- Several Defender assets are "welded" (generic + game-specific in one file) and must be split:
  - `roblox-dev` skill: keep generic engine knowledge shared; move Defender's "non-negotiable rules"
    and the `tools/luau-analyze.sh` gate into `defender-project`.
  - `roblox` agent: generic dev/job-driver → shared; Defender hooks → `defender-project`.
  - `studio-diagnostics` / `roblox-chars`: mostly generic → genericize, drop hardcoded Defender paths.
  - `roblox-gui` skill + `gui-builder` agent: **design system is per-game** (colors/fonts/tokens), so
    they stay in Defender; only the *technique* is shareable → defer full genericization.

## Target layout (end state)

```
roblox.workspace/
  .claude/
    skills/  roblox-dev (generic), studio-diagnostics (generic)
    agents/  roblox-dev (generic dev+job driver), roblox-chars (generic Meshy)
    settings.json                     # shared permissions + env
  tools/job.py                        # shared, game-agnostic job scaffolder (--project)
  GROUND-RULES.md                     # authoritative: GUI process, model-gen, human↔Claude split,
                                      #   job discipline, "always ask via the wizard" rule
  CLAUDE.md                           # workspace overview + shared/per-game split explanation
  Jobs/                               # workspace jobs (this one lives here)

roblox.defender/
  .claude/
    skills/  add-enemy, add-weapon, add-quest, add-consumable, game-balance,
             roblox-gui, defender-project (NEW, source of truth)
    agents/  gui-builder
  GAME.md                             # Defender vision: what it is + current & planned mechanics
  CLAUDE.md                           # thin pointer -> defender-project skill
  Planned/                            # one file per planned item
  Jobs/                               # existing job history stays

roblox.jungle/                        # scaffolded from the Defender template
  .claude/skills/  jungle-project (+ its own design/content skills as they're built)
  GAME.md
  CLAUDE.md                           # thin pointer -> jungle-project skill
  Planned/
  Jobs/
```

## Job scaffolder design (`roblox.workspace/tools/job.py`)

- `job.py new --project <workspace|defender|jungle> "Title" "Requirements"` → creates the next
  `Jobs/NNN/intake.md` **in that project's folder**, pre-filling the mandatory `**Project**:` field.
- `job.py new --project defender --from Planned/dash-ability.md` → promote a planned item to a job.
- `job.py plan NNN --project ...`, `job.py summary NNN ...`, `job.py release NNN ...` for later stages.
- Path resolution: workspace → `./Jobs`; defender/jungle → `../roblox.<game>/Jobs` (sibling repos).
- The auto-sync vs manual-copy table is **game-specific**, so those paths move into a small per-game
  config the script reads (workspace jobs skip the sync table entirely). Replaces the current
  Defender-only `job_manager.py`.

## Implementation steps (phased)

### Phase 1 — Workspace shared layer
1. Create `roblox.workspace/.claude/{skills,agents}` and `settings.json`.
2. Write `CLAUDE.md` (overview + split rules) and `GROUND-RULES.md` (incl. the wizard rule).
3. Build `tools/job.py` (generic scaffolder) and verify it creates a workspace + a game job correctly.

### Phase 2 — Defender split
4. Create `defender-project` skill = source of truth (architecture, sync rules, code standards,
   always-use directives — pulled from current `CLAUDE.md` + `roblox-dev` project rules).
5. Shrink `roblox.defender/CLAUDE.md` to a thin pointer to that skill.
6. Move generic `roblox-dev` / `studio-diagnostics` skills + `roblox-chars` / dev agent up to the
   workspace; leave game-specific skills/agents in Defender.
7. Add `roblox.defender/GAME.md` (vision) and `Planned/` (seed with any current backlog).

### Phase 3 — Jungle scaffold
8. Create `roblox.jungle/.claude/skills/jungle-project`, thin `CLAUDE.md`, `GAME.md`, `Planned/`, `Jobs/`
   from the Defender template so Jungle inherits the full shared toolkit on day one.

## What I need from you

- [ ] **Go-ahead** on this plan (and whether to do Phase 1 only first, or 1→3 in one pass).
- [ ] **Jungle concept** for its `GAME.md` — or I stub it and you fill it in later.
- [ ] **Git** — commit each repo as we complete its phase, or leave staging to you?
- [ ] Confirm it's fine to **move** (not copy) the generic skills out of Defender — after the move,
      opening Defender *solo* (not via the workspace) would no longer see the shared skills. You always
      use multi-root, so this should be fine, but it's a one-way trade worth confirming.

## Risks / notes

- Moving skills between separate git repos: history stays in Defender's repo (as deletions); new
  history starts in the workspace repo. Acceptable.
- Both games' skills load at once in multi-root — mitigated by each skill naming its game in the
  description. No code change needed, just discipline.

## Verification

- [ ] `job.py new --project workspace` and `--project defender` both create correct, Project-stamped intakes.
- [ ] After the Defender split, a fresh session in the multi-root workspace still surfaces all skills
      (shared + Defender) and the `defender-project` skill self-selects for Defender work.
- [ ] Jungle scaffold loads its `jungle-project` skill and shared skills with no Defender bleed-through.
