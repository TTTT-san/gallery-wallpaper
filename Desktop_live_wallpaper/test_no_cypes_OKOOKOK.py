import os
import win32gui
import win32con
import time

class CambiaWallpaper:
    def __init__(self):
        pass

    def change_wallpaper_win32(self, image_path):
        """Metodo veloce usando WIN32 API diretta"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File non trovato: {image_path}")

        # Imposta direttamente usando Win32
        win32gui.SystemParametersInfo(
            win32con.SPI_SETDESKWALLPAPER, 
            image_path, 
            win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
        )
        return True

def main():
    try:
        changer = CambiaWallpaper()
        image_path = r"C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\blu-haired\blueee_0001.png"

        # Timestamp di inizio
        start_time = time.time()
        print(f"Inizio: {time.ctime(start_time)}")

        success = changer.change_wallpaper_win32(image_path)
        
        if success:
            # Timestamp di fine
            end_time = time.time()
            print(f"Fine: {time.ctime(end_time)}")
            
            # Calcola la differenza
            duration = end_time - start_time
            print(f"Tempo impiegato: {duration:.4f} secondi")
            print("Wallpaper cambiato istantaneamente!")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    main()
