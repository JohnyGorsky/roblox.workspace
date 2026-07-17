# Roblox Luau scripting — authoritative reference

Sourced from official Creator Docs (`create.roblox.com/docs`), `luau.org`, and one Roblox DevForum
announcement (flagged). Current as of 2026-07. Items not verbatim in docs are flagged **[unverified]**.

## 1. Client–server security

**Three pillars:** (1) never trust the client, (2) server is authoritative, (3) security by design.
Assume every client-sent value is fabricated. This is inherent to client-server, not a Roblox quirk.

**A determined exploiter can:** decompile any replicated `LocalScript` *or any `ModuleScript`* (even
ones never run on the client); take network ownership of their character + unanchored parts; fire
`Touched`/`ProximityPrompt`/remotes at any range/frequency with **arbitrary arguments**; modify their
local DataModel without firing expected events. → **Never put logic or secrets in `ReplicatedStorage`
or `Workspace`.** Authoritative logic → `ServerScriptService`; secret assets → `ServerStorage`.

**Server authoritative loop:** receive input → validate it's possible & permissible → execute & update
authoritative state → replicate results.

**Where code runs:**
| Container | Runs | Client-visible? |
|---|---|---|
| `Script` (Server / in ServerScriptService) | server | no |
| `LocalScript`/`Script`(Client) in StarterPlayerScripts/StarterGui/ReplicatedFirst/StarterCharacterScripts | client | yes (decompilable) |
| `ModuleScript` | whoever `require`s it | decompilable if in a replicated container, even if never run client-side |
| `ServerStorage`/`ServerScriptService` | server only | no |
| `ReplicatedStorage` | both | yes — remotes + shared assets only, **no secrets** |

**RemoteEvent** = async one-way, no yield. **RemoteFunction** = sync two-way, sender yields for a return.
```lua
remoteEvent:FireServer(...)                     -- client→server
remoteEvent.OnServerEvent:Connect(function(player, ...) end)  -- player injected
remoteEvent:FireClient(player, ...) / :FireAllClients(...)    -- server→client
remoteEvent.OnClientEvent:Connect(function(...) end)
local ret = remoteFunction:InvokeServer(...)    -- client→server, yields
remoteFunction.OnServerInvoke = function(player, ...) return ... end
```
**Never `InvokeClient` from the server:** if the client errors, disconnects, or never returns, the
server errors or **yields forever**. Use `RemoteEvent`+`FireClient` for server→client.

**Remote arg marshalling:** functions → `nil`; metatables lost; tables copied (new identity);
**never pass a mixed numeric+string-keyed table**; instances not visible to the recipient → `nil`.

**Validate EVERY `OnServerEvent`/`OnServerInvoke` argument:** type (`typeof`), range/domain (clamp,
reject NaN via `x ~= x`), ownership/permission, cooldown/rate-limit per player, sanity heuristics.
Throughput cap ~**500 remote requests/sec per client** shared across remotes of a type **[unverified — from a .yaml summary]** — self-limit well below it.

**Exploit heuristics (server-side detection):** Fastest Completion Time, Rate of Gain, Action Cadence
(uniform intervals = automation). Use a **suspicion-scoring** system — never hard-kick on one trip;
act only after multiple varied detections cross a high threshold.

## 2. Modern Luau (current 2025–2026)

**Type modes** (first line): `--!nocheck` / `--!nonstrict` / `--!strict`. Workspace default via
`Workspace.LuauTypeCheckMode`.

**New Type Solver — GA 2025-11-20** (DevForum, official). Default for `nocheck`/`nonstrict`; strict must
opt in via `Workspace.UseNewLuauTypeSolver`. Old engine retiring end of 2026. New ModuleScripts:
`--!strict` + opt into the new solver.

**Types:** `local x: string?`, literal types (`"Hi"`), unions `A | B`, generics `type List<T> = {T}`,
`export type Foo = {...}`, casts `expr :: T`. Living ref: luau.org/typecheck.

**String interpolation (backticks)** — prefer over `..` / often over `string.format`:
```lua
print(`Hello {world}, {n + 1} times!`)
```
**if-else EXPRESSION** (else mandatory) — the correct replacement for `cond and a or b` (which breaks
when `a` is falsy): `local x = if cond then a else b`.

**Generalized iteration:** `for k, v in myTable do ... end` (no pairs/ipairs). Custom via `__iter`.

**Compound assignment:** `+= -= *= /= //= %= ^= ..=` (single LHS/RHS).

**`continue`** — allowed; must be the last statement in its block.

**`table`:** `insert/remove/find/concat/sort/clear/create(n,v)/clone(shallow)/freeze/isfrozen/move/pack/unpack`.

**`buffer`** — raw byte buffer for compact serialization / smaller replicated payloads:
`buffer.create/fromstring/tostring/len`, `read/write` `i8 u8 i16 u16 i32 u32 f32 f64`, `readbits`,
`copy`, `fill`.

**`task` library (use; the `wait`/`spawn`/`delay` globals are DEPRECATED):**
```lua
task.spawn(fn, ...)   task.defer(fn, ...)   task.delay(dur, fn, ...)
task.wait(dur?)       task.cancel(thread)   task.synchronize() / task.desynchronize()
```
Also prefer `:Connect`/`:Once` over legacy `:connect`.

## 3. Best-practice patterns

- **ModuleScript**: return one table; `require` caches per side. Shared→ReplicatedStorage,
  server→ServerScriptService/Storage, client→client tree.
- **OOP** via metatables (`__index`, `.new` + `setmetatable`, `:` methods pass `self`).
- **Connection management (leaks):** separate **permanent** connections (attribute/property signals)
  from **character-scoped** ones (Humanoid Health/Died); recreate the latter on `CharacterAdded`,
  `:Disconnect()` on death/respawn/leave. Undisconnected connections block GC. `Instance:Destroy()`
  disconnects its own events.
- **Attributes over Value objects**; listen via **`:GetAttributeChangedSignal(name)`** (reliable for
  rapid changes) not generic `AttributeChanged`.
- **CollectionService tags** to manage groups. **`:GetPropertyChangedSignal`** over polling.
- **`pcall`/`xpcall`** every DataStore/HttpService/MarketplaceService/TeleportService/MessagingService call.

## 4. Parallel Luau

`Actor` instances isolate execution; scripts under the SAME actor run sequentially — need multiple
actors for real parallelism. `task.desynchronize()` → parallel phase; `task.synchronize()` → serial
(required before mutating the DataModel). `RBXScriptSignal:ConnectParallel(fn)`. Safe in parallel: reads
+ pure compute (raycasts, procedural gen) on Safe/Read-Parallel APIs. Unsafe: mutating the DataModel,
writing outside your actor, `require()` while desynchronized. Cross-thread: `Actor:SendMessage`/
`BindToMessage(Parallel)`, `SharedTable` (atomic). Pattern: compute parallel → synchronize → apply.

## 5. Performance

MicroProfiler scopes (PreRender, physicsStepped, updateInvalidatedFastClusters, ProcessPackets).
Signals over polling; debounce/throttle. Break heavy loops with `task.wait()`; move pure compute to
Parallel Luau or `--!native`. Anchor static parts; adaptive physics stepping; lower CollisionFidelity.
Disable unused Humanoid states; animate NPCs client-side; object-pool respawns. Share asset IDs for
instancing; RenderFidelity/shadow culls. Never server-side `TweenService`; send only changed data.
**Disconnect connections** (GC); Instance Streaming for large worlds.

## 6. DataStores

- `GetAsync` (may be stale), `SetAsync` (write only; single-writer keys), **`UpdateAsync`**
  (read-modify-write; safe for concurrent servers; counts read+write; **callback may not yield**),
  `IncrementAsync`, `RemoveAsync`, `OrderedDataStore:GetSortedAsync` (leaderboards).
- **Wrap in `pcall` + retry w/ backoff.** **Session-lock** with a server-id token via `UpdateAsync`
  (concept documented; code **[unverified]**). Save on `PlayerRemoving` **and** `game:BindToClose()`.
  Check `GetRequestBudgetForRequestType` before bulk ops.
- **Limits:** value 4 MB (4,194,304 chars); key/name/scope 50 chars; per-key read 25 MB/min, write
  4 MB/min; server read/write budget `60 + players×40` per min; queue 30/op (errors 301–306).

## Deprecated / avoid
`wait/spawn/delay` globals → `task.*`; `:connect` → `:Connect`; `cond and a or b` → if-expression;
generic `AttributeChanged` for rapid updates → `:GetAttributeChangedSignal`; polling → property signals;
`SetAsync` on multi-writer keys → `UpdateAsync`; server-side Tween/NPC-anim → client; logic/secrets in
`ReplicatedStorage`/`Workspace` → `ServerScriptService`/`ServerStorage`; old type inference → New Solver.

## Sources
security-tactics, server-side-detection, events/remote, luau/type-checking, luau.org/{syntax,typecheck},
luau/strings, luau/control-structures, libraries/task, libraries/buffer, globals/RobloxGlobals,
scripting/multithreading, cloud-services/data-stores(+error-codes-and-limits),
performance-optimization/improve; New Type Solver GA DevForum announcement.
