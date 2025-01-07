import cv2
import os

def generate_frames_from_video(video_path, output_folder):
    # Carica il video
    cap = cv2.VideoCapture(video_path)
    
    # Ottieni le proprietà del video
    fps_original = cap.get(cv2.CAP_PROP_FPS)  # FPS originale del video
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Numero totale di frame
    duration = frame_count / fps_original  # Durata del video in secondi
    
    # Crea la cartella di output se non esiste
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Inizializza le variabili
    frame_num = 0
    output_frame_num = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Salva ogni frame
        output_filename = os.path.join(output_folder, f"frame_{output_frame_num:04d}.jpg")
        cv2.imwrite(output_filename, frame)
        output_frame_num += 1
        
        frame_num += 1
    
    # Rilascia il video
    cap.release()
    print(f"Generato {output_frame_num} frame in {output_folder} con fps={fps_original}")

# Esegui il metodo
video_path = r"C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\video\blue-haired-blind-girl.3840x2160.mp4"  # Modifica con il percorso del video
output_folder = 'output_frames_opencv'  # Cartella di destinazione per i frame
generate_frames_from_video(video_path, output_folder)
