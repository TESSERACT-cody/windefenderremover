import winreg

def create_registry_key_and_values():
    path = r"SOFTWAREPoliciesMicrosoftWindows DefenderReal-Time Protection"
    dword_values = [
        "DisableBehaviourMonitoring",
        "DisableOnAccessProtection",
        "DisableScanOnRealTimeEnable",
        "DisableIOAVPProtection"
    ]

    try:
        # Создаем ключ и все необходимые разделы, если их нет
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path)
        
        # Устанавливаем параметры DWORD со значением 1
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
