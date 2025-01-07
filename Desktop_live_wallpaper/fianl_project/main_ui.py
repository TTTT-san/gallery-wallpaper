import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from config import ConfigManager
from start_up import aggiungi_avvio_automatico, rimuovi_avvio_automatico
from video_frame_extractor import FrameExtractor
from wallpaper_changer import WallpaperChanger

class WallpaperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wallpaper Manager")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_config()

        self.selected_path = tk.StringVar()
        self.wallpaper_speed = tk.IntVar(value=5)
        self.is_video = tk.BooleanVar(value=False)
        self.startup_enabled = tk.BooleanVar(value=self.config.is_start_up)
        self.is_running = False

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")

        # File/Folder selection
        ttk.Label(frame, text="Select File or Folder:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.selected_path, width=40).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=self.browse_path).grid(row=0, column=2, padx=5, pady=5)

        # Radio buttons for file type
        ttk.Label(frame, text="Type:").grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(frame, text="Video", variable=self.is_video, value=True).grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(frame, text="Folder with Images", variable=self.is_video, value=False).grid(row=1, column=2, sticky="w")

        # Speed slider
        ttk.Label(frame, text="Speed (1-20):").grid(row=2, column=0, sticky="w")
        self.speed_slider = ttk.Scale(frame, from_=1, to=20, variable=self.wallpaper_speed, orient="horizontal")
        self.speed_slider.grid(row=2, column=1, columnspan=2, sticky="we", padx=5)

        # Current speed display
        self.speed_label = ttk.Label(frame, text=f"Current Speed: {self.wallpaper_speed.get()}")
        self.speed_label.grid(row=3, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        self.speed_slider.bind("<Motion>", self.update_speed_label)

        # Startup option
        ttk.Checkbutton(frame, text="Start on Boot", variable=self.startup_enabled, command=self.toggle_startup).grid(row=4, column=0, columnspan=3, sticky="w", padx=5, pady=5)

        # Status label
        self.status_label = ttk.Label(frame, text="Status: Idle")
        self.status_label.grid(row=5, column=0, columnspan=3, sticky="w", padx=5, pady=5)

        # Loading animation
        self.loading_label = ttk.Label(frame, text="", anchor="center")
        self.loading_label.grid(row=6, column=0, columnspan=3, sticky="we", padx=5, pady=5)

        # Start and Stop buttons
        self.start_button = ttk.Button(frame, text="Start", command=self.start_wallpaper_change)
        self.start_button.grid(row=7, column=0, pady=10, sticky="ew", padx=5)

        self.stop_button = ttk.Button(frame, text="Stop", command=self.stop_wallpaper_change, state="disabled")
        self.stop_button.grid(row=7, column=1, pady=10, sticky="ew", padx=5)

    def browse_path(self):
        if self.is_video.get():
            path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mkv;*.avi;*.mov")])
        else:
            path = filedialog.askdirectory()

        if path:
            self.selected_path.set(path)

    def toggle_startup(self):
        if self.startup_enabled.get():
            aggiungi_avvio_automatico()
            messagebox.showinfo("Startup Enabled", "The program will start on boot.")
        else:
            rimuovi_avvio_automatico()
            messagebox.showinfo("Startup Disabled", "The program will no longer start on boot.")

    def update_speed_label(self, event):
        self.speed_label.config(text=f"Current Speed: {int(self.wallpaper_speed.get())}")
        if self.is_running:
            self.update_wallpaper_speed()

    def start_wallpaper_change(self):
        path = self.selected_path.get()
        if not os.path.exists(path):
            messagebox.showerror("Error", "The selected path does not exist.")
            return

        self.config.wallpaper_path = path
        self.config.is_video = self.is_video.get()
        self.config.wallpaper_velocity = self.wallpaper_speed.get()
        self.config.is_start_up = self.startup_enabled.get()

        self.config_manager.save_config(config_model=self.config)

        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="Status: Running")

        if self.is_video.get():
            threading.Thread(target=self.convert_video_to_images, daemon=True).start()
        else:
            self.start_wallpaper_loop()

    def stop_wallpaper_change(self):
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Status: Stopped")
        self.loading_label.config(text="")
        messagebox.showinfo("Wallpaper Manager", "Wallpaper change process stopped.")

    def update_wallpaper_speed(self):
        self.config.wallpaper_velocity = self.wallpaper_speed.get()
        self.config_manager.save_config(config_model=self.config)
        print(f"Speed updated to: {self.wallpaper_speed.get()}")

    def convert_video_to_images(self):
        try:
            self.loading_label.config(text="Extracting frames... Please wait.")
            self.extractor = FrameExtractor(self.config.wallpaper_path)
            target_interval = self.wallpaper_speed.get() / 10

            path_folder = self.extractor.extract_frames_by_time_interval(target_interval=target_interval)
            self.config.wallpaper_path = path_folder

            self.loading_label.config(text="")
            self.status_label.config(text="Status: Conversion Complete")
            self.start_wallpaper_loop()
        except Exception as e:
            self.loading_label.config(text="")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def start_wallpaper_loop(self):
        try:
            changer = WallpaperChanger(self.config.wallpaper_path)
            self.status_label.config(text="Status: Wallpaper Loop Running")
            while True:
                changer.type_loop_sequantiol(skip=1)
                
                if self.is_running:
                    self.extractor.delete_frames_folder()
                    messagebox.showinfo("Wallpaper Manager", "Deleted frames folder.")
                    self.status_label.config(text="Status: Frames Folder Deleted")
                    
                    break
           
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during wallpaper loop: {e}")
        finally:
            self.stop_wallpaper_change()

if __name__ == "__main__":
    root = tk.Tk()
    app = WallpaperApp(root)
    root.mainloop()
