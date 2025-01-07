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

def cambia_wallpapers_in_cartella(cartella):
    # Ottieni tutti i file nella cartella
    files = [f for f in os.listdir(cartella) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    
    if not files:
        print("Nessun file immagine trovato nella cartella.")
        return

    try:
        changer = CambiaWallpaper()

      

        # Cambia wallpaper per ogni file, saltando ogni 20esimo
        for idx, file in enumerate(files):
            if idx % 20 == 0:  # Skip ogni 20esimo
                start_time = time.time()
                image_path = os.path.join(cartella, file)
                changer.change_wallpaper_win32(image_path)
                # Timestamp di fine
                end_time = time.time()
                print(f"Cambiando wallpaper con il file {file}...")
                print(f"Inizio: {time.ctime(start_time)}")
                print(f"Fine: {time.ctime(end_time)}")
                    
                # Calcola la differenza
                duration = end_time - start_time
                print(f"Tempo impiegato: {duration:.4f} secondi")

    except Exception as e:
        print(f"Errore: {e}")

def main():
    cartella = r"C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\blu-haired"  # Sostituisci con il percorso della tua cartella
    cambia_wallpapers_in_cartella(cartella)

if __name__ == "__main__":
    main()
