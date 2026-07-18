---
name: roblox-audio
description: Roblox audio engineering for any game in this workspace — the modern audio-object API (AudioPlayer/AudioEmitter/AudioListener/Wire + effects), the legacy Sound API, 3D/spatial positioning (boat engine, animal growls, gunfire), dynamic/adaptive music (layered crossfade), reverb/EQ effects, and mobile perf. Use before adding/reviewing any sound, music, spatial audio, or audio effects. (Sourcing/licensing is in roblox-assets.)
---

# Roblox audio

Full API in [reference/audio.md](reference/audio.md). This is the working guide. **New audio-object API is
recommended for new work** (`Sound`/`SoundGroup` are "discouraged" but fine for quick cases).

## Spatial SFX (emit from a world position)

- **New:** `AudioPlayer → Wire → AudioEmitter` parented to the part; shape falloff with
  `emitter:SetDistanceAttenuation({[0]=1,[30]=0.6,[90]=0})`. The listener is auto-created via
  `SoundService.DefaultListenerLocation = Enum.ListenerLocation.Character` (or `.Camera`).
- **Legacy (simplest):** a `Sound` parented to a `BasePart`/`Attachment` is 3D positional; tune
  `RollOffMinDistance`/`MaxDistance`.
- **Last River:** boat engine = looping AudioPlayer/Emitter on the engine part, modulate `Volume`/
  `PlaybackSpeed` with throttle; animal growls = one-shot on the creature; gunfire = short one-shot on the
  muzzle Attachment (tight falloff, pooled).

## Dynamic music (layered crossfade)

Run parallel looping tracks started together; tween each layer's volume (an `AudioFader` per track, or a
`SoundGroup` per track) to blend calm → tension → combat and day → night via `TweenService`. **Keep music
client-side** (don't network it). Music-reactive VFX via `AudioAnalyzer`/`Sound.PlaybackLoudness`.

## Effects

Chain `Audio*` effects (Reverb/Echo/Equalizer/Fader/Analyzer) via Wires (per-emitter or bus), `Bypass` to
toggle. Cheap global ambience: `SoundService.AmbientReverb` (`Enum.ReverbType`) switched per zone
(cave/underwater/jungle).

## Perf (mobile)

`ContentProvider:PreloadAsync` zero-latency SFX (gunfire/UI); stream large music; **limit concurrent
one-shots** (pool + cull distant/quiet + dedupe rapid identical); prefer **mono** for spatial; `Bypass`
idle effect chains. Sourcing/licensing/scan → **`roblox-assets`** (audio ≤20MB/≤7min, private by default).
