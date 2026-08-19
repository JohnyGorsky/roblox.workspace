# Implementation Plan — Job #010

**Project**: `roblox.workspace`
**Created**: 2026-08-19 22:18:38
**Status**: Planning (awaiting go-ahead)

## Analysis

roblox.tide is a docs-only repo today (design pack v2: 13 pillars, 12 accepted decisions, 16 system docs, 10 content catalogs, 10 planned features, asset registry). It is already a folder in roblox.workspace.code-workspace. It is NOT yet known to tools/job.py, so no tide job can be scaffolded. Agreed with the user via wizard: tide keeps docs/features/ as design memory and uses the shared Jobs lifecycle for execution. This job only makes the workspace side of that possible; the tide-side scaffolding (Jobs/Planned/todo/findings, .jobconfig.json, studio/ sync tree, tide-project skill) is tide Job #001.

## Implementation steps

1. Add "tide": "../roblox.tide" to PROJECTS in tools/job.py
2. Update the job.py module docstring: project list, usage examples, and the project -> Jobs folder resolution notes
3. Verify: python tools/job.py list todo --project tide resolves, and new --project tide accepts the project
4. No changes to GROUND-RULES.md or CLAUDE.md needed - both describe projects generically; CLAUDE.md's example list is illustrative

## What I need from you

- [ ] _TODO: Studio actions, asset IDs, decisions, go-ahead_

## Verification

- [ ] _TODO: how we confirm it works_
