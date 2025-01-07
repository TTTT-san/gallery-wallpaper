import os
import shutil
from PIL import Image
import cv2
from tqdm import tqdm


class FrameExtractor:
    """Classe per estrarre e gestire i frame di un video."""

    def __init__(self, video_path: str):
        """
        Inizializza la classe con il percorso del video.
        :param video_path: Percorso del file video.
        """
        if not os.path.isfile(video_path):
            raise ValueError(f"Il file specificato non esiste: {video_path}")

        self.video_path = video_path
        self.output_dir = os.path.join(os.path.dirname(video_path), os.path.splitext(os.path.basename(video_path))[0] + "_frames")
        self.fps = -1
        
    def get_fps(self):
        """Restituisce gli FPS del video."""
        if self.fps == -1:
            print("FPS non ancora calcolati. Eseguire prima l'estrazione dei frame.")
            return -1
        return self.fps

    def get_total_frames(self):
        return self.total_frames
        
    def extract_exact_frames(self, num_frames: int = -1) -> str:
        """
        Estrae un numero esatto di frame distribuiti uniformemente da un video e li salva in una cartella.
        
        :param num_frames: Numero di frame da estrarre (-1 per tutti i frame).
        :return: Percorso della cartella contenente i frame estratti.
        """
        print("Avvio dell'estrazione dei frame...")

        # Creazione della cartella di output
        os.makedirs(self.output_dir, exist_ok=True)

        # Apertura del video
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Impossibile aprire il video: {self.video_path}")

        # Recupero dei dati del video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(cap.get(cv2.CAP_PROP_FPS))

        if num_frames == -1:
            num_frames = total_frames
        elif num_frames > total_frames:
            raise ValueError(f"Il numero di frame richiesto ({num_frames}) supera i frame totali ({total_frames}) nel video.")
        elif num_frames < -1:
            raise ValueError(f"Il numero di frame richiesto ({num_frames}) non è valido.")

        print(f"Video: {self.video_path}")
        print(f"FPS: {self.fps}")
        print(f"Frame totali: {total_frames}, Frame da estrarre: {num_frames}.")

        # Calcolo degli intervalli tra i frame da salvare
        frame_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]

        for frame_number in tqdm(frame_indices, desc="Estrazione dei frame", unit="frame", ncols=70):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            if not ret:
                print(f"Errore durante la lettura del frame {frame_number}.")
                continue

            # Salva il frame come immagine
            frame_filename = os.path.join(self.output_dir, f"frame_{frame_number:04d}.jpg")
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            image.save(frame_filename)

        cap.release()
        print(f"Tutti i frame sono stati salvati nella cartella: {self.output_dir}")
        return self.output_dir
    
    def extract_frames_by_fps(self, target_fps: int, sleep_time: float = 0.01) -> str:
        """
        Estrae i frame da un video a un determinato FPS e li salva in una cartella, limitando l'uso della CPU.
        
        :param target_fps: Frequenza dei frame da estrarre (FPS desiderato).
        :param sleep_time: Tempo di attesa (in secondi) tra ogni estrazione di frame per limitare l'uso della CPU.
        :return: Percorso della cartella contenente i frame estratti.
        """
        print(f"Avvio dell'estrazione dei frame con FPS = {target_fps}...")

        # Creazione della cartella di output
        os.makedirs(self.output_dir, exist_ok=True)

        # Apertura del video
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Impossibile aprire il video: {self.video_path}")

        # Recupero dei dati del video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Calcolo l'intervallo di estrazione in base agli FPS desiderati
        frame_interval = max(int(video_fps / target_fps), 1)

        print(f"Video FPS: {video_fps}, FPS richiesto per l'estrazione: {target_fps}")
        print(f"Frame totali: {total_frames}, Frame estratti ogni {frame_interval} frame.")

        frame_number = 0
        frame_counter = 0  # Conta i frame estratti
        import time
        # Inizializzazione della barra di progresso
        with tqdm(total=total_frames // frame_interval, desc="Estrazione dei frame", unit="frame", ncols=70) as pbar:
            while frame_number < total_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                ret, frame = cap.read()

                if not ret:
                    print(f"Errore durante la lettura del frame {frame_number}.")
                    break

                # Salva il frame come immagine
                frame_filename = os.path.join(self.output_dir, f"frame_{frame_number:04d}.jpg")
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_rgb)
                image.save(frame_filename)

                frame_counter += 1
                frame_number += frame_interval

                # Aggiorna la barra di progresso
                pbar.update(1)
                # Limita l'uso della CPU
                time.sleep(sleep_time)

        cap.release()
        print(f"{frame_counter} frame sono stati salvati nella cartella: {self.output_dir}")
        return self.output_dir
    
    
    def extract_frames_by_time_interval(self, target_interval: float = 0.9) -> str:
        """
        Estrae i frame da un video a intervalli di tempo regolari (ad esempio ogni 0.9 secondi)
        e li salva in una cartella.

        :param target_interval: Intervallo temporale tra i frame in secondi (default: 0.9).
        :return: Percorso della cartella contenente i frame estratti.
        """
        print(f"Avvio dell'estrazione dei frame con intervallo di {target_interval} secondi...")

        # Creazione della cartella di output
        os.makedirs(self.output_dir, exist_ok=True)

        # Apertura del video
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Impossibile aprire il video: {self.video_path}")

        # Recupero dei dati del video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Calcola la durata totale del video in secondi
        total_duration = total_frames / video_fps
        print(f"Durata totale del video: {total_duration:.2f} secondi.")

        # Calcola il numero di frame da estrarre a intervalli di target_interval secondi
        num_frames_to_extract = int(total_duration / target_interval)
        print(f"Numero di frame da estrarre: {num_frames_to_extract}")

        frame_counter = 0  # Conta i frame estratti

        # Inizializzazione della barra di progresso
        with tqdm(total=num_frames_to_extract, desc="Estrazione dei frame", unit="frame", ncols=70) as pbar:
            for i in range(num_frames_to_extract):
                # Calcola il tempo in secondi in cui estrarre il frame
                current_time = i * target_interval  # Tempo per estrarre il frame
                cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)  # Imposta il tempo in millisecondi
                ret, frame = cap.read()

                if not ret:
                    print(f"Errore durante la lettura del frame al tempo {current_time} secondi.")
                    break

                # Salva il frame come immagine
                frame_filename = os.path.join(self.output_dir, f"frame_{frame_counter:04d}.jpg")
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_rgb)
                image.save(frame_filename)

                frame_counter += 1

                # Aggiorna la barra di progresso
                pbar.update(1)
                import time
                time.sleep(0.01)

        cap.release()
        print(f"{frame_counter} frame sono stati salvati nella cartella: {self.output_dir}")
        return self.output_dir

    def extract_frames_by_time_interval_smooth(self, target_interval: float = 0.9, smooth_factor: float = 1.0) -> str:
        """
        Estrae i frame da un video a intervalli di tempo regolari (ad esempio ogni 0.9 secondi) e li salva in una cartella.
        
        Aggiustato per migliorare la fluidità in base alla lunghezza del video e ai frame rate.

        :param target_interval: Intervallo temporale tra i frame in secondi (default: 0.9).
        :param smooth_factor: Fattore di "fluidità" per regolare la frequenza di estrazione (1.0 = intervallo costante).
        :return: Percorso della cartella contenente i frame estratti.
        """
        print(f"Avvio dell'estrazione dei frame con intervallo di {target_interval} secondi...")

        # Creazione della cartella di output
        os.makedirs(self.output_dir, exist_ok=True)

        # Apertura del video
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Impossibile aprire il video: {self.video_path}")

        # Recupero dei dati del video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Calcola la durata totale del video in secondi
        total_duration = total_frames / video_fps
        print(f"Durata totale del video: {total_duration:.2f} secondi.")

        # Calcola il numero di frame da estrarre a intervalli di target_interval secondi
        num_frames_to_extract = int(total_duration / target_interval * smooth_factor)
        print(f"Numero di frame da estrarre: {num_frames_to_extract}")

        frame_counter = 0  # Conta i frame estratti

        # Inizializzazione della barra di progresso
        with tqdm(total=num_frames_to_extract, desc="Estrazione dei frame", unit="frame", ncols=70) as pbar:
            for i in range(num_frames_to_extract):
                # Calcola il tempo in secondi in cui estrarre il frame
                current_time = i * target_interval * smooth_factor  # Tempo per estrarre il frame
                cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)  # Imposta il tempo in millisecondi
                ret, frame = cap.read()

                if not ret:
                    print(f"Errore durante la lettura del frame al tempo {current_time} secondi.")
                    break

                # Salva il frame come immagine
                frame_filename = os.path.join(self.output_dir, f"frame_{frame_counter:04d}.jpg")
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_rgb)
                image.save(frame_filename)

                frame_counter += 1

                # Aggiorna la barra di progresso
                pbar.update(1)

        cap.release()
        print(f"{frame_counter} frame sono stati salvati nella cartella: {self.output_dir}")
        return self.output_dir

    def extract_frames_by_time_interval_og(self, target_interval: float = 0.9) -> str:
        """
        Estrae i frame da un video a intervalli di tempo regolari (ad esempio ogni 0.9 secondi) e li salva in una cartella.
        La velocità di visualizzazione rimane invariata rispetto al video originale.

        :param target_interval: Intervallo temporale tra i frame in secondi (default: 0.9).
        :return: Percorso della cartella contenente i frame estratti.
        """
        print(f"Avvio dell'estrazione dei frame con intervallo di {target_interval} secondi...")

        # Creazione della cartella di output
        os.makedirs(self.output_dir, exist_ok=True)

        # Apertura del video
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Impossibile aprire il video: {self.video_path}")

        # Recupero dei dati del video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Calcola la durata totale del video in secondi
        total_duration = total_frames / video_fps
        print(f"Durata totale del video: {total_duration:.2f} secondi.")

        # Calcola il numero di frame da estrarre a intervalli di target_interval secondi
        num_frames_to_extract = int(total_duration / target_interval)
        print(f"Numero di frame da estrarre: {num_frames_to_extract}")

        frame_counter = 0  # Conta i frame estratti

        # Inizializzazione della barra di progresso
        with tqdm(total=num_frames_to_extract, desc="Estrazione dei frame", unit="frame", ncols=70) as pbar:
            for i in range(num_frames_to_extract):
                # Calcola il tempo in secondi in cui estrarre il frame
                current_time = i * target_interval  # Tempo per estrarre il frame
                cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)  # Imposta il tempo in millisecondi
                ret, frame = cap.read()

                if not ret:
                    print(f"Errore durante la lettura del frame al tempo {current_time} secondi.")
                    break

                # Salva il frame come immagine
                frame_filename = os.path.join(self.output_dir, f"frame_{frame_counter:04d}.jpg")
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_rgb)
                image.save(frame_filename)

                frame_counter += 1

                # Aggiorna la barra di progresso
                pbar.update(1)

        cap.release()
        print(f"{frame_counter} frame sono stati salvati nella cartella: {self.output_dir}")
        return self.output_dir

    def delete_frames_folder(self) -> None:
        """
        Elimina la cartella che contiene i frame estratti.
        """
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
            print(f"La cartella dei frame è stata eliminata: {self.output_dir}")
        else:
            print("La cartella dei frame non esiste.")


# Esempio di utilizzo
if __name__ == "__main__":
    extractor = FrameExtractor(r"C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\utils_no_ffmpeg\video\blue-haired-blind-girl.3840x2160.mp4")
    
    # output_dir = extractor.extract_exact_frames(num_frames=10)  # Estrae 10 frame
    output_dir = extractor.extract_frames_by_fps(target_fps=5)  # Estrae frame con un FPS di 1
    print(f"Fps: {extractor.get_fps()}")
    print(f"Frame salvati nella cartella: {output_dir}")

    # (Facoltativo) Se vuoi, puoi eliminare la cartella dopo averla usata
    # extractor.delete_frames_folder()
    
    import argparse

    # parser = argparse.ArgumentParser(description="Estrazione di un numero esatto di frame da un video.")
    # parser.add_argument("video_path", type=str, help="Percorso del video.")
    # parser.add_argument("--num_frames", type=int, default=10, help="Numero esatto di frame da estrarre (default: 10).")
    # parser.add_argument("--delete", action="store_true", help="Elimina la cartella dei frame dopo l'estrazione.")
    # args = parser.parse_args()
