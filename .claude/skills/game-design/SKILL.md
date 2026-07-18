---
name: game-design
description: Game design, balance & replayability for Roblox games in this workspace — core loops, retention (D1/D7/D30) & onboarding, replayability patterns (procedural/roguelike/meta-progression/dailies/seasons), economy & difficulty balance, fair monetization, and the 2026 discovery algorithm / live-ops. Use when designing or reviewing gameplay, tuning balance/economy, planning progression or monetization, or reasoning about what makes a game repeatable and sticky. (A game's specific tuning numbers live in that game's own balance skill.)
---

# Game design, balance & replayability

Full sourced detail in [reference/game-design.md](reference/game-design.md). This is the working guide.
This skill = generic design principles; a game's concrete tuning numbers live in its own balance skill
(e.g. Defender's `game-balance`).

## The core

- **State the core loop in one sentence:** minute-to-minute action → the repeated defining action →
  a **progression engine**. No progression = boring. If you can't state it, players won't feel it.
- **Fun in <5 minutes**, tutorial embedded in real play (short). **Always a visible next unlock** at
  short / mid / long horizons. **Flow-tuned difficulty** (stair-step ramp with recovery beats).
- **Design for friends** — Roblox rewards co-play (retention *and* a discovery signal); single-player retains poorly.

## Replayability (for run-based / co-op games)

**Seeded procedural** runs + **roguelike permadeath** + **meta-progression unlocks** (softens permadeath)
+ **daily streaks** + **short weekly events** + **leaderboards** + **co-op roles**. Give players
**meaningful choices over what the RNG deals** — not pure luck. Add seasons/battle-pass/gacha only after
D1/D7 are healthy.

## Balance & economy

Dual currency (soft earned + hard). **Faucets ≈ sinks** — keep a next affordable goal; faucet>sink =
inflation, harsh sinks = churn. Difficulty in the flow channel; scale run baseline via unlocked tiers,
not one flat curve. **Never sell power (P2W).**

## Monetization (fair = retaining)

Sell **convenience / cosmetics / paid revives**; layer passes/products in **after retention is proven**;
genuine discounts only. ⚠️ **Engagement-Based/Premium Payouts were deprecated 2025-07-24 → Creator
Rewards** — don't reference "Premium Payouts" as current. Roblox promotes + pays out on retained,
co-playing users, so fairness is the strategy.

## Discovery & live-ops (2026)

The algorithm favors **long-term value over clickbait** (retention window widened to **28 days**);
intentional **co-play** is a strong signal. Thumbnail/title = CTR gate; low first-session bounce; growth
velocity → promotion flywheel. **Live-ops is the retention driver** — weekly-to-monthly updates (<~3 weeks
effort each), always tied to the core loop; abandoned games decay; don't break the core loop with a big update.

## Honesty about numbers

Roblox publishes **no official D1/D7/like-ratio benchmarks** — any specific threshold (e.g. "D1 >20%") is
third-party; label it as such. Real popularity CCU/visit figures fluctuate — treat as directional.
