---
name: roblox-studio
description: Roblox Studio features + the built-in Studio MCP for any game in this workspace — the MCP tool set & our verify/playtest discipline, the Assistant/agentic tools, editors (terrain, UI styling, material generator, animation), scripting (new Luau type solver, native codegen), testing (Device Emulator for mobile, Team Test), and recent 2025-2026 features worth using (texture streaming, occlusion culling, custom matchmaking, 120-stud lights). Use when driving Studio via MCP, choosing a Studio tool/feature, or setting up testing.
---

# Roblox Studio & the Studio MCP

Full detail in [reference/studio.md](reference/studio.md). This is the working guide.

## Driving Studio via the MCP (how we build)

Studio ships a built-in MCP; Claude Code connects via the committed `roblox.workspace/.mcp.json`. Master
tool = **`execute_luau`** (run any Luau live); plus read (`search_game_tree`/`inspect_instance`/`script_*`),
build (`multi_edit`/`insert_asset`/`generate_mesh|material`), and **playtest** (`start_stop_play`,
`get_console_output`, `screen_capture`, `user_*_input`, `character_navigation`).

**Discipline (non-negotiable):**
- **Verify every scene/terrain edit** — read it back (`inspect_instance`/`ReadVoxels`) **and**
  `screen_capture` — before reporting done. (This rule was learned the hard way; see `roblox-terrain`.)
- Greybox live: `execute_luau` → `screen_capture` → iterate.
- Playtest loop: `start_stop_play` → drive with input tools → `get_console_output` + `screen_capture`.
- Studio must be open with the place loaded; `set_active_studio` if multiple.

## MCP testing gotchas (learned the hard way — Job 022)

- **`execute_luau` runs in a SEPARATE Luau context from the running game scripts.** Its `require(Module)`
  returns a *fresh* module instance with its own upvalue state (a ModuleScript's private `cache`/tables).
  So a service getter called there (e.g. `Profiles.getGold`) reads that fresh instance's empty state, NOT
  what the game credited. **Verify game state via SHARED Instances** — player attributes, `leaderstats`,
  `Workspace` attributes, or the DataStore directly — never via a module's private in-memory tables.
- **Session locks (not a Play/Edit data split) cause "stale profile" symptoms.** Edit-mode DataStore
  writes DO appear in Play (verified Job 025 — an Edit `SetAsync` profile loaded fine in Play). What bit
  us earlier was a non-stale **leftover session lock** sending the load to a non-saving in-memory fallback.
  So **seed/reset test profiles from Edit via `SetAsync` with NO `__lock`**, and start persistence tests
  from a genuinely clean, unlocked profile.
- **Work around the separate VM when testing:** test a server `RemoteFunction` with a **Client**-context
  `execute_luau` calling `rf:InvokeServer(...)` (hits the real server + real profile); test a load-driven
  path by **seeding the DataStore** (Edit `SetAsync`, no lock) and letting the game load it — don't mutate
  module state in `execute_luau` (different VM copy).
- **Forcing an end-state:** systems that continuously write an attribute each frame (e.g. `BoatServer`
  rewrites `Workspace.BoatDistance` from the hull) will clobber a manual override — change the *threshold*
  instead (e.g. set `RiverEndDistance = 0`) to trip a monitor.
- Some emoji (e.g. 🪙) render as a tofu box in Roblox `TextLabel`s — avoid them in UI text.

## Which Studio tool for the job

- **Hand-sculpt hero terrain** → Terrain Editor (Generate/Sculpt/Sea Level). Scripted/procedural terrain →
  `roblox-terrain` skill via MCP.
- **Consistent HUD theming** → **UI Styling** (StyleSheet/StyleRule, released Jan 2026) — see `roblox-ui`.
- **Materials** → Material Generator (text→PBR). **Meshes** → `generate_mesh` / Meshy (`roblox-chars`).
- **Animation** → Animation Editor (see `roblox-animation`). **Avatar rig** → Avatar Auto-Setup.
- **Assets** → Toolbox / Asset Manager / Creator Store — see `roblox-assets` (scan for scripts!).

## Testing (mobile-first)

- Test modes: **Play** / **Play Here** / **Run** (server, no char) / **Team Test** (multiplayer, one at a time).
- **Device Emulator** (Test menu) — emulate phones/tablets, resolutions, touch controls. **Use it to verify
  every HUD/menu on mobile.** Full multitouch may still need a real device.
- Raise **Editor Quality Level** to preview real lighting/water in edit view; MicroProfiler for frame timing.

## Scripting notes

New Luau **Type Solver GA** (opt strict in via `Workspace.UseNewLuauTypeSolver`; templates default
Nonstrict); type checking is Studio-edit-only. `--!native`/`@native` for hot server compute. Debugger,
Command Bar, Output, MicroProfiler standard. Our external-editor flow = Rojo + `luau-lsp`.

## Recent features worth using (for a co-op mobile game)

Texture Streaming + Occlusion Culling + **SLIM** (perf on low-end), **Custom Matchmaking** (party/co-op
sessions → our lobby→reserved-server flow), light `Range` up to **120 studs**, aerodynamic forces (beta),
DragDetectors, non-destructive Reimport. The Assistant is agentic (Planning Mode, Playtesting Agent beta) —
but generated scripts "might not function flawlessly," so we author + verify, not blind-accept.
