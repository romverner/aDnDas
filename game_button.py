import logging
import constants as _c
import pygame

class PGButton:
    """
    Class for a button in pygame
    """
    def __init__(self, x_pos, y_pos, width, height, callback=None, text, 
            disp, log=logging.getLogger(), color=_c.BUTTON_COLOR,
            click_color=_c.DEPRESSED_BUTTON, border_color=_c.BORDER_COLOR,
            click_border_color=_c.DEPRESSED_BORDER):
        self.callback = callback
        self.log = log
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.disp = disp
        self.width = width
        self.height = height
        self.click_count = 0
        self.color = color
        self.click_color = click_color
        self.border_color = border_color

        # pygame objects
        self.button_border = pygame.draw.rect(self.disp,  
                self.border_color,
                self.get_rect())
        self.button_top = pygame.draw.rect(self.disp,
                self.color,
                (self.x_pos, self.y_pos, self.width-4, self.height-4))

    def get_rect(self):
        return (self.x_pos, self.y_pos, self.width, self.height)

    def check_collision(self, pos):
        return self.button_border.collidepoint(pos)

    def mouse_down_event(self):
        self.button_border = pygame.draw.rect(self.disp,  
                self.click_border_color,
                self.get_rect())
        self.button_top = pygame.draw.rect(self.disp,
                self.click_color,
                (self.x_pos, self.y_pos, self.width-4, self.height-4))

    def mouse_up_event(self):
        self.click_count += 1
        self.log.debug("{} clicked ({} times)".format(self, self.click_count))
        self.button_border = pygame.draw.rect(self.disp,  
                self.border_color,
                self.get_rect())
        self.button_top = pygame.draw.rect(self.disp,
                self.color,
                (self.x_pos, self.y_pos, self.width-4, self.height-4))
        if self.callback is not None:
            self.callback()

    def __repr__(self):
        return "{} button at {},{}".format(self.text, self.x_pos, self.y_pos)

