# Roblox monetization implementation — reference

Sourced from official Creator Docs, current 2026-07. Not-verbatim items flagged **[unverified]**.
Design/what-to-sell is in `game-design`; this is the **implementation**. **Prompts are client-callable;
ownership checks + grants are server-side.**

## MarketplaceService

**Prompts:** `PromptProductPurchase(player, productId)` (dev products — repeatable),
`PromptGamePassPurchase(player, gamePassId)`, `PromptPurchase(player, assetId)` (catalog),
`PromptSubscriptionPurchase(player, subscriptionId)` (id is a **string**), `PromptBundlePurchase`.
(`PromptPremiumPurchase` deprecated.)
**Info/ownership (yield → `pcall`):** `GetProductInfoAsync(id, Enum.InfoType)` (`GetProductInfo`
deprecated), `UserOwnsGamePassAsync(userId, passId)` (**pass UserId, not player**),
`PlayerOwnsAssetAsync(player, assetId)`, `GetUserSubscriptionStatusAsync(player, subId)` (server-only),
`GetDeveloperProductsAsync()`.
**Events:** `PromptGamePassPurchaseFinished(player, passId, wasPurchased)`,
`PromptProductPurchaseFinished(userId, productId, isPurchased)` (**userId, not player**),
`PromptSubscriptionPurchaseFinished(user, subId, didTry)`. ⚠️ **`...Finished` events only mean the prompt
closed / user tried — NOT a reliable grant. Money-bearing dev-product grants go through `ProcessReceipt`.**

## ProcessReceipt — the critical path (idempotency)

`MarketplaceService.ProcessReceipt = fn(receiptInfo) → Enum.ProductPurchaseDecision` — set **once, server-side**.
`receiptInfo`: `PlayerId`, `ProductId`, **`PurchaseId`** (unique receipt id), `CurrencySpent`, `CurrencyType`,
`PlaceIdWherePurchased`. Return **`PurchaseGranted`** (only after the grant is durably saved) or
**`NotProcessedYet`** (Roblox **re-calls later / on rejoin / on other servers** until Granted). The same
`PurchaseId` **will** arrive more than once → **grant exactly once.**

**Documented 5-step flow:** player loaded on this server? (else NotProcessedYet) → `PurchaseId` not already
recorded? → award in-memory → record the `PurchaseId` → **save; only return Granted after save succeeds.**
```lua
local store = DataStoreService:GetDataStore("PurchaseHistory")
local grants = { [123123] = function(player) --[[ e.g. paid revive / +currency ]] return true end }
MarketplaceService.ProcessReceipt = function(r)
    local player = Players:GetPlayerByUserId(r.PlayerId)
    if not player then return Enum.ProductPurchaseDecision.NotProcessedYet end
    local key = ("%d_%s"):format(r.PlayerId, r.PurchaseId)   -- idempotency key = PurchaseId
    local granted = false
    local ok = pcall(function()
        store:UpdateAsync(key, function(done)                 -- atomic; not SetAsync
            if done then granted = true; return done end      -- already granted → don't repeat
            local h = grants[r.ProductId]
            if h and h(player) then granted = true; return true end
            return nil                                         -- grant failed → don't record → retry
        end)
    end)
    return (ok and granted) and Enum.ProductPurchaseDecision.PurchaseGranted
        or Enum.ProductPurchaseDecision.NotProcessedYet
end
```
(In production fold `PurchaseId` into the player's session-locked profile — one source of truth. See `roblox-data`.)

## Game passes (one-time perks — cosmetics)

Create on dashboard → id. Check each join (server): `pcall(function() return
MarketplaceService:UserOwnsGamePassAsync(player.UserId, passId) end)`; prompt if not owned; re-apply the perk
every session (don't rely on the Finished event across sessions). `GamePassService:PlayerHasPass` is
deprecated — use `UserOwnsGamePassAsync`.

## Developer products (repeatable — paid revives, currency)

Create on dashboard → id → `PromptProductPurchase(player, productId)` → **grant ONLY in `ProcessReceipt`**
(idempotent). Paid revive = a grant handler that restores/respawns; currency pack = increments the profile.

## Subscriptions

Via MarketplaceService (string ids). `PromptSubscriptionPurchase`; check server-side with
`GetUserSubscriptionStatusAsync` (returns `{IsSubscribed, IsRenewing, ExpireTime, ...}`) — **revoke benefits
when it lapses** (re-check on join). Metadata via `GetSubscriptionProductInfoAsync`.

## Currency, membership, payouts

No API to read a player's Robux balance. Premium: `Player.MembershipType` (`Enum.MembershipType`) — prefer
`Player.HasRobloxSubscription` for the platform sub. ⚠️ **Engagement-Based/Premium Payouts DEPRECATED
2025-07-24 → Creator Rewards** (a dashboard program, no runtime API).

## Best practices
Server-authoritative ownership + grants; **ProcessReceipt idempotency** is the #1 rule; `pcall` every
yielding call; right signal per product (passes/subs → ownership/status checks each session; dev products →
ProcessReceipt); no misleading/auto-fired prompts; don't sell power (see `game-design`).

## Sources
classes/{MarketplaceService,Player}, production/monetization/{developer-products,game-passes,subscriptions,
engagement-based-payouts}, cloud-services/data-stores/player-data-purchasing.
