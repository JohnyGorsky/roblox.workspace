# Roblox audio — reference

Sourced from official Creator Docs, current 2026-07. Not-verbatim items flagged **[unverified]**.

## Which API (2026)

Docs mark **`Sound`/`SoundGroup`/`SoundEffect` as "discouraged"** in favor of the modern **audio-object
API** (`AudioPlayer` + `Wire` graph). Use the **new API** for new work; the legacy `Sound` API is fully
functional, ubiquitous, and simpler for quick cases.

## New audio-object API (graph)

Audio flows through objects connected by **`Wire`**s. Roles: **Producers** (`AudioPlayer`,
`AudioDeviceInput`), **Consumers** (`AudioEmitter`, `AudioDeviceOutput`), **Modifiers** (`Audio*` effects).
Pins: output `"Output"`, input `"Input"`.
- **2D:** `AudioPlayer → Wire → AudioDeviceOutput`. **3D:** `AudioPlayer → Wire → AudioEmitter` (in world)
  + `AudioListener → Wire → AudioDeviceOutput` (auto-managed).
- **`Wire`:** `SourceInstance`, `SourceName` (default `"Output"`), `TargetInstance`, `TargetName`
  (set `"Input"`), `Connected`.
- **`AudioPlayer`:** `Asset` (ContentId), `Looping`, `IsPlaying`, `IsReady`, `Volume`, `PlaybackSpeed`,
  `PlaybackRegion`/`LoopRegion`, `TimePosition`; `Play(atTime?)`/`Stop()`; events `Ended`/`Looped`.
  (Note: `Looping`/`IsPlaying`, not legacy `Looped`/`Playing`.)
- **`AudioEmitter`** (spatial out; **position = parent's** — parent to a part/Attachment):
  **`SetDistanceAttenuation({[studs]=gain})`** shapes falloff (new-API RollOff), `SetAngleAttenuation` for
  directional sources.
- **`AudioListener`** (ear): usually auto-created — set `SoundService.DefaultListenerLocation =
  Enum.ListenerLocation.Character` (or `.Camera`) and the engine makes the listener + per-player
  `AudioDeviceOutput`. `AudioInteractionGroup` scopes who hears what.
- **`AudioDeviceInput`** (mic/voice): `Player`, `Muted`, `Volume` — push-to-talk via `Muted`.
- **Effects** (chain via Wires; each has `Bypass`): `AudioFader` (`Volume` — use for crossfades),
  `AudioEqualizer` (`LowGain`/`MidGain`/`HighGain`/`MidRange`), `AudioReverb`, `AudioEcho`, `AudioChorus`,
  `AudioAnalyzer` (`PeakLevel`/`RmsLevel`/`GetSpectrum()` → music-reactive VFX). `AudioCompressor` etc.
  exist **[props unverified]**.

**Script pattern (boat-engine emitter):**
```lua
local p = Instance.new("AudioPlayer"); p.Asset="rbxassetid://<id>"; p.Looping=true; p.Parent=enginePart
local e = Instance.new("AudioEmitter"); e.Parent=enginePart; e:SetDistanceAttenuation({[0]=1,[30]=0.6,[90]=0})
local w = Instance.new("Wire"); w.SourceInstance=p; w.TargetInstance=e; w.TargetName="Input"; w.Parent=enginePart
p:Play()
```

## Legacy Sound API

- **`Sound`:** `SoundId`, `Volume`, `Looped`, `PlaybackSpeed`, `TimePosition`, `Playing`,
  `PlaybackLoudness` (live loudness → reactive VFX), `RollOffMode`/`RollOffMinDistance`/`RollOffMaxDistance`,
  `SoundGroup`; `Play()`/`Stop()`/`Pause()`/`Resume()`; events `Ended`/`Loaded`/`DidLoop`.
  **A `Sound` parented to a BasePart/Attachment is 3D positional** (attenuates by RollOff).
- **`SoundGroup`** (`Volume` + parented `SoundEffect`s: Reverb/Equalizer/Echo/…). Route via `sound.SoundGroup`.
- **`SoundService`:** `AmbientReverb` (`Enum.ReverbType` — global env reverb preset per zone, cheap),
  `DefaultListenerLocation`, `PlayLocalSound(sound)` (non-spatial local play), `SetListener`.

## Spatial (emit from a world position)

**Legacy:** looping `Sound` in the creature's `HumanoidRootPart`/Attachment, tune RollOff min/max.
**New:** `AudioPlayer → AudioEmitter` on the part + `SetDistanceAttenuation` (+ `AngleAttenuation` for
gun muzzle/horn). Boat engine = looping, modulate `Volume`/`PlaybackSpeed` (or an `AudioFader`) with
throttle. Gunfire = short one-shot on the muzzle Attachment, tight falloff, pooled/limited.

## Dynamic / adaptive music

Run parallel looping tracks (new: each through an `AudioFader`; legacy: one `SoundGroup` each), started
together (phase-aligned), and **tween each fader/group `Volume`** to bring layers in/out (calm → tension →
combat; day → night). Drive from game state via `TweenService`. Music-reactive UI via `AudioAnalyzer` /
`Sound.PlaybackLoudness`. **Keep music client-side** (don't stream over network).

## Effects & perf

New: insert `Audio*` effects into the wire chain (per-emitter or bus), `Bypass` to toggle. Legacy: parent
`SoundEffect`s to a Sound/SoundGroup + `SoundService.AmbientReverb` per zone.
**Perf/mobile:** `ContentProvider:PreloadAsync({...})` for zero-latency SFX (gunfire/UI); stream large
music; **limit concurrent one-shots** (pool + cull distant/quiet + dedupe rapid identical SFX); prefer
**mono** for spatial (cheaper + needed for spatialization); music client-local; `Bypass` idle effect chains.
**Licensing/sourcing → the `roblox-assets` skill** (inventory-first → Creator Store → license → approval;
audio ≤20MB/≤7min/≤48kHz, private by default).

## Sources
audio/{objects,assets}, tutorials/.../audio/{add-3D-audio,add-2D-audio}, classes/{AudioPlayer,AudioEmitter,
AudioListener,AudioDeviceOutput,AudioDeviceInput,Wire,AudioFader,AudioEqualizer,AudioReverb,AudioEcho,
AudioChorus,AudioAnalyzer,Sound,SoundGroup,SoundService}.
