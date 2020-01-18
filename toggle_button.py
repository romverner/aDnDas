import logging
import constants as _c
import pygame
import game_button

class ToggleButton(game_button.PGButton):
    def __init__(self, *args, **kwargs):
        game_button.PGButton.__init__(self, *args, **kwargs)
        self.clicked = False

    def mouse_down_event(self):
        pass

    def mouse_up_event(self):
        self.click_count += 1
        self.log.debug("{} clicked ({} times)".format(self, self.click_count))
        if self.clicked:
            self.draw_unclicked()
            self.clicked = False
        else:
            self.draw_clicked()
            self.clicked = True
        if self.callback is not None:
            self.callback()