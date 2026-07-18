---
name: roblox-multiplayer
description: Roblox multiplayer & networking for any game in this workspace — replication & remotes (RemoteEvent/RemoteFunction/UnreliableRemoteEvent), network ownership (esp. for a shared physics vehicle/boat), TeleportService reserved servers & party teleport, matchmaking (SocialService party, MemoryStore queues), cross-server MessagingService, and latency. Use before building/reviewing lobby→game teleport, co-op/party flow, network ownership, replication, or cross-server logic.
---

# Roblox multiplayer & networking

Full API in [reference/multiplayer.md](reference/multiplayer.md). This is the working guide. **Server is
authoritative — validate every remote arg.**

## Remotes

`RemoteEvent` (async one-way) = default. `RemoteFunction` only when you need a return (**never
`InvokeClient`**). `UnreliableRemoteEvent` for continuous/cosmetic streams only (no ordering/delivery).
No mixed numeric+string table keys; functions/metatables don't survive the boundary.

## Network ownership (the boat)

Owner simulates lag-free. `SetNetworkOwner(driver)` on the hull when a player drives → responsive steering
that replicates to passengers; `SetNetworkOwnershipAuto()` on dismount. Keep the boat **unanchored** (anchored
can't be client-owned). **Never** give clients ownership of scoring/damage/objective parts; plausibility-check
owned-part positions server-side (owners can cheat physics).

## Lobby → reserved server (Last River P6)

**Server-only; not in Studio.** Keep the party together with **one** teleport of all players into one
reserved server:
```lua
local code = TeleportService:ReserveServerAsync(gamePlaceId)
local opt = Instance.new("TeleportOptions"); opt.ReservedServerAccessCode = code
opt:SetTeleportData({...NON-secret context...})            -- teleport data is PUBLIC
TeleportService:TeleportAsync(gamePlaceId, partyPlayers, opt)  -- pcall + SafeTeleport retry
```
Read on arrival: `Player:GetJoinData().TeleportData` (server) / `GetLocalPlayerTeleportData()` (client).
Handle `TeleportInitFailed` + retry. Detect instance type via `game.PrivateServerId`/`PrivateServerOwnerId`
(reserved = non-empty id + owner 0).

## Matchmaking & party

Default matchmaking excludes reserved servers (good — outsiders can't join your private instance). Custom =
**MemoryStore `GetQueue` + `ReserveServerAsync` + `TeleportAsync`**. Party: `SocialService`
(`GetPlayersByPartyId`/`GetPartyAsync`/`PromptGameInvite`), `Player.PartyId`/`FollowUserId`. Secure match
state → DataStore/MemoryStore keyed by `PrivateServerId` (not teleport data).

## Cross-server & rejoin

`MessagingService` (best-effort pub/sub, ≤1kB, notification not storage) for lobby↔instance signals;
`MemoryStore` for shared/queue state. On rejoin, restore from `GetJoinData`/MemoryStore; persist the
`ReservedServerAccessCode` so friends rejoin the same instance.
