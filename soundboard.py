import vlc
import constants as _c

class Soundboard:
    def __init__(self):
        self.megalovania = vlc.MediaPlayer(_c.MEGALOVANIA)

    def play_megalovania(self):
        self.megalovania.play()

    def stop_megalovania(self):
        self.megalovania.stop()