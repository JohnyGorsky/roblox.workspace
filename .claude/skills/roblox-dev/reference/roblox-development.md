# Roblox Development Reference

Condensed reference for Roblox + Luau development, distilled from the official
Roblox Creator Documentation (source: [Roblox/creator-docs](https://github.com/Roblox/creator-docs),
published at https://create.roblox.com/docs). Use it as the authoritative knowledge base
when writing or reviewing Luau game code. When a detail is missing or you suspect an API
changed, fetch the live page (links are inline) rather than guessing.

---

## 1. Luau Language

Luau is Roblox's scripting language — a gradually-typed dialect of Lua 5.1 with added
type checking, performance optimizations, and ergonomic syntax.

### Data types
Six core types: `nil`, `boolean`, `number` (double-precision float; no separate int type),
`string`, `table`, and Roblox `Enum`. Roblox also adds engine datatypes such as `Vector3`,
`CFrame`, `Color3`, `UDim2`, `Instance`, `BrickColor`, `Ray`, and `Random`.

### Variables & scope
- `local x = 1` — block-scoped. **Always prefer `local`**; globals are slow and leak across a script.
- Variables are references for tables/instances, values for primitives.
- Multiple assignment: `local a, b = 1, 2`. Swap: `a, b = b, a`.

### Control structures
```lua
if cond then ... elseif cond2 then ... else ... end
while cond do ... end
repeat ... until cond
for i = 1, 10, 2 do ... end          -- numeric
for index, value in ipairs(arr) do end   -- arrays (stops at first nil)
for key, value in pairs(dict) do end      -- dictionaries
for k, v in myTable do ... end            -- generalized iteration (Luau)
```
`continue` and `break` are supported.

### Operators
- Arithmetic: `+ - * / // % ^` (`//` is floor division).
- Compound assignment: `+= -= *= /= //= %= ^= ..=`.
- Relational: `== ~= < > <= >=` (note `~=` not `!=`).
- Logical: `and`, `or`, `not`. `a and b or c` is the common ternary idiom.
- Concatenation: `..`. Length: `#t`.

### Strings
- Single, double, or `[[ long bracket ]]` literals.
- **String interpolation** (Luau): `` `Hello {playerName}, score {score}` ``.
- Key `string` library fns: `string.format`, `string.split`, `string.find`, `string.gsub`,
  `string.sub`, `string.match`, `string.rep`, `string.upper/lower`.

### Tables
Tables are the only data structure — used as arrays, dictionaries, or mixed.
```lua
local arr = {"a", "b", "c"}          -- 1-based array
local dict = {health = 100, name = "X"}
```
- **Tables are references**: assigning to a new variable does not copy. Use `table.clone()`
  for a shallow copy; recurse for a deep copy.
- Library: `table.insert`, `table.remove`, `table.find`, `table.concat`, `table.sort`,
  `table.clear`, `table.freeze` (read-only), `table.isfrozen`, `table.create`.
- Avoid mixed numeric+string-keyed tables when sending over remotes (keys can be lost).

### Functions
```lua
local function add(a: number, b: number): number
    return a + b
end
local f = function(...) end           -- anonymous / vararg
```
- Multiple return values: `return a, b`. Captured with `local x, y = f()`.
- Methods use `:` (passes `self`): `obj:method()` ≡ `obj.method(obj)`.

### Metatables
Enable operator overloading and OOP. Common metamethods: `__index` (fallback lookup / class
methods), `__newindex`, `__add`, `__eq`, `__tostring`, `__call`. The standard OOP pattern:
```lua
local Animal = {}
Animal.__index = Animal
function Animal.new(name)
    return setmetatable({name = name}, Animal)
end
function Animal:speak() print(self.name) end
```

### Type checking (gradual typing)
- Default mode is non-strict. Opt in per-script with `--!strict` (or `--!nonstrict`, `--!nocheck`) on line 1.
- Annotations: `local n: number`, `function f(p: Part): boolean`.
- Custom types: `type Vector = {x: number, y: number}`. Optional: `string?`. Unions: `number | string`.
  Exported: `export type Foo = {...}` then `require(M).Foo` elsewhere.
- Use strict typing in new ModuleScripts to catch bugs at edit time.

Refs: https://create.roblox.com/docs/luau · tables, functions, metatables, type-checking subpages.

---

## 2. Scripts, Execution Model & Services

### Script types
- **Script** — runs on the server (set `RunContext` or place in `ServerScriptService`).
- **LocalScript** — runs on a client (in `StarterPlayer`, `StarterGui`, `ReplicatedFirst`, or character).
- **ModuleScript** — shared, reusable code. Returns a single value (usually a table).
  Loaded once per environment via `require(module)` and cached.

### Getting services
Always use `game:GetService("Name")` (not `game.Name`):
```lua
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
```

### Common services
| Service | Use |
|---|---|
| `Players` | Player join/leave, character management |
| `ReplicatedStorage` | Shared client+server assets/scripts/remotes |
| `ServerScriptService` | Server-only scripts (not replicated to client) |
| `ServerStorage` | Server-only assets (not replicated to client) |
| `RunService` | Frame events: `Heartbeat`, `RenderStepped` (client only), `Stepped`; `IsServer/IsClient/IsStudio` |
| `TweenService` | Interpolate properties smoothly |
| `DataStoreService` | Persistent data |
| `MarketplaceService` | Passes, products, subscriptions |
| `UserInputService` / `ContextActionService` | Input (client) |
| `CollectionService` | Tag and batch-manage instances |
| `PathfindingService` | NPC navigation |
| `TeleportService` | Move players between places/servers |
| `HttpService` | `JSONEncode/JSONDecode`, external requests (if enabled) |
| `Debris` | Auto-destroy instances after a delay |
| `SoundService` | Audio |

### Instance API essentials
- `Instance.new("Part")`, `:Clone()`, `:Destroy()`, `:FindFirstChild(name)`, `:WaitForChild(name)`,
  `:GetChildren()`, `:GetDescendants()`, `:IsA("BasePart")`, `:FindFirstChildOfClass(...)`,
  `:FindFirstChildWhichIsA(...)`, `:FindFirstAncestor(...)`.
- `:WaitForChild` yields until present — use for replicated objects that may not exist yet;
  cache the result, don't call repeatedly in hot paths.

### Attributes
- `instance:SetAttribute(name, value)` / `:GetAttribute(name)`.
- **Listen with `:GetAttributeChangedSignal(name)`**, not the generic `AttributeChanged` —
  the dedicated signal is reliable for rapid server→client replication; the generic event
  can miss changes that happen close together (e.g. several attributes set during spawn).
- Property equivalent: `:GetPropertyChangedSignal(prop)` instead of polling.

---

## 3. Client–Server Communication

FilteringEnabled is always on: clients cannot directly change the server's world; the **server
is the source of truth**. Cross-boundary messaging goes through remotes in `ReplicatedStorage`.

### RemoteEvent — one-way, async, no return
```lua
-- Server
local re = ReplicatedStorage.Remotes.DoThing
re.OnServerEvent:Connect(function(player, ...)   -- player is injected automatically
    -- VALIDATE everything before acting
end)
re:FireClient(player, data)        -- server → one client
re:FireAllClients(data)            -- server → all clients

-- Client
re:FireServer(data)                -- client → server
re.OnClientEvent:Connect(function(...) end)
```

### RemoteFunction — two-way, yields for a return
```lua
-- Server
rf.OnServerInvoke = function(player, ...) return result end
-- Client
local result = rf:InvokeServer(data)   -- yields until the server returns
```
Prefer RemoteEvents for most cases. **Never invoke client→ from the server** (`:InvokeClient`):
a disconnect or client error can yield forever or error.

### Data marshalling limits (what crosses a remote)
- Functions become `nil`. Metatables are stripped.
- Instances not replicated to the receiver (e.g. `ServerStorage` contents on the client) arrive as `nil`.
- Non-string table keys may be coerced; avoid mixed numeric/string-keyed tables.

### Security rules
1. **Never trust the client.** Validate type, range, ownership, cooldown, and game-state legality server-side.
2. Rate-limit / debounce remote handlers (track last-call time per player).
3. Keep secret data and authoritative configs in `ServerStorage` / `ServerScriptService`.
4. Sanitize any user-generated strings (chat, names) before display or storage.

Ref: https://create.roblox.com/docs/scripting/events/remote

---

## 4. Data Persistence (DataStores)

```lua
local DataStoreService = game:GetService("DataStoreService")
local store = DataStoreService:GetDataStore("PlayerData")

local ok, data = pcall(function() return store:GetAsync("player_"..userId) end)
```

### Operations
- `GetAsync(key)` — read (may be slightly stale due to caching).
- `SetAsync(key, value)` — overwrite. Risky under concurrent multi-server writes.
- `UpdateAsync(key, fn)` — read-modify-write atomically; `fn(old)` returns the new value.
  **The callback may not yield** (no `task.wait`). Prefer this when keys are shared across servers.
- `IncrementAsync(key, delta)` — atomic integer change.
- `RemoveAsync(key)` — delete, returns old value.
- Ordered data stores: `OrderedDataStore` + `GetSortedAsync()` for leaderboards (no metadata/versioning).

### Best practices
- **Wrap every call in `pcall`** — network calls fail intermittently; handle and retry/back off.
- Save on `PlayerRemoving` *and* on `game:BindToClose()` (server shutdown) — BindToClose has a
  short window, so save all players in parallel and wait.
- Respect request budgets (`DataStoreService:GetRequestBudgetForRequestType`); throttle bulk ops.
- Implement session locking (store a lock token / server id) to prevent two servers clobbering data.
- Version your saved schema so you can migrate old saves.
- Keep keys consistent (e.g. `"player_" .. player.UserId`).

Ref: https://create.roblox.com/docs/cloud-services/data-stores

---

## 5. Players & Characters

```lua
Players.PlayerAdded:Connect(function(player)
    player.CharacterAdded:Connect(function(character)
        local humanoid = character:WaitForChild("Humanoid")
        local root = character:WaitForChild("HumanoidRootPart")
        -- character setup
    end)
end)
Players.PlayerRemoving:Connect(function(player) --[[ save data ]] end)
```
- `Humanoid` drives characters: `Health`, `MaxHealth`, `WalkSpeed`, `JumpPower`/`JumpHeight`,
  `HipHeight`, `AutoJumpEnabled`; signals `HealthChanged`, `Died`, `StateChanged`.
- `Humanoid:LoadAnimation(animation)` → `AnimationTrack` (or use an `Animator`). `track:Play()/Stop()/AdjustSpeed()`.
- R15 vs R6 rigs differ in part count; imported/custom rigs need `HumanoidRootPart` + proper `HipHeight`.

### Connection lifecycle
Separate **permanent** connections (attribute signals — survive respawn) from **character-scoped**
connections (Humanoid health, body parts — disconnect and recreate on each `CharacterAdded`).
Always `:Disconnect()` character connections on respawn/leave to avoid leaks and double-fires.

---

## 6. Animation

- Upload animations → get `rbxassetid://<id>`. Create an `Animation` instance with that id.
- Load on the Humanoid/Animator, keep the returned `AnimationTrack`, and play it.
- `AnimationTrack` priorities: `Core < Idle < Movement < Action` decide which track shows.
- For custom/imported models, disable the default `Animate` script if you drive animations manually
  (otherwise it conflicts).
Ref: https://create.roblox.com/docs/animation

---

## 7. UI / GUI

- `ScreenGui` (client, in `StarterGui`) → `Frame`, `TextLabel`, `TextButton`, `ImageLabel`,
  `ScrollingFrame`, etc.
- Sizing with `UDim2.new(scaleX, offsetX, scaleY, offsetY)`; position likewise. Prefer scale for
  resolution independence. Use `UIAspectRatioConstraint`, `UIListLayout`, `UIGridLayout`, `UIPadding`.
- Buttons fire `.Activated` / `.MouseButton1Click`. Drive UI from data via attribute/property signals.
- Keep UI logic in LocalScripts; never trust UI-sent values on the server without validation.
Ref: https://create.roblox.com/docs/ui

---

## 8. Performance & Memory

1. **Object pooling** — reuse parts/instances instead of `new`/`Destroy` churn.
2. **Debounce** rapid events; **throttle** per-frame work (accumulate dt, act every N seconds).
3. Use `RunService.Heartbeat` for server loops; `RenderStepped` only for client per-frame rendering.
4. Prefer **signals** (`GetAttributeChangedSignal`, `GetPropertyChangedSignal`) over polling.
5. Cache `WaitForChild`/`GetService` results; avoid repeated tree walks (`GetDescendants` in loops).
6. Use `CollectionService` tags to manage groups instead of scanning the workspace.
7. Disconnect unused connections; `Destroy()` frees instance memory and disconnects its events.
8. Use `task.spawn`/`task.defer`/`task.delay` (not deprecated `spawn`/`delay`/`wait`); `task.wait()` over `wait()`.
9. Stream large worlds with workspace streaming; keep network ownership sensible for physics.
Ref: https://create.roblox.com/docs/performance-optimization

---

## 9. Code Style & Conventions (Roblox/Luau)

- `local` everything; one service-require block at the top of each script.
- PascalCase for instances/ModuleScripts/classes; camelCase for locals/functions; UPPER_SNAKE for constants.
- Use `task.*` scheduler functions and `:Connect` (not legacy `:connect`).
- Annotate public ModuleScript APIs with types; consider `--!strict`.
- Guard external calls (DataStore, HttpService, MarketplaceService) with `pcall`.

---

## When to fetch live docs
This file is a snapshot. Re-check the source for: newly added APIs, deprecation status of an API,
exact method signatures/parameters, quota/limit numbers, and anything security-sensitive. Fetch the
raw markdown from `https://raw.githubusercontent.com/Roblox/creator-docs/main/content/en-us/<path>.md`
or the rendered page at `https://create.roblox.com/docs/<path>`.
