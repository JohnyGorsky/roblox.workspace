# Roblox asset management — reference

Sourced from official Creator Docs, current 2026-07. Not-Roblox-doc items flagged **[unverified]**.

## 1. Asset types

Everything is a cloud asset with a numeric id. **`Enum.AssetType`** (61 items) — key ones: `Image`(1),
`Audio`(3), `Mesh`(4), `Model`(10), `Shirt`(11)/`Pants`(12), `Decal`(13), `Animation`(24), `Package`(32),
`Plugin`(38), `MeshPart`(40), the accessory/body/animation types, `FontFamily`(73), `Video`(62).

**Content-referenced (`rbxassetid://<ID>`) vs inserted instances** — the key split:
- **Content** populates a property: `MeshPart.MeshId`, `Decal.Texture`/`ImageLabel.Image`,
  `Sound.SoundId`/`AudioPlayer.Asset`, `Animation.AnimationId`, `FontFamily`.
- **Instances** are whole trees you fetch + parent: **Models, Packages, plugins** (via `InsertService:LoadAsset`
  / `AssetService:LoadAssetAsync`).
- **Mesh** = geometry asset; **MeshPart** = the instance that points at it via `MeshId`. **Model** = a
  container of instances. **Package** = a *versioned, linked* group (dedup/reuse across places).

## 2. Storage

- **ServerStorage** = server-only templates (never replicated; safe from exploiters). **ReplicatedStorage** =
  shared/client-visible assets (UI templates, `Animation`s). **Workspace** = present in the world.
- **IDs vs instances:** referencing by id lets the engine **deduplicate** — many MeshParts sharing one
  `MeshId` (or images sharing one id) load the content **once**. Cheapest for repeated content.
- **Packages:** converting creates a child **`PackageLink`** (don't delete/move it — that unlinks it).
  `PackageLink.AutoUpdate` pulls new versions when a place opens in Studio (**modified copies don't
  auto-update**). Full version history.
- **Privacy:** imported assets are **private by default** (visible only to you in the Toolbox Inventory
  until moderated); **Asset Privacy** defaults new assets to **Restricted** — an asset "cannot load in
  Studio or at runtime" without explicit permission (why pasting a gated asset into another game can fail).
- **On disk (Rojo/Sync):** code + instances sync as files, but **id-referenced content (meshes/images/audio)
  and hand-placed Workspace/ServerStorage content live in the cloud + the saved place, not the git repo.**
  Reference them by `rbxassetid://` in properties.
- **Org:** a well-known `Assets` folder by type (e.g. `ReplicatedStorage/Assets/{Models,Animations,UI}` for
  shared; `ServerStorage` for server-only). Asset Manager mirrors this cloud-side.

## 3. Finding / inserting

- **Toolbox** tabs: **Creator Store** (public marketplace — models/decals/meshes/audio/plugins/videos/fonts),
  **Inventory / Recent / Creations** (your own). **Asset Manager** manages Images/Meshes/Audio/Packages/Places
  (import → images become Decals, meshes → MeshParts, audio → Sounds).
- **API:** `InsertService:LoadAsset(id)` / `LoadAssetVersion(vId)` / `GetLatestAssetVersionAsync(id)`;
  `AssetService:LoadAssetAsync` (modern), `CreateAssetAsync`/`CreateAssetVersionAsync`,
  `GetAssetIdsForPackageAsync`, `GetBundleDetailsAsync`, `GetAudioMetadataAsync`, `SearchAudioAsync`,
  EditableImage/Mesh + `CreateMeshPartAsync`. **Deprecated:** `GetFreeModels/GetFreeDecals`, `Insert`,
  `SearchAudio`, `GetAssetIdsForPackage`.
- **Our MCP:** `search_asset` (scopes: `user`/`group`/`universe`/`creator_store`/`auto`), `insert_asset(id)`.

## 4. Licensing (be concrete)

- **Creator Store free asset** → taking it grants a **license to use it within Roblox Studio/experiences**
  per the Roblox Terms — **not** ownership, **not** rights to use outside Roblox. Must comply with Community
  Rules/DMCA.
- **Paid:** only **models & plugins** are sellable (verified seller); models $2.99–$49.99, plugins $4.99–$249.99.
- **Distributed assets must NOT** obscure engine features in scripts, require remote assets, or include
  obfuscated code (Roblox forbids exactly the backdoor patterns — §5).
- **Audio:** use **Creator Store audio** (100k+ free) or your **own imports where you hold the rights**;
  audio is privacy-protected by default. Limits: mp3/ogg/wav/flac, <20 MB, <7 min, ≤48 kHz; 2,000 imports/30d
  (verified) / 100 (unverified).
- **AI-generated output ownership [unverified]** — governed by Roblox AI/Terms, not one docs page; you're
  responsible for non-infringing prompts. Third-party generators (Meshy) carry their **own** license.
- **External sources (Flaticon/Pixabay) [unverified vs Roblox]** — you must hold the rights and satisfy that
  source's license (Flaticon free needs attribution — hard in-game, prefer CC0/paid; Pixabay = Pixabay
  license) AND pass Roblox Community Rules/DMCA. Uploading assets you don't own = a violation regardless of source.

## 5. SECURITY — malicious scripts in inserted assets

Free/Toolbox **Models can hide `Script`/`LocalScript`/`ModuleScript` backdoors** (remote access: spawn/kick/ban,
steal data, run arbitrary code). **No official Roblox scanner exists** — scanning is a manual discipline.

**Scan every inserted asset (before Play):**
```lua
for _, inst in ipairs(model:GetDescendants()) do
    if inst:IsA("LuaSourceContainer") then          -- catches Script, LocalScript, ModuleScript
        print(inst.ClassName, inst:GetFullName())    -- then read inst.Source
    end
end
```
**Red flags in `.Source`:** `require(<numeric id>)` (remote module = classic backdoor); `HttpService`
Get/Post to unknown URLs; `getfenv`/`setfenv`/`loadstring`; base64/hex/`string.char` blobs, `\ddd` spam
(obfuscation); hidden/oddly-named objects, invisible unicode, `Disabled` scripts that re-enable; scripts
touching Players/teleport/ban/DataStore/RemoteEvents you didn't make.
**Rule:** an art/model asset has **no legitimate reason to ship scripts** — **delete every
`LuaSourceContainer` you didn't write.** Insert+scan in an **isolated test place**; **never Play before scanning**.

## 6. Best practices

Dedupe by id (reuse one MeshId/image/SoundId); keep an **asset manifest** (names→ids, centralized/greppable);
version reused assets as **Packages**; org an `Assets` folder by type; build in **moderation lead time**
(uploads pending until approved); keep assets private/Restricted; **scan every inserted third-party asset**.

## Sources
enums/AssetType, classes/{AssetService,InsertService}, projects/assets(+manager,packages), studio/toolbox,
production/creator-store, resources/limited-use-license, audio/assets, studio/texture-generator; Roblox ToU/Creator Store Terms.
