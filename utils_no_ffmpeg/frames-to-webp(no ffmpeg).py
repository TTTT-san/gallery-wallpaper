import os
import math
from PIL import Image
import re
from tqdm import tqdm

def crea_animazione_webp_incrementale(input_dir, output_file, max_memory_mb=500, max_frames=200, fps=30, quality=100,lossless=True,optimize=False):
    # Verifica esistenza directory di input
    if not os.path.exists(input_dir):
        print(f"Errore: La cartella {input_dir} non esiste.")
        return

    # Raccolta e ordinamento dei file immagine
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        print(f"Errore: Nessuna immagine trovata nella cartella {input_dir}.")
        return

    try:
        image_files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))
    except ValueError:
        print("Errore: Assicurati che i nomi dei file contengano numeri per l'ordinamento.")
        return

    # Calcolo massimo batch di frame
    max_frame_batch = get_max_frames_batch(input_dir, max_memory_mb)
    image_files = image_files[:min(max_frames, len(image_files))]
    total_frames = len(image_files)
    num_batches = math.ceil(total_frames / max_frame_batch)

    duration =(1000 / fps)
    # Creazione della cartella di output
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    print(f"Input directory: {input_dir}")
    print(f"Output file: {output_file}")
    print(f"Total frames: {total_frames}")
    print(f"Max frames per batch: {max_frame_batch}")
    print(f"FPS: {fps} | Duration avg: {duration} ms")
    print(f"Qualità: {quality}")
    

    # Creazione animazione WebP con gestione del residuo
    with tqdm(total=total_frames, desc="Creazione animazione WebP", unit="frame") as pbar:
        residual = 0  # Accumulatore del residuo temporale
        exact_duration = 1000 / fps  # Durata precisa per frame in millisecondi
        int_duration = int(exact_duration)  # Durata intera approssimata

        for batch_idx in range(num_batches):
            start_idx = batch_idx * max_frame_batch
            end_idx = min((batch_idx + 1) * max_frame_batch, total_frames)
            batch = [Image.open(os.path.join(input_dir, img_file)) for img_file in image_files[start_idx:end_idx]]

            # Calcola la durata del batch corrente
            frame_duration = int_duration + (1 if residual >= 0.5 else 0)
            residual = (residual + exact_duration - frame_duration) % 1  # Aggiorna il residuo

            if batch_idx == 0:
                batch[0].save(
                    output_file,
                    save_all=True,
                    append_images=batch[1:],
                    loop=0,
                    duration=frame_duration,
                    quality=quality,
                    lossless=lossless,
                    optimize=optimize,
                )
            else:
                with Image.open(output_file) as img:
                    img.save(
                        output_file,
                        save_all=True,
                        append_images=batch,
                        loop=0,
                        duration=frame_duration,
                        quality=quality,
                        lossless=lossless,
                        optimize=optimize,
                    )

            pbar.update(len(batch))


    print(f"File .webp salvato con successo: {output_file}")


def get_max_frames_batch(input_dir, max_memory_mb=500):
    all_files = os.listdir(input_dir)
    for filename in all_files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            first_image_path = os.path.join(input_dir, filename)
            first_image = Image.open(first_image_path)
            break
    else:
        print("Errore: Nessuna immagine valida trovata per calcolare il batch.")
        return 1

    width, height = first_image.size
    max_frames_batch = int(max_memory_mb * 1024 * 1024 / (width * height * 3))
    return max_frames_batch


# Parametri di input
input_dir = r"C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\3820"
output_webp = "./output/blue-haired-avg-lossless.gif"
max_frames = 1000
fps = 60

crea_animazione_webp_incrementale(input_dir, output_webp, max_frames=max_frames, fps=fps)
