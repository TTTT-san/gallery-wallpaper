import os
from PIL import Image

resolutions = {
    "SD": (640, 480),
    "HD": (1280, 720),
    "FHD": (1920, 1080),
    "2K": (2560, 1440),
    "4K": (3840, 2160),
    "8K": (7680, 4320)
}

def resize_image(image, target_width, target_height):
    """
    Ridimensiona un'immagine mantenendo il rapporto di aspetto e ritagliandola per adattarla alla dimensione target.

    Args:
    - image (PIL.Image): Oggetto PIL Image da ridimensionare.
    - target_width (int): Larghezza desiderata.
    - target_height (int): Altezza desiderata.

    Returns:
    - PIL.Image: Immagine ridimensionata.
    """
    width, height = image.size
    aspect_ratio = width / height

    # Calcola le dimensioni ridimensionate mantenendo il rapporto di aspetto
    if aspect_ratio > 1:
        new_width = target_width
        new_height = round(new_width / aspect_ratio)
    else:
        new_height = target_height
        new_width = round(new_height * aspect_ratio)

    # Ridimensiona l'immagine mantenendo il rapporto di aspetto
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    # Ritaglia l'immagine per adattarla alla dimensione target
    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    right = (new_width + target_width) / 2
    bottom = (new_height + target_height) / 2
    cropped_image = resized_image.crop((left, top, right, bottom))

    return cropped_image


def read_and_resize_images(input_folder, target_width=1920, target_height=1080):
    """
    Legge tutte le immagini nella cartella specificata, ridimensionandole mantenendo un rapporto di aspetto di 16:9 (1920x1080).
    Restituisce una lista di immagini ridimensionate.

    Args:
    - input_folder (str): Cartella contenente le immagini da leggere e ridimensionare.
    - target_width (int): Larghezza desiderata per il ridimensionamento.
    - target_height (int): Altezza desiderata per il ridimensionamento.

    Returns:
    - list: Lista di oggetti PIL Image delle immagini ridimensionate.
    """
    images = []

    print("Leggendo e ridimensionando le immagini...")
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff')):
            file_path = os.path.join(input_folder, file_name)
            print(f"Processing: {file_name}")
            with Image.open(file_path) as img:
                # Converti l'immagine in modalità "RGB" se necessario
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                # Ridimensiona l'immagine mantenendo il rapporto di aspetto e facendo uno zoom
                resized_img = resize_image(img, target_width, target_height)
                images.append(resized_img)
                #print(f"{resized_img} size: {resized_img.size}")

    print("Elaborazione completata per tutte le immagini.")
    return images


def save_animation(images, output_folder, output_filename, duration):
    """
    Salva una GIF animata utilizzando le immagini fornite nella cartella di output specificata.
    
    Args:
    - images (list): Lista di oggetti PIL Image rappresentanti i frame dell'animazione.
    - output_folder (str): Cartella di output dove salvare la GIF.
    - output_filename (str): Nome del file GIF di output.
    - duration (int): Durata di ogni frame dell'animazione in millisecondi.
    """
    try:
        # Crea la cartella di output se non esiste
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Cartella di output '{output_folder}' creata.")
        
        # Crea il percorso completo del file di output
        output_file = os.path.join(output_folder, output_filename)
        
        print(f"Salvataggio della GIF: {output_file}...")
        
        # Controlla che tutte le immagini siano oggetti PIL.Image
        for img in images:
            if not isinstance(img, Image.Image):
                raise ValueError("Tutti gli elementi in 'images' devono essere oggetti PIL.Image.")
        
        # Salva la GIF con loop infinito
        images[0].save(output_file, save_all=True, append_images=images[1:], duration=duration, loop=0)
        
        print(f"GIF salvata come {output_file}")
    
    except FileNotFoundError:
        print(f"Impossibile creare la cartella di output '{output_folder}'.")
    except ValueError as ve:
        print(f"Errore di tipo: {ve}")
    except Exception as e:
        print(f"Si è verificato un errore durante il salvataggio della GIF: {e}")


def make_unique_filename(output_folder, output_filename):
    """
    Se il file esiste già nella cartella di output, aggiunge un numero incrementale al nome del file fino a ottenere un nome univoco.
    Restituisce il nome completo del file univoco.
    """
    base_name, ext = os.path.splitext(output_filename)
    counter = 1
    while os.path.exists(os.path.join(output_folder, output_filename)):
        output_filename = f"{base_name}_{counter}{ext}"
        counter += 1
    return output_filename


def create_webp_animation(input_folder, output_folder, output_filename, resolution="FHD", duration=500):
    """
    Legge le immagini dalla cartella di input, le ridimensiona, e crea una GIF animata WebP nella cartella di output.
    """
    width, height = get_resolution(resolution)
    
    print(f"Risoluzione selezionata: {format_resolution(resolution)}")
    
    # Verifica l'esistenza della cartella di input
    if not os.path.exists(input_folder):
        print(f"La cartella di input '{input_folder}' non esiste.")
        return
     
    try:
        # Legge e ridimensiona le immagini
        images = read_and_resize_images(input_folder, width, height)
        
        # Crea il nome univoco del file di output
        output_file = make_unique_filename(output_folder, output_filename)

        # Salva la GIF animata
        save_animation(images, output_folder, output_file, duration)
    
    except Exception as e:
        print(f"Si è verificato un errore durante la creazione della GIF WebP: {str(e)}")


def get_resolution(name):
    """
    Restituisce le dimensioni di risoluzione corrispondenti al nome dato.
    """
    return resolutions.get(name, (0, 0))


def format_resolution(name):
    """
    Formatta il nome della risoluzione con le dimensioni corrispondenti.
    """
    width, height = get_resolution(name)
    return f"{name}: {width}x{height}"

def validate_input_output_folders(input_folder, output_folder):
    """
    Verifica se i percorsi di input e output sono validi.
    """
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"La cartella di input '{input_folder}' non esiste.")

    if os.path.exists(output_folder):
        if not os.path.isdir(output_folder):
            raise NotADirectoryError(f"Il percorso di output '{output_folder}' esiste ma non è una cartella.")
    else:
        os.makedirs(output_folder)
        print(f"Cartella di output '{output_folder}' creata.")
            
def main():
    try:
        # Input da parte dell'utente
        input_folder = input("Inserisci il percorso della cartella contenente le immagini: ").strip()
        output_folder = input("Inserisci il percorso della cartella di output: ").strip()

        # Validazione dei percorsi di input e output
        validate_input_output_folders(input_folder, output_folder)

        output_filename_base = input("Inserisci il nome base del file GIF WebP di output: ").strip()
      
        # Selezione dell'estensione
        output_extension = input("Inserisci l'estensione dell'output desiderata (webp o gif): ").strip().lower()
        if output_extension not in ['webp', 'gif']:
            print("Estensione non valida. Utilizzando l'estensione di default 'webp'.")
            output_extension = 'webp'

        resolution_name = input("Seleziona la risoluzione desiderata (SD, HD, FHD, 2K, 4K, 8K): ").strip()
        if resolution_name not in resolutions:
            raise ValueError("Risoluzione non valida. Seleziona tra SD, HD, FHD, 2K, 4K, 8K.")

        frame_duration_seconds = int(input("Inserisci la durata di ogni frame dell'animazione in secondi: ").strip())
        duration = frame_duration_seconds * 1000  # Converti secondi in millisecondi

        # Crea la GIF WebP
        create_webp_animation(input_folder, output_folder, f"{output_filename_base}.{output_extension}", resolution_name, duration)
        
    except ValueError as ve:
        print(f"Errore: {ve}")
    
    except FileNotFoundError as fnfe:
        print(f"Errore: {fnfe}")

    except Exception as e:
        print(f"Si è verificato un errore imprevisto: {str(e)}")

if __name__ == "__main__":
    main()