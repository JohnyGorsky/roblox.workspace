---
name: roblox-monetization
description: Roblox monetization implementation (APIs) for any game in this workspace — MarketplaceService prompts/ownership checks/events, the ProcessReceipt idempotency pattern (grant a dev product exactly once), game passes (cosmetics), developer products (paid revives/currency), subscriptions, and membership. Use before building/reviewing any purchase flow, paid revive, game pass, dev product, shop, or receipt handling. (What to sell / fairness is in game-design.)
---

# Roblox monetization (implementation)

Full API in [reference/monetization.md](reference/monetization.md). This is the working guide. **Prompts are
client-callable; ownership checks + grants are server-side.** Design/fairness → `game-design`.

## The #1 rule: ProcessReceipt idempotency

Dev-product grants (paid revives, currency) run **only** in `MarketplaceService.ProcessReceipt` (set once on
the server). Key on the unique **`PurchaseId`**, grant exactly once, and **return `PurchaseGranted` only
after the durable save succeeds** (else `NotProcessedYet` → Roblox retries). Use `UpdateAsync` (atomic), not
`SetAsync`. **Never grant money-bearing items from `...PurchaseFinished` events** (they don't guarantee
payment settled and aren't retried). Full pattern in the reference.

## Game passes (cosmetics — Last River)

Check **each join** server-side: `UserOwnsGamePassAsync(player.UserId, passId)` (pass UserId) → prompt with
`PromptGamePassPurchase` if not owned → re-apply the perk. Don't rely on the Finished event across sessions.

## Developer products (paid revive / soft-currency packs)

`PromptProductPurchase(player, productId)` → grant in `ProcessReceipt`. Paid revive = restore/respawn in the
grant handler; currency pack = increment the profile. Both repeatable, both idempotent.

## Subscriptions

`PromptSubscriptionPurchase` (string id); verify with `GetUserSubscriptionStatusAsync` server-side and
**revoke benefits when lapsed** (re-check on join).

## Always
`pcall` every yielding Marketplace call; server validates ownership (client claims are UI-only); no
misleading/auto-fired prompts. Persist purchase history in the session-locked profile (see `roblox-data`).
Note: Engagement/Premium Payouts are deprecated → Creator Rewards (dashboard, no runtime API).
