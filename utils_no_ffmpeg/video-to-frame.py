import os
import cv2
from pathlib import Path
from tqdm import tqdm

def video_to_frames(video_path, output_folder, frame_name):
    """
    Converte un video in singoli frame e li salva in una cartella specifica.

    :param video_path: Percorso del file video.
    :param output_folder: Cartella dove salvare i frame.
    :param frame_name: Prefisso del nome dei file frame.
    """
    # Verifica se il file video esiste
    if not os.path.exists(video_path):
        print(f"Errore: il file video '{video_path}' non esiste.")
        return

    # Apri il video
    cap = cv2.VideoCapture(video_path)

    # Ottieni il numero totale di frame nel video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Crea la cartella di output se non esiste già
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    # Salva i frame
    frame_count = 0
    for _ in tqdm(range(total_frames), desc="Salvataggio frame", unit="frame"):
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = output_folder / f"{frame_name}_{frame_count:04d}.png"
        cv2.imwrite(str(frame_path), frame)
        frame_count += 1

    # Rilascia la risorsa video
    cap.release()

    print(f"Salvati {frame_count} frame nella cartella '{output_folder}'.")

def get_videos_in_folder(folder_path):
    """
    Ritorna un elenco di file video presenti nella cartella.

    :param folder_path: Percorso della cartella.
    :return: Lista di file video.
    """
    valid_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv')
    folder = Path(folder_path)
    return [file for file in folder.iterdir() if file.is_file() and file.suffix.lower() in valid_extensions]

def get_valid_input(prompt, validator):
    """
    Richiede un input valido all'utente.

    :param prompt: Messaggio da mostrare all'utente.
    :param validator: Funzione che valida l'input.
    :return: Input valido dell'utente.
    """
    while True:
        user_input = input(prompt)
        if validator(user_input):
            return user_input
        else:
            print("Input non valido. Riprova.")

def is_valid_video_or_folder(path):
    """
    Verifica se il percorso è un file video o una cartella esistente.

    :param path: Percorso fornito dall'utente.
    :return: True se valido, False altrimenti.
    """
    return os.path.isfile(path) or os.path.isdir(path)

def choose_video_from_folder(folder_path):
    """
    Permette all'utente di scegliere un video tra quelli presenti in una cartella.

    :param folder_path: Percorso della cartella.
    :return: Percorso del video scelto.
    """
    videos = get_videos_in_folder(folder_path)
    if not videos:
        print(f"Nessun file video trovato nella cartella '{folder_path}'.")
        return None
    elif len(videos) == 1:
        print(f"Trovato un unico video: {videos[0].name}.")
        return str(videos[0])
    else:
        print("Sono stati trovati più video. Scegli uno dei seguenti:")
        for idx, video in enumerate(videos, start=1):
            print(f"{idx}. {video.name}")
        while True:
            choice = input("Inserisci il numero del video desiderato: ")
            if choice.isdigit() and 1 <= int(choice) <= len(videos):
                return str(videos[int(choice) - 1])
            else:
                print("Scelta non valida. Riprova.")

# Chiedi all'utente il percorso del video o della cartella contenente i video
video_or_folder = get_valid_input("Inserisci il percorso del video o della cartella contenente i video: ", is_valid_video_or_folder)

# Determina il file video da utilizzare
if os.path.isdir(video_or_folder):
    video_path = choose_video_from_folder(video_or_folder)
    if not video_path:
        exit("Nessun video selezionato. Programma terminato.")
else:
    video_path = video_or_folder

# Chiedi la cartella di output e il nome base per i frame
output_folder = get_valid_input("Inserisci il nome della cartella di output: ", lambda x: x.strip() != "")
frame_name = get_valid_input("Inserisci il nome base per i frame: ", lambda x: x.strip() != "")

# Esegui la conversione
video_to_frames(video_path, output_folder, frame_name)
