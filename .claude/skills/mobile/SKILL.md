---
name: mobile
description: Mobile/touch UI engineering for any Roblox game in this workspace — how to MEASURE a phone layout instead of guessing (the Device Emulator gives real TouchEnabled, real ViewportSize, real safe-area canvas and Roblox's own TouchGui rects), the screen regions Roblox reserves for its thumbstick/jump button, why pixel MinSize floors break on high-DPI devices, the ways UI measurement silently lies, and thumb-zone/tap-target principles. Use BEFORE building or fixing any HUD, menu, control or layout that a phone player will see, and whenever asked "does this work on mobile".
---

# Mobile & touch — measure, don't guess

Companion to `roblox-ui` (generic UI engineering) and `roblox-studio` (the emulator + MCP). This skill is
the **mobile-specific** layer: what a phone actually reports, what Roblox already owns on that screen, and
the failure modes that cost Jobs #094–#099 four rounds of rework.

**The one-line lesson:** every mobile bug in those jobs came from *reasoning about* a phone layout instead
of *measuring* one. The emulator was available the whole time.

---

## 1. FIRST ACTION, ALWAYS: get the real numbers

Do this **before** designing, and before saying anything needs a real device.

**Test → Device** in Studio, pick a phone preset, Play, then run the probe in
[reference/probe.luau](reference/probe.luau) via `execute_luau` (datamodel: **Client**).

It reports, all real:

| Reading | Why it matters |
|---|---|
| `UserInputService.TouchEnabled` | **Desktop Play reports `false`** — touch-only branches never run, so touch UI is never even built. Measuring mobile there measures nothing. |
| `Camera.ViewportSize` | The device's **GUI coordinate space** — see §2, this is the one that bites. |
| `GuiService:GetGuiInset()` | The real top-bar inset (measured **58 px**; older docs still say 36). |
| A `ScreenGui`'s `AbsoluteSize` per `ScreenInsets` mode | The **usable canvas**, which is smaller than the viewport. |
| `PlayerGui.TouchGui` children | **Roblox's own controls**, with real rectangles (§3). |

## 2. ⚠️ ViewportSize is NOT the screenshot's pixel size

Measured on a phone preset: **`ViewportSize` = 666 × 374**, usable **666 × 316** after insets — while the
device screenshot was ~1536 × 710.

**Consequence: a pixel value is ~2.3× larger relative to the canvas than any desktop test suggests.**

This is what broke Job #095: a `UISizeConstraint.MinSize` of 420 px, tuned against a desktop-sized
viewport so five thumb-sized badges would fit, became **~80% of the usable canvas** on a phone and pushed
the nav rail up under the Roblox topbar.

**Rules that follow:**

- **A hard pixel floor is a bug waiting for a device.** Size from the canvas
  (`gui.AbsoluteSize`), cap as a *fraction* of it, and let the element degrade gracefully:
  `prefer 58 px → accept 44 px → never exceed ~60% of canvas height`.
- Recompute on `AbsoluteSize` change, so orientation changes and the emulator are handled for free.
- Aspect-ratio testing does **not** reveal this. Only reading `ViewportSize` on a touch canvas does.

## 3. The screen is not all yours — Roblox reserves these

Measured on a 666 × 316 usable canvas. **No in-house overlap harness knows these exist unless you tell it.**

| Roblox control | Rect | Meaning |
|---|---|---|
| `ThumbstickStart` | x 29..103, y 223..297 | movement |
| `DynamicThumbstickFrame` | x −100..266, y 105..416 | **the whole bottom-left quadrant is movement** |
| `JumpButton` | x 571..641, y 226..296 | bottom-right |
| Top bar inset | 58 px off the top | menu/chat/voice |

**Therefore, on touch:**
- **Bottom-left belongs to movement.** Never put a control or readout there.
- **Bottom-right belongs to jump** (and, in our games, the fire button).
- **The top-left is usually free** and is the natural home for a glanceable vitals column.
- Anything the player *presses* wants the bottom band; anything they *glance at* can go up top.

⚠️ **Measure against `DynamicThumbstickFrame`, NOT `ThumbstickStart`.** `ThumbstickStart` is only the
stick's *resting dot* (74×74). The dynamic thumbstick **spawns wherever the thumb lands**, so the real
reservation is the frame — which on a 666-wide canvas runs to **x = 266**, more than twice as far right.
Job #099 moved the hotbar to x=150 measured against the resting dot, verified it "clean", and it was
still inside the live stick area. Diff against **every** `TouchGui` child, not the one that looks like
the control.

Always diff your UI against `TouchGui` rects, not just against your own elements.

## 4. What lies to you when measuring UI

All four verified during #095/#097/#099 — each produced a confident, wrong number:

1. **A cloned GUI does not run its runtime code.** Anything sized imperatively by a script (a `resize()`
   bound to `AbsoluteSize`, a `layoutCluster()`) keeps the pixel value the *live* session had and reports
   the same number at every simulated viewport.
2. **Forcing hidden children `Visible = true` changes `UIListLayout` flow.** Hotbar slots measured
   57×57 that way; they are really 76×76. Enable the **`ScreenGui`** only — a panel's own children are
   already in their natural visible state.
3. **`TextLabel.TextFits` is unreliable on an off-screen clone.** Text that measured "fits" was plainly
   clipped on the device.
4. **A `MaxSize` written for one layout silently strangles another.** A 110 px width cap meant for a
   narrow rail collapsed a new multi-column overlay to 110 px wide.

5. **A checker that only compares ACROSS ScreenGuis has a blind spot the size of a HUD.** Job #099's
   first version skipped any pair sharing an owner (`if a.owner ~= b.owner`), so two elements colliding
   *inside* `BoatHud` — vitals against cargo, say — could never be reported. It printed "zero
   collisions" while measuring a fraction of the screen. **Compare every painted element against every
   other**, then filter deliberately.
6. **But a naive "any overlap is a bug" check is worse than useless — it cries wolf.** Intentional
   layering is everywhere: a gauge's `Value` text sits *on* its `Fill`; a hotbar slot's `Key` number
   sits *on* its `Art`. Skipping ancestor/descendant pairs is **not enough**, because those are
   *siblings*. The working rule: **only flag a pair whose nearest common ancestor is a top-level HUD
   block or higher.** Two things inside one small component are composition; two components on top of
   each other are a bug.

**So:** an offline harness is trustworthy for **static rectangle collisions** and little else. Text fit,
script-sized elements and anything touching CoreGui must be measured **live in the emulator** — and a
surprising number gets re-measured a second way before you act on it.

## 4a. Three more ways a check passes while the screen is wrong

7. **A tap-target scan must include TRANSPARENT buttons.** Filtering by "does it paint" is right for
   overlap and wrong for tap size: a `GuiButton` with a clear background and no text still takes taps.
   The objectives tray's `Header` was a transparent 150×32 `TextButton` covering its whole card — under
   the 58 px floor, and invisible to a paint-filtered audit. **If it can be tapped, it must clear the
   floor, visible or not.**
8. **A pixel `MinSize` silently overrides a scale change.** Narrowing a card's `Size` to `0.10` did
   nothing because a `UISizeConstraint.MinSize = (150, 32)` clamped it straight back. The property you
   edited *was* correct; something else won. **After changing a size, read back `AbsoluteSize`** — never
   assume the value you wrote is the value that renders.
9. **Measure in the state the problem was REPORTED in.** A tray was measured and screenshotted while
   `Visible = false` — the numbers looked fine and the picture showed nothing, and neither meant
   anything. **Confirm the element is actually on screen before believing either.** State coverage is
   part of verification, not a bonus.

## 4b. ⚠️ NUMBERS ARE NOT ENOUGH — LOOK AT THE SCREEN

Every "verified clean" claim in Job #099 that later turned out wrong was wrong *numerically first*: the
script said pass, and the screenshot said otherwise. **Do both, every time:**

1. `screen_capture` the state you just changed.
2. **Actually read the image** — is any text cut mid-word? is anything half off an edge? does a control
   sit where a thumb goes? do two panels visibly touch?
3. Then run the measurement to get exact rectangles for whatever the eye flagged.

A number tells you *how much*; only the picture tells you *whether it looks broken*. Clipped text,
missing icons, placeholder art and "reads as an empty box" are all invisible to a rectangle checker and
obvious in one screenshot. **If you are reporting a mobile layout as done and you have not looked at a
picture of it, you have not verified it.**

## 5. Text: it wraps, it does not shrink forever

`TextScaled` has a **`MinTextSize` floor** (12 px in our `Components.applyText`). Below that, text
**cannot** shrink out of a box that is too small — it **wraps**, and the overflow is simply cut.

So narrowing a panel to fix a horizontal collision can silently clip it vertically. Job #095 narrowed a
hint panel 0.44 → 0.32 to clear a top bar; the title then wrapped to two lines in a one-line box and
shipped severed mid-sentence.

**Check both:** after any width change, verify the label still has room for the number of lines it now
wraps to. "It no longer collides" is not "it still reads".

## 6. Researched principles (external, and they agree with the above)

- **Tap targets:** 44 pt (iOS) / 48 dp (Android) is the floor. **We use 58 px as our own stricter
  target** for gameplay controls, degrading to 44 only when the canvas genuinely cannot hold it. Make the
  *hit area* larger than the visual if they must differ.
- **Thumb zones:** the bottom and bottom-corners are the reachable "prime" zone; the top is hardest to
  reach. Primary actions belong low, readouts belong high — which is exactly what §3's reservations force
  anyway.
- **Scale, not offset** for position and size; `UIAspectRatioConstraint` to stop distortion;
  `UISizeConstraint` to clamp — but see §2 about pixel floors.
- **`ScreenInsets = CoreUISafeInsets`** for interactive UI (notches, Dynamic Island, top bar);
  `None` only for full-bleed non-interactive art.
- **Declutter aggressively.** Small screen + two thumbs = anything non-essential is in the way. Prefer
  collapsed panels and one-shot hints over persistent chrome.
- ⚠️ **Draw what the player HAS, not what they could have.** The single biggest space win in Job #099
  was not resizing anything — it was rendering only *populated* hotbar slots instead of every *unlocked*
  one. Six boxes (four of them empty rectangles with a number in them) forced a two-row block taking
  **9.5%** of the screen; showing the two items actually carried made it one row at **2.9%**, with the
  slots still at full 58 px. On desktop the empty slots are a harmless advertisement of inventory you
  own; on a phone they are the layout problem. **Before shrinking a component, check whether some of it
  should be on screen at all.**
- **Feedback on every tap** — colour change, small scale tween, sound.
- **Landscape vs portrait:** decide and enforce. Locking one orientation removes an entire class of
  layout failure; do it via `PlayerGui.ScreenOrientation` from a synced script (a property set on
  `StarterGui` lives only in the `.rbxl` and is invisible to git).

## 7. Multi-touch — the ONE thing the emulator cannot do

The emulator is **single-pointer**. "Two thumbs at once" needs real hardware. Everything else on this page
is answerable at your desk.

Related trap: **`MouseButton1Down`/`Up`/`MouseLeave` do not support multi-touch.** Roblox routes only the
*first* active touch through mouse emulation, so a second finger on a second button may never register.
For any control that can be held simultaneously with another, track a per-`InputObject`
`InputBegan`/`InputEnded` pair, plus a service-level `UserInputService.InputEnded` fallback so a finger
that slides *off* the button still releases it.

## 7b. Hiding something on mobile: gate where the DECISION is made

Hiding a HUD element on touch failed **three times in a row** in Job #099 before it stuck. Each failure
is a different mechanism and all three are common in this codebase:

1. **`gui.Enabled = false` at construction** — overwritten by the script's own state driver, which
   unconditionally re-enables the element every time it runs.
2. **Gating inside that driver** — still overwritten, because `IntroHudGate` keeps a list of HUD
   ScreenGuis, hides them for the cold open, then calls `setHudEnabled(true)` when the intro ends. The
   driver never ran again, so the gate never re-fired.
3. **An early `return` placed after `Components.screen(...)`** — the ScreenGui already existed, so
   `IntroHudGate:FindFirstChild(name)` still found it and switched it on.

**What works: return BEFORE anything is created.** If the ScreenGui never exists, nothing can re-enable
it. Check what else touches your element by name (`grep` the HUD lists) before assuming one flag is enough.

**And verify at the right MOMENT.** An earlier "verified hidden" reading was taken *during* the intro,
before the hand-over fired — it was true and meaningless. Wait for the HUD to be handed over, then wait
a few seconds more, then measure.

## 8. Checklist before calling any mobile work done

- [ ] Measured in the **Device Emulator**, not reasoned about.
- [ ] `ViewportSize` and usable canvas recorded; no hard pixel floor sized against a desktop viewport.
- [ ] Diffed against **`TouchGui`** rects, not just our own elements.
- [ ] Bottom-left kept clear for movement; bottom-right clear for jump/fire.
- [ ] Every tap target ≥ 58 px (or a documented, deliberate 44).
- [ ] Text re-checked for **wrapping/clipping** after any width change.
- [ ] Touch-only changes gated on `UserInputService.TouchEnabled` so desktop cannot regress.
- [ ] Anything hidden on mobile: confirm the information still reaches the player somewhere.
- [ ] Only multi-touch deferred to hardware — nothing else.

## 9. Case history (why each rule exists)

| Job | What went wrong | Rule it produced |
|---|---|---|
| #094 | `UIListLayout.SortOrder` defaults to **`Name`**; buttons named from glyphs rendered `▶` before `◀`, so steering was inverted on every phone | Never rely on name order; set `SortOrder` **and** `LayoutOrder` |
| #094 | Touch buttons on `MouseButton1*` — two thumbs did not work | §7 |
| #095 | 420 px `MinSize` = 80% of a phone canvas | §2 |
| #095 | Narrowed a panel to fix a collision, clipped its text | §5 |
| #095/#097 | Harness reported stale/forced sizes as fact | §4 |
| #097 | Shared `Components.button` floor at 34 px left real-money buy buttons untappable | §6 tap targets |
| #099 | Our rail sat on top of Roblox's thumbstick | §3 |
| #099 | Moved the hotbar clear of `ThumbstickStart` — still inside `DynamicThumbstickFrame` | §3 |
| #099 | Six 58 px slots don't fit the bottom band between stick (x266) and fire (x526) — wrapped to 3×2 | §3 + §6 |
| #099 | …then found 4 of those 6 were EMPTY slots; drawing only carried items took it from 9.5% to 2.9% of screen | §6 |
| #099 | Spent four jobs deferring to "a real phone" with the emulator one click away | §1 |
| #099 | Hiding a HUD element on touch took three attempts — construction flag, then driver gate, then early return | §7b |
| #099 | "Verified hidden" was measured during the intro, before the re-enable fired | §7b |
| #099 | "Zero collisions" from a checker that skipped same-ScreenGui pairs | §4.5 |
| #099 | Reported layouts as clean from numbers alone; the screenshots showed clipped text and empty-looking buttons | §4b |
| #099 | A transparent 150×32 button escaped the tap audit because it did not paint | §4a.7 |
| #099 | Narrowed a card's Size; a `MinSize` clamp put it straight back | §4a.8 |
| #099 | Measured and screenshotted a tray that was `Visible = false` | §4a.9 |
