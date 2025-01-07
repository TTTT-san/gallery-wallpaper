from tkinter import Tk, filedialog


class FileChooser:
    """Gestisce la selezione di file o cartelle tramite il file explorer."""

    @staticmethod
    def _print_menu():
        """Stampa il menu per la selezione delle opzioni."""
        print("\nSeleziona una delle seguenti opzioni:")
        print("1: Carica un file video (es. .mp4, .webm, .avi)")
        print("2: Carica una cartella di immagini")
        print("0: Esci")

    @staticmethod
    def _validate_choice(choice):
        """Verifica che la scelta dell'utente sia valida."""
        return choice in {"0", "1", "2"}

    @staticmethod
    def choose_file_or_folder():
        """
        Permette all'utente di scegliere un file o una cartella tramite il file explorer.
        
        :return: Percorso del file o della cartella selezionata.
        """
        root = Tk()
        root.withdraw()  # Nasconde la finestra principale di Tkinter
        root.update_idletasks()

        while True:
            FileChooser._print_menu()
            choice = input("Inserisci il numero corrispondente: ").strip()

            if not FileChooser._validate_choice(choice):
                print("Opzione non valida, riprovare.")
                continue

            if choice == "0":
                print("Uscita dal programma.")
                break

            if choice == "1":
                file_path = filedialog.askopenfilename(
                    title="Seleziona un file video",
                    filetypes=[("Video files", "*.mp4;*.webm;*.avi")]
                )
                if file_path:
                    print(f"File video selezionato: {file_path}")
                    return file_path,True
                else:
                    print("Nessun file selezionato. Riprovare.")
            elif choice == "2":
                folder_path = filedialog.askdirectory(title="Seleziona una cartella")
                if folder_path:
                    print(f"Cartella selezionata: {folder_path}")
                    return folder_path,False
                else:
                    print("Nessuna cartella selezionata. Riprovare.")

        root.destroy()  # Chiude correttamente la finestra di Tkinter
        return None


# Esempio di utilizzo
if __name__ == "__main__":
    chooser = FileChooser()
    selected_path = chooser.choose_file_or_folder()
    if selected_path:
        print(f"Percorso selezionato: {selected_path}")
    else:
        print("Nessun percorso selezionato.")
