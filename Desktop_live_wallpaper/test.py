import os
import time
import ctypes
from ctypes import wintypes
import win32gui
import win32con
import win32api
import pythoncom
from comtypes import GUID
import comtypes.client

class UltraFastWallpaperChanger:
    def __init__(self):
        # Inizializzazione per metodo WIN32
        self.user32 = ctypes.WinDLL('user32')
        self.SystemParametersInfoW = self.user32.SystemParametersInfoW
        self.SystemParametersInfoW.argtypes = [
            wintypes.UINT,
            wintypes.UINT,
            wintypes.LPWSTR,
            wintypes.UINT
        ]
        
        # Inizializzazione per metodo COM
        try:
            # Crea il GUID per IDesktopWallpaper
            CLSID_DesktopWallpaper = GUID('{C2CF3110-460E-4fc1-B9D0-8A1C0C9CC4BD}')
            # Registra l'interfaccia COM
            pythoncom.CoInitialize()
            self.wallpaper = comtypes.client.CreateObject(
                CLSID_DesktopWallpaper,
                clsctx=comtypes.CLSCTX_LOCAL_SERVER
            )
        except Exception:
            self.wallpaper = None
            print("Metodo COM non disponibile, useremo solo WIN32")

    def change_wallpaper_win32(self, image_path):
        """Metodo veloce usando WIN32 API diretta"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File non trovato: {image_path}")

        # Imposta direttamente usando Win32
        win32gui.SystemParametersInfo(
            win32con.SPI_SETDESKWALLPAPER, 
            image_path, 
            win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
        )
        return True

    def change_wallpaper_com(self, image_path):
        """Metodo veloce usando COM"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File non trovato: {image_path}")

        if self.wallpaper:
            try:
                self.wallpaper.SetWallpaper(None, image_path)
                return True
            except Exception as e:
                print(f"Errore COM: {e}")
                return False
        return False

    def change_wallpaper_fastest(self, image_path):
        """Prova entrambi i metodi e usa il più veloce"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File non trovato: {image_path}")

        # Prova prima il metodo COM (generalmente più veloce)
        if self.wallpaper:
            try:
                start = time.perf_counter()
                self.wallpaper.SetWallpaper(None, image_path)
                end = time.perf_counter()
                print(f"Tempo COM: {(end-start)*1000:.2f}ms")
                return True
            except:
                pass

        # Fallback a WIN32 se COM fallisce
        try:
            start = time.perf_counter()
            result = self.change_wallpaper_win32(image_path)
            end = time.perf_counter()
            print(f"Tempo WIN32: {(end-start)*1000:.2f}ms")
            return result
        except Exception as e:
            print(f"Errore WIN32: {e}")
            return False

    def __del__(self):
        try:
            pythoncom.CoUninitialize()
        except:
            pass

def main():
    try:
        changer = UltraFastWallpaperChanger()
        image_path = r"C:\Users\tesha_r2hyiga\Desktop\gallery-wallpaper\blu-haired\blueee_0001.png"
        
        print("\nTestiamo entrambi i metodi separatamente:")
        
        # Test WIN32
        start = time.perf_counter()
        changer.change_wallpaper_win32(image_path)
        win32_time = time.perf_counter() - start
        print(f"Tempo metodo WIN32: {win32_time*1000:.2f}ms")
        
        time.sleep(0.1)  # Piccola pausa tra i test
        
        # Test COM
        if changer.wallpaper:
            start = time.perf_counter()
            changer.change_wallpaper_com(image_path)
            com_time = time.perf_counter() - start
            print(f"Tempo metodo COM: {com_time*1000:.2f}ms")
        
        # Usa il metodo più veloce
        print("\nCambio wallpaper usando il metodo più veloce:")
        changer.change_wallpaper_fastest(image_path)
        
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    main()