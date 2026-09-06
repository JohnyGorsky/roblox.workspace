# Job #013 — Implementation plan: NIGHTWEAVE avatar bundle

**Project**: `workspace` (standalone, no game yet)
**Path chosen**: free / own-inventory only. No Marketplace publish, no Premium, no Robux.

## Design

Original spider-hero, deliberately sharing no protected element of any existing franchise:

| Element | Choice | Why it's clean |
|---|---|---|
| Palette | matte black + electric cyan | not the black/red pairing |
| Web pattern | hexagonal circuit traces on ribs, spine, outer arms | not radial webbing |
| Lenses | angular chevron, cyan | not teardrop |
| Emblem | hex-bodied angular spider | spiders aren't ownable; stylisation is distinct |
| Silhouette | hooded bodysuit | generic to the genre |

## Assets produced

| File | What |
|---|---|
| `assets/nightweave-concept-front.png` | Meshy nano-banana concept, T-pose front (3 credits) |
| `assets/nightweave-body.glb` | meshy-7 image-to-3D, 2K PBR (30 credits) |
| `assets/nightweave-body.fbx` | same model, FBX |

Meshy task ids: text-to-image `01a07791-337e-774b-a633-4d6c9ba00c70`, image-to-3D `01a07794-b48a-7070-98e8-8acd3d4b69e3`. Total spend 33 credits.

## Verified mesh facts (probed from the GLB, not assumed)

- 10,441 triangles — under Roblox's 10,742 total body budget
- 1 mesh, 1 material, 3 textures: base_color, metallic_roughness, normal
- no skin, no animation — Auto Setup supplies the R15 armature
- bbox 1.834 (X) x 1.903 (Y) x 0.37 (Z) in metres — arm span ~= height, so a true T-pose
- **no emissive map** — the cyan glow is baked into base colour only

## Known risks, from Roblox's stated Auto Setup requirements

1. **Hood is unsupported body geometry.** Roblox lists loose clothing/capes/hair as not supported for a
   body mesh. Our hood is merged into the head. Mitigation: split it off and rebuild it as a rigid
   accessory on `HatAttachment` (4k tri cap, 2048 texture, Material=Plastic, Transparency=0).
2. **No eyes or mouth on the mask.** Auto Setup wants 2 half-sphere eyes with no shared vertices plus 3
   isolated mouth parts (upper teeth, lower teeth, tongue) to generate FACS. A masked head has none.
   Face conversion is expected to fail; accept it and ship without facial animation.
3. **Scale.** Model is ~1.9 units tall (metres). A Roblox Normal-scale body wants 3.6-9.5 studs. Set the
   scale in the 3D Importer, or let Auto Setup normalise.
4. **Orientation.** Roblox requires the body front to face **negative Z**. Bounding box is symmetric in Z
   so this cannot be confirmed from the file — check it in the importer preview and rotate if needed.

## Steps

- [x] Concept image generated and approved
- [x] 3D body generated, downloaded, verified under budget
- [ ] Import `nightweave-body.glb` via Studio **Home > Import** (3D Importer). Manual — the file picker
      cannot be driven over MCP.
- [ ] Confirm orientation (front faces -Z) and scale in the importer preview
- [ ] Select the model > **Avatar** tab > **Avatar Setup**
- [ ] Preset = **Development Avatar** (not Platform Avatar — we are not publishing), Type = **Body**
- [ ] Click **Set Up**; expect the face stage to fail, accept and continue
- [ ] Use **Check Body** and **Test in Experience** to validate
- [ ] **Save** to inventory (free; no publishing advance because nothing is published)
- [ ] Assign as `StarterCharacter`, or apply via `HumanoidDescription` on NPCs
- [ ] Optional: cyan glow via `Highlight` / `PointLight`, since there is no emissive map
- [ ] Optional: hood as a separate rigid accessory

## Cost reference (why we chose the free path)

| Path | ID verify | Premium | Upload fee | Advance |
|---|---|---|---|---|
| Own inventory / own game | not for plain meshes | no | 0 | 0 |
| Marketplace, priced | yes | Premium 1000/2200 | 80 R$ | 2,500 R$ for a Body |
| Marketplace, free | yes | yes | 80 R$ | per-unit x quantity — the most expensive option |

Non-Limited Marketplace items **cannot** be priced at zero. Giving an item away requires publishing it as
a free Limited, which charges a per-unit fee (e.g. 200 copies x 100 R$ = 20,000 R$).
