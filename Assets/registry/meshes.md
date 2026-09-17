# Meshes / MeshParts — shared catalog

Our own uploads (`johnygorsky10`, owned). Pulled 2026-07-18 — **first 20 (more exist)**. Mostly generic
Meshy mesh geometry with default names (`Mesh_0`, `Mesh1.0`, `char1`, `mesh`) — **need identifying/renaming**
to be reusable. Likely Defender. See [README](README.md).

| Name | MeshId | Project | Notes |
|------|--------|---------|-------|
| char1 | 140462614439629 | defender? | Meshy char geometry |
| char1 | 133110221747894 | defender? | Meshy char geometry |
| Mesh0 | 139789890117773 | defender? | generic — identify |
| Mesh0 | 131968998492029 | defender? | generic — identify |
| Mesh1.0 | 139205996159601 | defender? | generic — identify |
| Mesh1.0 | 136139623333385 | defender? | generic — identify |
| Mesh1.0 | 133911491369254 | defender? | generic — identify |
| Mesh1.0 | 132212733948860 | defender? | generic — identify |
| Mesh1.0 | 129930376371454 | defender? | generic — identify |
| Mesh_0 | 138273915327879 | defender? | generic — identify |
| Mesh_0 | 136457112671624 | defender? | generic — identify |
| Mesh_0 | 136424108139596 | defender? | generic — identify |
| Mesh_0 | 135362823540180 | defender? | generic — identify |
| Mesh_0 | 130142682098348 | defender? | generic — identify |
| Mesh_0.001 | 136410369508802 | defender? | generic — identify |
| Mesh_0.001 | 135486754993460 | defender? | generic — identify |
| mesh | 132624490770255 | defender? | generic — identify |
| mesh | 131151328831282 | defender? | generic — identify |
| mesh | 130065095214037 | defender? | generic — identify |
| mesh | 129275866852991 | defender? | generic — identify |

## Jungle / Last River — boat parts (Job #066, 2026-08-01)

Meshy image-to-3D from the ChatGPT concept renders in `roblox.jungle.game/assets/Images/Boat/`. Imported
as MeshParts into **`ServerStorage/AssetLibrary/BoatParts/`** in each place (ServerStorage is place content
— Rojo does not sync meshes, so the game place needs its own import of the same GLBs).

**The mesh id is not how the game finds these** — `ReplicatedStorage.Boat.BoatParts` clones them **by
child name**, because `MeshPart.MeshId` cannot be written at runtime. Renaming a library part breaks the
boat; these ids are recorded for re-import and traceability.

| Library name | MeshId | Texture (SurfaceAppearance ColorMap) |
|---|---|---|
| BowLight | 91153379103503 | 72102968129139 |
| CargoDeck | 121083381228019 | 119081266186647 |
| DriverSeat | 92120079364409 | 140610533419505 |
| FuelTank | 113505197391374 | 115431947897232 |
| GunBarrel | 138785726504897 | 100500739458123 |
| GunBarrelHeavy | 105379146957646 | 125399060972623 |
| GunBase | 83630637675983 | 111010550488859 |
| GunSeat | 126708341359233 | 85901689715275 |
| FuelStation | 97274117345322 | 139253829174682 |
| Hull | 89521912881313 | 81439616488445 |
| HullPlate | 109319594296029 | 78389231815302 |
| MedicStation | 117730471003292 | 132698765638109 |
| Motor | 93982818285882 | 128752134878843 |
| RepairStation | 125616975055918 | 103397061424892 |
| SearchLightHead | 127871044013620 | 86825455345521 |
| CargoRacks | 133551732172203 | 74860403316923 |
| RampBow | 130643201140870 | 109947758749150 |
| SearchlightMast | 110987057092036 | 111425767337644 |

> ⚠️ **`SearchLightHead` has a capital L.** `BoatParts` matches that spelling exactly; do not "fix" it in
> one place without the other.
>
> **Job #067 added 3 more (2026-08-02):** `CargoRacks` (the `trailer` module — replaced a fabricated
> greybox slab), `RampBow` (the new `ramps` module) and `SearchlightMast` (was a plain grey pole).
> `SearchlightMast` is a chunky riveted PEDESTAL on purpose — a 0.8-stud pole is the geometry Meshy
> reconstructs worst. `RampBow` imported with a SQUARE footprint (4.21 x 1.20 x 4.21), so it is placed low
> on the foredeck and passes *under* the gun mount rather than in front of it.
>
> **All 15 imported (2026-08-01).** `Motor2` reuses the `Motor` mesh (it is the same engine mirrored), and
> crew seats reuse `GunSeat` — so 15 meshes cover 17 part slots.
>
> **Deliberately NOT meshes:** the searchlight **mast** (a 0.8-stud pole reconstructs badly; stays a Studio
> part) and any **cargo trailer/barge** (there is no towed body — cargo lives on the rear `CargoDeck`).
>
> ⚠️ **These are imported into the LOBBY place only.** `ServerStorage` is place content and Rojo does not
> sync meshes, so the GAME place needs its own import of the same GLBs
> (`roblox.jungle.game/assets/Images/Boat/Objects/`) under the same names.

## Jungle / Last River — LOBBY hero props (recorded 2026-08-02, Job #069)

Found by the Job #069 lobby asset inventory. These are **user Meshy uploads imported straight into the
LOBBY place**, and until now their ids were recorded **nowhere but the `.rbxl`** — not here, not in
`ASSETS.md`, not in any script. Lose the place file and there was no way back to them; the GAME place
could not reuse them either. That is the gap this section closes.

Like the boat parts above, **the mesh id is not how the game finds these.** Scripts bind to stations by
the `Station` **attribute** (`LobbyStations`, and since Job #074 the GAME place's `StartShopServer` too),
never by mesh or model name — so the two misspellings below are harmless. The ids are recorded for
**re-import and traceability**.

> ⚠️ **A station mesh dropped into a place imports with `CollisionFidelity = Box`.** On the Robux Shop
> hut (15 × 18.8 × 20) that is an invisible 20-stud cube — the counter and the space under the eaves are
> sealed and you cannot walk up to it. Set `PreciseConvexDecomposition` **in Edit and save the place**;
> a runtime script cannot write the property. Caught on the game-place copy in Job #074.

| In-place name | MeshId | What it is | Where |
|---|---|---|---|
| `Plane` | 118873896425222 | Cargo plane — the airfield landmark | `Scenery.Plane` · `AssetLibrary/Plane` |
| `char1` | 108352617907497 | **The Pilot NPC body** (22-bone rig; idle anim `71254620030056`) | `workspace.Pilot` · `AssetLibrary/Characters/Pilot` |
| `SkillTrainer` | 107408955523438 | Skill Trainer stall (blue awning + chalkboard) | `AssetLibrary/Structures/SkillTrainer` |
| `Boutnies` ⚠️ *(sic)* | 119564283624615 | **Bounties** stall — misspelled in the place | `AssetLibrary/Structures/Bounties` |
| `RobuxhShop` ⚠️ *(sic)* | 81119390187013 | **Robux Shop** kiosk — misspelled in the place. **Used in BOTH jungle places** (Job #074) | LOBBY `AssetLibrary/Structures/RobuxShop` · GAME `Workspace.SpawnBase.Stands.RobuxShop` |
| `BoatUpgrade` | 118860073556013 | Boat Upgrades mechanic rig at the dock | `AssetLibrary/Structures/BoatUpgrades` |
| `RunWay` | 114620021340964 | Airstrip tile — **6 instances**, z −154 → −485 | `Scenery.RunWay` ×6 · `AssetLibrary/Plane/RunWay` |
| `Mesh1.0` ❓ | 139814217941669 | **UNIDENTIFIED** — generic Meshy name, someone should look at what it actually is. Distinct from the `Mesh1.0` Defender ids at the top of this file | lobby place |

Each carries a full `SurfaceAppearance` (ColorMap + Normal + Roughness + Metalness) from the Meshy
import — those map ids are not listed individually; re-importing the mesh brings them.

> ⚠️ **LOBBY place only**, same caveat as the boat parts: `ServerStorage` is place content and Rojo does
> not sync meshes, so the GAME place needs its own import.
>
> Full context — every id the lobby uses, and what transfers to the GAME place:
> `roblox.jungle.game/LOBBY-ASSET-INVENTORY.md`.

## MAGNET SWEEP — the player's hero magnet (job 016, 2026-08-31)

The magnet the player carries. Generated with Meshy **from the game's own key art**, not from a
prompt: `assets/concept_art/Logo2.png` → crop → `image_to_image` (isolate on plain grey) →
`image_to_3d` (meshy-7, PBR, 2K, triangle, remesh to 8k).

| Asset | Id |
|---|---|
| Mesh | `117205352084553` |
| ColorMap | `86179837697259` |
| NormalMap | `137866197232825` |
| MetalnessMap | `80189603883950` |
| RoughnessMap | `132128183093036` |

**8,021 triangles · 1.9031 × 1.7924 × 0.5396 studs · `AlphaMode = Overlay`.**
Local **+X is the open end** (the chrome pole faces); local **+Y is the RED arm**, −Y the **CYAN**
arm. Verified by photographing the imported mesh at identity rotation beside a marker cube, not by
trusting the exporter.

🔴 **Why this table matters.** `SurfaceAppearance` maps **cannot be written by a script** — the write
fails with *"lacking capability Plugin"* in a real `LocalScript`, even though it succeeds from the
command bar (`roblox.magnet-sweep/docs/PITFALLS.md` #63). So the textured `MeshPart` is authored in
the editor and lives in `ReplicatedStorage.MagnetMesh` inside the `.rbxl`. **This table is the only
record of those ids outside the place file** — exactly as for the `MaterialVariant` maps above.
`Config.Magnet.MESH` carries them too, for rebuilding.

Source files: `roblox.magnet-sweep/assets/generated/magnet-v2/` (GLB) and `magnet-ref-v2.png` (the
image the mesh was built from).

### Superseded: v1, the crane-mounted magnet

| Mesh | ColorMap | NormalMap | MetalnessMap | RoughnessMap |
|---|---|---|---|---|
| `86157306292256` | `109787130538997` | `138863826664865` | `81566437829958` | `113031954681661` |

Built from `Robot.png`, where the magnet hangs off a robot arm — so its pole faces are **capped by a
crane mount** and it is all-red rather than the red + cyan the style guide and the game's own logo
both call for. Wrong object for a hand prop. Kept in the place as
`ReplicatedStorage.MagnetMesh_v1_craneMount` and on disk at `assets/generated/magnet/`.


## Magnet Sweep / collectible scrap (verified 2026-09-13, game Job 023)

Existing owner-generated/imported Meshy assets, not new purchases or imports.
Each `ServerStorage.ImportedMeshes.<name>` contains one textured MeshPart and no
scripts. Runtime `ScrapMeshPool` clones that part directly under `Workspace.Scrap`;
`ScrapSpec.mesh` names the template. Preserve these names and native proportions.
The textures below are `TextureID`, not SurfaceAppearance ColorMap bindings.

| Template | MeshId | TextureID |
|---|---|---|
| bead | 74569087922881 | 100160542963496 |
| washer | 119906234344638 | 135746242970372 |
| screw | 127423414316621 | 110317630475066 |
| nut | 86635625770592 | 81381021406972 |
| bolt | 71325276750015 | 80685746271196 |
| spring | 82185162635099 | 106995717053635 |
| gear | 70619800931195 | 87074942083197 |
| pipe | 137115916578352 | 132361584447457 |
| block | 135756743579726 | 116487463119349 |
| windup | 101614295152317 | 101346650869515 |
| toycar | 86293891189362 | 117668295562086 |
| toyrobot | 120629952351811 | 81855496919651 |

Disk sources: `roblox.magnet-sweep/assets/generated/scrap/`. Floor 1 uses the first
eight types; all twelve bindings passed the isolated pool test. The disk/import
audit is `roblox.magnet-sweep/Jobs/023/asset-import-audit.md`. Its one unimported
gantry crane remains optional and was not imported for this work.

## Workspace / standalone (added 2026-09-06, Job #013)

| Name | MeshId | Project | Notes |
|------|--------|---------|-------|
| mesh (Nightweave source body) | 81520046220289 | inventory (workspace) | **Ours, Meshy meshy-7 image-to-3D.** Single unrigged T-pose body, 10441 tris, 4.77 x 4.95 x 0.96 studs at import scale factor 2.6. The pre-Auto-Setup source for NightWaveMan (75637982489690). Carries a SurfaceAppearance, not a TextureID. |

## Magnet Sweep / Scrap Sweeper Guardian (generated 2026-09-13, game Job 023)

Owner imported all three approved GLBs and authorized assembly. All imports and
the assembled prefab contain **zero scripts**, scanned before Play. Owner approved
concept, modular split and 90 credits. All three Meshy tasks succeeded for exactly
90 credits; balance 1,470. No paid retries or extra processing. Owner's Meshy Pro
generation; original GLBs and reference PNGs preserved.

| Name | Roblox ID | Project | Source | Stored at | Scan / status |
|---|---|---|---|---|---|
| Scrap Sweeper static body | 88805956145384 | Magnet Sweep | Meshy 01a09ad9-dc99-745c-a38d-67f17e436f70; local cleanup | roblox.magnet-sweep/assets/generated/guardian/body-import.glb | 0 scripts; 5,012 tris; assembled |
| Scrap Sweeper reusable wheel | 75795598576104 | Magnet Sweep | Meshy 01a09ad9-ea5a-72ed-833f-863ed52b32fb | roblox.magnet-sweep/assets/generated/guardian/wheel.glb | 0 scripts; 1,046 tris; reused twice |
| Scrap Sweeper brush roller | 89525706022226 | Magnet Sweep | Meshy 01a09b4a-f554-727f-9bd6-2dc1b574cfaf; local radial barrel/subdivision repair | roblox.magnet-sweep/assets/generated/guardian/brush-import-v3.glb | 0 scripts; 2,198 tris; earlier candidates rejected |

Full provenance, file hashes, preparation scripts and review evidence:
roblox.magnet-sweep/Jobs/023/guardian-asset-results.md and
assets/generated/guardian/README.md. Keep separate component scales and mount axes;
Studio imports include a baked 180-degree Y rotation plus recentering, already
compensated in the assembly. Full-sweep clearance and desktop player-camera
idle/alert checks passed. Mobile measurement remains open.
Eye and beacon are separate authored Roblox components, not new Meshy files.
Independent technical geometry review passed for the three listed files. The
brush has angled closed bands rather than a continuous spiral; owner aesthetic
acceptance of that source simplification remains open.

Originals: `ServerStorage.GuardianSourceImports`. Editable assembly:
`Workspace.DemoRoom.13_Guardian.ScrapSweeper`. Reusable prefab:
`ServerStorage.GuardianTemplates.ScrapSweeper`. PBR maps are in images.md;
TextureID is empty. Recovery and independent Play review:
`roblox.magnet-sweep/Jobs/023/guardian-assembly-results.md`. No guardian gameplay
controller or permanent room instance was installed during assembly.
