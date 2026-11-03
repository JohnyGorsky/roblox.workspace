# studio-save.ps1 -- press Ctrl+S in Roblox Studio for an owner who is away from the PC.
#
# Owner, 2026-11-02 ("Can you save place?" / "I am not at pc" / "Add it"): allowed by ONE exact rule in
# .claude/settings.local.json. It brings the Studio window to the front and presses Ctrl+S -- ONLY if Studio is
# verifiably the foreground window afterwards; otherwise it sends nothing and exits 2. Save = a new version in the
# place's history; it never publishes the live game.
#
# Usage (exactly this, so the allow rule matches):
#   powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:/Dati/Work/roblox.workspace/tools/studio-save.ps1
Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;
public static class W {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int cmd);
  [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern void keybd_event(byte vk, byte scan, uint flags, UIntPtr extra);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
}
"@
$p = Get-Process RobloxStudioBeta -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
if (-not $p) { "NO STUDIO WINDOW"; exit 1 }
$h = $p.MainWindowHandle
if ([W]::IsIconic($h)) { [W]::ShowWindow($h, 9) | Out-Null }   # restore if minimised
# An ALT tap lets a background process take the foreground (Windows' foreground lock).
[W]::keybd_event(0x12, 0, 0, [UIntPtr]::Zero); [W]::keybd_event(0x12, 0, 2, [UIntPtr]::Zero)
[W]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 600
$fg = [W]::GetForegroundWindow()
$sb = New-Object System.Text.StringBuilder 512
[W]::GetWindowText($fg, $sb, 512) | Out-Null
if ($fg -ne $h) { "NOT SENT: foreground is '" + $sb.ToString() + "', not Studio"; exit 2 }
# Ctrl+S
[W]::keybd_event(0x11, 0, 0, [UIntPtr]::Zero)
[W]::keybd_event(0x53, 0, 0, [UIntPtr]::Zero)
Start-Sleep -Milliseconds 80
[W]::keybd_event(0x53, 0, 2, [UIntPtr]::Zero)
[W]::keybd_event(0x11, 0, 2, [UIntPtr]::Zero)
Start-Sleep -Milliseconds 1500
$fg2 = [W]::GetForegroundWindow()
$sb2 = New-Object System.Text.StringBuilder 512
[W]::GetWindowText($fg2, $sb2, 512) | Out-Null
"SENT Ctrl+S to Studio. Foreground now: '" + $sb2.ToString() + "'"
