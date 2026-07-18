---
name: roblox-camera
description: Roblox camera control for any game in this workspace — the Camera object, Scriptable vs Custom, RenderStep timing, a mobile-friendly custom chase/follow camera (with a ready boat chase-cam), default-camera tuning (zoom/occlusion/touch modes), camera shake & FOV punch, and gotchas. Use before building/reviewing any custom camera, chase cam, first-person, camera shake, or mobile camera controls.
---

# Roblox camera

Full API + a ready boat chase-cam in [reference/camera.md](reference/camera.md). This is the working guide.
**All camera code runs in a LocalScript (per-client).**

## Custom camera essentials

- `camera.CameraType = Enum.CameraType.Scriptable` **before** driving `camera.CFrame` (else default scripts
  overwrite you). Return control with `CameraType = Custom`.
- Drive it in **`RunService:BindToRenderStep(name, Enum.RenderPriority.Camera.Value, fn)`** — NOT Heartbeat
  (or it lags a frame). Update **`camera.Focus`** every frame.
- **Frame-rate-independent smoothing:** lerp alpha = `1 - math.exp(-k*dt)`, never a constant (a fixed 0.1
  moves faster at 240 FPS than 30).

## Boat chase-cam (Last River)

See the reference for the full pattern: follow behind+above the hull, **look-ahead** along
`AssemblyLinearVelocity`, **collision-aware** (raycast from boat to desired cam pos, pull in on hit),
smoothed, **speed-based FOV**, and a decaying-trauma **shake** applied after the aim. Fire `addShake()` on
impacts/rapids.

## Mobile

A Scriptable camera turns off default touch controls — provide your own via `UserInputService` (touch
`Delta`) + `ContextActionService:BindAction(..., createTouchButton=true)` for on-screen buttons. Respect
GUI insets. For default-camera games, set `Player.DevTouchCameraMovementMode`.

## Shake & effects

No built-in shake: multiply the final CFrame by a decaying `CFrame.Angles(...)*CFrame.new(...)` (quadratic
trauma feels best), applied **after** the follow calc so it doesn't feed smoothing. `Humanoid.CameraOffset`
for default-camera bob. FOV punch = add to `FieldOfView`, lerp back (stay 1–120).

## Clean up
On leaving the boat: `UnbindFromRenderStep(name)` + `CameraType = Enum.CameraType.Custom`.
