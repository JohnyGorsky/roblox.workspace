# Images / decals / icons — shared catalog

Our own uploads (`johnygorsky10`, owned). Pulled 2026-07-18 — **first 20 (more exist)**. Mostly Meshy
PBR texture maps (`Material_*`, NormalMaps) + a few named. Likely Defender. See [README](README.md).
(No `Decal`-type assets found in inventory.)

| Name | rbxassetid | Project | Notes |
|------|------------|---------|-------|
| **BoatInfo** | **113207367236651** | **jungle** | "HOW TO USE THE BOAT" infographic — deposit in the centre area, fuel station, repair station. Uploaded by the user 2026-08-18 for Job #098's landing-zone sign. Wide ~16:9. |
| iron_armor_transparent_v3 | 139087440968888 | defender | armor UI/texture |
| knight_pants | 137273386338288 | defender | clothing texture |
| Developer Product Image Asset | 137143700075888 | defender | dev product icon |
| Meshy_AI Roblox-ready bone pillar (texture) | 139802119746368 | defender | Meshy texture |
| Meshy_AI ruined two-story medieval (texture) | 135902718090023 | defender | Meshy texture |
| Generated NormalMap | 140350034709597 | defender? | PBR normal map |
| Texture | 137550338421387 | defender? | generic — identify |
| Material_0.001 | 140728827009274 | defender? | Meshy PBR map |
| Material_0.001 | 140621996578063 | defender? | Meshy PBR map |
| Material_0.001 | 139958905147562 | defender? | Meshy PBR map |
| Material_0.001 | 139247375524099 | defender? | Meshy PBR map |
| Material_0.001 | 138518855074908 | defender? | Meshy PBR map |
| Material_0.001 | 138342921959654 | defender? | Meshy PBR map |
| Material_0.001 | 138105847758159 | defender? | Meshy PBR map |
| Material_0.001 | 137249905823294 | defender? | Meshy PBR map |
| Material_0.001 | 136091918577698 | defender? | Meshy PBR map |
| Material_1 | 139795932112986 | defender? | Meshy PBR map |
| Material_1 | 136604350619537 | defender? | Meshy PBR map |
| Material.001 | 136510985700654 | defender? | Meshy PBR map |
| Material.001 | 136201028229092 | defender? | Meshy PBR map |

## Jungle / Last River — our uploads. Added 2026-07-20 (Job #064)

| Name | rbxassetid | Project | Notes |
|------|------------|---------|-------|
| LoadingBackground | 73636751330777 | jungle | loading-screen key art. Used as `BG_FALLBACK` in `lobby/.../LobbyLoading.local.luau` + `sync/.../GameLoading.local.luau`; a `ReplicatedFirst.LoadingBackground` ImageLabel in the place overrides it |

### Lobby UI icon set (jungle) — uploaded 2026-07-30. Source PNGs: `assets/Images/Icons/`

Flaticon set for the lobby GUI (ASSETS.md §1.9). All 23 verified in Studio 2026-07-30 (`GetProductInfo`
→ name match, AssetTypeId 1 = Image). **These are full-color flat icons, not mono silhouettes** — so
`ImageColor3` tinting does not apply (it multiplies and would muddy them); color is baked in.

| Name | rbxassetid | Role in the GUI |
|------|------------|-----------------|
| close | 140590179467868 | panel close button (all 4 lobby panels) |
| coin | 77292050689166 | Gold currency chip + every cost row |
| shop | 113169065974317 | ROBUX SHOP button / station sign |
| star | 123611506595607 | major (gold) skill · SkillTrainer sign |
| wrench | 90679964955780 | utility skill · BoatUpgrades sign |
| user_group | 103042204848069 | the 4 party pads · PARTY button |
| calendar | 78068320446462 | WEEKLY OBJECTIVES |
| check | 108692155956143 | CLAIMED / OWNED / MAX states |
| target_bounty | 106187109040565 | Bounties station sign |
| cogwheel_gear | 94903113819644 | engine (`motors`, `motor2`) |
| shield | 111545806353192 | hull (`hull`, `hullkit`) |
| fuel-station | 128001249531842 | fuel (`diesel`, `fueltank`, `refuel`) |
| box_Create | 123909056802404 | storage (`cargo`, `trailer`) |
| tools | 109933399936454 | equipment (`repair`) |
| motorboat | 79958224084386 | "Boat" skill group header |
| navy_crew | 108066459106452 | "Crew" skill group header |
| ship-wheel | 124599807882020 | `rudder` (Rudder Tuning) |
| first-aid-kit | 87252065857781 | `medic` (Combat Medic) |
| machine-gun | 120983452101559 | `gun`, `gunupgrade` |
| spotlight | 111067444220887 | `searchlight` (Searchlight Rig) |
| money-bag | 121749397596257 | `scavenge` (Scavenger's Instinct) |
| winner_trophy | 72442029972402 | weekly-objective score reward |
| roblox | 100088930369566 | R$ price rows |

### Trading-post ammo icons (jungle) — uploaded 2026-08-23 (Job #104), game place

Source PNGs: `roblox.jungle.game/assets/Images/`. **Verified in Studio 2026-08-23** —
`MarketplaceService:GetProductInfo(id, Enum.InfoType.Asset)` returned a name match and AssetTypeId **1**
(Image) for both, creator `johnygorsky10`. Full-colour flat, matching the sets above (no `ImageColor3`).

| Name | rbxassetid | Theme key | Role in the GUI |
|------|------------|-----------|-----------------|
| clip | 98656594796808 | `pistolAmmo` | "Pistol Ammo" row, dock/village trading post |
| bullets | 107222226747372 | `shotgunAmmo` | "Shotgun Ammo" row, dock/village trading post |

⚠️ Deliberately **not** the existing `ammoBox` crate glyph: that one is the BOAT TURRET's ammo (cargo
chip, gunner readout, and the row now named "Turret Ammo"). Handheld ammo and turret ammo are separate
pools, and one shared icon across three rows is what made the turret row read as "the ammo" in the first
place — the confusion Job #104 was raised to fix.

### Monetization icons (jungle) — uploaded via Creator Hub product/pass thumbnails, 2026-07-20

Uploading a product/pass thumbnail also mints a normal owned image asset, so these **are** usable in-game
(`rbxassetid://…`) for shop rows. Art source: `roblox.jungle.game/assets/Images/Purchase/`. Mapping verified
2026-07-30: gold packs via Studio `MarketplaceService:GetProductInfo(id, Enum.InfoType.Product).IconImageAssetId`
(all 4 MATCH), passes via `apis.roblox.com/game-passes/v1/<id>/product-info`.

| Name | rbxassetid | Project | For (product/pass ID) |
|------|------------|---------|-----------------------|
| 10 Gold icon | 121862847548970 | jungle | dev product `3610663250` (`10.png`) |
| 25 Gold icon | 95542160791148 | jungle | dev product `3610663288` (`25.png`) |
| 60 Gold icon | 74400053482366 | jungle | dev product `3610663341` (`60.png`) |
| 150 Gold icon | 80233861953394 | jungle | dev product `3610663385` (`150.png`) |
| Armored Boat pass icon | 138728521842994 | jungle | game pass `1919001295` (`Boat.png`) |
| Boat Paint Pack pass icon | 70530350071757 | jungle | game pass `1919355255` (`Paint.png`) |
| Cosmetic Bundle pass icon | 130780112255781 | jungle | game pass `1918077339` (`Cosmetics.png`) |

#### Transparent-PNG versions — **use these IN-GAME** (uploaded 2026-07-31, verified in Studio)

The Creator Hub thumbnails above are matted onto an opaque square/disc, so they render as a white blob
behind the art inside a round badge. These alpha-channel re-uploads are what `Theme.productIcon` points
at; the Hub ids stay above because they're what the store listings themselves display.

| Name | rbxassetid | Project | For |
|------|------------|---------|-----|
| 10_transparent | 72255341573939 | jungle | dev product `3610663250` |
| 25_transparent | 114957317211525 | jungle | dev product `3610663288` |
| 60_transparent | 100983946600429 | jungle | dev product `3610663341` |
| 150_transparent | 133943328068949 | jungle | dev product `3610663385` |
| Boat_transparent | 130910653087108 | jungle | game pass `1919001295` |
| Paint_transparent | 82416796032835 | jungle | game pass `1919355255` |
| Cosmetics_transparent | 95212286807985 | jungle | game pass `1918077339` — ⛔ **pass removed from the in-game shop, Job 067** |
| SelfRevive | 131281323216251 | jungle | dev product `3612677893` (uploaded 2026-08-01) |
| Game Pass Icon | 130798210334331 | jungle | game pass `1935044952` Extra Inventory Slots (2026-08-02). Hub thumbnail, but **has alpha** — verified in Play, used directly in-game, no transparent re-upload needed |

> `Developer Product Image Asset` `124951966292519` (same 2026-08-01 batch) is the Creator Hub's own copy
> of the Self Revive thumbnail. Use `131281323216251` in-game — the Hub copy is matted, like the pass
> thumbnails above.

> Superseded pass-icon uploads (10:13 PM batch, replaced by the 10:15 PM ones): `119971224828477`,
> `77302146173024` — do not use.

---

### In-run HUD icon set — **⏳ PENDING, Job #075 (2026-08-02), game place**

The game place's HUD was rebuilt on the design system in Job #075. The **"Lobby UI icon set" above
already covers most of it** — all five role glyphs (`ship-wheel` / `machine-gun` / `fuel-station` /
`tools` / `first-aid-kit`), plus coin, shield, box, check, close, trophy, motorboat, shop, roblox. The
16 below are what has **no honest substitute**.

**⚠️ Source from the SAME Flaticon author as the Lobby UI icon set** (ASSETS.md §1.9: *"one pack, one
author — mixed packs are the #1 way an icon set looks amateur"*). Full-colour flat, matching that set.

**Nothing is broken while these are missing.** Each key exists in `Theme.icon` with an empty id and is
listed in `Theme.iconPending`; `Components.iconId` substitutes the fallback below, so the HUD renders at
the right size and reads correctly in a screenshot. `Theme.reportPendingIcons()` prints the outstanding
list on every Studio start.

| # | Icon wanted | Theme key | Placeholder | Used by | Priority |
|---|---|---|---|---|---|
| 1 | Scrap / salvage pile | `salvage` | `crate` | Salvage currency chip | required |
| 2 | Metal plate / girder | `metal` | `tools` | cargo chip | required |
| 3 | Ammo box / bullets | `ammoBox` | `gun` | cargo chip, dock shop, gunner readout | required |
| 4 | Heart | `heart` | `medkit` | player health bar | required |
| 5 | Machete / sword | `machete` | `tools` | hotbar slot (Sword) | required |
| 6 | Pistol | `pistol` | `gun` | hotbar slot, dock shop | required |
| 7 | Bandage | `bandage` | `medkit` | bandage chip, dock shop | required |
| 8 | Checkered / finish flag | `flag` | `bounty` | END marker on the river bar | required |
| 9 | Warning triangle | `warning` | `bounty` | boat-under-attack strip | required |
| 10 | Sun | `sun` | `star` | DAWN banner | required |
| 11 | Moon | `moon` | `star` | NIGHTFALL banner | required |
| 12 | Skull | `skull` | `crew` | downed overlay, spectate tag, crew-lost result | required |
| 13 | Shotgun | `shotgun` | `gun` | hotbar slot, dock shop | optional |
| 14 | Rope / knot | `rope` | `tools` | untie / cast-off button | optional |
| 15 | Map pin | `pin` | `fuel` | dock pin on the river bar, zone banner | optional |
| 16 | Clipboard | `clipboard` | `check` | objectives tray header | optional |

**To land one:** paste the `rbxassetid://` into `Theme.icon`, then delete that key's row from BOTH
`Theme.iconPending` and `Theme.iconFallback` — and copy `Theme.luau` to the other tree, since
`sync/ReplicatedStorage/UI/` and `lobby/sync/ReplicatedStorage/UI/` are byte-identical by contract.

**Needs no asset:** the steer/throttle glyphs `◀ ▶ ▲ ▼` render in Builder Sans.

## MAGNET SWEEP — kit material maps (job 004, 2026-08-29)

32 PBR maps generated by Roblox's in-Studio AI material generator for the eight `MaterialVariant`s of
the factory kit. Listed by variant rather than one row each, because they are only ever used as a set.
**Full detail, tiling values and regeneration notes: `roblox.magnet-sweep/assets/registry/materials.md`.**

| Variant | Project | ColorMap | MetalnessMap | RoughnessMap | NormalMap |
|---|---|---|---|---|---|
| MS_Grate | magnet-sweep | 100119051349971 | 132053598171455 | 78256880787920 | 137375523932036 |
| MS_HazardStripe | magnet-sweep | 103050299200645 | 117906733335492 | 134330463575716 | 83184191742997 |
| MS_PaintedGloss | magnet-sweep | 111026565076154 | 87609501643080 | 123751890194778 | 89586080218274 |
| MS_PaintedWorn | magnet-sweep | 124108636299304 | 114284043803829 | 79490079202981 | 124715682578441 |
| MS_Rubber | magnet-sweep | 74703843274122 | 140307446791387 | 90679658033575 | 137841782403441 |
| MS_Rust | magnet-sweep | 81056345994054 | 99395386129739 | 102414771701915 | 103451965489156 |
| MS_SteelBrushed | magnet-sweep | 116298729078775 | 83981204598228 | 115986479017417 | 110127036576212 |
| MS_SteelDark | magnet-sweep | 135097875820869 | 87513260802763 | 93359546170082 | 79095706302185 |

Created by us, owned by `johnygorsky10`. These properties are `PluginSecurity` on read, so no runtime
script can recover them from the place — this table is the only record outside the `.rbxl`.

## MAGNET SWEEP — loading screen plate (job 015, 2026-08-31)

| Asset | Id | Source |
|---|---|---|
| Loading-screen backdrop | `88620361473282` | `roblox.magnet-sweep/assets/generated/loading-backdrop.png` |

**Not generated — derived from art we already owned.** `assets/concept_art/Arena.png` downscaled to
640 x 360, Gaussian-blurred at radius 16 and darkened to 42 % brightness with PIL, then uploaded via
the Studio MCP's `upload_image`.

⚠️ **`upload_image` only accepts http/https URLs**, not local paths. The working route is a throwaway
`python -m http.server` bound to `127.0.0.1` in the asset directory, then passing the localhost URL.
Kill the server afterwards.

**Reproducible**: the source PNG is in git, so the exact plate can be rebuilt and re-uploaded without
guessing at the blur values. Used by `studio_game/ReplicatedFirst/BootScreen.local.luau`.


## Workspace / standalone (added 2026-09-06, Job #013)

Nightweave body PBR set - a **SurfaceAppearance** on the source MeshPart, not a plain TextureID.

| Name | rbxassetid | Project | Notes |
|------|------------|---------|-------|
| Nightweave ColorMap | 130215752622606 | inventory (workspace) | SurfaceAppearance.ColorMap, 2K. Cyan glow is painted into albedo - there is **no emissive map**, so it does not actually emit. Use a Highlight or PointLight for real glow. |
| Nightweave NormalMap | 97856583270635 | inventory (workspace) | SurfaceAppearance.NormalMap, 2K |
| Nightweave MetalnessMap | 121252940941051 | inventory (workspace) | SurfaceAppearance.MetalnessMap, 2K |
| Nightweave RoughnessMap | 103664110001347 | inventory (workspace) | SurfaceAppearance.RoughnessMap, 2K |

## Magnet Sweep / Scrap Sweeper PBR (imported 2026-09-13, game Job 023)

Owner-generated Meshy assets, imported by owner. SurfaceAppearance bindings;
TextureID is empty. Source masters are 2048 square; live decoded copies inspected
at 1024 square. Original imports are in `ServerStorage.GuardianSourceImports`.

| Part | ColorMap | NormalMap | MetalnessMap | RoughnessMap |
|---|---|---|---|---|
| Body | 96054821549988 | 139450593979299 | 140721649448864 | 77394837853258 |
| Wheel (reused twice) | 110529437656435 | 99562938106107 | 139045191543267 | 134734516735547 |
| Brush | 88928107249950 | 135249936229030 | 119688159797977 | 111796109405863 |

Actual Play rendering and independent decoded-map samples checked. The
instance-based loading probe passed all 15 unique mesh/map IDs. Recovery preserves
every map binding in `roblox.magnet-sweep/Jobs/023/guardian.snapshot.json`.
See that job's `guardian-assembly-results.md` for evidence and limits.
