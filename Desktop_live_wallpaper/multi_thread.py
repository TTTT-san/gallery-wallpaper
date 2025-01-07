import os
import ctypes
import time
from multiprocessing import Process, Value, Lock

SPI_SETDESKWALLPAPER = 20

def set_wallpaper(image_path):
    """Cambia il background di Windows."""
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

def process_skip(images, index, lock, delay=10, skip=2):
    """Processo separato che cambia lo sfondo con uno skip di 2."""
    while True:
        with lock:
            current_index = index.value
            index.value += skip
            if index.value >= len(images):
                index.value = index.value % len(images)
            image_path = images[current_index]
        
        print(f"[Processo separato] Cambia sfondo: {image_path}")
        set_wallpaper(image_path)

if __name__ == "__main__":
    # Cartella contenente i frame
    image_folder = r"C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\blu-haired"
    skip_main = 5  # Skip fisso per il main loop
    delay_main = 5  # Ritardo nel main loop
    delay_process = 10  # Ritardo nel processo separato

    # Ottieni tutti i file immagine
    images = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))])

    if not images:
        print("Nessuna immagine trovata nella cartella frames.")
        exit(1)

    # Sincronizzazione e contatore
    lock = Lock()
    index = Value('i', 0)  # Contatore condiviso

    # Avvia processo separato
    process = Process(target=process_skip, args=(images, index, lock, delay_process))
    process.start()

    try:
        while True:
            # Main loop cambia sfondo con skip fisso
            with lock:
                current_index = index.value
                index.value += skip_main
                if index.value >= len(images):
                    index.value = index.value % len(images)
                image_path = images[current_index]
            
            print(f"[Main loop] Cambia sfondo: {image_path}")
            set_wallpaper(image_path)
    except KeyboardInterrupt:
        print("Terminazione richiesta dall'utente.")
        process.terminate()
        process.join()
