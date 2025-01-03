import os
import subprocess

# Creazione della cartella ./palette se non esiste
palette_dir = './palette'
if not os.path.exists(palette_dir):
    os.makedirs(palette_dir)

# Video input (modifica con il percorso del tuo video)
video_path = r'C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\video\blue-haired-blind-girl.1920x1080.mp4'

# Parametri
fps = 10
size = {"width": 320, "height": -1}

# Lista di comandi per generare diverse palette
commands = [
    # 1. Palette standard
    [
        'ffmpeg', 
        '-i', video_path, 
        '-vf', f'fps={fps},scale={size["width"]}:{size["height"]},palettegen', 
        os.path.join(palette_dir, 'palette_standard.png')
    ],
    # 2. Palette con dithering Bayer
    [
        'ffmpeg', 
        '-i', video_path, 
        '-vf', f'fps={fps},scale={size["width"]}:{size["height"]},palettegen=stats_mode=diff', 
        os.path.join(palette_dir, 'palette_bayer.png')
    ],
    # 3. Palette con Floyd-Steinberg dithering
    [
        'ffmpeg', 
        '-i', video_path, 
        '-vf', f'fps={fps},scale={size["width"]}:{size["height"]},palettegen=stats_mode=diff', 
        os.path.join(palette_dir, 'palette_floyd_steinberg.png')
    ],
    # 4. Palette con max_colors=512
    [
        'ffmpeg', 
        '-i', video_path, 
        '-vf', f'fps={fps},scale={size["width"]}:{size["height"]},palettegen=max_colors=512', 
        os.path.join(palette_dir, 'palette_max_colors.png')
    ],
    # 5. Palette con risoluzione ridotta
    [
        'ffmpeg', 
        '-i', video_path, 
        '-vf', f'fps={fps},scale=160:-1:flags=lanczos,palettegen', 
        os.path.join(palette_dir, 'palette_low_res.png')
    ],
    # 6. Palette con risoluzione elevata
    [
        'ffmpeg', 
        '-i', video_path, 
        '-vf', f'fps={fps},scale=640:-1:flags=lanczos,palettegen', 
        os.path.join(palette_dir, 'palette_high_res.png')
    ],
    # 7. Palette con solo colori dominanti
    [
        'ffmpeg', 
        '-i', video_path, 
        '-vf', f'fps={fps},scale={size["width"]}:{size["height"]},palettegen=stats_mode=single', 
        os.path.join(palette_dir, 'palette_dominant.png')
    ],
    # 8. Palette con max_colors=128
    [
        'ffmpeg', 
        '-i', video_path, 
        '-vf', f'fps={fps},scale={size["width"]}:{size["height"]},palettegen=max_colors=128', 
        os.path.join(palette_dir, 'palette_128_colors.png')
    ],
    # 9. Palette con colori bilanciati
    [
        'ffmpeg', 
        '-i', video_path, 
        '-vf', f'fps={fps},scale={size["width"]}:{size["height"]},palettegen=stats_mode=balanced', 
        os.path.join(palette_dir, 'palette_balanced.png')
    ],
    # 10. Palette con ottimizzazione statistica
    [
        'ffmpeg', 
        '-i', video_path, 
        '-vf', f'fps={fps},scale={size["width"]}:{size["height"]},palettegen=stats_mode=diff,stats_file=stats.log', 
        os.path.join(palette_dir, 'palette_optimized.png')
    ]
]

# Esegui ogni comando
for cmd in commands:
    try:
        subprocess.run(cmd, check=True)
        print(f"Palette generata: {cmd[-1]}")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante la generazione della palette: {e}")
