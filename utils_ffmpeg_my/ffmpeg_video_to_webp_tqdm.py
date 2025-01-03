from tqdm import tqdm
import subprocess
import os
import re
from dotenv import load_dotenv
import traceback
import multiprocessing
from moviepy.editor import VideoFileClip


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

    def create_webp_animation(self, video_path, output_path, fps=10, quality=0, 
                                ffmpeg_path='C:/ffmpeg/bin/ffmpeg.exe', size={"width": -1, "height": -1}): 
            """
            Crea un'animazione WebP a partire da un video utilizzando ffmpeg con barra di progresso.
            
            :param video_path: Percorso del video di input.
            :param output_path: Percorso di destinazione per l'animazione WebP.
            :param fps: Numero di fotogrammi per secondo nell'animazione WebP.
            :param quality: Qualità dell'animazione (0-100, dove 0 è la peggiore qualità e 100 la migliore).
            :param ffmpeg_path: Percorso del file eseguibile ffmpeg.
            """

            video = VideoFileClip(video_path)
            fps = video.fps
            print(f"FPS: {fps}")

            height = video.size[1]
            width = video.size[0]
            print(f"Dimensioni: {width}x{height}")

            video.close()

            try:
                # Verifica file di input
                if not os.path.exists(video_path):
                    raise FileNotFoundError(f"Il file di input '{video_path}' non esiste.")
                
                # Verifica directory di output
                output_dir = os.path.dirname(output_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)


                # Controlla il numero di core disponibili
                num_cores = multiprocessing.cpu_count()

                # Usa 2 thread se il sistema ha almeno 2 core
                threads = 2 if num_cores >= 2 else 1
                print(f"Numero di core disponibili: {num_cores}. Usando {threads} thread per la conversione.")
                print("HW acceleration:",'auto')
                # Crea il comando
                if output_path.endswith('.gif'):
                    # command = [
                    #     ffmpeg_path,
                    #     '-hwaccel', 'auto',
                    #     '-i', video_path,
                    #     '-vf', f'fps={fps},scale={(size["width"])}:{size["height"]}',
                    #     '-loop', '0',
                    #     '-r', str(fps),
                    #     '-f', 'gif',
                    #     output_path
                    # ]
                #     command = [
                #         ffmpeg_path,
                #         '-hwaccel', 'auto',
                #         '-i', video_path,
                #         '-vf', f'fps={fps},scale={(size["width"])}:-1', #{size["height"]} # ffmpeg -i input.mp4 -vf "eq=contrast=0.5:brightness=0.5:saturation=0.5" output.mp4
                #         '-loop', '0',
                #         '-r', str(fps),
                #         '-f', 'gif',
                #         '-q:v', '31',
                #         '-crf', '51',
                #         '-pix_fmt', 'rgb24',
                #         '-compression_level', '3', # valore di compressione (0-3)
                #         '-lossless', '0',
#                #         '-preset','slow',# I preset disponibili sono: ultrafast, superfast, veryfast, faster, fast, medium (default), slow, slower, veryslow
                #         output_path
                 #    ]
                    command = [
                         ffmpeg_path,
                         '-hwaccel', 'auto', # non funge credo
                         '-i', video_path,
                         '-i', r'C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\palette\palette_bayer.png',  # Percorso del file della palette
#                         '-filter_complex', f'[0][1:v]paletteuse=dither=none,scale={size["width"]}:-1,fps={fps}',
                         '-filter_complex', f'fps={fps},scale={size["width"]}:-1:flags=lanczos,paletteuse=dither=none',
                         '-loop', '0',
                         '-r', str(fps),
                         '-f', 'gif',
                         '-compression_level', '3', # valore di compressione (0-9)
                         '-lossless', '0',
                         '-crf', '30',
                         '-preset','slow',# I preset disponibili sono: ultrafast, superfast, veryfast, faster, fast, medium (default), slow, slower, veryslow
                         output_path
                     ]



                else:
                    command = [
                        ffmpeg_path,  # Usa il percorso completo di ffmpeg.exe
                        '-hwaccel', 'auto',  # Accelerazione hardware automatica
                        '-i', video_path,  # Input video
                        '-vcodec', 'libwebp',  # Usa il codec WebP
                        '-loop', '0',  # Loop infinito
                        '-crf', str(quality),  # Qualità crf (0-51, dove 0 è la peggiore qualità e 51 la migliore)
                        '-vf', f'fps={fps},scale={(size["width"])}:{size["height"]}',  # Filtro fps e scale
                        '-threads', str(threads),  # Numero di thread
                        '-n',  # Forza sovrascrittura
                        output_path  # Output WebP
                    ]


                # Esegui FFmpeg
                process = subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True)

            # Durata del video
                duration = None
                for line in process.stderr:
                    match = re.search(r"Duration: (\d+):(\d+):(\d+)", line)
                    if match:
                        hours, minutes, seconds = map(int, match.groups())
                        duration = hours * 3600 + minutes * 60 + seconds
                        break
                
                if not duration:
                    duration = 10  # Imposta durata di fallback

                import time
                # Barra di progresso
                with tqdm(total=duration, unit='s', desc="Creazione animazione WebP",ncols=80) as pbar:
                    last_elapsed_time = -1  # Variabile per tenere traccia dell'ultimo tempo aggiornato
        
                    # Start del tempo per controllo aggiornamenti
                    start_time = time.time()  
                    
                    for line in process.stderr:
                        match = re.search(r"time=(\d+):(\d+):(\d+)\.(\d+)", line)
                        if match:
                            hours, minutes, seconds, _ = match.groups()
                            elapsed_time = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
                            
                            # Aggiorna la barra di progresso solo quando il tempo è cambiato
                            if elapsed_time > last_elapsed_time:
                                time_diff = elapsed_time - last_elapsed_time
                                pbar.update(time_diff)  # Incrementa la barra
                                last_elapsed_time = elapsed_time  # Aggiorna l'ultimo tempo
                                
                            # Verifica se è passato abbastanza tempo per un altro aggiornamento
                            if (time.time() - start_time) >= 0.1:  # Frequenza di aggiornamento ogni 100ms
                                start_time = time.time()  # Riavvia il timer

                # Attendi che il processo finisca
                process.wait()

                print(f"Animazione WebP creata con successo: {output_path}")

            except FileNotFoundError as fnf_error:
                print(f"Errore: {fnf_error}")
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

