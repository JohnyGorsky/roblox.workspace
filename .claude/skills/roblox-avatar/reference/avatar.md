# Roblox avatar: appearance, clothing, accessories, scaling & tools — reference

Sourced from official Creator Docs, current 2026-07. Not-verbatim items flagged **[unverified]**.

> **Deprecation:** prefer the **`Async`** appearance methods. `Humanoid:ApplyDescription()`,
> `ApplyDescriptionReset()`, `Players:GetHumanoidDescriptionFromUserId()`/`...FromOutfitId()` are
> deprecated in favor of `ApplyDescriptionAsync`, `ApplyDescriptionResetAsync`,
> `GetHumanoidDescriptionFromUserIdAsync`, `GetHumanoidDescriptionFromOutfitIdAsync`. (Guide samples
> still show old names; both work — new code uses Async.)

## 1. HumanoidDescription (the whole look in one object)

**Classic clothing/face:** `Shirt`, `Pants`, `GraphicTShirt`, `Face` (all number asset ids).
**Body parts:** `Head`, `Torso`, `LeftArm`, `RightArm`, `LeftLeg`, `RightLeg` (number);
colors `HeadColor`…`RightLegColor` (Color3).
**Scales (number):** `HeightScale`, `WidthScale`, `DepthScale`, `HeadScale`, `BodyTypeScale`,
`ProportionScale` (last two R15-only).
**Accessories (string, comma-separated asset ids):** `HatAccessory`, `HairAccessory`, `FaceAccessory`,
`FrontAccessory`, `BackAccessory`, `NeckAccessory`, `ShouldersAccessory`, `WaistAccessory`;
`AccessoryBlob` (layered/advanced data).
**Animations (number):** `Climb/Fall/Idle/Jump/Mood/Run/Swim/WalkAnimation`.
**Other:** `StaticFacialAnimation` (bool), `UseAvatarSettings` (bool).
**Methods:** `GetAccessories(includeRigid)` / `SetAccessories(list, includeRigid)` (entries
`{Order=, AssetId=, AccessoryType=}`), `AddEmote/RemoveEmote/GetEmotes/SetEmotes/Get/SetEquippedEmotes`.

**Humanoid:** `ApplyDescriptionAsync(desc, assetTypeVerification?)` (merge),
`ApplyDescriptionResetAsync(desc, ...)` (**resets to defaults first — clears anything not in desc**),
`GetAppliedDescription()`. **Players:** `GetHumanoidDescriptionFromUserIdAsync(userId)`,
`GetHumanoidDescriptionFromOutfitIdAsync(outfitId)`, `GetCharacterAppearanceInfoAsync(userId)`,
`CreateHumanoidModelFromDescriptionAsync(desc, Enum.HumanoidRigType.R15)` → a fresh rig Model (great for NPCs).

**Safe merge pattern:** `GetAppliedDescription()` → mutate the clone → `ApplyDescriptionAsync`. Don't
hand-edit Shirt/Pants instances *and* apply a description in the same frame.

## 2. Clothing (classic)

`Shirt.ShirtTemplate`, `Pants.PantsTemplate`, `ShirtGraphic.Graphic` (+ `.Color3`) — all ContentIds;
parent them into the character model. **Classic** = flat texture on body meshes (cheap). **Layered** =
3D `Accessory` mesh that wraps/deforms to any body shape and stacks (§3). Classic for simple/cheap;
layered for real garments that fit varied scales and stack.

## 3. Accessories & layered clothing

`Accessory` (inherits `Accoutrement`); property `AccessoryType` (Enum). Attaches via a `Handle`
BasePart with an `Attachment` whose name matches one on the character (HatAttachment, etc.) **[stub page — attach detail on Accoutrement]**.
`Enum.AccessoryType`: Unknown, Hat, Hair, Face, Neck, Shoulder, Front, Back, Waist, TShirt, Shirt,
Pants, Jacket, Sweater, Shorts, LeftShoe, RightShoe, DressSkirt, Eyebrow, Eyelash.
**Humanoid:** `AddAccessory(accessory)`, `RemoveAccessories()`, `GetAccessories()`.
**Layered clothing:** garments are Accessories whose Handle carries `WrapLayer` (wraps outward; props
`Enabled`, `Order`, `Color`, `AutoSkin`, `BindOffset`…) + `WrapTarget` cage on the body **[unverified]**.
Apply via `HumanoidDescription:SetAccessories(list, true)` or `AccessoryBlob`. For "give this catalog
look," prefer building a HumanoidDescription over hand-inserting Accessory instances.

## 4. Scaling (R15)

**A. HumanoidDescription scales** (§1) — one-shot, applied on ApplyDescription.
**B. Live `NumberValue` children of the Humanoid:** `BodyHeightScale`, `BodyWidthScale`,
`BodyDepthScale`, `HeadScale` (+ `BodyProportionScale`, `BodyTypeScale`) — changing them resizes body +
accessories live, **only if `Humanoid.AutomaticScalingEnabled = true`**. Use for runtime/tweened size.

## 5. Dressing characters (SERVER-side)

NPC = a Model with a Humanoid. Do it on the server.
```lua
-- A) clone a real avatar/outfit
local desc = Players:GetHumanoidDescriptionFromUserIdAsync(userId)  -- or ...FromOutfitIdAsync
npc.Humanoid:ApplyDescriptionAsync(desc)

-- B) build from scratch
local desc = Instance.new("HumanoidDescription")
desc.Shirt, desc.Pants = 855788007, 855789603
desc.HatAccessory = "2551510151,2535600138"
desc:SetAccessories({ {Order=1, AssetId=6984769289, AccessoryType=Enum.AccessoryType.Sweater} }, false)
npc.Humanoid:ApplyDescriptionAsync(desc)

-- C) spawn a new rig from a description (no premade model)
local model = Players:CreateHumanoidModelFromDescriptionAsync(desc, Enum.HumanoidRigType.R15)

-- Players, spawn already dressed:
Players.CharacterAutoLoads = false
Players.PlayerAdded:Connect(function(p) p:LoadCharacterWithHumanoidDescription(desc) end)
```
Classic clothing also works by parenting `Shirt`/`Pants` into the model; rigid accessories via
`Humanoid:AddAccessory(inst)`.

## 6. Tools (giving & equipping items)

`Tool` props: `RequiresHandle` (bool — needs a child BasePart named exactly **`Handle`**;
without one the tool drops on equip), `CanBeDropped`, `Enabled`, `Grip`/`GripPos`/`GripForward`/
`GripRight`/`GripUp` (CFrame/Vector3), `ToolTip`, `ManualActivationOnly`, `TextureId` (backpack icon)
**[unverified name]**. Methods `Activate()`/`Deactivate()`. Events (fire on the **client** for the
holder): `Equipped(mouse)`, `Unequipped()`, `Activated()`, `Deactivated()`.

**Containers:** `StarterPack` (Tools copied into every player's Backpack on spawn); `StarterGear`
(per-Player; copied to Backpack on spawn — persists across respawns for that player); `Backpack` (live
inventory; the equipped tool reparents into the Character while held).

**Give / equip / remove:**
```lua
local t = ReplicatedStorage.WaterSpell
t:Clone().Parent = player.Backpack       -- available now
t:Clone().Parent = player.StarterGear    -- re-granted each respawn
player.Character.Humanoid:EquipTool(toolInstance)   -- force-equip
player.Character.Humanoid:UnequipTools()            -- put away
tool:Destroy()                                       -- remove from inventory
```
`RequiresHandle=false` → no world model (ability/inventory items); drive everything from events.
Deprecated: `HopperBin`/`Flag` — use `Tool` **[unverified]**.

## 7. Gotchas & best practices

- **Server-side** for appearance + tool grants (they replicate authoritatively). Tool *input* events
  fire in a LocalScript inside the Tool → use a LocalScript for input + RemoteEvent to a server Script
  for authoritative effects (per `roblox-scripting` security).
- **Timing:** apply after the character/Humanoid exists (`CharacterAdded` + wait for Humanoid), or use
  `CharacterAutoLoads=false` + `LoadCharacterWithHumanoidDescription`. `CharacterAppearanceLoaded` fires
  when the default look finishes loading **[unverified]**.
- **Async methods yield & can error** → wrap `Get...Async`/`ApplyDescriptionAsync` in `pcall`.
- `ApplyDescriptionResetAsync` wipes anything not in the desc; `ApplyDescriptionAsync` merges — choose deliberately.
- Performance: each rigid accessory = extra parts/attachments; layered clothing adds deform cost. Keep
  accessory counts modest on crowds; `CreateHumanoidModelFromDescriptionAsync` once, then clone identical NPCs.

## Sources
classes/{HumanoidDescription, Humanoid, Players, Tool, Shirt, Pants, ShirtGraphic, Accessory, WrapLayer,
StarterGear, StarterPack, Backpack}, enums/AccessoryType, characters/appearance, players/tools,
tutorials/.../create-player-tools.
