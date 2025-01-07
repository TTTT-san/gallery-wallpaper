import random
import os
import ctypes
import time


class WallpaperChanger:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.image_files = sorted(
            [f for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif'))]
        )
        if not self.image_files:
            raise FileNotFoundError("Nessuna immagine trovata nella cartella.")
        self.num_images = len(self.image_files)

    def setFps(self,fps):
        if fps < 0:
            raise ValueError("FPS deve essere maggiore di 1")
        self.fps = fps

    @staticmethod
    def set_wallpaper(image_path):
        """
        Imposta l'immagine specificata come sfondo del desktop.
        """
        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
           # print(f"Sfondo impostato: {image_path}")
        except Exception as e:
            print(f"Errore nell'impostare lo sfondo: {e}")

    def type_loop_sequantiol(self,skip = -1):
        """
        Cambia lo sfondo in modo sequenziale, senza salti.
        """
        print("Cambiamento sequenziale dello sfondo...")
        print(f"Numero di immagini trovate: {self.num_images}")
        print("Premi CTRL+C per interrompere il loop.")
        print(f"Salto: {skip}")
        print("---")
        
        if skip == -1:
            skip =  5 if self.fps > 30 else 1 # piu alti sono gli fps piu skip è alto(piu fluido)
        index = 0
        while True:
            image_path = os.path.join(self.folder_path, self.image_files[index])
            self.set_wallpaper(image_path)
            index = (index + skip) % self.num_images
    def loop_sequential(self,skip = -1):
        """
        Cambia lo sfondo in modo sequenziale, senza salti.
        """
        print("Cambiamento sequenziale dello sfondo...")
        print(f"Numero di immagini trovate: {self.num_images}")
        print("Premi CTRL+C per interrompere il loop.")
        print(f"Salto: {skip}")
        print("---")
        
        if skip == -1:
            skip =  5 if self.fps > 30 else 1 # piu alti sono gli fps piu skip è alto(piu fluido)
        index = 0
        while True:
            image_path = os.path.join(self.folder_path, self.image_files[index])
            self.set_wallpaper(image_path)
            index = (index + skip) % self.num_images

    def _random_biased_skip(self, skip_range):
        """
        Genera un valore casuale per il salto con bias verso i valori inferiori del range.
        """
        min_skip, max_skip = skip_range
        if random.random() < 0.9:  # Bias verso i valori bassi
            return random.randint(min_skip, (min_skip + max_skip) // 2)
        else:
            return random.randint((min_skip + max_skip) // 2, max_skip)

    def loop_with_random_skips(self, skip_range=(5, 10), delay=0.1, boost_value=10, boost_probability=0.2):
        """
        Cambia lo sfondo con salti casuali e occasionali "boost".
        """
        index = 0
        while True:
            skip = boost_value if random.random() < boost_probability else self._random_biased_skip(skip_range)
            image_path = os.path.join(self.folder_path, self.image_files[index])
            self.set_wallpaper(image_path)
            time.sleep(delay)
            index = (index + skip) % self.num_images

    def loop_with_wave_skips(self, skip_range=(2, 5), delay=0.1):
        """
        Cambia lo sfondo con salti che oscillano gradualmente tra i valori minimi e massimi.
        """
        index = 0
        skip = skip_range[0]
        incrementing = True

        while True:
            if incrementing:
                skip += 1
                if skip >= skip_range[1]:
                    incrementing = False
            else:
                skip -= 1
                if skip <= skip_range[0]:
                    incrementing = True

            image_path = os.path.join(self.folder_path, self.image_files[index])
            self.set_wallpaper(image_path)
            time.sleep(delay)
            index = (index + skip) % self.num_images

    def loop_with_decrementing_skips(self, skip_range=(5, 10), delay=0.8):
        """
        Cambia lo sfondo con salti che si riducono gradualmente, poi si resetta.
        """
        index = 0
        skip = self._random_biased_skip(skip_range)
        decrementing = False

        while True:
            if decrementing:
                skip //= 2
                if skip <= skip_range[0]:
                    decrementing = False
            else:
                skip = self._random_biased_skip(skip_range)
                if skip >= (skip_range[0] + skip_range[1]) // 2:
                    decrementing = True

            image_path = os.path.join(self.folder_path, self.image_files[index])
            self.set_wallpaper(image_path)
            time.sleep(delay)
            index = (index + skip) % self.num_images


# Esempio di utilizzo
if __name__ == "__main__":
    
    folder_path = r"C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\blu-haired"  # Modificare con il percorso corretto
    changer = WallpaperChanger(folder_path)
    changer.setFps(30)
    changer.loop_with_random_skips(skip_range=(5, 20), delay=0.1)  # Usa un metodo specifico per cambiare sfondo
