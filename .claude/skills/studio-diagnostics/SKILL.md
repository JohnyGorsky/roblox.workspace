---
name: studio-diagnostics
description: Generate Roblox Studio Command Bar utility scripts for any game in this workspace — chunked structure exports (object tree, GUI, model), property/issue diagnostics, and Meshy.ai imported-humanoid fix scripts (HipHeight, Motor6D reparent/offsets, anchoring, PrimaryPart). Use to inspect Studio state, debug a broken/invisible/jittering imported model, export a hierarchy to a file, or troubleshoot why a system isn't working in-game.
---

# Studio diagnostics & fix scripts

> **Prefer the Roblox Studio MCP when it's connected.** For inspecting/repairing a live Studio
> session, the MCP tools (`search_game_tree`, `inspect_instance`, `script_read`/`multi_edit`,
> `execute_luau`, `get_console_output`, `screen_capture`) are faster and need no human paste step.
> Use this Command Bar flow as the **fallback** — when MCP isn't connected (Studio closed, client not
> trusted) or when an export is too large to return through a tool call. The patterns below still
> apply either way (an export/diagnostic/fix can run just as well via `execute_luau`).

These are **one-shot scripts pasted into the Studio Command Bar** (View → Command Bar) — they are
NOT game code and don't sync. They read/repair the live Studio session and print to the Output
window. Claude generates them; the **human** pastes them and reports the Output back (Claude has no
Studio runtime). **Save any script worth keeping under the active job's `Jobs/NNN/` folder.** Use
`roblox-dev` for engine APIs; pair with the `roblox-chars` agent and the game's enemy skill when
fixing imported enemies.

## Categories

1. **Export** — dump an instance tree / GUI / model structure to Output (chunked to beat the line cap).
2. **Diagnostic** — walk a model/system, print properties, count issues/warnings, summarize.
3. **Fix** — apply known corrections to a broken import/config (Meshy humanoids especially).
4. **Check** — quick single-aspect verification (parts exist, sounds present, spawned correctly).

## The export→diagnose→fix→verify loop
Run an **export** → copy Output to a file → read it / plan → run a **fix** → run a **diagnostic** to
confirm → Play-test. Repeat if needed. (This is the loop behind most past mob/GUI jobs.)

## Pattern 1 — chunked export

The Output window truncates long dumps, so exports collect everything into a table, then print one
slice per run; you bump `CHUNK_NUMBER` and re-run until done.
```lua
-- ⭐ CHANGE THIS each run: 1, 2, 3, ...
local CHUNK_NUMBER = 1
local LINES_PER_CHUNK = 500          -- lower (300/200/100) if Output still truncates

local output = {}
-- ... walk the target tree, table.insert(output, "...") for each line ...

local total = #output
local startIdx = (CHUNK_NUMBER - 1) * LINES_PER_CHUNK + 1
local endIdx = math.min(startIdx + LINES_PER_CHUNK - 1, total)
print(string.format("CHUNK %d of %d (lines %d-%d of %d)",
    CHUNK_NUMBER, math.ceil(total / LINES_PER_CHUNK), startIdx, endIdx, total))
if startIdx > total then
    print("NO MORE CHUNKS")
else
    for i = startIdx, endIdx do print(output[i]) end
    print(endIdx < total and ("SET CHUNK_NUMBER = " .. (CHUNK_NUMBER + 1) .. " and run again")
                          or "ALL EXPORTED")
end
```
Use for: object tree, a GUI hierarchy (emit JSON-ish lines with properties — see the game's GUI
skill for its expected structure format), or a single model's parts/Motor6Ds.

## Pattern 2 — diagnostic checker

Walk the target, print grouped properties, and tally issues with an actionable summary.
```lua
local issues, warnings = 0, 0
local function check(ok, passMsg, failMsg)
    if ok then print("PASS: " .. passMsg) else print("FAIL: " .. failMsg); issues += 1 end
end

local model = workspace:FindFirstChild("<Target>")
check(model ~= nil, "<Target> exists", "<Target> not found")
if model then
    local hum = model:FindFirstChildOfClass("Humanoid")
    if hum then
        print(("[Humanoid] HipHeight=%s RigType=%s Health=%s")
            :format(hum.HipHeight, tostring(hum.RigType), hum.Health))
    end
    for _, p in ipairs(model:GetDescendants()) do
        if p:IsA("BasePart") then
            print(("%s  Anchored=%s CanCollide=%s Size=%s")
                :format(p.Name, tostring(p.Anchored), tostring(p.CanCollide), tostring(p.Size)))
        elseif p:IsA("Motor6D") then
            print(("Motor6D %s  Part0=%s C0=%s")
                :format(p.Name, p.Part0 and p.Part0.Name or "nil", tostring(p.C0.Position)))
        end
    end
end
print(issues == 0 and "ALL CHECKS PASSED" or ("INCOMPLETE — " .. issues .. " issue(s); fix above"))
```

## Pattern 3 — Meshy imported-humanoid fix

Imported (Meshy.ai) humanoids commonly break in a recurring way. Apply fixes in **this order** (the
proven sequence), then re-run a diagnostic:

1. **HipHeight** — set `humanoid.HipHeight` (legs hover/clip otherwise). Boar used `0.6`; tune per model.
2. **Motor6Ds parented to Torso** → reparent the joints (Neck, Hips, Shoulders) to `HumanoidRootPart`.
3. **Motor6D `Part0`** pointing at Torso → set `motor.Part0 = HumanoidRootPart`.
4. **Motor6D C0/C1 offsets** wrong → copy from a working reference rig of similar shape, OR compute
   from part geometry, OR restore known-good CFrames (last resort).
5. **`Torso.CanCollide = false`** (body shouldn't block the ground).
6. **`model.PrimaryPart = HumanoidRootPart`** (so `MoveTo`/CFrame work).
7. **Unanchor** all parts (`part.Anchored = false`) so physics/animation work.

```lua
local m = workspace:FindFirstChild("<ImportedModel>")
local hum = m:FindFirstChildOfClass("Humanoid")
local root = m:FindFirstChild("HumanoidRootPart")
hum.HipHeight = 0.6                                  -- (1) tune per model
for _, d in ipairs(m:GetDescendants()) do            -- (2)(3) move joints onto root, fix Part0
    if d:IsA("Motor6D") and d.Part0 and d.Part0.Name == "Torso" then
        d.Part0 = root
        d.Parent = root
    end
end
local torso = m:FindFirstChild("Torso"); if torso then torso.CanCollide = false end  -- (5)
m.PrimaryPart = root                                  -- (6)
for _, p in ipairs(m:GetDescendants()) do if p:IsA("BasePart") then p.Anchored = false end end -- (7)
print("Fix applied — re-run the diagnostic to verify")
```
**Generic vs model-specific:** steps 1, 2, 3, 5, 6, 7 generalize to any R6/imported humanoid. The
**C0/C1 offsets (step 4) are model-specific** — never copy Boar's exact CFrames to a different rig;
copy from a reference rig of the same body plan or compute from geometry.

> Note: a game's own spawn path (see its enemy skill / `roblox-chars`) typically handles the runtime
> anchor→settle→unanchor + disable-`Animate` flow for spawned mobs. These Command Bar fixes are for
> **fixing the saved template once** in Studio, before it's used by the spawner.

## Output & sync
- Scripts run in the **Command Bar**; copy the Output into a file under `Jobs/NNN/` if you need to keep it.
- Fixes mutate the **Studio** session — save the place / the affected server-only template so the
  change persists. Server-only template scripts still need the game's usual manual Studio handling.

## Verify
- [ ] Export: chunked, prints "SET CHUNK_NUMBER…" until "ALL EXPORTED"
- [ ] Diagnostic: prints grouped properties + an issue count + actionable summary
- [ ] Fix: applied in the documented order; offsets sourced per-model (not blindly copied); diagnostic re-run
- [ ] Script saved under `Jobs/NNN/` (not DiagnosticScripts); Studio session saved if a fix mutated it
