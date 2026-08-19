# Implementation Plan — Job #012

**Project**: `roblox.workspace`
**Created**: 2026-08-19 23:17:21
**Status**: Planning (awaiting go-ahead)

## Analysis

Both errors surfaced while writing the tide place-settings baseline, and both had the same root cause: stating Studio facts from training memory instead of checking the live Studio one MCP call away. The lighting error was already latent in the skills, so it would have been repeated in every game. Evidence used: two user screenshots (the Lighting Properties panel showing LightingStyle/PrioritizeLightingQuality and no Technology row; the File menu showing Experience Settings and Avatar Settings with no Game Settings entry) plus an MCP probe that read both new properties, attempted to write each its own value, and enumerated Enum.LightingStyle and Enum.Technology.

## Implementation steps

1. roblox-vfx SKILL.md: replace the Technology bullet and rewrite the Shadows and lighting tech section around LightingStyle/PrioritizeLightingQuality, noting both are read-only to scripts and that Enum.Technology no longer maps to a property
2. roblox-vfx reference/vfx.md: same correction in the Lighting service and Shadows sections, and fix the mobile/perf summary line that named Future as the heaviest Technology
3. roblox-studio SKILL.md: add a 'Where things live in the Studio UI' section - it had none, which is why there was nothing to check a menu path against - with the verified File menu split, ribbon tabs, and a table of settings scripts cannot touch
4. Put the verify-before-instruct rule at the top of that section, and add the read-only-to-scripts list (MaxPlayers, LightingStyle, PrioritizeLightingQuality, Creator Hub)
5. Correct the tide settings baseline and job 004 checklist, which carried the wrong menu path and a Lighting.Technology row
6. Save a memory for the behavioural lesson so it survives outside this repo

## What I need from you

- [ ] _TODO: Studio actions, asset IDs, decisions, go-ahead_

## Verification

- [ ] _TODO: how we confirm it works_
