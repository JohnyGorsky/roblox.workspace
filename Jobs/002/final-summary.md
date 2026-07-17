# Final Summary — Job #002: Set up Roblox Studio MCP

**Project**: `roblox.workspace`
**Completed**: 2026-07-17
**Status**: ✅ Completed & verified live

## What was implemented

Connected Claude Code to a live Roblox Studio session via the **built-in Studio MCP server** (Roblox
ships MCP inside Studio as of 2026; the old standalone `studio-rust-mcp-server` was archived and was
*not* used). Claude can now read and drive the open Studio place directly instead of handing the human
Command Bar scripts.

## Files changed

### roblox.workspace
- **`.mcp.json`** (new) — committed project registration of the `Roblox_Studio` MCP server. Reconciled
  to the exact command Studio's quick-connect panel generated for this machine:
  `cmd.exe /c "cd /d %LOCALAPPDATA%\Roblox && .\mcp.bat"` (stdio transport). `%LOCALAPPDATA%` resolves
  per-machine, so teammates with Studio get it automatically.
- **`GROUND-RULES.md`** — §2 rewritten: Claude now drives Studio via MCP; human keeps Studio open,
  presses Play to judge feel, and commits. The "Studio MCP is live" note replaces the earlier
  "being set up" note; MCP writes are gated by Claude Code's tool-permission prompts.
- **`.claude/skills/studio-diagnostics/SKILL.md`** — added a header: MCP preferred when connected,
  Command Bar flow is the fallback.

### Setup done on the user's machine (not in-repo)
- Enabled Studio → Assistant → Manage MCP Servers → **"Enable Studio as MCP server."**
- Restarted Claude Code to load the committed `.mcp.json` and approved the project MCP server.

## Verification (live)

- [x] `list_roblox_studios` → one instance, **"Jungle run"**.
- [x] `get_studio_state` → Edit mode, DataModel available.
- [x] `search_game_tree` → read the live place tree ("Place2").
- [x] `execute_luau` (Edit) → returned `42` (6×7); `print` appeared via `get_console_output`
      (`[MCP smoke test] Claude Code <-> Studio round-trip OK`). Write was console-only, nothing to revert.

## Notes / follow-ups

- **Not committed** — changes left in the `roblox.workspace` working tree for the user to review/commit.
- **Decisions:** committed project `.mcp.json` (not user-level); `studio-diagnostics` kept as fallback
  (not retired).
- **Observed (Jungle-setup scope, separate job):** the Studio console showed
  `Can't sync <service> to disk: Root file or folder is missing` for the six auto-sync services
  (ReplicatedFirst, ReplicatedStorage, ServerScriptService, ServerStorage, and both
  StarterCharacterScripts + StarterPlayerScripts). Jungle's on-disk `sync/` folder + `default.project.json`
  don't exist yet — to be addressed in the "set up Jungle" job. Confirms the sync layout recorded in
  `roblox.jungle/.jobconfig.json` and the `jungle-project` skill.
- **Security:** MCP `execute_luau` runs arbitrary Luau in the open place; Claude gates non-trivial /
  hard-to-reverse Studio changes behind a description + permission prompt.
