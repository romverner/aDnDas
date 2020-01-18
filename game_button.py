import logging
import constants as _c
import pygame

class PGButton:
    """
    Class for a button in pygame
    """
    def __init__(self, x_pos, y_pos, width, height, text, disp, 
            expand=False, callback=None, log=logging.getLogger(), 
            color=_c.BUTTON_COLOR,
            click_color=_c.DEPRESSED_BUTTON, border_color=_c.BORDER_COLOR,
            click_border_color=_c.DEPRESSED_BORDER, border_width=4,
            text_color=_c.BUTTON_TEXT_COLOR, font_height=0.33,
            click_text_color=_c.DEPRESSED_TEXT_COLOR):
        self.callback = callback
        self.log = log
        self.text = text
        self.text_color = text_color
        self.click_text_color = click_text_color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.disp = disp
        self.width = width
        self.height = height
        self.click_count = 0
        self.color = color
        self.click_color = click_color
        self.border_color = border_color
        self.click_border_color = click_border_color
        self.border_width = border_width
        self.button_border = None
        self.button_top = None
        self.expand = expand
        self.font = pygame.font.Font('freesansbold.ttf', int(self.height*font_height))

        self.draw_unclicked()

    def draw_unclicked(self):
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
                self.border_color,
                self.get_rect())
        self.button_top = pygame.draw.rect(self.disp,
                self.color,
                (self.x_pos, 
                    self.y_pos, 
                    self.width-self.border_width, 
                    self.height-self.border_width))

        # reposition the text
        self.text_rect.center = (int(self.width/2+self.x_pos), 
            int((self.height-self.border_width)/2+self.y_pos))
        self.disp.blit(self.text_surf, self.text_rect)

    def draw_clicked(self):
        """
        Helper method to draw the button with the depressed color scheme and text.
        """
        #make text surface and check whether to resize button
        self.text_surf = self.font.render(self.text, True, self.click_text_color) 
        self.text_rect = self.text_surf.get_rect()
        if self.text_rect.width > self.width and self.expand:
            self.width = self.text_rect.width*1.2

        # draw rectangeles for the button
        self.button_border = pygame.draw.rect(self.disp,  
                self.border_color,
                self.get_rect()
                )
        self.button_top = pygame.draw.rect(self.disp,
                self.click_color,
                (self.x_pos+self.border_width, 
                    self.y_pos+self.border_width, 
                    self.width-self.border_width, 
                    self.height-self.border_width)
                )

        # reposition the text
        self.text_rect.center = (int(self.width/2+self.x_pos), 
            int((self.height-self.border_width)/2+self.y_pos+self.border_width))
        self.disp.blit(self.text_surf, self.text_rect)


    def get_rect(self):
        return (self.x_pos, self.y_pos, self.width, self.height)

    def check_collision(self, pos):
        return self.button_border.collidepoint(pos)

    def mouse_down_event(self):
        self.draw_clicked()

    def mouse_up_event(self):
        self.click_count += 1
        self.log.debug("{} clicked ({} times)".format(self, self.click_count))
        self.draw_unclicked()
        if self.callback is not None:
            self.callback()

    def __repr__(self):
        return "{} button at {},{}".format(self.text, self.x_pos, self.y_pos)

