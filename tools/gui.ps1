# Drive ONLY the game window of a process: click / key / shot. Never captures the full desktop.
# usage: powershell -File gui.ps1 -ProcId 1234 -Action click -Arg "875,600"   (coords relative to the window's top-left)
#        powershell -File gui.ps1 -ProcId 1234 -Action key -Arg "o"           (SendKeys syntax)
#        powershell -File gui.ps1 -ProcId 1234 -Action shot -Arg "C:\path\out.png"
param([int]$ProcId, [string]$Action, [string]$Arg)
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class GuiWin {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint dx, uint dy, uint d, UIntPtr e);
}
"@
$p = Get-Process -Id $ProcId -ErrorAction Stop
$h = $p.MainWindowHandle
if ($h -eq [IntPtr]::Zero) { Write-Output "NO_WINDOW"; exit 2 }
[GuiWin]::ShowWindow($h, 9) | Out-Null
[GuiWin]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 400
$r = New-Object GuiWin+RECT
[GuiWin]::GetWindowRect($h, [ref]$r) | Out-Null
if ($Action -eq "click") {
  # pre-move a few pixels (so the game sees a mouse-move over the widget), then press and hold long enough to span several frames
  $xy = $Arg.Split(",")
  $cx = $r.L + [int]$xy[0]; $cy = $r.T + [int]$xy[1]
  [GuiWin]::SetCursorPos($cx - 6, $cy - 3) | Out-Null
  Start-Sleep -Milliseconds 200
  [GuiWin]::SetCursorPos($cx, $cy) | Out-Null
  Start-Sleep -Milliseconds 350
  [GuiWin]::mouse_event(2, 0, 0, 0, [UIntPtr]::Zero)
  Start-Sleep -Milliseconds 220
  [GuiWin]::mouse_event(4, 0, 0, 0, [UIntPtr]::Zero)
  Write-Output "CLICK $Arg"
} elseif ($Action -eq "scroll") {
  # Arg "x,y,delta": mouse wheel at (x,y) relative to the window; delta in wheel units (120 per notch, positive = up)
  $a3 = $Arg.Split(",")
  [GuiWin]::SetCursorPos($r.L + [int]$a3[0], $r.T + [int]$a3[1]) | Out-Null
  Start-Sleep -Milliseconds 200
  $d = [BitConverter]::ToUInt32([BitConverter]::GetBytes([int]$a3[2]), 0)
  [GuiWin]::mouse_event(0x0800, 0, 0, $d, [UIntPtr]::Zero)
  Write-Output "SCROLL $Arg"
} elseif ($Action -eq "key") {
  [System.Windows.Forms.SendKeys]::SendWait($Arg)
  Write-Output "KEY $Arg"
} elseif ($Action -eq "shot") {
  Start-Sleep -Milliseconds 400
  $w = $r.R - $r.L
  $hh = $r.B - $r.T
  $bmp = New-Object System.Drawing.Bitmap $w, $hh
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($r.L, $r.T, 0, 0, $bmp.Size)
  $bmp.Save($Arg, [System.Drawing.Imaging.ImageFormat]::Png)
  Write-Output ("SHOT {0}x{1} {2}" -f $w, $hh, $Arg)
}
