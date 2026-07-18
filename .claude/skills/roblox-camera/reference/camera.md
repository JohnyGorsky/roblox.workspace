# Roblox camera — reference

Sourced from official Creator Docs, current 2026-07. Not-verbatim items flagged **[unverified]**.
**Camera is per-client — all camera code runs in a LocalScript.**

## Camera object

`workspace.CurrentCamera`. Props: `CFrame` (drive this), `Focus` (CFrame — **update every frame**;
higher detail renders near it), `CameraType` (`Enum.CameraType`: `Custom`(5, default follow/zoom) /
`Scriptable`(6, you drive) / Fixed/Attach/Watch/Track/Follow/Orbital), `CameraSubject` (what default cam
follows), `FieldOfView` (1–120, default 70), `FieldOfViewMode`, `ViewportSize`. Methods:
`ScreenPointToRay`/`ViewportPointToRay` (inset vs no-inset), `WorldToScreenPoint`/`WorldToViewportPoint`,
`GetRenderCFrame()` (true rendered pose — use for VR/interp), `GetPartsObscuringTarget`, `ZoomToExtents`.

## Taking control (Scriptable)

```lua
camera.CameraType = Enum.CameraType.Scriptable  -- default scripts stop moving it
RunService:BindToRenderStep("Cam", Enum.RenderPriority.Camera.Value, updateFn) -- drive CFrame each frame
-- return control: UnbindFromRenderStep("Cam"); camera.CameraType = Enum.CameraType.Custom
```
`Enum.RenderPriority`: First(0) < Input(100) < **Camera(200)** < Character(300) < Last(2000). Use
`BindToRenderStep` at Camera priority (not Heartbeat, or the camera lags a frame). `PreRender` is the
modern `RenderStepped`.

## Boat chase-cam pattern (verified building blocks)

```lua
-- LocalScript. `boat` = the hull PrimaryPart. Frame-rate-independent smoothing via 1-exp(-k*dt).
local currentPos, shakeTrauma = camera.CFrame.Position, 0
local function update(dt)
    if not boat or not boat.Parent then return end
    local pos, vel = boat.Position, boat.AssemblyLinearVelocity
    local flat = Vector3.new(vel.X,0,vel.Z)
    local ahead = flat.Magnitude>1 and flat.Unit or boat.CFrame.LookVector
    local target = pos + ahead*8                                   -- look-ahead
    local desired = pos - boat.CFrame.LookVector*24 + Vector3.new(0,9,0)  -- behind+above
    local rp = RaycastParams.new(); rp.FilterType=Enum.RaycastFilterType.Exclude
    rp.FilterDescendantsInstances = {boat.Parent, player.Character}
    local hit = workspace:Raycast(pos, desired-pos, rp)            -- collision-aware
    if hit then desired = hit.Position + (pos-desired).Unit*1.5 end
    currentPos = currentPos:Lerp(desired, 1-math.exp(-6*dt))
    local cf = CFrame.lookAt(currentPos, target)
    if shakeTrauma>0 then                                          -- shake AFTER aim
        local s=shakeTrauma^2; local a=math.rad(6)*s
        cf = cf * CFrame.Angles((math.random()*2-1)*a,(math.random()*2-1)*a,(math.random()*2-1)*a)
        shakeTrauma = math.max(0, shakeTrauma - dt*1.5)
    end
    camera.CFrame, camera.Focus = cf, CFrame.new(target)
    camera.FieldOfView = 70 + math.clamp(flat.Magnitude/8,0,15)    -- speed FOV
end
camera.CameraType = Enum.CameraType.Scriptable
RunService:BindToRenderStep("BoatCam", Enum.RenderPriority.Camera.Value, update)
```

## Default cam & mobile

Default behavior = PlayerModule/CameraModule (follows `Humanoid` via `CameraSubject` + `Humanoid.CameraOffset`).
Tune via `StarterPlayer`/`Player`: `CameraMode` (`Classic`/`LockFirstPerson`), `CameraMinZoomDistance`/
`CameraMaxZoomDistance` (equal = locked zoom), `DevCameraOcclusionMode` (`Zoom`/`Invisicam`),
`DevTouchCameraMovementMode` (`UserChoice`/`Classic`/`Follow`/`Orbital`).
**Mobile:** a Scriptable camera disables default touch controls → add your own via `UserInputService`
(`TouchEnabled`, `TouchMoved`, InputObject `Delta`) and `ContextActionService:BindAction(..., createTouchButton=true)`
for on-screen buttons (recenter/boost). Respect GUI insets (`ViewportPointToRay` vs `ScreenPointToRay`).

## Shake / effects

No built-in shake — compose a decaying random offset CFrame onto the final CFrame (above), or
`Humanoid.CameraOffset` (Vector3) for default-camera bob/shake. FOV punch: add to `FieldOfView`, lerp back
(keep 1–120). Occlusion: `DevCameraOcclusionMode.Zoom`/`Invisicam`, or DIY via `workspace:Raycast`/
`GetPartsObscuringTarget`.

## Gotchas
Client-only; set `Scriptable` before driving CFrame; update at RenderPriority.Camera; **frame-rate-
independent smoothing** (`1-math.exp(-k*dt)`, not a constant alpha); update `Focus` each frame; clean up
(`UnbindFromRenderStep` + `CameraType=Custom`) on dismount; FOV 1–120.

## Sources
classes/{Camera,RunService,Player,StarterPlayer,Humanoid,ContextActionService,UserInputService},
enums/{CameraType,RenderPriority,CameraMode,DevCameraOcclusionMode,DevTouchCameraMovementMode},
workspace/camera, tutorials/.../controlling-the-users-camera.
