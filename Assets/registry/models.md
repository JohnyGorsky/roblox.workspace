# Models — shared catalog

All rows below are **our own uploads** (creator `johnygorsky10`, owned license, no third-party scan
needed). Pulled from inventory 2026-07-18 — **first 20 (search caps at 20/type; more exist — expand via
keyword search)**. Project tagged from names; `defender` = Roblox Defender (fantasy/combat). See [README](README.md).

| Name | rbxassetid | Project | Notes |
|------|------------|---------|-------|
| Boar (enemy rig) | reused from roblox.defender | jungle + defender | **Cross-game reuse, 0 credits.** R6 quadruped rig, 5 Motor6D with the SAME names as the Wolf, Humanoid, 3 bundled Sounds (`pig-noticed_me` 104582648268587, `pig-attack` 139588447817895, `pig-killed` 125997883726975). Jungle Job #078: `scale 0.778` -> 4.7x5.7x7.0 on a 4x3x7 hitbox, joint-swing gait (amplitude 0.5, 3.0 Hz - faster/shorter than the wolf, it trots). ⚠️ Its Motor6D C0/C1 do NOT match its part placement (Defender ships a `FixBoarMotor6DOffsets` patch for this) - `EnemyRig` now rebuilds the rest pose from the authored part CFrames at build time, so it no longer collapses to a 1.6-stud clump when unanchored. Also arrives wearing Defender's health-bar BillboardGui, which is stripped. |
| Wolf (enemy rig) | reused from roblox.defender | jungle + defender | **Cross-game reuse, 0 credits.** R6-style quadruped rig, 5 Motor6D (`Left/Right Hip`, `Left/Right Shoulder`, `Neck`), Humanoid + Animator, 2 bundled Sounds (`Sound` 1989743206, `Growl` 4064886644). Jungle Job #078: replaces the Panther as the riverbank land enemy, `scale 1.3`. **Ships NO animation ids** - its bundled `Animate` script drives joints off `Humanoid.Running`, which never fires for a PivotTo-driven creature, so the script is stripped at build and `EnemyRig` swings the joints instead. |
| WesternBandit (enemy rig) | reused from roblox.defender | jungle + defender | **Cross-game reuse, 0 credits.** Full R15 rig, 15 Motor6D, Humanoid + Animator, clothing/accessories, 6 bundled Sounds (EnemySpottedPlayer, EnemyScream1-4, Laugh1). Jungle Job #078: becomes every `CampGuard`. Plays Defender's standard animation ids on its own Animator - idle 123087002046013, run 913376220, hit 80792212061667. |
| Piranha (enemy) | Meshy 01a00695-9665-781f-896f-e5a203bc7a45 | jungle | Meshy-6 + PBR refine, ~1.2k tris, 0 scripts. `ServerStorage.AssetLibrary.Enemies.Piranha`, 2.24x3.41x7.60 studs. Job #078: `scale 0.526`, `yawOffset 0` (head at -Z; +Z pinches then flares to a zero-width caudal fin). Eye Attachments (+/-0.70, 0.85, -1.90). Source GLB `assets/Enemies/Piranha.glb`. **Deliberately SILENT** - see EnemyAssets. |
| RiverHippo (enemy) | Meshy 01a00695-d3b1-7951-adc0-7b939ba5a6a3 | jungle | Meshy-6 + PBR refine, ~3k tris, 0 scripts. `ServerStorage.AssetLibrary.Enemies.RiverHippo`, 6.04x6.70x11.40 studs. Job #078: `scale 1.053`, `yawOffset 0` (head at -Z; muzzle drops and there is a neck pinch at z=-2.76). Eye Attachments (+/-1.00, 2.90, -3.00). Shares the Crocodile's 5 sounds at wider rolloff. Source GLB `assets/Enemies/RiverHippo.glb`. |
| Aligator (crocodile enemy) | 83415039015970 | jungle | MeshPart mesh id, PBR via SurfaceAppearance, 0 scripts. `ServerStorage.AssetLibrary.Enemies.Aligator`. **RE-IMPORTED 2026-08-15 at 8.10x7.86x28.98** (was 7.10x4.00x20.68, a NON-uniform change) so `scale` is now 0.552 and the eye attachments were redone - re-measure if it changes again. `yawOffset 0` (head at -Z). `EyeLeft`/`EyeRight` Attachments at (+/-0.85, 3.74, -8.00) for the Job 039 glowing eyes - positions MEASURED by raycast cross-section, not eyeballed. |
| Lantern (camp practical) | Meshy 01a0074e-35ea-719a-8940-7646d992a016 | jungle | Meshy-6 + PBR refine, 1 MeshPart + SurfaceAppearance, 0 scripts. `ServerStorage.AssetLibrary.Props.Lantern`, ships **1.86x3.80x1.58**. Job #079: `CampDefs.SCALE.Lantern = 0.63` -> 2.39 studs, the FIXTURE for the two perimeter practicals at each camp; the `PointLight` sits 55% up it (`LIGHT.lanternFlame`). Stands on TOP of the sandbag wall — height MEASURED by `CampAmbience.mountFor`, never a constant (a `groundY + 5.30` constant floated every one by exactly 1.0 stud; see ASSETS.md §3.6). `CanCollide` off. Source GLB `assets/Objects/Ambient/Lantern.glb`. |
| LogJam (river obstacle) | Meshy 01a0074e-e117-7db5-8574-d7829511c679 | jungle | Meshy-6 + PBR refine, 1 MeshPart + SurfaceAppearance, 0 scripts. `ServerStorage.AssetLibrary.Props.LogJam`, ships **7.59x3.78x5.44**. Job #079: 4th `RiverBootstrap.OBSTACLES` type — `seatOn "float"`, `submerge 0.45`, slow **0.72** / damage **16** (between `Log` and `Rock`). ⚠️ Single-mesh obstacles are STRETCHED to the trigger box and then randomly yawed, so its trigger is **14x6x11** — within ~10% of the mesh's own proportions, which is what keeps it undistorted and readable from any angle. Art note: came back bleached/tidy rather than the mossy waterlogged tangle prompted for; **kept by user decision 2026-08-16**. Source GLB `assets/Objects/Ambient/LogJam.glb`. |
| GoldChest | Meshy 01a0074d-9ec4-7a36-b332-df39b73a665f | jungle | Meshy-6 + PBR refine, 1 MeshPart + SurfaceAppearance, 0 scripts. `ServerStorage.AssetLibrary.Props.GoldChest`, ships **9.44x7.36x11.40** (⚠️ bounding box inflated by coins scattered on the ground — the chest body is smaller). **NOT WIRED YET** — generated for "gold-chest buy-popup art", but `Theme.productIcon` already carries real transparent PNGs for all 4 gold packs and the shop draws flat images, not 3D. Candidate scale measured: **0.75** -> 7.08x5.52x8.55 (hero-sized beside a 2.90x4.60 `Barrel`). Source GLB `assets/GameObjects/Shop/GoldChest.glb`. |
| Meshy_AI heroic medieval knight (texture) | 138447940597211 | defender | Meshy character |
| Meshy_AI healing potion | 138075127153101 | defender | Meshy consumable |
| Meshy_AI dark cursed orb | 135371447340686 | defender | Meshy |
| Meshy_AI glowing translucent (orb) | 134798381581287 | defender | Meshy |
| Meshy_AI stylized ancient (statue?) | 134058433201609 | defender | Meshy |
| Meshy_AI Character_output | 133921737316240 | defender | Meshy character |
| Auto-setup character model | 133878447225239 | defender | rigged char |
| Meshy_AI Animation_Attack_withSkin | 133339186835381 | defender | skinned attack anim model |
| Meshy_AI fluffy tuft of white (sheep?) | 132381270331993 | defender | Meshy |
| Meshy_AI stylized wooden tree | 127939597000314 | defender | Meshy prop |
| Meshy_AI roblox-ready style le… (leaves?) | 127864360998133 | defender | Meshy |
| Meshy_AI roblox-ready style le… (leaves?) | 127615506994260 | defender | Meshy |
| Meshy_AI ornate skull (lowpoly) | 126541410856986 | defender | Meshy prop |
| Scene | 139941760439887 | defender? | Meshy scene export — verify |
| Scene | 132717810173375 | defender? | Meshy scene export — verify |
| Scene | 131813001000780 | defender? | Meshy scene export — verify |
| Scene | 131365139462063 | defender? | Meshy scene export — verify |
| Scene | 131290916613135 | defender? | Meshy scene export — verify |
| Scene | 129556472672203 | defender? | Meshy scene export — verify |
| Scene | 126694983926181 | defender? | Meshy scene export — verify |

## Third-party (Creator Store) — scanned before use

Free Creator Store inserts, **localized into a clean library** we duplicate from — so reuse doesn't
depend on the Store listing. **Script-scanned = 0 scripts** (foliage must have none). We always record
**where it lives in our folder**; the **origin rbxassetid only when known**. `Stored at` = library path
(lobby place). Row format: `Name | rbxassetid | Type | Project | Source | License | Stored at | Scanned? | Notes`.

| Name | rbxassetid (origin, if known) | Type | Project | Source | License | Stored at | Scanned? | Notes |
|------|------------|------|---------|--------|---------|-----------|----------|-------|
| PalmTall | 5031791950 | Model | jungle | Creator Store (Vupatu) | free | `ServerStorage/AssetLibrary/Foliage/PalmTall` | ✅ 0 scripts | chunky stylized palm; matched pair w/ PalmCurved |
| PalmCurved | 5031794668 | Model | jungle | Creator Store (Vupatu) | free | `ServerStorage/AssetLibrary/Foliage/PalmCurved` | ✅ 0 scripts | leaning variant |
| PalmLowPoly | 1436325105 | Model | jungle | Creator Store (LegendaryFrosts) | free | `ServerStorage/AssetLibrary/Foliage/PalmLowPoly` | ✅ 0 scripts | darker/thinner variant (2 MeshParts) |
| BushPack | 81654645105891 | Model | jungle | Creator Store (DoctorFir) | free | `ServerStorage/AssetLibrary/Foliage/BushPack` | ✅ 0 scripts | 8 MeshParts; broadleaf + small foliage + flowers |
| PalmCoconut | 18363394399 | Model | jungle | Creator Store (Trexlty) | free | `ServerStorage/AssetLibrary/Foliage/PalmCoconut` | ✅ 0 scripts | 4 MeshParts; ID confirmed by mesh-ID match |
| FernTall | — (origin unknown) | Model | jungle | Creator Store | free | `ServerStorage/AssetLibrary/Foliage/FernTall` | ✅ 0 scripts | 1 MeshPart; localized master (no origin ID) |
| JungleTreesPack | — (origin unknown, PSY0PZ) | Model | jungle | Creator Store (PSY0PZ) | free | `ServerStorage/AssetLibrary/Foliage/JungleTreesPack` | ✅ 0 scripts | 102 MeshParts; pre-arranged, rings the clearing. Dupe deleted. |
| RockA / RockB / RockC | 13967717089 | Model | jungle | Creator Store ("rocks 3", Yyyttrrrrre) | free | `ServerStorage/AssetLibrary/Rocks/*` | ✅ 0 scripts | Split from one oversized (771-stud) mesh into 3 rocks (S/M/L), scaled ~0.02. Placed on jungle floor + shore. |
| LogMossy | 18497743057 | Model | jungle | Creator Store ("AI Generated Mossy Tree Log", OptOff Studios) | free | `ServerStorage/AssetLibrary/Logs/LogMossy` | ✅ 0 scripts | Fallen log, scaled ~0.38 (~16 studs). Realistic/PBR moss — mild style clash but acceptable. |
| CrateWood | 3335320854 | Model | jungle | Creator Store ("military box", trimarkander) | free | `ServerStorage/AssetLibrary/Props/CrateWood` | ✅ 0 scripts | 66 parts (heavy) — use sparingly |
| AmmoBox | 12523523963 | Model | jungle | Creator Store ("AmmoKit", tqnk0) | free | `ServerStorage/AssetLibrary/Props/AmmoBox` | ✅ 0 scripts | olive ammo box, ~22 parts |
| Barrel | 3160087663 | Model | jungle | Creator Store ("Rusty Barrel", A_BoomStudio) | free | `ServerStorage/AssetLibrary/Props/Barrel` | ✅ 0 scripts | single rusty barrel, light (~6 parts) |
| BarrelsSet | 16944361687 | Model | jungle | Creator Store ("Barrels Ungroup", lennybox) | free | `ServerStorage/AssetLibrary/Props/BarrelsSet` | ✅ 0 scripts | barrel cluster, ~62 parts — 1–2 max |
| Tent | 7992921193 | Model | jungle | Creator Store ("Tent", Oneshot7577) | free | `ServerStorage/AssetLibrary/Props/Tent` | ✅ 0 scripts | olive canvas tent mesh (43-wide; placed at ~0.5) |
| SandbagWall | 119411292085005 | Model | jungle | Creator Store ("Sandbag wall", flensosten) | free | `ServerStorage/AssetLibrary/Props/SandbagWall` | ✅ 0 scripts | 1 mesh |
| SandbagBarrier | 78010383039337 | Model | jungle | Creator Store ("sandbag barrier", RuffyNic) | free | `ServerStorage/AssetLibrary/Props/SandbagBarrier` | ✅ 0 scripts | 18 mesh, ~15 wide |
| Plane (Meshy) | — (user Meshy) | Model | jungle | Meshy (user-generated) | n/a | `ServerStorage/AssetLibrary/Plane/Plane` + placed `Scenery.Plane` | ✅ 0 scripts | Olive cargo plane, 1 MeshPart, ~53×57. User-made + placed. CollisionFidelity=PreciseConvexDecomposition. |
| RangerTower | 81318418778699 | Model | jungle | Creator Store (DogZenith123) | free | `ServerStorage/AssetLibrary/Structures/RangerTower` | ✅ 0 scripts | Dark-wood watchtower, ~107 parts+21 unions. Placed @0.7 as Watchtower_NW/NE. |
| Dock | 3023220773 | Model | jungle | Creator Store ("Dock", Sxphies) | free | `ServerStorage/AssetLibrary/Structures/Dock` | ✅ 0 scripts | Wooden jetty ~32×13, 62 parts. Placed at east water; largest part renamed `Pier` for soundscape. |
| Pilot (Meshy) | — (user Meshy) | Model | jungle | Meshy (user-generated) | n/a | `workspace.Pilot` + `ServerStorage/AssetLibrary/Characters/Pilot` | ✅ 0 scripts | Skinned MeshPart `char1`, 22 bones, ~31k tris. AnimationController+Animator added; idle anim 71254620030056 (see animations.md) played by `PilotIdle.server.luau`. |
| BoatUpgrades station (Meshy) | — (user Meshy) | Model | jungle | Meshy (user-generated) | n/a | `Stations.BoatUpgrades` + `AssetLibrary/Structures/BoatUpgrades` | ✅ 0 scripts | Mechanic workbench rig. Swapped in for greybox; Station="BoatUpgrades" attr + Anchor/prompt transferred, grounded. |
| Bounties station (Meshy) | — (user Meshy) | Model | jungle | Meshy (user-generated) | n/a | `Stations.Bounties` + `AssetLibrary/Structures/Bounties` | ✅ 0 scripts | Swapped in for greybox; Station="Bounties" attr + Anchor/prompt transferred, grounded. |
| RobuxShop station (Meshy) | — (user Meshy) | Model | jungle | Meshy (user-generated) | n/a | `Stations.RobuxShop` + `AssetLibrary/Structures/RobuxShop` | ✅ 0 scripts | Wooden kiosk hut. Swapped in for greybox; Station="RobuxShop" attr + Anchor/prompt transferred, grounded, entry sign. |
| SkillTrainer station (Meshy) | — (user Meshy) | Model | jungle | Meshy (user-generated) | n/a | `Stations.SkillTrainer` + `AssetLibrary/Structures/SkillTrainer` | ✅ 0 scripts | Wooden stall, blue awning + chalkboard. Swapped in for greybox; Station="SkillTrainer" attr + Anchor/prompt transferred, grounded, entry sign. |

> **REJECTED (scan/weight):** `Jungle Trees Pack` (ClawWOMinerm, `119737242130790`) — carried a hidden
> `Script` ("PoseTexture" RunService/Lighting logic) + 3,335 parts. Deleted per scan rule; do not reuse.
> Also rejected (embedded scripts): `Low Poly Nature Pack` (NovaAquaStorm `92397845843006` — `CoreSkyboxSystem`;
> ZeroNeon `100428860346013` — `LightConfig`+2), `Lush Ivy Vine` (Bella `95095149446517` — PoseTexture/
> TextureConfiguration ×2), `Wall Vine` (`71567087607171` — LightConfig trio). `Mountain rocks`
> (`84900070002980`) degenerate bounds. Do not reuse.

---

### Jungle river-village huts — **Job #077, sourced 2026-08-05**

Creator Store, **all four from one author** (`Houseplant_Leaf`) so the set reads as one style — the
ASSETS.md §1.9 "one pack, one author" rule applied to props. Filipino *Bahay Kubo* stilt houses: a hut
raised on posts is what a river-village trading post actually looks like.

**Licence:** free, public. Description says *"Credits would be highly appreciated"* — attribution, not a
requirement. Add to the game's credits when there is one.

| Name | rbxassetid | Instances | Size (studs) | Notes |
|---|---|---|---|---|
| `BahayKubo1` | 6808910590 | 22 (16 part + 6 mesh) | 20×16×27 | |
| `BahayKubo2` | 6811407916 | 18 (10 part + 8 mesh) | 25×16×22 | |
| `BahayKubo5` | 10019841237 | 13 (9 part + 2 mesh + 2 union) | 30×22×34 | **best value** — largest footprint for fewest instances |
| `BahayKubo7` | 10031256291 | 95 (89 part + 4 mesh + 2 union) | 40×26×50 | ⚠️ heaviest by far; use once per village, not per camp |

**Localized** to `ServerStorage.AssetLibrary.Structures` in the GAME place.

#### SECURITY scan — passed, with a note worth keeping

`insert_asset` reported **`sandboxed: true` for #5 and #7** ("set Sandboxed property to true on all
scripts"), which reads like a script warning. A full descendant scan found **zero `LuaSourceContainer`,
zero RemoteEvent/RemoteFunction/BindableEvent, zero Tool, zero ClickDetector** in all four. So the flag
did not correspond to anything executable that survived insertion. **The lesson: the flag is not the scan.
Scan anyway** — and note that #1/#2 came back `sandboxed: false` while #5/#7 did not, so the flag does vary.

Cleanup applied on insert:
- **1 stray publisher `Camera` deleted from each** — Studio junk, not content.
- **`CollisionFidelity` → `PreciseConvexDecomposition`** on 15 instances across #1, #2 and #5. They shipped
  as `Default`, which on a house raised on stilts seals the underside — you could not walk beneath the
  floor, which is the entire reason the building is on stilts. (#7 already shipped Precise.)
- Everything forced `Anchored = true`.
