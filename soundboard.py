import vlc
import logging
import constants as _c

class Soundboard:
    def __init__(self, log=logging.getLogger()):
        self.log = log
        # currently focused index
        self.current_index = 0
        # array for sound file paths
        self.soundpath_list = [_c.MEGALOVANIA] * 20
        # array for vlc player instances
        self.vlc_player_list = [None] * 20
        # array for start/stop detection
        self.controller_list = [False] * 20

    def flip(self, index_in_arr):
        if self.controller_list[index_in_arr] is False:
            self.log.debug("starting on index {}".format(index_in_arr))
            self.vlc_player_list[index_in_arr] = vlc.MediaPlayer(
                self.soundpath_list[index_in_arr])
            self.vlc_player_list[index_in_arr].play()
            self.controller_list[index_in_arr] = True
        else:            
            self.log.debug("stopping on index {}".format(index_in_arr))
            self.vlc_player_list[index_in_arr].stop()
            self.controller_list[index_in_arr] = False

    def control(self, index_in_arr):
        self.log.debug("index: {}".format(index_in_arr))
        self.flip(index_in_arr)