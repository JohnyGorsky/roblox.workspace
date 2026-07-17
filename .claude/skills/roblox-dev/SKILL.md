---
name: roblox-dev
description: Roblox + Luau development knowledge base, sourced from the official Roblox Creator Documentation. Use when writing, reviewing, or debugging Luau scripts, RemoteEvents/Functions, DataStores, Humanoids/characters, animations, GUI, services, or any Roblox Studio gameplay feature — including questions about Roblox APIs, security, and performance best practices. Engine knowledge is game-agnostic; apply the active game's own project skill on top.
---

# Roblox Development

Authoritative, **game-agnostic** Roblox + Luau knowledge distilled from the official
[Roblox Creator Docs](https://create.roblox.com/docs) (`Roblox/creator-docs`). Use it whenever a task
involves Roblox Studio, Luau scripting, or engine APIs — for any game in this workspace.

## How to use this skill

1. **Read the reference** at [reference/roblox-development.md](reference/roblox-development.md) for the
   topic at hand (Luau language, services, remotes, DataStores, characters, animation, UI,
   performance, conventions). It is the primary source — prefer it over guessing.
2. **Verify before relying on a fragile detail.** The reference is a snapshot. For exact method
   signatures, quota numbers, or whether an API is deprecated, fetch the live page:
   - Raw markdown: `https://raw.githubusercontent.com/Roblox/creator-docs/main/content/en-us/<path>.md`
   - Rendered: `https://create.roblox.com/docs/<path>`
3. **Apply the active game's `<game>-project` skill** on top for that game's architecture, sync rules,
   file map, and non-negotiable conventions. This skill covers the engine; the project skill covers
   the game.

## General best-practice rules (apply everywhere)

These hold for any Roblox game; each game's project skill may add stricter rules.

- **Server is authoritative.** Never trust client input — validate type, range, ownership, and
  cooldown server-side. Never put server logic or secret data in `ReplicatedStorage`; keep sensitive
  assets in `ServerStorage`.
- **Use `:GetAttributeChangedSignal(name)`**, not the generic `AttributeChanged`, for reliable
  server→client updates (health, coins, xp, level). Use `:GetPropertyChangedSignal` over polling.
- **Wrap DataStore / HttpService / MarketplaceService calls in `pcall`** and handle failure.
- Separate **permanent** connections (attribute signals) from **character-scoped** connections
  (Humanoid/health) — disconnect the latter on respawn.
- Use the `task.*` scheduler (`task.wait`, `task.spawn`, `task.defer`), not legacy `wait`/`spawn`.
- **`.luau` extension**, PascalCase module/script names; add Luau type annotations on function
  signatures; consider `--!strict` in new ModuleScripts.

## Validate every script edit (static analysis)

Roblox projects here have no runtime test harness, so a **luau-lsp static analyzer is the
verification gate** — it catches syntax errors, type errors, undefined types, dead code,
unused/shadowed locals, cyclic `require`s, and deprecated APIs, far more than a syntax check.

Each game provides its own analyzer wrapper and sourcemap (paths differ per game — see that game's
`<game>-project` skill for the exact command, e.g. a `tools/luau-analyze.sh`). The rule is universal:
**after editing any `.luau`, run the game's analyzer on that file and resolve findings before moving
on.** Without a generated `sourcemap.json`, every `require()`/`WaitForChild(...)` is a
false-positive error — keep the sourcemap enabled.

## Asset sources

See the workspace `GROUND-RULES.md` (§4) — Meshy.ai for 3D models (via the `roblox-chars` agent),
Flaticon for icons, Pixabay for sounds. Claude produces prompts/integration code; the human imports
and supplies IDs.

See [reference/roblox-development.md](reference/roblox-development.md) for full details and code patterns.
