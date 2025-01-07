import os
import ctypes
import time
from multiprocessing import Lock

SPI_SETDESKWALLPAPER = 20

# Percorso del file di stato nella stessa cartella di main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "state.txt")

def set_wallpaper(image_path):
    """Cambia il background di Windows."""
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

def initialize_state_file():
    """Crea il file di stato se non esiste."""
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, "w") as f:
            f.write("0")  # Imposta l'indice iniziale a 0

def update_state_file(index):
    """Aggiorna il file di stato con l'indice attuale."""
    with open(STATE_FILE, "w") as f:
        f.write(str(index))

def load_state_file():
    """Carica l'indice dal file di stato."""
    with open(STATE_FILE, "r") as f:
        return int(f.read().strip())

if __name__ == "__main__":
    # Cartella contenente i frame
    image_folder = r"C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\blu-haired"
    skip_main = 5  # Skip fisso per il main loop
    delay_main = 5  # Ritardo nel main loop

    # Ottieni tutti i file immagine
    images = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))])

    if not images:
        print("Nessuna immagine trovata nella cartella frames.")
        exit(1)

    # Inizializza il file di stato
    initialize_state_file()

    # Sincronizzazione e contatore
    lock = Lock()
    index = load_state_file()

    try:
        while True:
            with lock:
                image_path = images[index]
                print(f"[Main loop] Cambia sfondo: {image_path}")
                set_wallpaper(image_path)

                # Aggiorna l'indice
                index += skip_main
                if index >= len(images):
                    index = index % len(images)

                # Scrivi il nuovo stato nel file
                update_state_file(index)

            #time.sleep(delay_main)
    except KeyboardInterrupt:
        print("Terminazione richiesta dall'utente.")
