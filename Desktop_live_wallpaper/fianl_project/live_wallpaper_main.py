import os
import argparse
from file_chooser import FileChooser
from wallpaper_changer import WallpaperChanger
from video_frame_extractor import FrameExtractor
from config import ConfigManager
from start_up import aggiungi_avvio_automatico, rimuovi_avvio_automatico
import tkinter
from tkinter import messagebox

def mostra_alert(message="Questa è una notifica di esempio!"):
    # Creazione della finestra principale (non visibile)
    finestra = tkinter.Tk()
    finestra.withdraw()  # Nasconde la finestra principale
    
    # Mostra il messaggio di avviso
    messagebox.showinfo(message=message)
    
    # Chiude la finestra principale
    finestra.destroy()


def check_path_safety(path: str) -> bool:
    """Check if the path is valid and safe."""
    if not os.path.exists(path):
        print(f"The path {path} does not exist.")
        return False
    if not os.path.isdir(path) and not os.path.isfile(path):
        print(f"The path {path} is neither a file nor a directory.")
        return False
    return True

def select_path_from_args(path):
    """Choose the path based on the provided arguments."""
    if path:
        if check_path_safety(path):
            return path
    # If the path is invalid or not provided, ask for manual input
    print("Invalid or missing path. Please select a file or folder.")
    selected_path, is_video = FileChooser.choose_file_or_folder()
    if not selected_path:
        print("No file or folder selected.")
        return None
    return selected_path

def main():
    """Main function to configure and start the wallpaper change process."""
    config_manager = ConfigManager()
    video_path = "/path/to/video"
    is_video = False

    # Retrieve configuration data
    config = config_manager.get_config()

    if config.is_start_up:
        print("The program is set to start up automatically.")
        is_video = config.is_video
        video_path = config.wallpaper_path
        wallpaper_speed = config.wallpaper_velocity
    print(str(config))
    
    selected_path = select_path_from_args(video_path)

    if not selected_path:
        return

    # Determine if the path is a video
    is_video = selected_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov'))

    if is_video:
        video_path = selected_path
    else:
        selected_folder = selected_path


    if is_video:
        frame_extractor = FrameExtractor(selected_path)
        if config.is_start_up:
            input_fps = wallpaper_speed
        else: 
            input_fps = input("Video speed (1 - 20) 1 = slow, 20 = fast: ")
            if input_fps.strip() == '':
                input_fps = 5
            # Check if it's a number
            elif input_fps.isdigit():
                input_fps = int(input_fps)
            else:
                raise ValueError("The input value is not a number.")
        selected_folder = frame_extractor.extract_frames_by_time_interval(target_interval=input_fps / 10)  # 0.9

    wallpaper_changer = WallpaperChanger(selected_folder)

    # Print initial settings before entering the loop
    print("\nInitial settings and information:")
    print(f"Selected file/folder: {selected_path}")
    
    
    
    config.is_video = is_video
    config.wallpaper_path = selected_path
    config.wallpaper_velocity = input_fps
    
    print("\nStarting the wallpaper change loop...")
    print("Press Ctrl+C to stop the process.")
    print("Config state")
    print("Video: ", config.is_video)
    print("Path: ", config.wallpaper_path)
    print("Speed: ", config.wallpaper_velocity)
    print("Start up: ", config.is_start_up)
    config_manager.save_config(config_model=config)
        
    try:
        wallpaper_changer.loop_sequential(skip=1)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print("Process interrupted by the user.")
        is_start_up = input("Do you want to add the program to the startup? (y/n): ")
        if is_start_up.lower() == "y":
            aggiungi_avvio_automatico()
            config.is_start_up = True
            config_manager.save_config(config_model=config)
            print("Program added to startup.")
        else:
            rimuovi_avvio_automatico()
            config.is_start_up = False
            config_manager.save_config(config_model=config)
            print("Program removed from startup.")
        
        
        if is_video:
            frame_extractor.delete_frames_folder()
            print("Process interrupted by the user.")

if __name__ == "__main__":
    main()
