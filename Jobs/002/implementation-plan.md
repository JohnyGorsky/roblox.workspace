# Implementation Plan — Job #002: Set up Roblox Studio MCP

**Project**: `roblox.workspace`
**Created**: 2026-07-17
**Status**: Planning (awaiting go-ahead)

## Analysis (from research, 2026)

- **Use the built-in Studio MCP server.** As of 2026, Roblox Studio ships an MCP server *inside
  Studio* — official docs: https://create.roblox.com/docs/studio/mcp. The old standalone
  `Roblox/studio-rust-mcp-server` was **archived 2026-04-03** and is deprecated; we will **not** use
  it. Open Cloud (`rblx-open-cloud`) is for published/cloud experiences, not a live local Studio — not
  relevant here.
- **Claude Code is an officially supported quick-connect client**, so setup is a Studio toggle, not a
  build. No Rust, no Node, no Rojo, no manual plugin.
- **Transport:** stdio — Claude Code launches the server via a shim at
  `%LOCALAPPDATA%\Roblox\mcp.bat`. It is not an HTTP/SSE server.
- **Capabilities** (read + write, broad): read the live tree (`search_game_tree`, `inspect_instance`);
  scripts (`script_read`, `multi_edit`, `script_search`, `script_grep`); `execute_luau` in
  Edit/Client/Server; playtesting (`start_stop_play`, `get_console_output`, `get_studio_state`,
  `screen_capture`); input simulation; asset generation (`generate_mesh`, `generate_material`,
  `insert_asset`); multi-instance (`list_roblox_studios`, `set_active_studio`).
- **Requires Studio open** with the place loaded — no session, no connectivity.
- **Security:** allows arbitrary Luau execution and modifying the open place. Trust is granted at the
  **client-connection** level (you approve which clients connect). Claude Code's own MCP tool
  permission prompts apply on top. (A per-tool-call approval UI in the built-in server is unverified.)

## Decisions

- **Server:** built-in Studio MCP (not the archived standalone).
- **Config scope:** ✅ **committed project `.mcp.json`** in `roblox.workspace` (created). The
  `%LOCALAPPDATA%` path resolves per-machine, so teammates with Studio get it automatically.
- **studio-diagnostics skill:** ✅ **keep as a fallback**, not retired. Command Bar scripts still work
  when Studio MCP isn't connected (Studio closed, client not trusted, or exports too large for a tool
  call). Add a note that MCP is preferred when connected.

## Implementation steps

### You do (on your machine — I can't)
1. Open Roblox Studio with a Defender place loaded.
2. Open **Assistant** → **… → Manage MCP Servers**.
3. Turn on **"Enable Studio as MCP server."**
4. Under **Quick connect**, toggle on **Claude Code**.
5. Tell me when the green "connected clients" indicator shows Claude Code (and keep Studio open).

_Fallback if quick-connect misbehaves — manual stdio entry:_
```json
{ "mcpServers": { "Roblox_Studio": {
  "command": "cmd.exe",
  "args": ["/c", "%LOCALAPPDATA%\\Roblox\\mcp.bat"]
} } }
```

### I do
6. Confirm the server registered (`claude mcp list` / inspect the written config). **A Claude Code
   restart may be needed** to load a newly added MCP server — I'll tell you if so.
7. Smoke-test read: `search_game_tree` / `inspect_instance` against the open place and report what I see.
8. Smoke-test write on something harmless (e.g. read a script, make a trivial reversible edit, or
   `execute_luau` a `print`) and confirm round-trip.
9. Update **`GROUND-RULES.md` §2** (division of labour) to reflect Claude driving Studio directly.
10. Add the "MCP preferred, Command Bar fallback" note to the **`studio-diagnostics`** skill.

## What I need from you

- [ ] **Go-ahead** on this plan.
- [ ] Do the Studio-side toggle (steps 1–5) and confirm Claude Code shows connected.
- [ ] **Config scope decision:** register the MCP server as a **committed project `.mcp.json`** in
      `roblox.workspace` (shared with any teammate who has Studio locally — the `%LOCALAPPDATA%` path
      resolves per-machine) vs **user-level / local** (per-machine, not committed). See wizard.

## Verification

- [ ] `claude mcp list` shows `Roblox_Studio` connected.
- [ ] I can read the live Defender tree via `search_game_tree`.
- [ ] A reversible write (edit / `execute_luau` print) round-trips and appears in Studio.
- [ ] GROUND-RULES §2 + studio-diagnostics updated.
