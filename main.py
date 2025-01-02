import os
from utils_ffmpeg_my.ffmpeg_video_to_webp_tqdm import VideoToWebpConverter
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from dotenv import load_dotenv

def main():
    load_dotenv()
    ffmpeg_path = os.getenv('FFMPEG_PATH')

    # Apri una finestra di esplorazione file per selezionare il video
    root = Tk()
    root.withdraw()
    video_path = askopenfilename(title="Seleziona il file video", filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    if not video_path:
        print("Nessun file video selezionato. Uscita.")
        return

    # Determina la directory di output in base alla directory del file video
    output_folder = os.path.join(os.path.dirname(video_path), "output")
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "result.webp")

    converter = VideoToWebpConverter(input_folder=os.path.dirname(video_path),
                                     output_folder=output_folder)

    selected_resolution = converter.select_resolution()
    print("Creazione animazione WebP in corso...")
    print(f"Video: {video_path}")
    print(f"Output: {output_path}")
    print(f"FFmpeg: {ffmpeg_path}")
    
    converter.create_webp_animation(video_path, output_path, fps=60, quality=100, ffmpeg_path=ffmpeg_path, size=selected_resolution)

if __name__ == "__main__":
    main()