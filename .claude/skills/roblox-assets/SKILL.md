---
name: roblox-assets
description: Roblox asset management & sourcing workflow for any game in this workspace — asset types & storage, finding assets (our inventory first, then Creator Store), licensing, the mandatory SECURITY scan (inserted models can hide backdoor scripts — scan & delete), the present-for-approval rule, and maintaining the per-game asset registry (what we created vs used). Use before searching for, inserting, or using ANY asset (model/mesh/image/audio/animation), or when organizing/where-to-store assets.
---

# Roblox assets — sourcing, security & registry

Full detail in [reference/assets.md](reference/assets.md). This is the **operative workflow**. The rules
below are authoritative (also in `GROUND-RULES.md §4`).

## The asset workflow (every time — no shortcuts)

1. **Our assets first.** Search the user's own inventory (`search_asset` scope `user`/`group`/`universe`)
   and the game's registry (below) **before** the public Creator Store (scope `creator_store`). Reuse
   what we already have.
2. **Present for approval.** Show the user candidates (name, thumbnail/id, type, source, license, free/paid).
   **Do NOT insert into the real place or use an asset until the user picks/approves it.** (Ask via the wizard.)
3. **Insert isolated + SCAN for scripts.** Insert the approved asset into an **isolated spot** (not the live
   game), then scan for scripts **before anything runs**:
   ```lua
   for _, i in ipairs(asset:GetDescendants()) do
       if i:IsA("LuaSourceContainer") then print(i.ClassName, i:GetFullName()) end  -- read i.Source
   end
   ```
   **Delete every `Script`/`LocalScript`/`ModuleScript` you didn't author** — an art/model asset has no
   legitimate reason to ship scripts. Red flags: `require(<id>)`, `HttpService`, `getfenv`/`loadstring`,
   obfuscated/base64 blobs, hidden/odd-named or self-re-enabling scripts. **Never Play before scanning.**
4. **Store it right.** Server-only templates → `ServerStorage`; shared/client (UI, Animations) →
   `ReplicatedStorage`; world content → `Workspace`. Dedupe by id (reuse one `MeshId`/image/`SoundId`).
5. **Log it in the registry** (below).

## Our-assets-first + registry (the asset catalog)

Each game keeps an **asset registry** — markdown, one file per asset type — listing **what we created**
and **what we used** (with ids, source, license, where stored). It's our fast, greppable catalog so we
reuse before re-sourcing. Location: `roblox.<game>/Assets/registry/` (see the scaffolded files + `_TEMPLATE.md`).
Update it whenever an asset is added. Format per entry:
`| name | rbxassetid | type | ours/created or source | license | stored-at | notes |`

## Sourcing options (in priority order)

1. **Our inventory / registry** (already own it, already scanned).
2. **Meshy** (custom 3D + rigged chars — via `roblox-chars`), **ChatGPT** (art → upload), which we create → we own the pipeline.
3. **Creator Store** (`search_asset` scope `creator_store`) — prefer **verified/known creators**, prefer
   **meshes/images (content)** over full Models when you only need art (less backdoor surface). Scan anyway.
4. **Pixabay** (sound), **Flaticon** (icons) — hold the rights / satisfy their license (Flaticon free needs
   attribution → prefer CC0/paid), and pass Roblox Community Rules.

## Licensing quick rules

Free Creator Store asset = license to use **in Roblox only** (not ownership, not external use). Audio: Creator
Store or your own rights only; privacy-protected. AI-output ownership & external-source attribution are the
grey areas — hold rights, don't infringe, check the source's terms (see reference §4). Never upload assets you
don't own.

## Asset types & storage (know these)

Content-referenced (`rbxassetid://`): meshes (`MeshId`), images (`Texture`/`Image`), audio (`SoundId`),
animations (`AnimationId`), fonts. Instance assets (parent a tree): Models, Packages. Package = versioned
linked group (keep the `PackageLink`). Imported assets are **private by default**; moderation adds lead time.
