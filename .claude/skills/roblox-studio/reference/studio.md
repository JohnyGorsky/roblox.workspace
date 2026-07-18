# Roblox Studio & the Studio MCP — reference (2026)

Sourced from official Creator Docs + Roblox DevForum/newsroom, current 2026-07. Not-primary-confirmed
items flagged **[unverified]**.

## The built-in Studio MCP (how *we* drive Studio)

Studio ships an **MCP server built in** (no install), stdio transport, connected via Assistant Settings →
MCP Servers → Quick connect (Claude Code is a supported client). "MCP clients can read and modify content
in your open places — only connect clients you trust." Our workspace registers it via committed
`roblox.workspace/.mcp.json` (see workspace Job 002).

**Tools exposed** (what Claude can call in this session):
- **Read:** `search_game_tree`, `inspect_instance`, `script_read`, `script_search` (fuzzy, ≤10),
  `script_grep` (≤50), `get_console_output`, `get_studio_state`.
- **Write/build:** `execute_luau` (run Luau — the master key), `multi_edit` (create/edit scripts),
  `insert_asset`, `generate_mesh` / `generate_material` / `generate_procedural_model` (+ `wait_job_finished`),
  `search_asset`, `upload_image`, `store_image`.
- **Playtest (added Mar 2026):** `start_stop_play`, `get_console_output`, `screen_capture`,
  `character_navigation`, `user_keyboard_input`, `user_mouse_input`.
- **Session:** `list_roblox_studios`, `set_active_studio`. Docs: `http_get` (whitelisted Roblox docs), `skill`.

**Our MCP discipline** (from hard-won experience — see `roblox-terrain`):
- **Verify every scene/terrain edit** by reading it back (`inspect_instance`/`ReadVoxels`) **and**
  `screen_capture` before reporting done — never assume a fill/edit worked.
- Greybox live: build/sculpt via `execute_luau`, screenshot, iterate.
- Playtest loop: `start_stop_play` → drive with input tools → `get_console_output` + `screen_capture`.
- Studio must be **open with the place loaded**; pick the active instance with `set_active_studio`.

## Assistant & the agentic direction

Studio **Assistant** (GA): Q&A, create/modify objects+scripts, `/generate_mesh`, `/insert_asset`,
procedural models (**50 per rolling 24h**, up to 8 parts), asset search+insert, **viewport screenshot
analysis**, **Planning Mode** (editable task manifest before execution), cloud-synced/branchable threads.
Docs caution generated scripts "might not function flawlessly." 2026 push: agentic loops + a
**Playtesting Agent (beta)** that drives the character as automated QA.

## AI generation in Studio (now)

- **Mesh Generation** — textured 3D from text (Cube model). **Material Generator** — released; text-prompt
  PBR variants (Model → Material → Generate New Material). **Procedural models** via Assistant/MCP.
- **Texture Generator** exists; **built-in skybox generation [unverified]**; **conversational NPC** dialogue
  is beta **[unverified GA]**.

## Editors & managers

- **Terrain Editor:** Generate (procedural biomes+seed), Sculpt/Draw/Smooth/Sea Level, heightmap+colormap
  import. (For scripted terrain use `roblox-terrain`; hand-sculpt hero terrain here.)
- **Material Manager / Generator.** **Animation Editor** (Avatar tab; keyframe editor — see `roblox-animation`).
- **UI Styling / Style Editor** (full release Jan 2026): `StyleSheet`/`StyleRule`/`StyleLink`, CSS-like
  global UI overrides, publishable — use for consistent HUD theming (see `roblox-ui`).
- **Avatar Auto-Setup** (auto-rig/cage a mesh into an avatar). **Asset Manager / Toolbox / Creator Store**
  (see `roblox-assets`). **Team Create** collaboration; comments/annotations roadmapped **[unverified GA]**.

## Scripting in Studio

- **New Luau Type Solver — GA Nov 2025.** `Workspace.UseNewLuauTypeSolver` (Default/Enabled/Disabled) +
  `LuauTypeCheckMode` (templates default Nonstrict). Type checking = Studio editing only, not runtime.
  Old solver available through 2026. (See `roblox-scripting`.)
- **Native codegen** `--!native` (whole script) or `@native` (per function). Script Editor autocomplete +
  Code Assist; Debugger, Command Bar, Output, **MicroProfiler**. External editor via Rojo + `luau-lsp`
  (our setup); first-party file-sync roadmapped **[unverified]**.

## Testing & mobile verification

- **Test modes:** **Play** (spawn at SpawnLocation), **Play Here** (at camera), **Run** (server, no
  character), **Team Test** (multiplayer; one session at a time). (Via MCP: `start_stop_play`.)
- **Device Emulator** (Test menu) — emulate phones/tablets/console, resolutions/aspect ratios, touch
  controls; **essential for mobile-first UI checks** (full multitouch may still need a real device).
- **Editor Quality Level** raises lighting/water preview fidelity in edit view; rendering/physics stats
  overlays; MicroProfiler for frame timing. **[unverified exact setting labels — confirm in docs/studio/setup.]**

## Recent updates worth using (2025–2026)

- **Perf (mobile):** Occlusion Culling, **Texture Streaming**, **SLIM** (lightweight interactive models).
- **Matchmaking:** Custom Matchmaking (party/co-op sessions) — relevant to our lobby→server flow.
- **Lighting:** light `Range` limit **doubled to 120 studs**. **Physics:** aerodynamic forces (beta).
- **UI:** DragDetectors, UIStroke scaling, UI Styling. **UGC:** non-destructive Reimport (beta), sell models.
- New customizable **menu + ribbon** Studio UI (Nov 2025).

## Sources
docs/studio/{mcp,testing-modes,terrain-editor,material-generator,texture-generator,setup},
docs/assistant/guide, docs/ui/styling, docs/luau/native-code-gen; DevForum New Type Solver GR,
Assistant+MCP+playtest (Mar 2026), UI Styling full release, 2025 EoY recap; newsroom "Studio Going Agentic".
