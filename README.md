# Desktop Live Wallpaper

Un progetto che permette di avere l effetto live wallpaper dinamico sul desktop.

Questo progetto consente di:
1. Prendere un video in formato MP4, WEBP, o GIF e convertirlo in frame, oppure utilizzare una cartella con immagini o frame già esistenti.
2. Cambiare lo sfondo del desktop frame per frame, creando un live wallpaper dinamico.

---

## Come utilizzare il progetto

Per utilizzare il progetto, seguire i seguenti passaggi:

1. Assicurati di aver installato le dipendenze necessarie (vedi la sezione **Dipendenze**).
2. Configura i percorsi per le risorse (ad esempio, video o cartella di immagini).
3. Esegui il file principale del progetto.
4. (Facoltativo) Crea un file eseguibile utilizzando PyInstaller (vedi la sezione **Creazione di un file eseguibile**).

---

## Struttura del Progetto

La cartella principale del progetto si trova in:
```
Desktop_live_wallpaper/final_project
```

### Struttura del progetto:
```plaintext
final_project/
|-- main.py             # Script principale del progetto
|-- resources/          # Cartella contenente video, immagini o frame
|-- config/             # File di configurazione
|-- output/             # Cartella per output temporaneo
|-- README.md           # Documentazione del progetto
```

Il progetto permette di creare un file eseguibile utilizzando **PyInstaller**. Di seguito sono riportati i comandi principali:

### Installazione di PyInstaller

Per installare PyInstaller:
```bash
pip install pyinstaller
```

### Creazione di un file eseguibile

Con console attiva:
```bash
python -m PyInstaller script.py
```

Senza console attiva:
```bash
python -m PyInstaller --windowed script.py
python -m PyInstaller --noconsole script.py
```

---

## Futuri sviluppi

Riscrivere questo progetto in **C#** come applicazione WIN32 per il Microsoft Store.

### Funzionalità da aggiungere:
1. Cambiare lo sfondo in base al **tempo**.
2. Cambiare lo sfondo in base alla **posizione del mouse**.
3. Cambiare lo sfondo in base alla **posizione del mouse e al tempo**.
4. Cambiare lo sfondo in base alle **condizioni meteorologiche**.
5. Integrare una UI per configurare facilmente le impostazioni.


---

## Dipendenze

Assicurati di avere installato i requisiti necessari per il progetto.

### Installazione delle dipendenze
1. Installa le librerie richieste:
   ```bash
   pip install -r requirements.txt
   ```

2. Disinstalla la libreria **ffmpeg-python** se presente:
   ```bash
   pip uninstall ffmpeg-python
   ```

3. Installa **FFmpeg** seguendo i passaggi:
   - Scarica FFmpeg da [questa pagina](https://github.com/BtbN/FFmpeg-Builds/releases).
   - Estrai l'archivio nella directory desiderata.
   - Imposta la variabile `PATH_FFMPEG` nel file `./env`, indicando il percorso di `ffmpeg.exe`.

---

## Risorse

### Wallpaper
- [AlphaCoders](https://alphacoders.com)
- [HDQ Walls](https://hdqwalls.com)

### Live Wallpaper
- [Motion Backgrounds](https://motionbgs.com)

### Strumenti
- [EZGIF Tools](https://ezgif.com)

---

## Funzionalità Interessanti

1. Cambia sfondo dinamicamente in base a:
   - Tempo del giorno (mattino, pomeriggio, sera, notte).
   - Posizione del mouse sullo schermo.
   - Condizioni meteo in tempo reale.

2. Integrazione con API per il meteo per ottenere dati in tempo reale.

3. Animazioni fluide per transizioni di sfondo utilizzando **FFmpeg**.

---

## Note Aggiuntive

- La gestione dinamica degli sfondi può essere combinata con l'uso di video o GIF per un'esperienza più immersiva.
- Gli strumenti suggeriti possono aiutare a creare wallpaper personalizzati.

---

### Contatti
Per suggerimenti o richieste di supporto, crea una segnalazione nel repository GitHub!
