# Job #011: Ground rules: Claude tests via Studio MCP; ask before the device emulator

**Project**: `roblox.workspace`
**Created**: 2026-08-19 22:39:32
**Status**: Requirements Gathering (intake)

## Requirements / goal

Two new authoritative rules in GROUND-RULES.md section 2, applying to every game. (1) Claude runs the tests: Claude drives playtests end-to-end through the Studio MCP (start_stop_play, user input, console, screen_capture) and reports what it observed; the human remains the authority on gameplay feel and whether something is fun/right, but is no longer the one who must press Play to find out whether it works. This amends the existing 'Press Play and judge gameplay feel' human bullet. (2) Claude must ASK before switching Studio to the device/mobile emulator (Test to Device), because it changes the human's Studio state. The ask is a permission gate on their session, NOT permission to skip mobile measurement - the mobile and roblox-studio skills say Test to Device is the first action always for mobile questions, and four Defender jobs were burned deferring mobile work to a real phone. Claude must still ask for the emulator rather than guessing at a phone layout or claiming a real device is needed. Not adopted: restoring desktop view afterwards, once-per-session approval, and gating plain Play sessions.

## Checklist

- [ ] Requirements reviewed (this intake)
- [ ] Implementation plan created & agreed
- [ ] Implementation completed
- [ ] Final summary + changelog written
