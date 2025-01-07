

# Percorso della cartella contenente i frame
FRAME_FOLDER = r"C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\blu-haired"
import ctypes
import time
import os
import subprocess
# Funzione per cambiare lo sfondo e calcolare il tempo
def change_wallpaper(image_path):
    start_time = time.time()  # Tempo prima del cambio
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)  # Cambia lo sfondo
    subprocess.run(['RUNDLL32.EXE', 'user32.dll,UpdatePerUserSystemParameters', '1', 'True'])
    
    end_time = time.time()  # Tempo dopo il cambio
    
    # Calcola la differenza di tempo
    time_difference = end_time - start_time
    
    # Stampa il timestamp e la differenza di tempo
    print(f"Wallpaper changed at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"Time taken to change: {time_difference:.5f} seconds")
    
    return time_difference

# Funzione per cambiare tutti i wallpaper in una cartella
def update_wallpapers_from_folder(folder_path):
    if not os.path.exists(folder_path):
        print("La cartella non esiste.")
        return
    
    # Ottieni i percorsi di tutte le immagini nella cartella
    images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    # Cambia lo sfondo per ogni immagine
    for image in images[:50]:
        change_wallpaper(image)
        time.sleep(1/60)  # Tempo tra i cambi di sfondo, puoi regolarlo

# Esempio di utilizzo
folder =FRAME_FOLDER # Sostituisci con il percorso della tua cartella
update_wallpapers_from_folder(folder)
