# Final Summary — Job #001: Workspace & multi-game project setup

**Project**: `roblox.workspace`
**Completed**: 2026-07-17
**Status**: ✅ Completed (all 3 phases)

## What was implemented

Stood up the authoritative shared layer and the per-game convention, split the "welded" Defender
assets, and scaffolded Jungle. Everything loads correctly in the multi-root workspace.

### Phase 1 — Workspace shared layer (`roblox.workspace`)
- `.claude/settings.json` — shared permissions; **denies `git commit`/`git push`** (never-commit rule).
- `CLAUDE.md` — workspace overview + how config loads across the multi-root (skills/agents load from
  all folders; CLAUDE.md/settings only from the workspace).
- `GROUND-RULES.md` — authoritative rules: never-commit, always-ask-via-wizard, human↔Claude division
  of labour, GUI conventions, model/asset generation, job discipline, always-use skills.
- `tools/job.py` — game-agnostic job scaffolder driven by `--project`; resolves the target repo,
  stamps the mandatory **Project** field, and uses each game's `.jobconfig.json` for the sync table.
  Smoke-tested against workspace, defender, and jungle.

### Phase 2 — Defender split (`roblox.defender`)
- **Moved to shared** (now in `roblox.workspace/.claude`): `roblox-dev` skill, `studio-diagnostics`
  skill, `roblox-chars` agent, `roblox` agent — all genericized (game-specific paths/rules removed).
- **New `defender-project` skill** = source of truth: architecture, sync table, file map, code
  standards, the `tools/luau-analyze.sh` command, non-negotiable rules, content-skill index.
- `CLAUDE.md` shrunk to a thin pointer to that skill.
- `.jobconfig.json` — Defender's verified auto-sync vs manual-copy paths.
- `GAME.md` (first-draft vision, has TODOs to refine) + `Planned/README.md` (backlog convention).
- **Left in place** (correctly game-specific): `add-enemy`, `add-weapon`, `add-quest`,
  `add-consumable`, `game-balance`, `roblox-gui` skills; `gui-builder` agent.

### Phase 3 — Jungle scaffold (`roblox.jungle`)
- `.claude/skills/jungle-project/SKILL.md` (stub mirroring defender-project), thin `CLAUDE.md`,
  `GAME.md` stub, `Planned/README.md`, `.jobconfig.json` stub (Roblox defaults, marked to verify),
  and an empty `Jobs/`.

## Files changed

### roblox.workspace (new)
- `.claude/settings.json`, `CLAUDE.md`, `GROUND-RULES.md`, `tools/job.py`
- `.claude/skills/roblox-dev/**`, `.claude/skills/studio-diagnostics/**` (moved in + genericized)
- `.claude/agents/roblox.md`, `.claude/agents/roblox-chars.md` (moved in + genericized)
- `Jobs/001/*` (this job)

### roblox.defender
- **Removed** (moved to workspace): `.claude/skills/roblox-dev/`, `.claude/skills/studio-diagnostics/`,
  `.claude/agents/roblox.md`, `.claude/agents/roblox-chars.md`
- **Added**: `.claude/skills/defender-project/SKILL.md`, `.jobconfig.json`, `GAME.md`, `Planned/README.md`
- **Edited**: `CLAUDE.md` (now a thin pointer)

### roblox.jungle (new)
- `.claude/skills/jungle-project/SKILL.md`, `CLAUDE.md`, `GAME.md`, `.jobconfig.json`,
  `Planned/README.md`, `Jobs/.gitkeep`

## Notes / follow-ups

- **Not committed** — per the standing rule, all changes are left in the working trees of all three
  repos for the user to review and commit.
- `job_manager.py` / `job.py` still exist in `roblox.defender` (the old Defender-only tool). Left
  untouched; can be removed in a follow-up job now that the shared `tools/job.py` supersedes it.
- `GAME.md` (Defender) and all Jungle stubs contain TODOs to fill in.
- GUI genericization deferred: the design system stays per-game; only the technique is shareable.

## Verification

- [x] `job.py` creates Project-stamped intakes for workspace/defender/jungle (tested, cleaned up).
- [x] `job.py summary` categorizes files via each game's `.jobconfig.json` (tested on jungle).
- [x] New skills surfaced by the loader mid-session (`defender-project`, updated `roblox-dev`,
      genericized `studio-diagnostics` all appeared).
- [x] Full structure verified across all three repos.
- [ ] User confirms a fresh multi-root session loads shared + per-game skills with no bleed-through.
