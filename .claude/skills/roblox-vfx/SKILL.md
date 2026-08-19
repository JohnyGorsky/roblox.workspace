---
name: roblox-vfx
description: Roblox visual effects & lighting for any game in this workspace — ParticleEmitter, Beam, Trail, legacy Fire/Smoke/Sparkles/Explosion, PointLight/SpotLight/SurfaceLight, the Lighting service (day/night, fog), Atmosphere/Sky, post-processing (Bloom/Blur/ColorCorrection/DepthOfField/SunRays), and shadows. Use before adding/reviewing any particle, beam, trail, light, glow, fog, sky, post-effect, or shadow — and for day/night cycles. Mind mobile perf.
---

# Roblox VFX & lighting

Full API in [reference/vfx.md](reference/vfx.md). This is the working guide. **Mind mobile cost** —
effects are GPU-heavy and our games are mobile-first.

## Gotchas (get these right)

- **Beam has NO `Emit`/`Clear`** — only `SetTextureOffset`. **ParticleEmitter** has `Emit(count)`+`Clear()`;
  **Trail** has `Clear()`.
- **Trail `WidthScale` is a NumberSequence** (not a number). **Atmosphere `Decay` is a Color3** (not a number).
- **`Lighting.Technology` NO LONGER EXISTS on the Lighting instance** (verified 2026-08-19 — not even
  readable from Luau). It is replaced by **`LightingStyle`** (`Enum.LightingStyle`: `Realistic`=0,
  `Soft`=1) and **`PrioritizeLightingQuality`** (bool). Both are **read-only to scripts**, even under
  plugin capability — they are Properties-panel values only.
- Particle **`Rate` is capped 400/s desktop, 100/s mobile**; `Lifetime` max 20s; flipbooks auto-disable on low memory.
- `LightEmission = 1` → additive blending (glow). `ZOffset` layers emitters without changing screen size.

## Quick recipes

- **Burst (muzzle/impact/pickup):** a disabled `ParticleEmitter`, call `:Emit(n)` on the event.
- **Glow:** `ParticleEmitter`/`Beam`/`Trail` with `LightEmission = 1` + a bright `Color`.
- **Boat wake / speed lines:** `Trail` between two attachments on the hull; `TextureMode = Wrap`.
- **Water splash / spray:** upward `ParticleEmitter`, `Acceleration` gravity, blue-white `Color` fading `Transparency`.
- **Engine smoke:** `Smoke` (simple) or a `ParticleEmitter` with dark `Color`, slow `Speed`, rising `Acceleration`.
- **Energy/laser link:** `Beam` between attachments, `CurveSize` for sag, animated `SetTextureOffset`.
- **Day/night:** tween `Lighting.ClockTime` (0–24) over time; pair with `Atmosphere` + `ColorCorrectionEffect`
  tint for dawn/dusk/night mood (fits the Jungle day/night pillar).
- **Jungle atmosphere:** `Atmosphere` (`Haze`, `Density`, greenish `Color`) instead of basic Fog; light
  `SunRaysEffect` through canopy; subtle `DepthOfFieldEffect`.

## Shadows & lighting tech

**Current model (verified against live Studio 2026-08-19).** `Lighting.Technology` is gone; the two
properties that exist are:

| Property | Values | Notes |
|---|---|---|
| `LightingStyle` | `Realistic` (0), `Soft` (1) | `Realistic` is the high-quality path (the old `Future` role) — **heaviest on mobile**. `Soft` is the cheaper default |
| `PrioritizeLightingQuality` | bool | Trades shadow range against view distance under load |

**Both are read-only to scripts** — set them in the Properties panel with `Lighting` selected, per place.
A script cannot configure or repair them, so they belong on a human checklist and in a settings spec.

`Lighting.GlobalShadows` (master toggle), `Lighting.ShadowSoftness` and `BasePart.CastShadow` **are**
scriptable. Keep shadow-casting local lights few and don't stack post-effects.

`Enum.Technology` still exists (`Legacy`/`Voxel`/`Compatibility`/`ShadowMap`/`Future`/`Unified`) but no
longer maps to a property — treat any doc or answer that says "set Lighting.Technology" as out of date.
