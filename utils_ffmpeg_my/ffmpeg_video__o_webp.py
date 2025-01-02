from ffmpeg import FFmpeg
import os
import traceback

def create_webp_animation(video_path, output_path, fps=10, scale_width=640, quality=50):
    """
    Crea un'animazione WebP a partire da un video utilizzando ffmpeg.

    :param video_path: Percorso del video di input.
    :param output_path: Percorso di destinazione per l'animazione WebP.
    :param fps: Numero di fotogrammi per secondo nell'animazione WebP.
    :param scale_width: Larghezza dell'immagine di output (mantiene le proporzioni).
    :param quality: Qualità dell'animazione (0-100, dove 0 è la peggiore qualità e 100 la migliore).
    """
    try:
        # Verifica che il video di input esista
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Il file di input '{video_path}' non esiste.")
        
        # Verifica se il file di input è un video
        if not os.path.isfile(video_path):
            raise FileNotFoundError(f"Il percorso '{video_path}' non è un file video valido.")

        # Verifica che la cartella di destinazione esista
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            raise FileNotFoundError(f"La cartella di destinazione '{output_dir}' non esiste.")
        
        # Verifica che la cartella di destinazione sia una directory
        if not os.path.isdir(output_dir):
            raise FileNotFoundError(f"Il percorso '{output_dir}' non è una directory valida.")
        
        # Creazione dell'animazione WebP
        ffmpeg = (
            FFmpeg(executable='C:/ffmpeg/bin/ffmpeg.exe')
            .option("y")  # Forza sovrascrittura file di output
            .input(video_path)  # Percorso del video di input
            .output(
                output_path,  # Percorso dell'animazione WebP di output
                vcodec="libwebp",  # Usa il codec WebP
                loop=0,  # Loop infinito
                qscale=quality,  # Controllo della qualità (0-100)
                vf=f"fps={fps}"  # Filtro di scalatura e fps
            )
        )

        ffmpeg.execute()
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


# Esempio di utilizzo
video_path = './video/blue-haired-blind-girl.3840x2160.mp4'  # Percorso del video di input
output_path = './output/offfmpeg-blue-hiared-blind-girl-original-size.webp'  # Percorso di destinazione per l'animazione WebP

print("Creazione animazione WebP in corso...")
print(f"Video: {video_path}")
print(f"Output: {output_path}")
create_webp_animation(video_path, output_path, fps=60, quality=100)
