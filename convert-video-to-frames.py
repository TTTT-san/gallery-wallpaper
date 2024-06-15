import imageio
import os


def make_unique_filename(output_folder, output_filename):
    """
    Se il file esiste già nella cartella di output, aggiunge un numero incrementale al nome del file fino a ottenere un nome univoco.
    Restituisce il nome completo del file univoco.
    """
    base_name, ext = os.path.splitext(output_filename)
    counter = 1
    new_filename = output_filename
    while os.path.exists(os.path.join(output_folder, new_filename)):
        new_filename = f"{base_name}_{counter}{ext}"
        counter += 1
    return os.path.join(output_folder, new_filename)

def convert_video(input_video, output_pattern, output_format='webp', max_fps=30, max_duration=10):
    try:
        # Verifica l'esistenza della cartella di input
        input_folder = os.path.dirname(input_video)
        os.makedirs(input_folder, exist_ok=True)
        
        
         # Verifica se il file di input esiste
        if not os.path.exists(input_video):
            print(f"Il file di input '{input_video}' non esiste.")
            return
        
        # Verifica l'esistenza della cartella di output
        output_folder = os.path.dirname(output_pattern)
        os.makedirs(output_folder, exist_ok=True)
        print(f"Cartella di output creata o già esistente: {output_folder}")

        print(f"Inizia la conversione del video {input_video} in formato {output_format.upper()}.")

        # Caricamento delle informazioni sul video di input
        reader = imageio.get_reader(input_video)
        fps = reader.get_meta_data()['fps']
        total_frames = reader.get_length()
        print(f"Frame rate del video: {fps}")
        print(f"Numero totale di frame nel video: {total_frames}")

        # Calcolo dei parametri di conversione
        target_fps = min(fps, max_fps)
        max_frames_to_extract = int(target_fps * max_duration)
        frames_to_extract = min(total_frames, max_frames_to_extract)
        print(f"Frame rate massimo desiderato: {target_fps}")
        print(f"Numero massimo di frame da estrarre: {frames_to_extract}")

        # Calcolo degli indici dei frame da estrarre
        frame_interval = int(fps / target_fps)
        frames_indices = range(0, frames_to_extract * frame_interval, frame_interval)

        # Verifica se il file di output esiste già
        if os.path.exists(output_pattern):
            output_pattern = make_unique_filename(output_folder, os.path.basename(output_pattern))
            print(f"Un file con lo stesso nome esiste già. Generato un nome univoco: {output_pattern}")

        # Conversione in formato specificato
        with imageio.get_writer(output_pattern, format=output_format, fps=target_fps) as writer:
            for idx in frames_indices:
                frame = reader.get_data(idx)
                writer.append_data(frame)

                # Visualizzazione avanzamento ogni 100 frame
                if (idx + 1) % 100 == 0 or (idx + 1) == len(frames_indices):
                    print(f"Frame {idx + 1} su {len(frames_indices)} convertiti in {output_format.upper()}.")

        print(f"Conversione completata. I file sono stati salvati in: {output_folder}")

    except Exception as e:
        print(f"Si è verificato un errore durante la conversione del video {input_video}:")
        print(str(e))

    finally:
        if 'reader' in locals():
            reader.close()  # Chiudi il lettore se è stato aperto
import os

def suggest_input_filename(input_folder):
    """
    Suggerisce il nome del file .mp4 di input se esiste esattamente un file .mp4 nella cartella di input.
    """
    try:
        mp4_files = [filename for filename in os.listdir(input_folder) if filename.lower().endswith('.mp4')]
        
        if len(mp4_files) == 1:
            print(f"Unico file.mp4: {mp4_files[0]}")
            return mp4_files[0]
        
        elif len(mp4_files) > 1:
            print("Ci sono più file .mp4 nella cartella di input. Specifica il nome manualmente.")
            return None
        
        else:
            print(f"Nessun file .mp4 trovato nella cartella di input '{input_folder}'.")
            return None

    except FileNotFoundError:
        print(f"La cartella di input '{input_folder}' non esiste.")
        return None

    except Exception as e:
        print(f"Si è verificato un errore durante la ricerca dei file .mp4: {str(e)}")
        return None

def main(): 
    try:
        # Input della cartella contenente i video .mp4
        input_folder = input("Inserisci il nome della cartella contenente i video .mp4: ").strip()
        if not os.path.exists(input_folder):
            raise FileNotFoundError(f"La cartella di input '{input_folder}' non esiste.")

        # Suggerimento per il nome del file di input .mp4
        suggested_input_name = suggest_input_filename(input_folder)

        # Input del nome del file di output
        output_filename = input("Inserisci il nome del file di output: ").strip()

        # Verifica se è stato suggerito un nome di input e se il nome di output corrisponde
        if suggested_input_name and output_filename == suggested_input_name:
            print("Il nome di output non può essere lo stesso del file di input suggerito.")
            output_filename = input("Inserisci un altro nome per il file di output: ").strip()

        # Input dell'estensione dell'output (webp o gif)
        output_extension = input("Inserisci l'estensione dell'output (webp o gif): ").strip().lower()
        if output_extension not in ['webp', 'gif']:
            print("Estensione non valida. Utilizzando l'estensione di default 'webp'.")
            output_extension = 'webp'

        # Input della cartella di output
        output_folder = input("Inserisci la cartella di output dove salvare il file: ").strip()
        os.makedirs(output_folder, exist_ok=True)

        # Visualizzazione dei percorsi e nomi dei file inseriti
        print(f"Percorso del video di input: {input_folder}")
        print(f"Cartella di output: {output_folder}")
        print(f"Nome del file di output: {output_filename}.{output_extension}")

        # Esecuzione della conversione del video con i valori inseriti dall'utente
        input_video_path = os.path.join(input_folder, suggested_input_name) if suggested_input_name else None
        output_video_path = os.path.join(output_folder, f"{output_filename}.{output_extension}")
        convert_video(input_video_path, output_video_path, output_format=output_extension)

    except FileNotFoundError as e:
        print(f"Errore: {str(e)}")

    except Exception as e:
        print(f"Si è verificato un errore: {str(e)}")

if __name__ == "__main__":
    main();