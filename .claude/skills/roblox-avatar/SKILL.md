---
name: roblox-avatar
description: Roblox character appearance & equipment for any game in this workspace — dressing characters/NPCs (HumanoidDescription, classic Shirt/Pants, accessories, layered clothing), character scaling, and Tools (Handle, equipping, Backpack/StarterPack/StarterGear, giving/removing items). Use before writing/reviewing anything that dresses a character, customizes avatars, spawns dressed NPCs, or gives/equips tools/weapons.
---

# Roblox avatar: dressing characters & giving tools

Full API in [reference/avatar.md](reference/avatar.md). This is the working guide. Do appearance + tool
grants **server-side** (they replicate authoritatively).

## Dress a character (HumanoidDescription is the one-shot way)

`HumanoidDescription` holds a whole look: `Shirt`/`Pants`/`GraphicTShirt`, body part ids + colors,
`*Scale` fields, comma-separated accessory strings (`HatAccessory`…`WaistAccessory`), animation ids.
Prefer the **`Async`** methods (the non-Async ones are deprecated):
```lua
-- copy a real avatar/outfit
local desc = Players:GetHumanoidDescriptionFromUserIdAsync(userId)   -- or ...FromOutfitIdAsync
npc.Humanoid:ApplyDescriptionAsync(desc)
-- or build from scratch (Shirt/Pants + SetAccessories{ {Order=,AssetId=,AccessoryType=} , ... })
-- or spawn a fresh rig: Players:CreateHumanoidModelFromDescriptionAsync(desc, Enum.HumanoidRigType.R15)
```
Safe edit = `GetAppliedDescription()` → mutate clone → `ApplyDescriptionAsync`. `ApplyDescriptionAsync`
**merges**; `ApplyDescriptionResetAsync` **wipes** anything not in the desc. Wrap Async calls in `pcall`.
Spawn players pre-dressed: `CharacterAutoLoads=false` + `Player:LoadCharacterWithHumanoidDescription(desc)`.

## Clothing & accessories

- **Classic** (cheap texture): `Shirt.ShirtTemplate`, `Pants.PantsTemplate`, `ShirtGraphic.Graphic` —
  parent into the model. **Layered** (3D garments that wrap/stack, fit any body): Accessories with
  `WrapLayer`; apply via `HumanoidDescription:SetAccessories(list, true)`.
- `Humanoid:AddAccessory(inst)` / `RemoveAccessories()` / `GetAccessories()`. `Enum.AccessoryType`
  (Hat/Hair/Face/…/Jacket/Sweater/Shorts/LeftShoe/…). Keep accessory counts modest on crowds/NPCs.

## Scaling (R15)

HumanoidDescription scale fields for one-shot; or live `NumberValue` children of the Humanoid
(`BodyHeightScale`/`BodyWidthScale`/`BodyDepthScale`/`HeadScale`) **with `Humanoid.AutomaticScalingEnabled=true`**
for runtime/tweened resizing.

## Tools (give & equip items)

A `Tool` needs a child BasePart named exactly **`Handle`** (or set `RequiresHandle=false` for
ability/inventory items with no world model — drive it purely from events). Props: `CanBeDropped`,
`Enabled`, `Grip*`, `ToolTip`, `TextureId` (backpack icon), `ManualActivationOnly`.
**Input events fire on the CLIENT** (in a LocalScript inside the Tool): `Equipped(mouse)`, `Unequipped`,
`Activated`, `Deactivated` → use a LocalScript for input + RemoteEvent to a server Script for
authoritative effects (see `roblox-scripting`).
```lua
tool:Clone().Parent = player.Backpack      -- available now
tool:Clone().Parent = player.StarterGear   -- re-granted each respawn
player.Character.Humanoid:EquipTool(tool)  -- force-equip;  :UnequipTools() to put away
tool:Destroy()                             -- remove from inventory
```
`StarterPack` = tools for everyone each spawn; `StarterGear` = per-player, survives respawn; `Backpack`
= live inventory. Deprecated: `HopperBin` — use `Tool`.

## Timing & pitfalls

Apply appearance/tools after the character exists (`CharacterAdded` + wait for Humanoid). Async methods
yield/error → `pcall`. Don't hand-edit Shirt/Pants instances *and* apply a description in the same frame.
