from tqdm import tqdm
import subprocess
import os
import re
from dotenv import load_dotenv
import traceback


load_dotenv(dotenv_path='./.env')


class VideoToWebpConverter:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.size = {
            "sd": {
                "width": 640,
                "height": 480
            },
            "hd": {
                "width": 1280,
                "height": 720
            },
            "fhd": {
                "width": 1920,
                "height": 1080
            },
            "2k": {
                "width": 2560,
                "height": 1440
            },
            "4k": {
                "width": 3840,
                "height": 2160
            },
            "8k": {
                "width": 7680,
                "height": 4320
            },
            "original": {
                "width": -1,
                "height": -1
            }
        }

    def create_webp_animation(self,video_path, output_path, fps:int=10, quality=50, 
                              ffmpeg_path='C:/ffmpeg/bin/ffmpeg.exe', size={"width": -1, "height": -1}): 
        """
        Crea un'animazione WebP a partire da un video utilizzando ffmpeg con barra di progresso.
        
        :param video_path: Percorso del video di input.
        :param output_path: Percorso di destinazione per l'animazione WebP.
        :param fps: Numero di fotogrammi per secondo nell'animazione WebP.
        :param quality: Qualità dell'animazione (0-100, dove 0 è la peggiore qualità e 100 la migliore).
        :param ffmpeg_path: Percorso del file eseguibile ffmpeg.
        """
        try:
            # Verifica che il video di input esista
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Il file di input '{video_path}' non esiste.")
            
            # Verifica che la cartella di destinazione esista
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                raise FileNotFoundError(f"La cartella di destinazione '{output_dir}' non esiste.")
        
            print("size", size)
        # Nuovo comando con filtro scale per ridurre la larghezza
            command = [
                ffmpeg_path,  # Usa il percorso completo di ffmpeg.exe
                '-i', video_path,  # Input video
                '-vcodec', 'libwebp',  # Usa il codec WebP
                '-loop', '0',  # Loop infinito
                '-q:v', str(quality),  # Qualità
                '-vf', f'fps={fps},scale={(size["width"])}:{size["height"]}',  # Filtro fps e scale
                '-y',  # Forza sovrascrittura
                output_path  # Output WebP
            ]
            
            # Esegui FFmpeg con tqdm
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            # Estrai la durata del video
            duration = None
            for line in process.stderr:
                # Trova la durata del video nelle informazioni ffmpeg
                match = re.search(r"Duration: (\d+):(\d+):(\d+)", line)
                if match:
                    hours, minutes, seconds = map(int, match.groups())
                    duration = hours * 3600 + minutes * 60 + seconds
                    break
            
            # Se non troviamo la durata, imposta un valore di fallback
            if not duration:
                duration = 10  # Imposta 10 secondi come fallback
            
            # Crea una barra di progresso
            with tqdm(total=duration, unit='s', desc="Creazione animazione WebP") as pbar:
                for line in process.stderr:
                    # Cerca il tempo trascorso nel log di ffmpeg
                    match = re.search(r"time=(\d+):(\d+):(\d+)\.(\d+)", line)
                    if match:
                        hours, minutes, seconds, _ = match.groups()
                        elapsed_time = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
                        pbar.n = elapsed_time
                        pbar.last_print_n = elapsed_time
                        pbar.update(0)  # Forza l'aggiornamento della barra di progresso

            # Attendi che il processo di FFmpeg finisca
            process.wait()

            print(f"Animazione WebP creata con successo: {output_path}")

        except FileNotFoundError as fnf_error:
            print(f"Errore: {fnf_error}")
            # Stampa il traceback per un errore più dettagliato
            print("Dettagli dell'errore:")
            traceback.print_exc()

        except PermissionError as perm_error:
            print(f"Errore di permessi: {perm_error}")
        
        except Exception as e:
            print(f"Errore durante la creazione dell'animazione WebP: {e}")
            traceback.print_exc()


    def select_resolution(self):
        print("Scegli la risoluzione desiderata:")
        print("---------------------------")
        for i, resolution in enumerate(self.size, start=1):
            dimensions = self.size[resolution]
            if resolution == "original":
                print(f"{i} - {resolution.upper()}: originale")
                continue
            print(f"{i} - {resolution.upper()}: {dimensions['width']}x{dimensions['height']}")
        print("---------------------------")

        while True:
            user_input = input("Inserisci il numero della risoluzione: ")
            if user_input.isdigit() and 1 <= int(user_input) <= len(self.size):
                selected_resolution = list(self.size.keys())[int(user_input) - 1]
                selected_dimensions = self.size[selected_resolution]
                print(f"Hai scelto la risoluzione {selected_resolution.upper()}: {selected_dimensions['width']}x{selected_dimensions['height']}")
                return selected_dimensions
            else:
                print("Ingresso non valido. Riprova.")

# Esempio di utilizzo
load_dotenv()
ffmpeg_path = os.getenv('FFMPEG_PATH')

