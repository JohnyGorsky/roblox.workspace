# Codex instructions for the Roblox workspace

This is the shared entry point for Codex sessions started in `roblox.workspace`.
The existing Claude instructions remain the project knowledge base. Read them as
instructions for the coding agent; do not assume Claude-specific tools or automatic
skill loading exist in Codex.

## Read at session start

1. Read [CLAUDE.md](CLAUDE.md) and [GROUND-RULES.md](GROUND-RULES.md).
2. Identify the project and place from the user's request and existing task records.
   An open Studio instance alone does not select a task or authorize game edits.
3. Read that project's `CLAUDE.md` and project skill below. Follow its required
   reading order, including handoff, pitfalls, relevant systems, and decisions.
4. Read shared and project `.claude/skills/<name>/SKILL.md` files relevant to the
   work, plus references they require. Read `.claude/agents/` instructions when
   using those specialties. Select by project, not just by a matching keyword.
5. Check the latest `Jobs/` intake, implementation plan, and summaries, then
   `Planned/`, `todo/`, and `findings/`. Reconcile stale handoffs with newer records
   and actual Studio state before saying what is implemented or what comes next.

## Project map

Paths are relative to this workspace. Each sibling is a separate repository.
`roblox.workspace.code-workspace` lists all six roots; the shorter list in
`CLAUDE.md` is historical (see workspace TODO 0001).

| Project | Claude entry point | Project skill |
|---|---|---|
| Workspace | [CLAUDE.md](CLAUDE.md) | Shared `.claude/skills/` |
| Defender | [CLAUDE.md](../roblox.defender/CLAUDE.md) | [defender-project](../roblox.defender/.claude/skills/defender-project/SKILL.md) |
| Jungle | [CLAUDE.md](../roblox.jungle.game/CLAUDE.md) | `jungle-project` is referenced but missing; see below |
| The Last Tide | [CLAUDE.md](../roblox.tide/CLAUDE.md) | [tide-project](../roblox.tide/.claude/skills/tide-project/SKILL.md) |
| ELEVATOR 13 | [CLAUDE.md](../roblox.13floors/CLAUDE.md) | [13floors-project](../roblox.13floors/.claude/skills/13floors-project/SKILL.md) |
| Magnet Sweep | [CLAUDE.md](../roblox.magnet-sweep/CLAUDE.md) | [magnet-sweep-project](../roblox.magnet-sweep/.claude/skills/magnet-sweep-project/SKILL.md) |

Jungle's referenced architecture skill was absent on 2026-09-13. Search again
before Jungle work. Its `CLAUDE.md`, `GAME.md`, `STYLEGUIDE.md`, `ASSETS.md`, and
[jungle-style](../roblox.jungle.game/.claude/skills/jungle-style/SKILL.md) provide
available context; do not claim the missing skill was loaded.

This file does not automatically cover a session started directly in a sibling
repository. Such a session must also read this shared entry point and ground rules.

## Working agreements

- Follow system/developer instructions and the user's current authorization.
  Among repository documents, `GROUND-RULES.md` governs workflow; current accepted
  decisions govern design. Historical skill summaries do not undo later decisions.
- Never stage for a commit, commit, or push. The user handles version control.
  A job plan saying "commit" does not override this standing rule.
- Every change belongs to a job in its owning project. Keep the intake, plan,
  final summary, and changelog. Honor agreement already recorded in the session;
  do not re-ask settled design questions. Stay within the authorized place/system.
- Every job gets an independent reviewer given the requirement and repository,
  without the implementer's theory. After one failed fix, get fresh eyes before
  another attempt; after two failures, reopen the diagnosis.
- Use available Codex question tools for necessary decisions. Claude's
  `AskUserQuestion`, `Skill`, and `Task` names are workflow references, not tools
  to pretend are available. Claude permission settings do not grant Codex access.
- Use live Roblox Studio MCP when available. List instances and use an explicit
  `studio_id`; establish the intended place before modifying it. Inspect before
  claiming implementation state. The agent runs functional tests through MCP.
- Verify player-visible changes in Play at the player's camera. Keep matching
  before/after captures, read back changes, and state a check's failure condition.
  `IMPLEMENTED` is not `VERIFIED`. Stop play sessions you started.
- Measure mobile layouts in the Device Emulator, with authorization to change the
  user's Studio device mode. Do not replace measurement with reasoning.
- Run the game's analyzer after Luau edits and before playtests. Baseline files
  outside the repo need absolute paths because analyzer wrappers change directory.
- Follow the asset order in ground rules: own registry/inventory, then Creator
  Store; present requests/candidates in a table and honor asset approvals. Scan
  inserted assets for scripts before Play and update the shared asset registry.
  Leave missing slots empty and observable; do not invent placeholder assets.

## Corrections that must travel with the older instructions

- [Finding 0003](findings/0003-never-create-or-delete-directories-insid.md): Sync
  deletion works in both directions. Preserve mapped service directories and
  `.gitkeep` files; never recursively clean directories in a sync root. Magnet
  Sweep PITFALLS 11b clarifies that content subfolders within services are allowed.
  Verify propagation after a restart; existing scripts alone do not prove sync.
- [Finding 0002](findings/0002-roblox-animation-skill-states-two-engine.md) corrects
  stale animation priority and NPC playback instructions in the shared skill.
  Consult that correction and current official engine references before use.
- [Finding 0001](findings/0001-camera-release-after-screen-capture-used.md) corrects
  Edit-camera release: `Fixed`, followed by a separate read-back. Do not copy the
  old unconditional `Custom` advice from diagnostics or terrain instructions.
- Follow each game's latest verified sync layout and central configuration when
  older content templates disagree. Do not transplant another game's layout.
- For Magnet Sweep, decisions 0020-0025 supersede older generated-room, guardian,
  refresh, and ownership summaries. Rooms remain editor-placed and hand-editable;
  runtime contents use markers. Never regenerate a room over the user's edits.

## Restart recovery

The 2026-09-13 recovery is recorded in [Jobs/014/resume.md](Jobs/014/resume.md).
It identifies Magnet Sweep job 023 and records Studio state ahead of both the
old handoff and Git. Treat it as a dated snapshot, then inspect current records
and Studio again. Do not promote an Edit inspection into gameplay verification.
