import win32api
import win32gui
import win32con
import os
from pathlib import Path
import time

# Percorso della cartella contenente i frame
FRAME_FOLDER = r"C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\blu-haired"


# Funzione per cambiare lo sfondo usando PyWin32
def set_wallpaper(image_path):
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, 
                                "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "Wallpaper", 0, win32con.REG_SZ, image_path)
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, image_path, 1 + 2)

# Ottieni i file della cartella
def get_frames(folder_path):
    return sorted(Path(folder_path).glob("*.jpg")) + sorted(Path(folder_path).glob("*.png"))

# Funzione principale per animare gli sfondi con FPS
def animate_wallpaper(folder_path, fps=30):
    frames = get_frames(folder_path)
    if not frames:
        raise ValueError("La cartella non contiene immagini valide (.jpg, .png).")

    frame_duration = 1 / fps  # Durata di ogni frame in secondi

    while True:
        for frame in frames:
            start_time = time.time()
            set_wallpaper(str(frame))
            elapsed = time.time() - start_time
            time.sleep(max(0, frame_duration - elapsed))

# Testa il programma
if __name__ == "__main__":
    try:
        animate_wallpaper(FRAME_FOLDER, fps=60)
    except Exception as e:
        print(f"Errore: {e}")
