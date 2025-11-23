import winreg

def set_reg_dword(root, path, name, value):
    try:
        key = winreg.CreateKeyEx(root, path, 0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
        winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
        winreg.CloseKey(key)
        print(f"Успешно установлено: {name} = {value} в {path}")
    except PermissionError:
        print("Ошибка: недостаточно прав. Запустите скрипт от имени администратора.")
    except Exception as e:
        print(f"Ошибка при установке {name}: {e}")

def main():
    base_path = r"SOFTWAREPoliciesMicrosoftWindows Defender"
    rtp_path = base_path + r"Real-Time Protection"
    value = 1

    # Создаем параметр DisableAntiSpyware в base_path
    set_reg_dword(winreg.HKEY_LOCAL_MACHINE, base_path, "DisableAntiSpyware", value)

    # Создаем параметры в подветке Real-Time Protection
    params = [
        "DisableBehaviourMonitoring",
        "DisableOnAccessProtection",
        "DisableScanOnRealTimeEnable",
        "DisableIOAVPProtection"
    ]
    for param in params:
        set_reg_dword(winreg.HKEY_LOCAL_MACHINE, rtp_path, param, value)

if __name__ == "__main__":
    main()
