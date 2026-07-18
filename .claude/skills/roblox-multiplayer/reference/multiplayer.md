# Roblox multiplayer & networking — reference

Sourced from official Creator Docs, current 2026-07. Not-verbatim items flagged **[unverified]**.
**Server is the source of truth.**

## Replication & remotes

Server property changes under replicated containers replicate to clients; `BasePart` physics replicates
from its **network owner** (below); ServerStorage/ServerScriptService + client-only instances don't replicate.
| Direction | Class · method | handler |
|---|---|---|
| Client→Server | `RemoteEvent:FireServer` | `OnServerEvent(player, ...)` |
| Server→client(s) | `RemoteEvent:FireClient(player,...)` / `FireAllClients(...)` | `OnClientEvent` |
| Blocking two-way | `RemoteFunction:InvokeServer` | `OnServerInvoke = fn(player,...)` |
| High-rate/cosmetic | `UnreliableRemoteEvent` | (no ordering/delivery guarantee) |
- `RemoteEvent` = default (async one-way). `RemoteFunction` only when you need a return; **avoid
  `InvokeClient`** (client disconnect errors/hangs the server). `UnreliableRemoteEvent` = continuous/
  non-critical streams only.
- **Arg marshalling:** functions→nil; metatables lost; tables copied (new identity); **no mixed
  numeric+string keys**; non-visible instances→nil. **Validate every arg server-side.**

## Network ownership (who simulates)

Owner simulates with **zero latency**, streams state to others. Default: server owns all → engine
**auto-assigns** to nearby clients; **anchored parts always server-owned**. Ownership applies to the whole
unanchored assembly. `BasePart:SetNetworkOwner(player)` (nil = server), `GetNetworkOwner()`,
`SetNetworkOwnershipAuto()`, `GetNetworkOwnershipAuto()`, `CanSetNetworkOwnership() → (bool, reason?)`.
**Boat:** `SetNetworkOwner(driver)` on sit → driver steers lag-free, replicates to passengers; reclaim
(`SetNetworkOwnershipAuto()`) on dismount. **Exploit caution:** owners can teleport/fake-Touch owned parts —
never give clients ownership of scoring/damage/objective parts; server-side plausibility-check owned positions.

## TeleportService (reserved servers — the party flow)

**Server-only; does NOT run in Studio.** `TeleportService:TeleportAsync(placeId, {players}, options)` —
pass the **whole party array in one call** to keep them together. Reserved private server:
`code, privateId = TeleportService:ReserveServerAsync(placeId)` (`ReserveServer` deprecated).
```lua
local opt = Instance.new("TeleportOptions")
opt.ShouldReserveServer = true        -- or opt.ReservedServerAccessCode = code (existing reserve)
opt:SetTeleportData({partyLeader = leader.UserId})   -- ⚠️ PUBLIC/unencrypted — no secrets
TeleportService:TeleportAsync(gamePlaceId, partyPlayers, opt)
```
Read on arrival: server `Player:GetJoinData().TeleportData` (+ SourcePlaceId/LaunchData); client
`TeleportService:GetLocalPlayerTeleportData()`. **Failure:** `pcall` the call **and** connect
`TeleportService.TeleportInitFailed(player, Enum.TeleportResult, msg, placeId, opts)` — use the docs'
`SafeTeleport` retry (attempt limit + delay; handle `Flooded`/`Failure`/etc.). Loading GUI:
`SetTeleportGui(gui)` (scripts inside don't run during teleport). Legacy `Teleport(...)` is client-callable
→ **discouraged**; use server-driven `TeleportAsync`. Harden with the "Secure within universe only" teleport setting.

## Matchmaking & party

Default matchmaking scores eligible servers and **excludes reserved servers** (why they're right for a
private co-op instance). Code-level custom matchmaking = **build it: MemoryStore Queue + ReserveServerAsync
+ TeleportAsync**. **`SocialService`:** `GetPlayersByPartyId(partyId)`, `GetPartyAsync(partyId)` (per member:
UserId/PlaceId/JobId/PrivateServerId/ReservedServerAccessCode → follow a friend into their reserved server),
`PromptGameInvite`, `CanSendGameInviteAsync`. `Player.PartyId` (empty if none), `Player.FollowUserId`
(joined-to-follow), `Player.Team`. **Keep party together:** collect intended players → `ReserveServerAsync`
once → single `TeleportAsync(gamePlaceId, {all}, opts)`.

## Latency & server info

`Player:GetNetworkPing()` (seconds) to size interpolation buffers. Boat = network-ownership *is* the
prediction. `game.JobId` (this instance), `game.PrivateServerId` (non-empty = reserved/VIP),
`game.PrivateServerOwnerId` (0 = reserved via ReserveServerAsync; ≠0 = VIP) → detect StandardServer(lobby)
vs ReservedServer(co-op instance).

## Cross-server (MessagingService + MemoryStore)

`MessagingService:PublishAsync(topic, msg)` / `SubscribeAsync(topic, cb)` (cb gets `{Data, Sent}`) —
**best-effort, unordered, notification not storage**; limits ~1kB/msg, send `600 + 240×players`/min,
recv `40 + 80×servers`/min **[verify]**; `pcall` + unsubscribe on leave. **`MemoryStoreService`:** `GetQueue`
(matchmaking queues), `GetSortedMap` (live leaderboards/skill queues), `GetHashMap` (session registries) —
fast, cross-server, TTL (≤45d), `UpdateAsync` no-yield transform.

## Co-op matchmaking flow

Lobby enqueues players (MemoryStore Queue, respect `PartyId`) → coordinator server dequeues, groups 1–6 →
`ReserveServerAsync` → `TeleportAsync({matched}, opts w/ ReservedServerAccessCode)` → secure state in
MemoryStore/DataStore keyed by `privateId`; `MessagingService` to coordinate.

## Gotchas
One teleport call = party together; reserve (don't rely on public matchmaking) for private instances;
server-authoritative everything; teleport data is public (secrets → DataStore/MemoryStore); handle teleport
failures; rejoin via GetJoinData/MemoryStore; boat single stable owner (unanchored); UnreliableRemoteEvent
cosmetic-only; no `InvokeClient`; TeleportService not in Studio.

## Sources
scripting/events/remote, physics/network-ownership, classes/{TeleportService,Player,DataModel,
MessagingService,SocialService,BasePart,UnreliableRemoteEvent}, projects/teleporting, matchmaking,
cloud-services/{cross-server-messaging,memory-stores}.
