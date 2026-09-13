# Job 014: Codex instruction bridge and task recovery

**Project:** `roblox.workspace`
**Created:** 2026-09-13
**Status:** Complete - documentation reviewed and verified, 2026-09-13

## Request

Read all Claude instructions, create Codex instructions if needed, and identify the next task after a restart.

## Scope

- Read the shared instructions and each sibling project's Claude instruction files.
- Add a workspace `AGENTS.md` that routes Codex to the existing sources and records relevant corrections.
- Identify the Magnet Sweep resume point from job records, accepted decisions, Git history, and read-only Studio inspection.
- Record the result in this workspace job. No gameplay changes, commits, publishing, or changes to sibling repositories.

## Authorization

The user directly requested this instruction setup and task recovery. Routine documentation choices are covered by that request.

## Verification

Check instruction links, read back the new files, review the diff, and obtain an independent review. Keep observed implementation separate from gameplay verification.
