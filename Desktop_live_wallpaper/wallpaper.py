import random
import os
import ctypes
import time
import winreg as reg

def set_wallpaper(image_path):
    """
    Imposta lo sfondo del desktop con l'immagine specificata.
    """
    registry_key = r"Control Panel\Desktop"
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, registry_key, 0, reg.KEY_SET_VALUE) as key:
            reg.SetValueEx(key, "Wallpaper", 0, reg.REG_SZ, image_path)
            reg.SetValueEx(key, "WallpaperStyle", 0, reg.REG_SZ, "2")  # "2" per adattato
            reg.SetValueEx(key, "TileWallpaper", 0, reg.REG_SZ, "0")  # "0" per disattivare il tiling
        
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        print(f"Sfondo impostato: {image_path}")
    except Exception as e:
        print(f"Errore nell'impostare lo sfondo: {e}")

        
def random_biased(skip_range):
    x = skip_range[0]
    y = skip_range[1]
    # Controllo che x sia inferiore a y
    if x > y:
        x, y = y, x

    # Scegliere se generare un numero vicino a x o vicino a y (70% per x)
    if random.random() < 0.9:
        # Genera un numero più vicino a x
        return random.randint(x, (x + y) // 2)
    else:
        # Genera un numero più vicino a y
        return random.randint((x + y) // 2, y)


def change_wallpaper_in_loop(folder_path, skip_range=[5, 10], change_delay=0.1, boost_value=10, boost_chance=0.2):
    """
    Cambia lo sfondo con uno skip casuale (tra x e y) che occasionalmente
    viene sostituito da un boost di valore fisso.
    
    - `skip_range`: Intervallo di skip normale (x, y).
    - `boost_value`: Valore fisso per il boost.
    - `boost_chance`: Probabilità (tra 0 e 1) che venga attivato il boost.
    """
    image_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif'))])

    if not image_files:
        print("Nessuna immagine trovata nella cartella.")
        return

    index = 0
    num_images = len(image_files)
    skip = 0  # Skip iniziale
    x, y = skip_range

    boost = False  # Flag per gestire il boost
    while True:
        
        # Determina se applicare il boost o usare lo skip normale
        if random.random() < boost_chance:
            skip = boost_value + skip  # Applica il boost
            boost = True
        else:
            if boost:
                skip = 5  # Ripristina lo skip normale dopo il boost
                boost = False
            else: 
                skip = random.randint(x, y)  # Usa uno skip casuale tra x e y

        print(f"Skip: {skip}")
        # Cambia lo sfondo
        image_path = os.path.join(folder_path, image_files[index])
        set_wallpaper(image_path)
        time.sleep(change_delay)  # Ritardo per garantire fluidità

        # Aggiorna l'indice dell'immagine
        index = (index + skip) % num_images
def change_wallpaper_in_loop_bad(folder_path, skip_range=[5, 10], change_delay=0.1):
    """
    Cambia lo sfondo seguendo un ciclo con incremento/decremento graduale dello skip:
    1. Incrementa skip fino a mid.
    2. Incrementa skip fino a y.
    3. Decrementa skip fino a mid.
    4. Decrementa skip fino a x.
    Lo skip è costante in ogni fase.
    """
    image_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif'))])

    if not image_files:
        print("Nessuna immagine trovata nella cartella.")
        return

    index = 0
    num_images = len(image_files)
    
    # Estrai i valori da skip_range
    x, y = skip_range
    mid = (x + y) // 2  # Calcola il valore medio tra x e y
    skip = x  # Imposta lo skip iniziale uguale a x
    
    # Fasi: Incremento fino a mid, incremento fino a y, decremento fino a mid, decremento fino a x
    phase = 0  # Contatore delle fasi
    
    print("Cambio sfondo in loop...")
    print(f"- Skip: {skip}")
    print(f"- Fase: {phase}")
    print(f"- Mid: {mid}")
    print(f"- X: {x}")
    print(f"- Y: {y}")

    while True:
        # Cambia lo sfondo
        image_path = os.path.join(folder_path, image_files[index])
        set_wallpaper(image_path)
        time.sleep(change_delay)  # Ritardo per garantire fluidità

        # Aggiorna l'indice dell'immagine
        index = (index + skip) % num_images
        print("skip:", skip)
        # Cambia fase e logica di incremento/decremento dello skip
        if phase == 0:  # Da X a mid (incremento)
            skip += 1
            if skip >= mid:  # Raggiunge mid, cambia fase
                phase += 1
        elif phase == 1:  # Da mid a Y (incremento)
            skip += 1
            if skip >= y:  # Raggiunge y, cambia fase
                phase += 1
        elif phase == 2:  # Da Y a mid (decremento)
            skip -= 1
            if skip <= mid:  # Raggiunge mid, cambia fase
                phase += 1
        elif phase == 3:  # Da mid a X (decremento)
            skip -= 1
            if skip <= x:  # Raggiunge x, riparti da X
                phase = 0  # Riparti da X
                skip = x  # Imposta skip a X

def change_wallpaper_in_loop_bad(folder_path, skip_range=[2, 5], change_delay=0.1):
    """Cambia lo sfondo con un comportamento a onda fluido."""
    image_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif'))])

    if not image_files:
        print("Nessuna immagine trovata nella cartella.")
        return

    index = 0
    num_images = len(image_files)
    skip = skip_range[0]
    incrementing = True  # Direzione iniziale


    while True:
        print(f"Skip: {skip}")
        if incrementing:
            skip += 1
            if skip >= skip_range[1]:  # Raggiunge il massimo
                incrementing = False
        else:
            skip -= 1
            if skip <= skip_range[0]:  # Raggiunge il minimo
                incrementing = True

        image_path = os.path.join(folder_path, image_files[index])
        set_wallpaper(image_path)
        time.sleep(change_delay)
        index = (index + skip) % num_images

def change_wallpaper_in_loop2(folder_path, skip_range=[5, 10], change_delay=0.8):
    """Cambia lo sfondo in un loop, riducendo gradualmente lo skip se supera la metà del range."""
    # Ottieni tutte le immagini nella cartella, in ordine alfabetico
    image_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif'))])

    if not image_files:
        print("Nessuna immagine trovata nella cartella.")
        return

    index = 0
    num_images = len(image_files)
    skip = random_biased(skip_range)  # Primo skip casuale
    decrementing = False  # Flag per gestire la diminuzione dello skip

    while True:
        # Riduci lo skip se è in modalità decremento
        # Controlla se lo skip supera la metà del range
        if skip >= (skip_range[0] + skip_range[1]) // 2:
            decrementing = True  # Avvia la modalità decremento
            print("Inizio decremento skip...")
        else :
            skip = random_biased(skip_range)  # Genera un nuovo skip

        if decrementing:
            skip  = skip // 2
            print(f"- Skip decremento: {skip}")
            if skip <= skip_range[0]:  # Quando si raggiunge l'estremità inferiore
                decrementing = False  # Fine della modalità decremento    

        print(f"Skip: {skip}")
        # Assicurati che lo skip sia sempre minore del numero di immagini
        if skip >= num_images:
            skip = num_images - 1

        image_path = os.path.join(folder_path, image_files[index])
        set_wallpaper(image_path)

        # Aggiungi un ritardo per evitare sovraccarico
        time.sleep(change_delay)

        index = (index + skip) % num_images  # Aggiorna l'indice

# Esegui il cambio dello sfondo in loop con skip
folder_path = r"C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\blu-haired"  # Sostituire con il percorso della cartella
change_wallpaper_in_loop(folder_path, skip_range=[5,20], change_delay=0.1)  # Cambia sfondo saltando 5-10 immagini ogni volta
