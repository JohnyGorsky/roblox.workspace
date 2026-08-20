# FINDING 0001: Camera release after screen_capture used the wrong CameraType

**Project:** `roblox.workspace`
**Status:** fixed (2026-08-20) — Fixed in the same pass it was found: skill and memory corrected to Enum.CameraType.Fixed, and both tide places verified reading Fixed.
**Severity:** med
**Created:** 2026-08-20 08:55:42

**Symptom:** screen_capture with a camera position leaves workspace.CurrentCamera.CameraType = Scriptable, which locks the Edit viewport. Job 007 restored it with Enum.CameraType.Custom - the runtime default - and the write reported success (Fixed -> Custom), but the value did not hold: when the user tried to navigate, the camera was Scriptable again and the viewport was locked. The correct Edit-mode value is Fixed, which is what an untouched place reports - the lobby place, never captured in, read Fixed throughout and was the available control sample. Fixed. Both the memory note and the roblox-studio skill said Custom and now say Fixed, with the added rule to read CameraType back in a SEPARATE call because a successful write is not proof it held. Broader lesson, same as workspace finding on Studio UI: verify against an untouched reference rather than trusting a write.
**Where:** _TODO: file / system_
**Repro / notes:** _TODO_
**Fix idea:** _TODO_
