---
name: roblox-scripting
description: Roblox Luau scripting standards for any game in this workspace — client-server security & exploit-hardening, modern Luau (new type solver, task library, string interpolation, if-expressions), best-practice patterns (modules, OOP, connection/leak management, attributes), Parallel Luau, performance, and DataStore rules. Use before writing/reviewing Luau, wiring RemoteEvents/RemoteFunctions, handling player data, or reasoning about security/performance. Complements roblox-dev (broad engine) and roblox-physics.
---

# Roblox scripting (Luau, security, best practice)

Full details + exact APIs in [reference/luau-scripting.md](reference/luau-scripting.md). This is the
working discipline. `roblox-dev` covers broad engine APIs; this skill is security + modern Luau +
patterns + perf + DataStores.

## Security — the non-negotiables (real money = attackers try)

1. **Never trust the client. Server is authoritative.** Every client-sent value is potentially forged.
2. **No logic or secrets in `ReplicatedStorage`/`Workspace`** — exploiters decompile any replicated
   `LocalScript` *and any `ModuleScript`* (even ones never run client-side). Authoritative logic →
   `ServerScriptService`; secret assets → `ServerStorage`.
3. **Validate EVERY `OnServerEvent`/`OnServerInvoke` argument**, in order:
   type (`typeof`) → range/domain (clamp; reject NaN via `x ~= x`) → ownership/permission →
   per-player cooldown/rate-limit → sanity heuristics. Only then mutate authoritative state.
4. **Never `RemoteFunction:InvokeClient` from the server** (client can error, disconnect, or never
   return → server yields forever). Server→client = `RemoteEvent:FireClient`.
5. **Remote payloads:** no mixed numeric+string-keyed tables; functions/metatables don't survive;
   instances the recipient can't see arrive as `nil`. Self-limit well under the ~500 req/s/client cap.
6. **Detect cheating with heuristics + suspicion scoring** (fastest-time, rate-of-gain, action-cadence);
   never hard-kick on one trip.

## Modern Luau — use these (avoid the deprecated column)

- **`task.*`** (`wait/spawn/defer/delay/cancel`), never the `wait`/`spawn`/`delay` globals. `:Connect`/`:Once`.
- **`--!strict`** in new ModuleScripts; the **New Type Solver** is GA (2025-11) — opt in via
  `Workspace.UseNewLuauTypeSolver`; old inference retires end of 2026.
- **String interpolation** `` `{x}` `` over `..`; **if-else expression** `if c then a else b`
  (replaces the buggy `c and a or b`); **generalized iteration** `for k,v in t do`.
- **Attributes** + `:GetAttributeChangedSignal(name)` over Value objects / generic `AttributeChanged`.
- **`:GetPropertyChangedSignal`** over polling. **`buffer`** for compact replicated payloads.

## Patterns & leak discipline

- ModuleScript returns one table; place by side (shared→ReplicatedStorage, server→ServerScriptService/
  Storage, client→client tree). OOP via metatables.
- **Connections leak GC if not disconnected.** Separate **permanent** connections (attribute/property
  signals) from **character-scoped** (Humanoid Health/Died) — recreate on `CharacterAdded`,
  `:Disconnect()` on death/respawn/leave. `Instance:Destroy()` disconnects its own events.
- **`pcall`** every DataStore/HttpService/MarketplaceService/TeleportService/MessagingService call.

## Parallel Luau (for heavy compute — e.g. procedural generation)

`Actor`s isolate execution (need multiple for real parallelism). `task.desynchronize()` → parallel
(reads + pure compute only), `task.synchronize()` → serial (required before mutating the DataModel;
and before `WriteVoxels`). Cross-thread via `SharedTable` / `Actor:SendMessage`.

## Performance quicklist

Signals over polling; debounce/throttle; break heavy loops with `task.wait()`; move pure compute to
Parallel Luau; never server-side Tween; send only changed data; disconnect connections; Instance
Streaming for big worlds; anchor static parts.

## DataStores

`UpdateAsync` (not `SetAsync`) for keys multiple servers touch — and its callback **must not yield**.
Wrap in `pcall` + retry w/ backoff; **session-lock** with a server-id token; save on `PlayerRemoving`
**and** `game:BindToClose()`; check `GetRequestBudgetForRequestType`. Value cap 4 MB.
