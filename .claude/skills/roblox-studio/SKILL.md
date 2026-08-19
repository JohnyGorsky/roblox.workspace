---
name: roblox-studio
description: Roblox Studio features + the built-in Studio MCP for any game in this workspace — the MCP tool set & our verify/playtest discipline, the Assistant/agentic tools, editors (terrain, UI styling, material generator, animation), scripting (new Luau type solver, native codegen), testing (the DEVICE EMULATOR — which gives real TouchEnabled, real ViewportSize and Roblox's own TouchGui rects, and answers almost every mobile question without a phone — plus Team Test), and recent 2025-2026 features worth using (texture streaming, occlusion culling, custom matchmaking, 120-stud lights). Use when driving Studio via MCP, choosing a Studio tool/feature, or setting up testing.
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

## Where things live in the Studio UI

⚠️ **Verify before you instruct.** Roblox renames and moves this UI often. Do **not** state a menu path
from memory — check the live Studio, or ask for a screenshot. Saying "File → Game Settings" to a user
whose Studio has no such entry wastes their time and costs trust. Everything below was verified against
live Studio on **2026-08-19**; re-verify after a Studio update.

**There is no "Game Settings" any more.** It was split:

| What you want | Where it is |
|---|---|
| Max players — called **"Maximum Visitor Count"** | **Creator Hub** → Creations → *experience* → Places → *place* → **Access** → Basic Settings. ✅ verified 2026-08-19. `File → Experience Settings` may also work; unverified |
| Who may join a place directly (**Direct Access Control**) | Same Access page. `Fully Open` allows deep links, game invites and insecure client teleports from *any* universe; `Secure within Universe only` restricts to secure server teleports — the right choice for a run/session place reached from a lobby |
| **Social Slots** (friends joining your server) | Same Access page. Right for a lobby, usually wrong for a fixed-size session place |
| Avatar type (R6/R15), scaling, animations | `File → Avatar Settings` — its own entry, *not* inside Experience Settings |
| Place/experience configs | `File → Open Configs` |
| **Studio's own preferences** (themes, editor, network) | `File → Studio Settings` (`Alt+S`) — a different thing entirely; don't confuse it with Experience Settings |
| Lighting style / shadows quality | **Properties panel**, not a dialog: Explorer → select `Lighting` → `LightingStyle`, `PrioritizeLightingQuality`. Read-only to scripts, per place |
| Playable devices | Creator Hub (create.roblox.com), on the experience's Settings page |

**Menu bar:** File, Edit, View, Plugins, Test, Window, Help.

**Ribbon tabs:** Home, Avatar, UI, Script, Model, Plugins (+). **There is no Test ribbon tab** — playtest
is the ▶/⏸/⏹ transport buttons at the top-left with a mode dropdown beside them, plus the `Test` menu.
The Home tab carries Select/Move/Scale/Rotate/Transform, snap toggles, Part/Terrain/Character/GUI/Script/
Import, Material/Color, Group/Lock/Anchor, and the Explorer/Properties/Toolbox/Assets toggles.

**Settings a script cannot touch** — these need a human click, so put them on a checklist rather than
attempting them in code:

- `Players.MaxPlayers` / `PreferredPlayers` — read-only to scripts, **including** the MCP's plugin
  context. The assignment fails outright.
- `Lighting.LightingStyle` / `PrioritizeLightingQuality` — same.
- Anything on the Creator Hub (playable devices, monetization, genre, privacy).

Before telling a human to click something, prefer proving what the property does over MCP first: read it,
try assigning its own value back, and report whether it is writable. That converts a guess into a fact.

## Which Studio tool for the job

- **Hand-sculpt hero terrain** → Terrain Editor (Generate/Sculpt/Sea Level). Scripted/procedural terrain →
  `roblox-terrain` skill via MCP.
- **Consistent HUD theming** → **UI Styling** (StyleSheet/StyleRule, released Jan 2026) — see `roblox-ui`.
- **Materials** → Material Generator (text→PBR). **Meshes** → `generate_mesh` / Meshy (`roblox-chars`).
- **Animation** → Animation Editor (see `roblox-animation`). **Avatar rig** → Avatar Auto-Setup.
- **Assets** → Toolbox / Asset Manager / Creator Store — see `roblox-assets` (scan for scripts!).

## Testing (mobile-first)

- Test modes: **Play** / **Play Here** / **Run** (server, no char) / **Team Test** (multiplayer, one at a time).
- Raise **Editor Quality Level** to preview real lighting/water in edit view; MicroProfiler for frame timing.

### ⚠️ THE DEVICE EMULATOR IS THE MOBILE ANSWER — USE IT BEFORE SAYING "NEEDS A REAL DEVICE"

> **Ask the human before flipping `Test → Device`** — it takes over their Studio session (GROUND-RULES §2).
> The gate is on the switch, not on the measurement: still ask for the emulator rather than
> guessing at a layout or deferring the question to "a real device".

**Test → Device.** This section is emphatic because Jobs #094–#099 burned four jobs' worth of effort
deferring mobile questions to "a real phone" while the emulator sat one click away and could have
answered nearly all of them immediately.

**What a desktop Play session tells you about mobile: nothing.** It reports
`UserInputService.TouchEnabled = false`, so every touch-gated branch never runs — the touch controls are
never even built. Measuring the "mobile HUD" there measures something that does not exist.

**What the emulator gives you, all of it real and measurable via `execute_luau`:**

| | |
|---|---|
| `UserInputService.TouchEnabled` | **true** — touch-only UI actually builds |
| `Camera.ViewportSize` | the device's REAL GUI coordinate space |
| `GuiService:GetGuiInset()` | the true top-bar inset |
| A `ScreenGui`'s `AbsoluteSize` | the real usable canvas per `ScreenInsets` mode |
| `PlayerGui.TouchGui` | Roblox's OWN controls, with real rects: `ThumbstickStart`, `ThumbstickEnd`, `JumpButton` |

**⚠️ `ViewportSize` is NOT the screenshot's pixel size.** On a phone preset it came back **666 × 374**
(usable **666 × 316** after insets) where the device screenshot was ~1536 × 710. **Every pixel `MinSize`
floor is therefore ~2.3× larger relative to the canvas than a desktop test suggests** — this is what
broke the lobby rail in #095 (a 420 px floor became ~80% of the screen). Aspect-ratio testing does not
reveal it; only reading `ViewportSize` on a touch canvas does.

**Always check our UI against `TouchGui`.** Roblox's thumbstick and jump button are real, they are
big, and no in-house overlap harness knows they exist. Measured on a phone preset: thumbstick
`x 29..103, y 223..297`; jump `x 571..641, y 226..296`; and `DynamicThumbstickFrame` reserves the whole
bottom-left quadrant. **The bottom-left belongs to movement — do not put UI there.**

**The one thing it genuinely cannot do:** multi-touch. It is single-pointer, so "two thumbs at once"
still needs hardware. That is the *only* claim worth deferring to a real device.

### Measuring UI: what lies to you

Verified failures from #095/#097/#099 — all produced confident, wrong numbers:

1. **Cloning a GUI to measure it does not run its runtime code.** Anything sized imperatively by a
   script (a `resize()` on `AbsoluteSize`, a `layoutCluster()`) keeps whatever pixel value the live
   session had, and reports the same number at every simulated viewport.
2. **Forcing hidden children `Visible = true` changes `UIListLayout` flow.** Hotbar slots read 57×57
   that way and are really 76×76.
3. **`TextLabel.TextFits` is not reliable on an off-screen clone.** Text that measured "fits" was
   plainly clipped on the device. `applyText`'s `TextScaled` has a **12 px `MinTextSize` floor**, so
   text cannot shrink out of a too-small box — it wraps, and the overflow is simply cut.

**So:** a harness is trustworthy for *static rectangle collisions*. For text fit, script-sized elements
and anything involving CoreGui, measure **live in the emulator**, and re-measure a surprising number a
second way before acting on it.

## Scripting notes

New Luau **Type Solver GA** (opt strict in via `Workspace.UseNewLuauTypeSolver`; templates default
Nonstrict); type checking is Studio-edit-only. `--!native`/`@native` for hot server compute. Debugger,
Command Bar, Output, MicroProfiler standard. Our external-editor flow = Rojo + `luau-lsp`.

## Recent features worth using (for a co-op mobile game)

Texture Streaming + Occlusion Culling + **SLIM** (perf on low-end), **Custom Matchmaking** (party/co-op
sessions → our lobby→reserved-server flow), light `Range` up to **120 studs**, aerodynamic forces (beta),
DragDetectors, non-destructive Reimport. The Assistant is agentic (Planning Mode, Playtesting Agent beta) —
but generated scripts "might not function flawlessly," so we author + verify, not blind-accept.
