import vlc
import constants as _c

class Soundboard:
    def __init__(self):

        # currently focused index
        self.current_index = 0
        # array for sound file paths
        self.soundpath_list = [_c.MEGALOVANIA] * 20
        # array for vlc player instances
        self.vlc_player_list = [None] * 20
        # array for start/stop detection
        self.controller_list = [False] * 20

    def flip(self):
        if self.controller_list[self.current_index] is False:
            self.vlc_player_list[self.current_index] = vlc.MediaPlayer(
                self.soundpath_list[self.current_index]).play()
            self.controller_list[self.current_index] = True
        else:
            self.vlc_player_list[self.current_index] = vlc.MediaPlayer(
                self.soundpath_list[self.current_index]).stop()
            self.controller_list[self.current_index] = False

    def control(self, index_in_arr):
        self.current_index = index_in_arr
        self.flip()