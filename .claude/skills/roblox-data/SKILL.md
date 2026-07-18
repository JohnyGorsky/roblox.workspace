---
name: roblox-data
description: Roblox data persistence for any game in this workspace — DataStoreService (GetAsync/SetAsync/UpdateAsync/IncrementAsync), session locking (dupe/rollback protection), the load/auto-save/PlayerRemoving/BindToClose lifecycle, leaderboards (leaderstats + OrderedDataStore), versioning, budgets/limits, and MemoryStore. Use before building/reviewing any player data saving, progression/currency/unlocks persistence, leaderboards, or cross-server ephemeral state.
---

# Roblox data persistence

Full API in [reference/data.md](reference/data.md). This is the working guide. **Server-side only; `pcall`
everything.**

## The three rules

1. **`UpdateAsync` for anything shared** (atomic read-modify-write), not `SetAsync` (blind overwrite = data
   loss under concurrency). The transform **must not yield**; `return nil` cancels.
2. **Session locking** — write a GUID `LockId` into key metadata on load (via UpdateAsync), heartbeat it via
   the auto-save loop, steal it only if stale, release on exit. Prevents dupe exploits / rollbacks.
3. **The save trio:** load on `PlayerAdded` → **periodic auto-save** loop → save on `PlayerRemoving` →
   **`game:BindToClose()`** (save all remaining players in parallel in the ~30s window). Skipping BindToClose loses data.

## Player progression (Last River meta currency / unlocks)

Load profile on join (defaults if new), keep it in memory (session-locked), mutate via UpdateAsync, save on
the trio above. Store a `dataVersion` + run **migrations** on load. Fold purchase `PurchaseId`s into this
same profile (one source of truth — see `roblox-monetization`). Community **ProfileStore** implements all of
this; it's the de-facto standard.

## Leaderboards

- **`leaderstats`** folder (exact name) under the Player = the in-game list — **display only**.
- **Persistent global:** `OrderedDataStore` + `GetSortedAsync(false, N)` (top N; integer scores only).
  **Weekly:** a dated store name (`"Leaderboard_2026_W29"`). Resolve names via `GetNameFromUserIdAsync`.
- **Live cross-server board:** MemoryStore `SortedMap`.

## Limits & reliability
Value 4 MB; per-key 4 MB write/min; check `GetRequestBudgetForRequestType` before bursts; retry with
exponential backoff. Recover bad writes via 30-day version history. Test with **Studio Access to API
Services** on a **separate place** (Studio shares live data).

## MemoryStore
`GetQueue` (matchmaking), `GetSortedMap` (live boards), `GetHashMap` (session state) — fast, cross-server,
TTL ≤45d. Durable → DataStore; ephemeral/live → MemoryStore.
