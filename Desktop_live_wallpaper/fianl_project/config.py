import json
import os

class ConfigModel:
    def __init__(self, wallpaper_path="/path/to/default/wallpaper", is_video=False, wallpaper_velocity=10, is_start_up=False):
        self.wallpaper_path = wallpaper_path
        self.is_video = is_video
        self.wallpaper_velocity = wallpaper_velocity
        self.is_start_up = is_start_up

    def to_dict(self):
        """Converte l'oggetto in un dizionario per la serializzazione JSON."""
        return {
            "wallpaper_path": self.wallpaper_path,
            "is_video": self.is_video,
            "wallpaper_velocity": self.wallpaper_velocity,
            "start_up": self.is_start_up
        }

    @staticmethod
    def from_dict(data):
        """Crea un oggetto ConfigModel da un dizionario (deserializzazione)."""
        return ConfigModel(
            wallpaper_path=data.get("wallpaper_path", "/path/to/default/wallpaper"),
            is_video=data.get("is_video", False),
            wallpaper_velocity=data.get("wallpaper_velocity", 10),
            is_start_up=data.get("start_up", False)
        )

class ConfigManager:
    def __init__(self, config_file_path="config.json"):
        self.config_file_path = config_file_path
        self.config_data = self.load_or_create_config()

    def load_or_create_config(self):
        """Carica o crea il file di configurazione."""
        default_config = ConfigModel()  # Usa i valori di default definiti nella classe modello
        
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, "r") as f:
                data = json.load(f)
            print("Config caricato con successo.")
            return ConfigModel.from_dict(data)  # Deserializza i dati in un oggetto ConfigModel
        else:
            print("File di configurazione non trovato. Creando un nuovo file con i valori di default.")
            self.save_config(default_config)  # Salva il file con i valori di default
            return default_config

    def save_config(self, config_model):
        """Salva i dati nel file di configurazione."""
        with open(self.config_file_path, "w") as f:
            json.dump(config_model.to_dict(), f, indent=4)  # Serializza l'oggetto in un dizionario
        print("Config salvato con successo.")

    def get_config(self):
        return self.config_data

    def update_config(self, key, value):
        """Modifica un parametro nel config."""
        if hasattr(self.config_data, key):
            setattr(self.config_data, key, value)
            self.save_config(self.config_data)  # Salva il file aggiornato
            print(f"Configurazione aggiornata: {key} = {value}")


if __name__ == "__main__":
    # Esempio di utilizzo della classe
    config_manager = ConfigManager()

    # Recupera i dati del config
    config = config_manager.get_config()

    # Modifica alcuni valori
    config.wallpaper_path = "/path/to/updated/wallpaper"
    config.is_video = True
    config.wallpaper_velocity = 30  # nuova velocità
    config.is_start_up = True

    # Salva il config modificato
    config_manager.save_config(config)

    # Stampa il config aggiornato
    print(config.to_dict())
