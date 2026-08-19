# Implementation Plan — Job #011

**Project**: `roblox.workspace`
**Created**: 2026-08-19 22:39:48
**Status**: Planning (awaiting go-ahead)

## Analysis

GROUND-RULES.md section 2 currently splits labour so that Claude drives Studio via MCP (line 27 already lists 'trigger playtests') while the human 'Press Play and judge gameplay feel' (line 39). The two rules the user asked for resolve an ambiguity in that split and add a new gate. Nothing in GROUND-RULES.md currently mentions the device emulator or mobile at all - grep found zero hits - so the emulator rule is new text, and it must be written to override without contradicting the skills: both the mobile skill ('FIRST ACTION, ALWAYS: Test to Device') and roblox-studio ('THE DEVICE EMULATOR IS THE MOBILE ANSWER - USE IT BEFORE SAYING NEEDS A REAL DEVICE') are emphatic because Defender jobs 094-099 burned four rounds deferring mobile questions. Ground rules win over skills, so the new rule must explicitly say it gates the SWITCH and not the MEASUREMENT, otherwise a reader resolves the conflict by skipping mobile testing. User decisions via wizard: workspace-wide (all games); Claude runs the test and the human still judges feel; ask-first-but-never-defer only - restoring desktop view, once-per-session approval and gating plain Play were all offered and NOT selected, so they must not be written in.

## Implementation steps

1. Amend the Claude-does list in section 2: Claude runs functional verification end-to-end via MCP and reports observations
2. Amend the human-does Play bullet: the human judges feel/fun and is no longer the one who must press Play to learn whether something works
3. Add a short device-emulator gate to section 2: ask before Test to Device, with an explicit never-defer clause naming the anti-patterns (guessing at a phone layout, claiming a real device is needed when the emulator answers it)
4. Cross-check the mobile and roblox-studio skills still read correctly under the new rule; do not edit them unless they now contradict it
5. Verify: grep the new rules, confirm no unselected option leaked in, confirm section numbering and the always-use-skills list are untouched

## What I need from you

- [ ] _TODO: Studio actions, asset IDs, decisions, go-ahead_

## Verification

- [ ] _TODO: how we confirm it works_
