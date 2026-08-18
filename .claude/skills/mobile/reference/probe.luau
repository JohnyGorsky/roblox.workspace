--!nonstrict
-- probe.luau — the FIRST thing to run for any mobile question.
--
-- Studio: Test → Device → pick a phone preset → Play. Then paste this into `execute_luau` with
-- datamodel = **Client**. It answers, with real numbers, what a desktop Play session cannot:
--   · is touch actually on (desktop Play says NO, so touch UI never even builds)
--   · what GUI coordinate space the device really reports (NOT the screenshot's pixel size)
--   · how much canvas the safe-area insets actually leave
--   · where Roblox's OWN controls sit, so you can avoid them
--   · which of our elements collide with them, or with each other
--
-- ⚠️ Run it AFTER the HUD has been handed over (intro finished) and a few seconds beyond, or you will
-- measure a state that is about to be overwritten. See SKILL.md §7b.

local Players = game:GetService("Players")
local UserInputService = game:GetService("UserInputService")
local GuiService = game:GetService("GuiService")

local player = Players.LocalPlayer
local pg = player:WaitForChild("PlayerGui")
local cam = workspace.CurrentCamera
local out = {}

-- ── 1. the device ────────────────────────────────────────────────────────────────────────────────
table.insert(out, ("TouchEnabled      %s"):format(tostring(UserInputService.TouchEnabled)))
if not UserInputService.TouchEnabled then
	table.insert(out, "  ⚠️ NOT A TOUCH SESSION — turn the Device Emulator on. Everything below is meaningless.")
end
table.insert(out, ("Camera.ViewportSize  %d x %d   (aspect %.2f)")
	:format(cam.ViewportSize.X, cam.ViewportSize.Y, cam.ViewportSize.X / cam.ViewportSize.Y))
local i1, i2 = GuiService:GetGuiInset()
table.insert(out, ("GetGuiInset          top-left %d,%d   bottom-right %d,%d"):format(i1.X, i1.Y, i2.X, i2.Y))

for _, mode in ipairs({
	Enum.ScreenInsets.None,
	Enum.ScreenInsets.CoreUISafeInsets,
	Enum.ScreenInsets.DeviceSafeInsets,
}) do
	local p = Instance.new("ScreenGui")
	p.ScreenInsets = mode
	p.Enabled = false
	p.Parent = pg
	task.wait()
	table.insert(out, ("  canvas @ %-34s %d x %d  origin %s")
		:format(tostring(mode), p.AbsoluteSize.X, p.AbsoluteSize.Y, tostring(p.AbsolutePosition)))
	p:Destroy()
end

-- ── 2. what Roblox already owns ──────────────────────────────────────────────────────────────────
table.insert(out, "")
table.insert(out, "RESERVED BY ROBLOX (never put UI here):")
local reserved = {}
local tg = pg:FindFirstChild("TouchGui")
if not tg then
	table.insert(out, "  (no TouchGui — is the character loaded and touch on?)")
else
	for _, d in ipairs(tg:GetDescendants()) do
		if d:IsA("GuiObject") and d.Visible and d.AbsoluteSize.X > 20 and d.Name ~= "TouchControlFrame" then
			reserved[d.Name] = {
				x1 = d.AbsolutePosition.X, y1 = d.AbsolutePosition.Y,
				x2 = d.AbsolutePosition.X + d.AbsoluteSize.X, y2 = d.AbsolutePosition.Y + d.AbsoluteSize.Y,
			}
			table.insert(out, ("  %-24s x %4.0f..%4.0f   y %4.0f..%4.0f")
				:format(d.Name, d.AbsolutePosition.X, d.AbsolutePosition.X + d.AbsoluteSize.X,
					d.AbsolutePosition.Y, d.AbsolutePosition.Y + d.AbsoluteSize.Y))
		end
	end
end
-- TouchControlFrame is a FULL-SCREEN container, not a control — counting it makes every element look
-- like a collision. Excluded above on purpose.

-- ── 3. ours, as actually rendered ────────────────────────────────────────────────────────────────
local function shown(o)
	local c = o
	while c and c ~= pg do
		if c:IsA("GuiObject") and not c.Visible then return false end
		if c:IsA("ScreenGui") and not c.Enabled then return false end
		c = c.Parent
	end
	return true
end
local function paints(o)
	if not o:IsA("GuiObject") then return false end
	if o.BackgroundTransparency < 0.99 then return true end
	if o:IsA("TextLabel") or o:IsA("TextButton") or o:IsA("TextBox") then
		return o.Text ~= "" and o.TextTransparency < 0.99
	end
	if o:IsA("ImageLabel") or o:IsA("ImageButton") then
		return o.Image ~= "" and o.ImageTransparency < 0.99
	end
	return false
end

local mine = {}
for _, g in ipairs(pg:GetChildren()) do
	if g:IsA("ScreenGui") and g.Enabled and g.Name ~= "TouchGui" and not g.Name:match("^__") then
		for _, d in ipairs(g:GetDescendants()) do
			if paints(d) and shown(d) and d.AbsoluteSize.X > 0 then
				table.insert(mine, { owner = g.Name, name = d.Name, inst = d,
					x1 = d.AbsolutePosition.X, y1 = d.AbsolutePosition.Y,
					x2 = d.AbsolutePosition.X + d.AbsoluteSize.X, y2 = d.AbsolutePosition.Y + d.AbsoluteSize.Y,
					w = d.AbsoluteSize.X, h = d.AbsoluteSize.Y, tap = d:IsA("GuiButton") })
			end
		end
	end
end
table.insert(out, "")
table.insert(out, ("OURS: %d painted elements on screen"):format(#mine))

-- ── 4. collisions ────────────────────────────────────────────────────────────────────────────────
local function overlap(a, b)
	local ox = math.min(a.x2, b.x2) - math.max(a.x1, b.x1)
	local oy = math.min(a.y2, b.y2) - math.max(a.y1, b.y1)
	if ox > 0 and oy > 0 then return ox, oy end
	return nil
end

local hits = {}
for _, m in ipairs(mine) do
	for rn, r in pairs(reserved) do
		local ox, oy = overlap(m, r)
		if ox then
			table.insert(hits, ("  ⛔ %s/%s  vs ROBLOX %s   %.0fx%.0f"):format(m.owner, m.name, rn, ox, oy))
		end
	end
end
-- ⚠️ Compare EVERY pair, not just pairs from different ScreenGuis — an earlier version skipped
-- same-owner pairs and could not see two elements colliding inside one HUD. Then filter for the
-- overlaps that are actually bugs:
--   · skip ancestor/descendant (a child in its container is nesting)
--   · skip SIBLINGS inside one small component — a gauge's value text deliberately sits on its fill,
--     and a slot's key number deliberately sits on its art. Only flag pairs whose nearest common
--     ancestor is a top-level HUD block or the ScreenGui itself.
local function topBlock(o)
	-- the element's own top-level block within its ScreenGui
	local c = o
	while c and c.Parent and not c.Parent:IsA("ScreenGui") do c = c.Parent end
	return c
end
local seen = {}
for i = 1, #mine do
	for j = i + 1, #mine do
		local a, b = mine[i], mine[j]
		local ao, bo = a.inst, b.inst
		local nested = ao:IsDescendantOf(bo) or bo:IsDescendantOf(ao)
		local sameBlock = topBlock(ao) == topBlock(bo)
		if not nested and not sameBlock then
			local ox, oy = overlap(a, b)
			if ox and ox > 2 and oy > 2 then
				local k = a.owner .. "/" .. topBlock(ao).Name .. " <-> " .. b.owner .. "/" .. topBlock(bo).Name
				if not seen[k] then
					seen[k] = true
					table.insert(hits, ("  ⚠️ %s   %.0fx%.0f  [%s / %s]"):format(k, ox, oy, a.name, b.name))
				end
			end
		end
	end
end
table.insert(out, "")
table.insert(out, #hits == 0 and "COLLISIONS: none (ours vs ours, and ours vs Roblox's controls)" or "COLLISIONS:")
for _, h in ipairs(hits) do table.insert(out, h) end

-- ── 5. tap targets ───────────────────────────────────────────────────────────────────────────────
-- ⚠️ Scanned SEPARATELY from `mine`, and deliberately NOT filtered by `paints()`. A GuiButton with a
-- transparent background and no text still takes taps — Job #099's objectives tray header was a
-- transparent 150x32 TextButton covering its whole card, and it slipped through a paint-filtered audit
-- untouched. If it can be tapped, it must clear the floor, visible or not.
local FLOOR = 58
local small = {}
for _, g in ipairs(pg:GetChildren()) do
	if g:IsA("ScreenGui") and g.Enabled and not g.Name:match("^__") then
		for _, d in ipairs(g:GetDescendants()) do
			if d:IsA("GuiButton") and shown(d) and d.AbsoluteSize.X > 0
				and (d.AbsoluteSize.X < FLOOR or d.AbsoluteSize.Y < FLOOR) then
				table.insert(small, ("  %s/%s  %.0fx%.0f%s"):format(g.Name, d.Name,
					d.AbsoluteSize.X, d.AbsoluteSize.Y,
					d.BackgroundTransparency > 0.98 and "  (transparent — still tappable)" or ""))
			end
		end
	end
end
table.insert(out, "")
table.insert(out, #small == 0 and ("TAP TARGETS: all >= %d px"):format(FLOOR) or ("TAP TARGETS under %d px:"):format(FLOOR))
for _, s in ipairs(small) do table.insert(out, s) end

-- ⚠️ Anything sized imperatively by a script reports its LIVE value here and a stale one if you clone
-- it to simulate another viewport. Measure such elements in the emulator at each preset instead.
--
-- ⚠️ AND: this returns numbers, not judgement. `screen_capture` the same state and LOOK at it. Clipped
-- text, missing icons, placeholder art and "reads as an empty box" are all invisible here and obvious
-- in the picture. A clean report from this script is necessary, never sufficient.

return table.concat(out, "\n")
