import logging
import constants as _c
import pygame

class PgTitle:
    """
    Class for a button in pygame
    """
    def __init__(self, x_pos, y_pos, width, height, text, disp, 
            log=logging.getLogger(), font_height=0.2, color=_c.DEFAULT_TILE,
            text_color=_c.BUTTON_TEXT_COLOR, expand=False):
        self.log = log
        self.text = text
        self.text_color = text_color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.disp = disp
        self.width = width
        self.height = height
        self.color = color
        self.expand = expand
        self.font = pygame.font.Font('freesansbold.ttf', int(self.height*font_height))

        self.draw()

    def draw(self):
        """
        Helper method to draw the button with the unclicked color scheme and text.
        """
        # make text surface and check whether to resize button
        self.text_surf = self.font.render(self.text, True, self.text_color) 
        self.text_rect = self.text_surf.get_rect()
        if self.text_rect.width > self.width and self.expand:
            self.width = self.text_rect.width*1.2

        # draw rectangles for the button
        self.button_border = pygame.draw.rect(self.disp,  
                self.color,
                self.get_rect())

        # reposition the text
        self.text_rect.center = (int(self.width/2+self.x_pos), 
            int((self.height)/2+self.y_pos))
        self.disp.blit(self.text_surf, self.text_rect)

    def get_rect(self):
        return (self.x_pos, self.y_pos, self.width, self.height)
