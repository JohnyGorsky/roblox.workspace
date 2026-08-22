# GROUND-RULES.md — authoritative rules for the Roblox workspace

These rules are **authoritative** and apply to every game and every job. When a ground rule
conflicts with anything else, the ground rule wins. Claude must follow these without being reminded.

## 1. Standing rules (non-negotiable)

- **Claude never commits.** Claude makes file changes only; the **user is the only one who commits**
  (and pushes). Never run `git commit`/`git push`, never stage with intent to commit, even if a task
  seems to imply it.
- **Always ask via the wizard.** When Claude needs a decision or clarification, ask through the
  interactive **AskUserQuestion** interface — not as a plain-text list of questions.
- **Job-first, always.** Every change starts as an explicit job — even small ones. No ad-hoc
  changes. Describe the work, I open the job (`intake`), and we proceed through the lifecycle. See §5.
- **Every job declares its project** (`workspace` / `defender` / `jungle`) and touches only that one.
- 🔴 **Verify in GAMEPLAY, never in the editor.** Nothing a player sees may be signed off from an Edit
  session. Reproduce the symptom in Play, at the player's camera, before forming a hypothesis. See §7.
- 🔴 **Every job uses at least one agent.** An independent reviewer that is *not* told Claude's theory.
  After one failed fix, a fresh-eyes agent is mandatory before a second attempt. See §8.
- **Never edit a script outside the system/place you were asked to work on — confirm first.** A game
  can have multiple Rojo places (e.g. Jungle: GAME `/sync/` vs LOBBY `/lobby/sync/`). Identify which
  place/system owns a file before editing it; editing across that boundary needs explicit permission.
  When unsure whether a file is in scope, ask via the wizard.

## 2. Human ↔ Claude division of labour

**Claude does (in code / on disk, and now in Studio directly via the Roblox Studio MCP):**
- Write and edit Luau, module structure, definitions, and configuration.
- Scaffold and maintain jobs (intake → plan → summary → changelog).
- **Drive the live Studio session via MCP** — read the tree (`search_game_tree`/`inspect_instance`),
  read/edit scripts, run Luau (`execute_luau`), read console output, trigger playtests, capture the
  viewport. This replaces most Command Bar handoffs.
- Generate Meshy.ai prompts + rigging/export checklists.
- Consult the knowledge skills before guessing at APIs, balance, or design.
- **Script *procedural* terrain only** (via the `roblox-terrain` skill) — compute the geometry, never
  eyeball it, and **verify by voxel read-back + screenshot**. Hand-sculpting hero terrain is not Claude's job.
- **Run the tests.** Functional verification is Claude's job, not a handoff. Claude drives the
  playtest end-to-end through MCP — `start_stop_play`, `user_keyboard_input`/`user_mouse_input`,
  `character_navigation`, `get_console_output`, `screen_capture` — and **reports what it actually
  observed**, not what the code should do. "Please test this and tell me if it works" is not an
  acceptable handoff; find out.

**Human does (in Roblox Studio / external tools):**
- **Hand-sculpt hero/handcrafted terrain** (rivers, islands, set-pieces) with Studio's terrain tools —
  faster and better-looking than scripting it. Claude codes gameplay against what you build.
- Keep **Studio open with the target place loaded** (MCP has no connectivity otherwise), and choose
  which place is active.
- **Judge gameplay *feel*** — the human is still the one who decides if it's fun/right. You play
  when you want to form that judgement, **not** because Claude needs someone to find out whether its
  code works (see "Run the tests" above).
- Import Meshy.ai models, publish animations, and supply asset IDs.
- Source icons/sounds and provide their IDs.
- Review diffs and **commit**.

When work needs a human action, Claude states it explicitly and waits — it does not pretend a
Studio-side step is done.

**Ask before switching Studio to the device/mobile emulator.** `Test → Device` takes over the
human's Studio session and viewport, so Claude asks (via the wizard) before flipping it, and says
what it needs to measure.

This gate is about **their Studio state, not about whether to measure**. It is *not* licence to skip
mobile work — the `mobile` and `roblox-studio` skills are emphatic that the emulator is the mobile
answer, because Defender jobs #094–#099 burned four rounds of rework deferring phone questions that
the emulator would have settled immediately. So when a mobile question comes up, Claude **asks for
the emulator**; it does not:

- guess at a phone layout, or reason about one instead of measuring it;
- claim something "needs a real device" when the emulator would answer it (only genuine multi-touch
  does);
- quietly drop the mobile question because the gate felt like a no.

> **Studio MCP is live** (workspace Job 002, 2026-07-17). Registered via committed
> `roblox.workspace/.mcp.json`. Claude works in Studio directly; MCP writes execute arbitrary Luau in
> the open place, so Claude Code's tool-permission prompts gate them — Claude still describes any
> non-trivial or hard-to-reverse Studio change before applying it. **Always verify terrain/scene edits**
> by reading them back (`Terrain:ReadVoxels` / `inspect_instance`) **and** `screen_capture` before
> reporting done — never assume a `Fill`/edit worked. The Command Bar `studio-diagnostics` flow remains
> the **fallback** when MCP isn't connected (Studio closed, or exports too big for a tool call).

## 3. Building GUIs

- Each game owns its **design system** (colors, fonts, sizes, tokens) as a per-game skill (e.g.
  Defender's `roblox-gui`). Build UI to that game's system — never invent ad-hoc styling.
- Use the game's GUI builder agent/skill where one exists.
- New GUIs match the existing look of that game; if a token is missing, ask (via the wizard) rather
  than guessing brand values.

## 4. Generating models & assets

- **3D models / characters / enemies** — Meshy.ai text-to-3D:
  https://www.meshy.ai/workspace?model-tab=text-to-3d — use the `roblox-chars` agent for generation
  settings, prompt templates, rigging, export, and import fixes.
- **Icons** (UI, items) — Flaticon: https://www.flaticon.com/search?word=sword
- **Sound effects** — Pixabay: https://pixabay.com/sound-effects/search/purchase/
- Claude produces prompts/checklists and the integration code; the **human** does the actual
  generation, publishing, and import in Studio, then supplies IDs.

**Claude can also source assets directly via the Studio MCP — always present candidates for approval
before using them:**
- **Creator Store search** (`search_asset`) — find existing **models, meshes, images/decals, and
  audio** already on Roblox (free or paid), then `insert_asset`. Good for props, kits, SFX, music.
- **AI generation in Studio** — `generate_mesh`, `generate_material`, `generate_procedural_model`.
- **Upload** — `upload_image`/`store_image` for images the human made (e.g. **ChatGPT-generated art**,
  **Flaticon** icons) — hand Claude the file/ID and Claude wires it in.
- Human-preferred external sources stay: **Pixabay** (sound), **Flaticon** (icons), **ChatGPT (paid)**
  for design/art, **Meshy.ai** for custom 3D. Claude proposes → **human approves** → Claude integrates.
  Respect each source's license/attribution; Roblox moderates uploaded images/audio.

**🔴 STANDING RULE — who does what when an asset is needed (set 2026-08-20, applies to every project):**

When Claude concludes an asset is needed — a sound, a texture, a model, an icon — the sequence is fixed:

0. **Claude presents every asset request as a TABLE** (set 2026-08-21) — one asset per row, columns
   **Type** (sound/image/model/icon) · **Name** (the slot it fills) · **How to search** (exact terms and
   which source). Never prose per asset. Include candidate asset IDs in the table when the search already
   found some.
1. **Claude searches the asset market FIRST.** Our own registry and inventory, then the Creator Store via
   `search_asset`. Do not ask the human to go looking for something we may already own or that is one search
   away. "Try the market first" is not a suggestion; it is the first step.
2. **Claude plans the asset**, i.e. writes down *what is needed and why*: the slot it fills, how it will be
   driven at runtime, its length/loop/format requirements, and — critically — **what it must NOT contain**
   (e.g. rain must not have thunder baked in, because the two are levelled independently and anything baked
   in fires at the wrong moment).
3. **Claude suggests how to search for it** — the exact search terms, the source to try, and the acceptance
   criteria the human should judge a candidate against.
4. **The human finds and provides it.** They will supply ids.
5. **Claude wires it in, scans it, and logs it** in the shared registry.

The plan in step 2–3 is the deliverable, and it must be specific enough to search with. A request like
"we need a rain sound" is not usable; "a seamless 6–15 s rain-on-water loop, no thunder, no music, judged
under the live wind bed via the panel's audition tool" is.

**Leave the slot EMPTY rather than filling it with a placeholder.** A wrong sound or a stand-in texture is
much harder to notice than a missing one, and placeholders are how the wrong asset ends up shipping. Empty
slots must announce themselves (see `StormAudio.missing()`), and where possible be **auditionable at
runtime** so a candidate is judged in context rather than alone on a store page.

**Any question about an asset goes through the AskUserQuestion wizard, never prose.** See §1.

**Asset policy (mandatory — full workflow in the `roblox-assets` skill):**
- **Our assets first.** Search our own inventory + the game's **asset registry** before any public search.
- **Present before use.** Claude shows candidate assets (name/id/type/source/license) and **only uses one
  after the human approves it** — never insert into the live game or use an asset unverified.
- **Scan every inserted asset for scripts and delete any not needed.** Inserted Models can hide backdoor
  `Script`/`LocalScript`/`ModuleScript`s — scan (`GetDescendants` → `IsA("LuaSourceContainer")`) in
  isolation, delete anything Claude didn't author, and **never Play before scanning**.
- **Maintain the shared asset registry** — the single cross-project catalog at
  `roblox.workspace/Assets/registry/` (markdown per asset type) lists what we created vs used across all
  games (with ids/source/license/project/location), so we reuse before re-sourcing. Grep it before sourcing.

## 5. Job discipline

- Lifecycle: `intake.md` (what we plan) → `implementation-plan.md` (investigate, answer questions,
  list what's needed from the human, agree the approach) → implement → `final-summary.md` (what was
  implemented) + `changelog.md` (short, player-facing release note).
- **Implementation does not start until the implementation plan is agreed.**
- Scaffold with `python tools/job.py new --project <name> "Title" "Requirements"`.
- `changelog.md` is player-facing marketing copy (3–6 short bullets, one emoji per line, no code/file
  names). The technical detail lives in `final-summary.md`.

**Capture queues (each project has `todo/` and `findings/`):**
- **`todo/`** — quick tasks/thoughts/reminders, numbered `NNNN` (0000+), `Status: open → resolved`.
  Lighter than `Planned/` (future *features* that become Jobs).
- **`findings/`** — bugs noticed mid-flight but deferred, numbered `NNNN`, `Status: open → fixed`.
- Capture fast so nothing's lost: `job.py todo` / `job.py finding`; mark done with `job.py resolve`; see
  the queue with `job.py list <todo|finding> [--open]`. Promote anything that's real work into a **Job**.
  When you notice a bug you won't fix now, **log a finding** rather than dropping it.

## 6. Always-use skills

Before doing the matching work, Claude **must** consult the relevant skill rather than guessing:

- Any Luau / Roblox API / security / performance question → **`roblox-dev`** skill.
- Working inside a game → that game's **`<game>-project`** skill (architecture, sync rules, standards).
- Building/restyling UI → that game's GUI design skill.
- Adding content (enemy/weapon/quest/consumable) → that game's matching content skill.
- Setting or checking stats → that game's balance skill.
- Inspecting/fixing the live Studio session → **`studio-diagnostics`** skill.
- Meshy.ai model work → **`roblox-chars`** agent.

## 7. Verification discipline

Written after the Tide sea failure (jobs 028/029). Six rounds of "it's fixed now" were reported to the
user from screenshots that **could not have shown the bug**. Each rule below names the mistake it exists
to prevent, because a rule without its incident gets rationalised away.

### 🔴 Verify in gameplay, never in the editor

**The editor is for authoring. It is never evidence.** Edit does not run `LocalScript`s, so no client VFX
exists there, and anything created at runtime — VFX folders, terrain pasted from a `TerrainRegion`, spawned
props — is simply absent.

> **The incident.** A cloud-bank VFX drew ~129 sprites 340 studs from the camera, permanently, because its
> presence had a hardcoded floor and was never gated on the storm's distance. On the horizon they read as
> rectangular blocks. It is a **client** effect, so every Edit screenshot showed a clean sea. The user said
> "editor is fine, in game it sucks" — that sentence was the entire diagnosis, and it took far too long to
> act on it.

- Reproduce the symptom **in Play, at the reporter's camera angle**, before forming any hypothesis.
- ⚠️ **If Edit is the more convenient place to measure, treat that as a reason to distrust the result**, not
  a reason to use it. Convenience of measurement never outranks fidelity to the symptom.
- A level camera hides artefacts that a looking-down gameplay camera exposes. Match the real camera.

### 🔴 For any "works in X, broken in Y", diff the environments FIRST

Before any other investigation, enumerate what differs. "It looks fine in the editor" **is** this kind of
report. The checklist is cheap:

- client `LocalScript`s and the VFX they build
- instances created at runtime rather than saved in the place
- server-only systems, and anything driven by a tick
- `StreamingEnabled` and other place settings that only apply in-game

### 🔴 A verification must be able to fail

State what a failure would have looked like. If you cannot, the check is decoration.

> **The incident.** `tools/luau-analyze.sh` does `cd "$(dirname "$0")/.."`. A baseline built by writing
> `git show HEAD:<file>` into a temp directory and passing a *relative* path therefore analysed the repo's
> own working copy — the file was compared **against itself**, and "no new diagnostics" was reported twice
> from a check that was structurally incapable of failing. Pass absolute paths.

### Every visual change gets a before/after from the same camera

Keep the "before". Regressions in look are invisible without it.

> **The incident.** Water was brightened from 3.2% to 8.5% luminance to make a "sunny day". That collapsed
> the sea/sky value contrast, and value contrast is what the eye reads as texture and distance — so the sea
> appeared to stop a few hundred studs out. **The user found it, not Claude**, because Claude never compared
> against the pre-change state.

### Never assert a world fact from a constant — measure it

> **The incident.** `OCEAN_EXTENT_Z.min` said `-1000`; the water was actually filled to `-3070`. A visible
> world edge was reported to the user that does not exist. The `roblox-terrain` skill already said to measure
> rather than assume, and it was violated anyway.

### Two failed fixes for the same symptom → stop and re-open the diagnosis from zero

Including the question *"am I even in the right subsystem?"* Do not refine a theory that has already failed
twice; six consecutive rounds were spent inside a wrong frame (water colour, atmosphere, fog, streaming, a
mesh ocean) while the cause was a client script nobody had looked at.

### The user's words are the specification

A complaint repeated **unchanged** means Claude's model is wrong — not that the user missed the fix. When
someone says "the problem is the sea horizon" three times, stop substituting your own framing for theirs.

### Finding real bugs is not the same as finding the reported bug

> **The incident.** The investigation turned up genuinely dead levers — no sun disc in any sea state,
> `SunRaysEffect` enabled at intensity 0, a bloom threshold above anything on screen, no
> `ColorCorrectionEffect` at all. All real, all worth fixing, **and none of them was what the user reported.**
> Always ask explicitly: *does fixing this account for the symptom I was given?*

## 8. Agents on every job

**Every job uses at least one agent.** Not optional, not only when stuck.

- **Minimum:** one independent reviewer, given only the *symptom or requirement* and the repo — never
  Claude's hypothesis. Ask it what it would check first, and take the answer seriously when it disagrees.
- **Mandatory trigger:** after **one** failed fix, spawn a fresh-eyes agent **before** attempting a second.
- **Complex or stuck work:** several agents with deliberately different lenses (reproduce it / read the
  subsystem / attack the assumption).
- 🔴 **Do not tell the agent your theory.** The entire value is that it is not anchored to it. A reviewer
  handed the conclusion just confirms it.

**Why this is a standing rule.** The Tide sea failure was not a knowledge gap — the engine facts were all
measured correctly. It was a *structural* blind spot: verifying in the one environment where the bug could
not appear. Structural blind spots are invisible from the inside, which is precisely what a second pair of
eyes is for. A reviewer given only "the sea looks wrong in game, fine in editor" would very likely have
asked "why are you testing in Edit?" on the first pass.
