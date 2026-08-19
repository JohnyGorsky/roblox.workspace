# Final Summary — Job #011

**Project**: `roblox.workspace`
**Completed**: 2026-08-19 22:40:46
**Status**: ✅ Completed

## What was implemented

Two rules added to GROUND-RULES.md section 2, workspace-wide. (1) 'Run the tests' in the Claude-does list: functional verification is Claude's job, driven end-to-end through MCP (start_stop_play, user input, character_navigation, console, screen_capture), reporting what was observed rather than what the code should do, with 'please test this and tell me if it works' called out as an unacceptable handoff. The human-does Play bullet was rewritten to match - the human judges feel and plays to form that judgement, not because Claude needs someone to discover whether its code works. (2) A device-emulator gate after the human-action paragraph: ask via the wizard before Test to Device, because it takes over the human's Studio session, and state what needs measuring. The gate is written explicitly as being about their Studio state and NOT about whether to measure, with three named anti-patterns forbidden (guessing at a phone layout, claiming a real device is needed when only genuine multi-touch is, and quietly dropping the mobile question because the gate felt like a no). GROUND-RULES.md previously had zero mentions of mobile or the emulator. Because ground rules override skills, the mobile and roblox-studio skills - which both say Test to Device is the first action ALWAYS - would otherwise have been resolved by a reader in favour of skipping mobile testing, so a three-line blockquote pointing at the gate was inserted at each of those two instruction sites. Deliberately NOT written in, having been offered and not selected: restoring the desktop view afterwards, once-per-session approval instead of per-switch, and gating plain Play sessions.

### Files changed

- `GROUND-RULES.md`
- `.claude/skills/mobile/SKILL.md`
- `.claude/skills/roblox-studio/SKILL.md`

## Verification

- [x] Both rules present in `GROUND-RULES.md` §2; section numbering and §6 always-use-skills untouched
- [x] Grepped for the three unselected options — none leaked into the text
- [x] The emulator gate sits after the human-action paragraph, before the Studio-MCP blockquote
- [x] Pointer blockquote added at both contradicting skill sites (`mobile` §1, `roblox-studio` emulator section)
- [x] Rule (1) was exercised the same session: MCP-driven sync verification on both tide places,
      reported as observations (game place syncs, lobby place does not)
