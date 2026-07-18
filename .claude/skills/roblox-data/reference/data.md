# Roblox data persistence — reference

Sourced from official Creator Docs, current 2026-07. Not-verbatim/varying items flagged **[unverified]**.
**Server-side only.** `DataStoreService` = durable; `MemoryStoreService` = fast/ephemeral/cross-server.

## DataStoreService

`GetDataStore(name, scope?, options?)` (v2 — versioning+metadata), `GetOrderedDataStore(name, scope?)`
(sorted, **integer values only** — leaderboards), `GetRequestBudgetForRequestType(Enum.DataStoreRequestType)`
(check before bursts — **trust this at runtime over hard-coded limits**), `ListDataStoresAsync`,
`SetRateLimitForRequestType`.

## Operations (GlobalDataStore/DataStore)

- `GetAsync(key, opts?)` → `(value, keyInfo)`. **4-second local cache** (repeat reads free; bypass with
  `DataStoreGetOptions.UseCache=false`).
- `SetAsync(key, value, userIds?, opts?)` — blind overwrite; write budget only; **data-loss risk if two
  servers set the same key** → prefer UpdateAsync for shared keys.
- **`UpdateAsync(key, transform)`** — atomic read-modify-write, concurrency-safe; counts read+write.
  ⚠️ **The transform MUST NOT yield** (no wait/other async/WaitForChild); `return nil` cancels the write.
- `IncrementAsync(key, delta?)` (integer wrapper), `RemoveAsync(key)` (v2 keeps a 30-day tombstone).
- `DataStoreSetOptions:SetMetadata({...})`, `userIds={id}` (GDPR/ownership). `keyInfo`: `Version`,
  `CreatedTime`, `UpdatedTime`, `:GetUserIds()`, `:GetMetadata()`.
- **Versioning (v2):** backup on first write per key per UTC hour (30-day expiry; latest never expires);
  `ListVersionsAsync`, `GetVersionAsync(key, ver)`, `RemoveVersionAsync`, `ListKeysAsync` — rollback after bad writes.

## Limits & errors

Value **4 MB**; key/name/scope **50 chars**; per-key **25 MB read / 4 MB write per min**; server budget
≈ `60 + numPlayers×40` read/write **[verify at runtime]**; throttle errors **301–306**, ~**30 queued** per
type then dropped. **`pcall` every call; retry with exponential backoff; check budget.**

## Session locking (dupe/rollback protection) — do this

Guarantees at most one server owns a player's key. Pattern (Roblox's `SessionLockedDataStoreWrapper`):
1. **Acquire on load** via `UpdateAsync`: write a GUID **`LockId`** into the key metadata + keep it in memory.
2. **Verify:** if a foreign LockId exists and is newer than the expiry window → busy; if older → **stale, steal it**.
3. **Heartbeat:** the periodic auto-save loop keeps re-touching the key (refreshes the lock).
4. **Release** on `PlayerRemoving`/`BindToClose` (remove the LockId). Route **all** ops through `UpdateAsync`
   (only atomic primitive); each key has its own serial queue (prevents stale writes clobbering newer ones).

## Save lifecycle (non-negotiable trio)

`PlayerAdded` → load (pcall+UpdateAsync, acquire lock) + build `leaderstats`/profile (defaults if new).
**Periodic auto-save** loop (crash safety + lock heartbeat). `PlayerRemoving` → final save + release lock.
**`game:BindToClose(fn)`** → server shutdown, **~30s only** → save all remaining players **in parallel**
(thread per player). Without it, everything since the last save on a shutting-down server is lost.

## Leaderboards

- **`leaderstats`** = in-game player-list display (folder named exactly `leaderstats` under the Player, with
  `IntValue`/`NumberValue`/`StringValue` children). **Display only — not persistence.**
- **Global persistent:** `OrderedDataStore` + `GetSortedAsync(ascending, pageSize, min?, max?)` →
  `pages:GetCurrentPage()` (`.key`=userId, `.value`=score); `AdvanceToNextPageAsync`. **Weekly boards:** dated
  store name (`"Leaderboard_2026_W29"`). Resolve names with `Players:GetNameFromUserIdAsync`.

## MemoryStore (fast, ephemeral, cross-server)

`GetSortedMap` (live leaderboards / skill queues), `GetQueue` (matchmaking), `GetHashMap` (session registry).
TTL ≤45d (set per item); ≤1M items/100MB per structure; `UpdateAsync` no-yield transform. **DataStore for
durable profiles; MemoryStore for live/transient.**

## Best practices
Store a `dataVersion` in each profile + **migration** on load; `UpdateAsync` for shared, `SetAsync` only for
owned keys; the save trio; recover via version history; tag `userIds`; test with **Studio Access to API
Services** on a **separate place** (Studio shares live data). Community **ProfileStore** implements
session-lock + auto-save (de-facto standard) **[not official API]**.

## Sources
cloud-services/data-stores(+error-codes-and-limits, versioning-listing-and-caching, player-data-purchasing),
cloud-services/memory-stores, players/leaderboards, tutorials/.../create-leaderboard,
classes/{DataStoreService,GlobalDataStore,OrderedDataStore}.
