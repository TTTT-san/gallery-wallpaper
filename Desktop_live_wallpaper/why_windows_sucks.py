import ctypes
import os
import time

# Costanti per SystemParametersInfoW
SPI_SETDESKWALLPAPER = 20
SPIF_SENDWININICHANGE = 0x02
SPIF_UPDATEINIFILE = 0x01

# Funzione per cambiare lo sfondo
def change_wallpaper(image_path):
    if not os.path.exists(image_path):
        print(f"Errore: il file {image_path} non esiste.")
        return

    # Converte il percorso dell'immagine in una stringa Unicode
    image_path = image_path.replace("\\", "/")  # Normalizza i separatori dei percorsi
    image_path = ctypes.create_unicode_buffer(image_path)

    # Chiamata alla funzione SystemParametersInfoW per cambiare lo sfondo
    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, image_path, SPIF_SENDWININICHANGE | SPIF_UPDATEINIFILE
    )

    if result == 0:
        print(f"Errore nell'impostare lo sfondo. Codice errore: {ctypes.GetLastError()}")
    else:
        print(f"Wallpaper cambiato con successo in: {image_path.value}")

# Funzione principale per iterare sui frame
def cycle_wallpapers(folder_path):
    # Lista di file immagine nella cartella
    frames = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

    last_timestamp = time.time()  # Timestamp iniziale

    # Ciclo per cambiare lo sfondo per ogni immagine nella cartella
    for frame in frames:
        current_timestamp = time.time()  # Ottieni il timestamp attuale

        # Cambia lo sfondo
        change_wallpaper(frame)

        elapsed_time = current_timestamp - last_timestamp  # Calcola la differenza di tempo

        # Mostra il timestamp e la differenza di tempo
        print(f"\n[INFO] Cambiato wallpaper: {frame}")
        print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_timestamp))}")
        print(f"Differenza di tempo dall'ultimo cambiamento: {elapsed_time:.2f} secondi")

        # Aggiorna l'ultimo timestamp
        last_timestamp = current_timestamp


# Input del percorso della cartella contenente le immagini
folder_path = r"C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\blu-haired"

# Esegui la funzione di ciclo
cycle_wallpapers(folder_path)
