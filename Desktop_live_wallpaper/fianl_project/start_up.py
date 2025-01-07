import os
import sys

def aggiungi_avvio_automatico():
    """Crea un file batch per avviare automaticamente lo script all'avvio di Windows."""
    # Ottieni il percorso della cartella "Startup"
    startup_folder = os.path.join(os.getenv('APPDATA'), r"Microsoft\Windows\Start Menu\Programs\Startup")
    
    # Ottieni il percorso del file Python corrente
    percorso_script = os.path.abspath(sys.argv[0])  # Percorso del file attuale
    nome_batch = os.path.splitext(os.path.basename(percorso_script))[0] + ".bat"  # Nome del file batch
    
    # Percorso del file batch che verrà creato
    percorso_batch = os.path.join(startup_folder, nome_batch)
    
    # Contenuto del file batch
    contenuto_batch = f'@echo off\n py "{percorso_script}"\n'
    
    # Creazione del file batch nella cartella Startup
    with open(percorso_batch, 'w') as batch_file:
        batch_file.write(contenuto_batch)
    
    print(f"File batch creato nella cartella Startup: {percorso_batch}")
    print("Questo script verrà eseguito automaticamente all'avvio di Windows.")

def rimuovi_avvio_automatico():
    """Rimuove il file batch per disabilitare l'avvio automatico dello script."""
    # Ottieni il percorso della cartella "Startup"
    startup_folder = os.path.join(os.getenv('APPDATA'), r"Microsoft\Windows\Start Menu\Programs\Startup")
    
    # Ottieni il nome del file batch corrispondente
    percorso_script = os.path.abspath(sys.argv[0])  # Percorso del file attuale
    nome_batch = os.path.splitext(os.path.basename(percorso_script))[0] + ".bat"  # Nome del file batch
    
    # Percorso del file batch
    percorso_batch = os.path.join(startup_folder, nome_batch)
    
    # Verifica ed elimina il file batch
    if os.path.exists(percorso_batch):
        os.remove(percorso_batch)
        print(f"File batch rimosso: {percorso_batch}")
        print("Avvio automatico dello script disabilitato.")
    else:
        print(f"Nessun file batch trovato in: {percorso_batch}")
        print("L'avvio automatico non era abilitato.")

# Esempio di utilizzo
if __name__ == "__main__":
    scelta = input("Vuoi abilitare o disabilitare l'avvio automatico? (abilita/disabilita): ").strip().lower()
    if scelta == "abilita":
        aggiungi_avvio_automatico()
    elif scelta == "disabilita":
        rimuovi_avvio_automatico()
    else:
        print("Scelta non valida. Usa 'abilita' o 'disabilita'.")
