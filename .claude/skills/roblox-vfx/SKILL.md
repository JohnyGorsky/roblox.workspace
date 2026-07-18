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
- **`Lighting.Technology` is set in Studio's rendering settings, not by script** (deprecated as settable).
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

`Lighting.GlobalShadows` master toggle; `BasePart.CastShadow=false` on clutter; `ShadowSoftness` needs
**ShadowMap/Future** tech. `Voxel` = cheapest (blocky, 4-stud grid), `ShadowMap` = sharp sun shadows,
`Future` = best but **heaviest on mobile**. Keep shadow-casting local lights few; don't stack many
post-effects. Set the Technology to match the target device budget (in Studio settings).
