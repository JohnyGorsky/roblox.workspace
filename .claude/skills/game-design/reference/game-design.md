# Game design for Roblox — reference (2025–2026)

Sourced; evidence tagged `[OFFICIAL]` (Roblox docs/newsroom), `[INDUSTRY]` (game-design theory),
`[COMMUNITY]` (creators/analytics), `[OPINION]`. Numbers are "official" only from Roblox itself.

## 1. Core loop & engagement

**Core loop** `[OFFICIAL]` = (1) minute-to-minute interaction → (2) the most-repeated defining action →
(3) a **progression engine**. "Without a progression system, a game becomes repetitive, boring, and
shallow." Canonical: Explore → Fight → Upgrade.

**"One more run" drivers:** a **visible next unlock** `[COMMUNITY]`; **flow** — challenge tracks skill,
stair-step ramps with recovery dips `[INDUSTRY]`; **fun in <5 min** or players bounce `[OFFICIAL]`;
**social pull** — Roblox rewards friends playing together; single-player retains poorly `[OFFICIAL]`;
**clip-worthy moments** `[COMMUNITY]`.

**Loops of top games** (CCU/visit numbers are third-party/approx): Grow a Garden (plant→wait→sell→better
seeds/pets, AFK-friendly + fair — no whale steamroll); Blox Fruits (grind→level→unlock→harder zones);
**Dead Rails** (our genre — roguelike co-op: fuel the train, defend, scavenge, reach the border;
permadeath per run + meta-unlocks via bonds; day/night pacing; ~18-min sessions); Brookhaven (social
sandbox, cosmetic updates); tycoons/simulators (collect→upgrade→**rebirth/prestige**); obbies
(checkpoint mastery, weak native retention).

## 2. Replayability patterns (fit for a co-op survival run game)

- **Procedural/seeded** — new layout each run; seeds reproduce for debug + fair competition. **High.**
- **Roguelike run + permadeath** — bounded run = stakes; "structured variability." **Core.**
- **Meta-progression/unlocks** — persistent upgrades soften permadeath, reward experimentation. **Core.**
- **Prestige/rebirth** — reset for a permanent multiplier. Medium.
- **Leaderboards** (distance/speed), **daily rewards & streaks** (habit — High), **short weekly
  limited-time events** (FOMO — keep short), **seasons/battle pass** (once core is stable), **co-op roles**
  (interdependence — Core), **gacha/collection** cosmetics (Medium).
- **Agency rule** `[INDUSTRY]`: balance randomness vs agency — give **meaningful choices over what the RNG
  deals** (loot/route/class), not pure luck.

## 3. Progression, economy & balance

- **Retention (D1/D7/D30)** `[OFFICIAL]`: D1 ← tight core loop + FTUE (tutorial < ~5 min) + device perf;
  D7 ← clear short/long goals + content variety + balanced difficulty; D30 ← updates every **2–4 weeks
  (minor) / 2–3 months (major)** + social systems. Focus **D1 + session time** first. **Roblox publishes
  NO benchmark numbers** — any "good D1 = X%" is third-party.
- **FTUE** `[OFFICIAL]`: teach essentials (what + why), get to fun fast (starter items/currency, low early
  thresholds), leave them wanting more (multiple goals, milestone "moments of joy"). Keep tutorials short.
- **Economy** `[INDUSTRY]`: dual currency (soft earned + hard); **faucets ≈ sinks** (faucet>sink =
  inflation; too-harsh sinks = churn); sinks = upgrades/unlocks/cosmetics/consumables/repairs/revives;
  always keep a next affordable goal.
- **No pay-to-win** `[INDUSTRY]`+`[OFFICIAL policy]`: sell time/cosmetics/convenience, never power; don't
  give payers an advantage others "can't compete against."

## 4. Monetization that retains

Tools `[OFFICIAL]`: **game passes** (permanent perks), **developer products** (repeatable — revives,
currency, boosts), **private servers** (keep cheap), subscriptions, Creator Rewards. "Fair" = sell
**convenience/cosmetics/paid revives**, layer in **after retention is proven**, genuine discounts only.
**Correction** `[OFFICIAL]`: **Engagement-Based/Premium Payouts were DEPRECATED 2025-07-24 → replaced by
Creator Rewards** — don't cite "Premium Payouts" as current. The algorithm now pays out + promotes based
on **retained, co-playing users**, so fairness *is* the strategy.

## 5. Roblox discovery & live-ops

**2026 algorithm** `[OFFICIAL]`: "Recommended For You" favors **long-term value over clickbait**; retention
window widened **7 → 28 days** (D1 / D2–7 / D8–28 buckets); signals split into play-through / session
quality / spend; signal list + relative weights now shown in Creator Analytics (no exact % disclosed).
`[COMMUNITY]` reported extra signal: **7-day *intentional* co-play** (invites/friend-joins/private servers;
random matchmaking doesn't count). Third-party "targets" (NOT official): D1 >20%, D7 >8%, like >70%, 15+ min sessions.

**Levers:** thumbnail/icon+title (CTR gate); low first-session bounce; growth velocity → algorithmic
promotion flywheel; design for **invites/friend-joins**; clip-friendly for short-form/TikTok.
**Live-ops = the retention driver** `[OFFICIAL]`: weekly-to-monthly cadence, keep each cycle <~3 weeks of
effort, tie every update to the core loop, avoid burnout; **abandoned games decay**; a bad update can
*drop* retention (don't break the core loop). **Mobile-first** — majority of play is mobile; don't
prioritize fidelity over fun.

## 6. Checklist (make it sticky)

Core loop in one sentence · fun <5 min · always a visible next unlock (short/mid/long) · flow-tuned
difficulty · varied-but-familiar runs (seeded) · permadeath softened by meta-progression · designed for
friends · daily + weekly + seasonal reasons to return · faucets≈sinks, no P2W · monetize
convenience/cosmetics/revives after retention proven · clip-worthy moments · sustainable live-ops plan ·
mobile-first, device-tested.

**Pitfalls that kill replayability:** no progression engine; long/forced tutorial → bounce; difficulty
spikes/flats → out of flow; pure RNG (no agency); faucet>sink; selling power; monetizing too early;
single-player-only; ship-and-abandon; clickbait over substance (punished by the 28-day window); breaking
the core loop with a "big" update.

## [→ Last River] applied
Seeded procedural river runs + permadeath + persistent class/perk unlocks + short weekly events + daily
streaks + distance/speed leaderboards; co-op roles for interdependence; monetize **paid revives** (fits
permadeath, feels fair) + cosmetic boat/character skins + cheap private servers — no stat passes.
Battle pass + gacha cosmetics only after D1/D7 are healthy.

## Sources
Roblox: production/game-design/{core-loops,onboarding,liveops-essentials,design-for-roblox},
production/analytics/{retention,engagement}, production/monetization(+engagement-based-payouts), discovery,
2026 discovery newsroom. Industry: flow & difficulty-curve theory, roguelike agency, F2P economy design.
Community/trackers (directional only): RTrack/Rolimon's, Dead Rails & Grow-a-Garden analyses.
