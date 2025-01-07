import ctypes
import winreg
import os

SPI_SETDESKWALLPAPER = 20
SPIF_SENDCHANGE = 0x02

# Funzione per aggiornare lo sfondo modificando il registro
def change_wallpaper_via_registry(image_path):
    # Verifica che il file esista
    if not os.path.isfile(image_path):
        print("Il file specificato non esiste.")
        return

    try:
        # Aggiorna il registro di Windows
        reg_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Control Panel\Desktop",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(reg_key, "Wallpaper", 0, winreg.REG_SZ, image_path)
        winreg.CloseKey(reg_key)
        print("Registro aggiornato con il nuovo wallpaper.")
    except Exception as e:
        print(f"Errore durante l'aggiornamento del registro: {e}")
        return

    # Notifica il sistema per applicare i cambiamenti
    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, None, SPIF_SENDCHANGE
    )
    if result:
        print("Notifica inviata con successo. Lo sfondo dovrebbe essere aggiornato.")
    else:
        print("Errore durante l'invio della notifica al sistema.")

# Esempio di utilizzo
folder_path = r"C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\blu-haired\blueee_0001.png"
change_wallpaper_via_registry(folder_path)   
