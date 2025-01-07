import os
import ctypes
import time

SPI_SETDESKWALLPAPER = 20

# Percorso del file di stato nella stessa cartella di process.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "state.txt")

def set_wallpaper(image_path):
    """Cambia il background di Windows."""
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

def load_state_file():
    """Carica l'indice dal file di stato. Ritorna 0 se il file è vuoto o non valido."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            content = f.read().strip()
            if content.isdigit():  # Controlla che il contenuto sia un numero valido
                return int(content)
    return 0  # Valore predefinito se il file è vuoto o non esiste
 # Valore predefinito se il file è vuoto o non esiste


def process_skip(images, skip=20, delay=10):
    """Processo separato che si sincronizza con il main."""
    while True:
        # Carica l'indice dal file di stato
        index = load_state_file()
        if index == 0:
            print("[Processo] Attesa che il main sia avviato...")
            time.sleep(1)
            continue
        if index is None:
            print("[Processo] Attesa che il main sia avviato...")
            time.sleep(1)
            continue

        # Calcola il prossimo indice
        index += skip
        if index >= len(images):
            index = index % len(images)

        # Cambia sfondo
        image_path = images[index]
        print(f"[Processo separato] Cambia sfondo: {image_path}")
        set_wallpaper(image_path)

#        time.sleep(delay)

if __name__ == "__main__":
    # Cartella contenente i frame
    image_folder = r"C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\blu-haired"
    skip_process = 2  # Skip per il processo secondario
    delay_process = 10  # Ritardo nel processo secondario

    # Ottieni tutti i file immagine
    images = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))])

    if not images:
        print("Nessuna immagine trovata nella cartella frames.")
        exit(1)

    # Avvia il processo
    process_skip(images, skip_process, delay_process)
