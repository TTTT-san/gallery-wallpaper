import os
import ctypes
import time
import winreg as reg
import cv2
from tkinter import Tk, filedialog
from PIL import Image
from tqdm import tqdm


class VideoFrameExtractor:
    """Responsabile dell'estrazione dei frame da un video"""

    def __init__(self, video_path: str):
        self.video_path = video_path
        self.frames = []

    def extract_frames(self):
        """Estrai i frame dal video e salvali in una cartella"""
        print("Estrazione dei frame in corso...")

        output_dir = os.path.splitext(self.video_path)[0] + "_frames"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Impossibile aprire il video: {self.video_path}")

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frames = []

        print(f"Il video ha {frame_count} frame a {fps} fps.")
        for frame_number in tqdm(range(frame_count), desc="Estrazione dei frame", unit="frame"):
            ret, frame = cap.read()
            if not ret:
                break

            frame_filename = os.path.join(output_dir, f"frame_{frame_number:04d}.jpg")
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            image.save(frame_filename)
            self.frames.append(frame_filename)

        cap.release()
        print(f"{len(self.frames)} frame estratti e salvati nella cartella: {output_dir}")
        return self.frames


class WallpaperSetter:
    """Responsabile del cambiamento dello sfondo"""

    def __init__(self, style: int = 2):
        self.style = style

    def set_wallpaper(self, image_path: str):
        """Imposta lo sfondo del desktop con l'immagine specificata"""
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)  # Applica lo sfondo


class FileChooser:
    """Gestisce la selezione di file o cartelle tramite il file explorer"""

    @staticmethod
    def choose_file_or_folder():
        """Permette all'utente di scegliere un file o una cartella tramite il file explorer"""
        root = Tk()
        root.withdraw()  # Nascondi la finestra principale di Tkinter

        while True:
            print("\nSeleziona una delle seguenti opzioni:")
            print("1: Carica un file video")
            print("2: Carica una cartella di immagini")
            choice = input("Inserisci il numero corrispondente: ")

            if choice == '1':
                file_path = filedialog.askopenfilename(title="Seleziona un file video", filetypes=[("Video files", "*.mp4;*.webm;*.avi")])
                if file_path:
                    print(f"File video selezionato: {file_path}")
                    return file_path
                else:
                    print("Nessun file selezionato. Riprovare.")
            elif choice == '2':
                folder_path = filedialog.askdirectory(title="Seleziona una cartella")
                if folder_path:
                    print(f"Cartella selezionata: {folder_path}")
                    return folder_path
                else:
                    print("Nessuna cartella selezionata. Riprovare.")
            else:
                print("Opzione non valida, riprovare.")


class ProgressTracker:
    """Gestisce la barra di avanzamento con tqdm"""

    @staticmethod
    def track_progress(iterable, desc="In corso", unit="item"):
        """Avvia la barra di avanzamento per un'operazione"""
        return tqdm(iterable, desc=desc, unit=unit,ncols=100)


class WallpaperChanger:
    """Classe principale che coordina il cambiamento dello sfondo"""

    def __init__(self, file_path: str, interval_ms: int = 200, skip: int = 5, style: int = 2):
        self.file_path = file_path
        self.interval_ms = interval_ms
        self.skip = skip
        self.style = style
        self.frame_extractor = VideoFrameExtractor(self.file_path) if self.is_video() else None
        self.wallpaper_setter = WallpaperSetter(style)
        self.file_chooser = FileChooser()
        self.progress_tracker = ProgressTracker()
        self.image_files = self.load_images()
        self.index = 0
        self.last_update_time = time.time()

    def is_video(self):
        """Verifica se il file selezionato è un video"""
        return self.file_path.lower().endswith(('mp4', 'webm', 'avi'))

    def load_images(self):
        """Carica le immagini dal file o estrae i frame dal video"""
        if os.path.isdir(self.file_path):
            image_files = sorted([
                f for f in os.listdir(self.file_path)
                if f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif'))
            ])
            if not image_files:
                raise ValueError("La cartella non contiene immagini valide.")
            return [os.path.join(self.file_path, f) for f in image_files]  # Percorso assoluto per ogni immagine
        elif self.is_video():
            return self.frame_extractor.extract_frames()
        else:
            raise ValueError("Tipo di file non supportato. Deve essere una cartella di immagini o un video.")

    def change_wallpaper(self):
        """Cambia lo sfondo ogni intervallo definito"""
        current_time = time.time()
        if current_time - self.last_update_time >= self.interval_ms / 1000:
            image_path = self.image_files[self.index]
            # Assicurati che il percorso dell'immagine sia assoluto
            absolute_path = os.path.abspath(image_path)
            self.wallpaper_setter.set_wallpaper(absolute_path)
            self.last_update_time = current_time
            self.index = (self.index + self.skip) % len(self.image_files)

    def run(self):
        """Esegue il loop di cambio dello sfondo"""
        print("Cambio sfondo in esecuzione...")
        try:
            while True:
                self.change_wallpaper()
                time.sleep(0.01)  # Piccola pausa per ridurre il carico CPU
        except KeyboardInterrupt:
            print("Processo interrotto dall'utente.")


def main():
    """Funzione principale per configurare e avviare il cambiamento dello sfondo"""
    file_path = FileChooser.choose_file_or_folder()

    if not file_path:
        print("Nessun file o cartella selezionato.")
        return

    interval_ms_input = input("Inserisci l'intervallo in millisecondi tra i cambiamenti (premi Invio per default 200 ms): ")
    interval_ms = int(interval_ms_input) if interval_ms_input else 200

    skip_input = input("Quante immagini saltare ogni volta? (premi Invio per default 5): ")
    skip = int(skip_input) if skip_input else 5

    wallpaper_changer = WallpaperChanger(file_path, interval_ms, skip)

    # Stampa lo stato iniziale prima di entrare nel loop
    print("\nImpostazioni e informazioni iniziali:")
    print(f"File/Cartella selezionato: {file_path}")
    print(f"Intervallo tra cambiamenti sfondo: {interval_ms} ms")
    print(f"Skip per cambiamento frame: {skip}")
    print(f"Totale frame o immagini disponibili: {len(wallpaper_changer.image_files)}")
    
    wallpaper_changer.run()


if __name__ == "__main__":
    main()
