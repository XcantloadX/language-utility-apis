import tempfile

from makolang.backends.common import HTTPRequest

def play_sound(request: HTTPRequest):
    def playsound(file: str):
        try:
            import playsound
            from playsound import PlaysoundException
            playsound.playsound(f.name)
        except PlaysoundException as e:
            if 'MCI' in str(e):
                print(
                    "MCI error raised. This might be a playsound issue."
                    "Try `pip install playsound==1.2.2`."
                )
            else:
                raise
    
    def pygame(file: str):
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except ImportError:
            print("pygame not found, please install it manually.")
    
    def wmplayer(file: str):
        try:
            import subprocess
            path = r'c:\Program Files\Windows Media Player\wmplayer.exe'
            p = subprocess.Popen([path, file])
            p.wait()
        except Exception as e:
            print(f"Failed to play sound using Windows Media Player: {e}")
    
    def default_player(file: str):
        try:
            import os
            os.startfile(file)
        except Exception as e:
            print(f"Failed to play sound using media player: {e}")
    
    with tempfile.NamedTemporaryFile(suffix='.mp3') as f:
        f.write(request.request().content)
        f.flush()
        libraries = [playsound, pygame, wmplayer, default_player]
        for library in libraries:
            try:
                library(f.name)
                break
            except Exception as e:
                print(f"Failed to play sound using {library.__name__}: {e}")
        else:
            print("No suitable library found to play sound.")