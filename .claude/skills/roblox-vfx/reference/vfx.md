# Roblox VFX & lighting — reference

Sourced from official Creator Docs, current 2026-07. Types are as docs list them. Not-verbatim items
flagged **[unverified]**.

## ParticleEmitter

Props (type): `Rate` (num), `Lifetime` (NumberRange, **max 20s**), `Speed` (NumberRange), `SpreadAngle`
(Vector2), `Rotation`/`RotSpeed` (NumberRange), `Size`/`Transparency`/`Squash` (NumberSequence), `Color`
(ColorSequence), `Texture` (ContentId), `LightEmission` (0 normal → 1 additive glow), `LightInfluence`,
`Acceleration` (Vector3), `Drag`, `VelocityInheritance`, `EmissionDirection` (Enum.NormalId), `Orientation`
(Enum.ParticleOrientation: FacingCamera/FacingCameraWorldUp/VelocityParallel/VelocityPerpendicular),
`Shape`/`ShapeStyle`/`ShapeInOut`/`ShapePartial`, `ZOffset` (layer depth w/o size change), `WindAffectsDrag`,
`LockedToPart`, `TimeScale`, `Brightness`, `FlipbookLayout/Mode/Framerate`, `Enabled`.
**Methods:** `Emit(count)`, `Clear()`.
**Perf/mobile:** `Rate` capped **400/s desktop, 100/s mobile**; large on-screen size → GPU fill-rate;
overlapping transparent particles → overdraw; flipbooks use lots of memory and **auto-disable on
low-memory devices**.

## Beam

`Attachment0/1`, `CurveSize0/1`, `Width0/1`, `Texture`, `TextureMode` (Enum), `TextureSpeed`,
`TextureLength`, `Color` (ColorSequence), `Transparency` (NumberSequence), `LightEmission`, `Brightness`,
`FaceCamera` (bool), `Segments`, `ZOffset`, `Enabled`. **Only method: `SetTextureOffset(offset)` — NO
Emit/Clear.** Connects two attachments (lasers, ziplines, energy links, water streams).

## Trail

`Attachment0/1`, `Lifetime` (num), `Texture`, `TextureMode`, `TextureLength`, `Color` (ColorSequence),
`Transparency` (NumberSequence), **`WidthScale` (NumberSequence — not a number)**, `MinLength`,
`MaxLength`, `FaceCamera`, `LightEmission`, `Brightness`, `Enabled`. Method: `Clear()`. Follows a moving
part between two attachments (boat wake, projectile trail, speed lines).
**`Enum.TextureMode`** (Beam+Trail): `Stretch`(0), `Wrap`(1 tiles), `Static`(2).

## Legacy VFX (still valid; note deprecated props)

- **Fire** — `Size`, `Heat`, `Color`, `SecondaryColor`, `Enabled` (`TimeScale`/lowercase `size` deprecated).
- **Smoke** — `Size`, `Opacity`, `RiseVelocity`, `Color`, `Enabled`.
- **Sparkles** — `SparkleColor` (use this; `Color` deprecated), `Enabled`.
- **Explosion** — `BlastPressure`, `BlastRadius`, `DestroyJointRadiusPercent`, `ExplosionType`
  (`Craters`/`NoCraters`), `Position`, `Visible`; event `Hit(part, distance)`.
- Prefer **ParticleEmitter** for controllable/high-fidelity effects.

## Lights

Base `Light`: `Brightness`, `Color`, `Shadows` (bool), `Enabled`. **PointLight** +`Range`. **SpotLight**/
**SurfaceLight** +`Range`, `Angle`, `Face` (Enum.NormalId). Per-light `Shadows` only render with a
shadow-capable `Technology`. Keep shadow-casting lights few on mobile **[unverified cap]**.

## Lighting service

`Ambient`, `OutdoorAmbient`, `Brightness`, `ColorShift_Top/Bottom`, `EnvironmentDiffuseScale`,
`EnvironmentSpecularScale`, `ExposureCompensation`, `GlobalShadows` (bool), `ShadowSoftness`, `ClockTime`
(0–24), `TimeOfDay` ("HH:MM:SS"), `GeographicLatitude`, `FogStart`/`FogEnd`/`FogColor`.
Methods: `Get/SetMinutesAfterMidnight`, `GetSunDirection`, `GetMoonDirection`.
**Day/night:** animate `ClockTime` (or SetMinutesAfterMidnight). Prefer **`Atmosphere`** over basic Fog.
⚠️ **`Lighting.Technology` no longer exists on the Lighting instance** (verified 2026-08-19; reading it
from Luau fails). Use `LightingStyle` + `PrioritizeLightingQuality` — see Shadows below. Both are
read-only to scripts.

## Effect children of Lighting

- **Atmosphere** — `Density`, `Offset`, `Color`, **`Decay` (Color3 — not a number)**, `Glare`, `Haze`.
- **Sky** — skybox faces `Skybox{Bk,Dn,Ft,Lf,Rt,Up}` (ContentId), `SunAngularSize`, `MoonAngularSize`,
  `StarCount`, `CelestialBodiesShown`, `Sun/MoonTextureId`.
- **Post-processing** (all inherit `Enabled` from `PostEffect`):
  `ColorCorrectionEffect` (`Brightness`/`Contrast`/`Saturation`/`TintColor`), `BloomEffect`
  (`Intensity`/`Size`/`Threshold`), `BlurEffect` (`Size`), `DepthOfFieldEffect`
  (`FarIntensity`/`FocusDistance`/`InFocusRadius`/`NearIntensity`), `SunRaysEffect` (`Intensity`/`Spread`).
  Each is a full-screen GPU pass — stacking many is costly on mobile.

## Shadows

`BasePart.CastShadow` (false on clutter to save cost), `Lighting.GlobalShadows` (master toggle),
`Lighting.ShadowSoftness` (**only with ShadowMap/Future**), per-light `Shadows`.
**Current properties** (verified live 2026-08-19), both **read-only to scripts** — Properties panel only,
per place:
- **`Lighting.LightingStyle`** — `Enum.LightingStyle`: `Realistic`(0) = high-quality path, the old
  `Future` role, **heaviest on mobile**; `Soft`(1) = cheaper, and the default on new places.
- **`Lighting.PrioritizeLightingQuality`** (bool) — trades shadow range vs view distance under load.
  Consider `false` where long sightlines matter more than shadow detail (open water, distant POIs).

**`Enum.Technology`** still exists — `Legacy`(0), `Voxel`(1), `Compatibility`(2), `ShadowMap`(3),
`Future`(4), `Unified`(5) — but **no property consumes it any more**. `ShadowSoftness` used to require
ShadowMap/Future; re-verify its behavior under `LightingStyle` before relying on it.

## Mobile/perf summary
Particle Rate capped lower on mobile (100/s); flipbooks auto-disable on low memory; `LightingStyle =
Realistic` is the heaviest lighting path; `ShadowSoftness` needs ShadowMap/Future; disable `CastShadow` on clutter; minimize
shadow-casting local lights and stacked post-effects.

## Sources
classes/{ParticleEmitter,Beam,Trail,Fire,Smoke,Sparkles,Explosion,Light,PointLight,SpotLight,SurfaceLight,
Lighting,Atmosphere,Sky,PostEffect,ColorCorrectionEffect,BloomEffect,BlurEffect,DepthOfFieldEffect,
SunRaysEffect,BasePart}, enums/{TextureMode,ParticleOrientation,Technology,ExplosionType},
effects/particle-emitters, environment/lighting.
