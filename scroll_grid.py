import math
import pygame
import logging
import game_button
import constants as _c
from image_grid_cell import ImageCell


class ScrollGrid:
    def __init__(self, n_cols, width, height, img_list, 
            disp, x_pos, y_pos, x_pad=2, y_pad=2, scroll_width=10, 
            log=logging.getLogger(), bg_color=_c.BUTTON_COLOR, 
            border_color=_c.BORDER_COLOR, border_width=2,
            scroll_incr_percent=5):
        """
        A class to manage a group of buttons that should be spaced out into a 
        grid. All arguments provided in lists specify functionality in 
        column-major order, values of None in lists will populate a blank space
        in the corresponding position in the grid

        Args
        -----------
        n_rows: the number of rows in the grid
        n_cols: the number of columns in the grid
        width: the width of the grid object
        height: the height of the grid object
        img_list: rorw-major ordered text to place in each button
        scroll_width: width of the scroll bar in pixels
        disp: pygame display object to draw onto
        x_pos: x-coordinate of the grid's top left corner
        y_pos: y-coordinate of the grid's top left corner
        fit_to_text: boolean to shrink button width to fit text 
        x_pad: spacing between columns in pixels
        y_pad: blank spacing between rows in pixels
        log: logging module instance to write to
        scroll_incr: pixels to move with each click of the scroll bar
        NOTE: the remainder of the arguments specify the colors and borders in
              the grid. Each of the color arguments should be provided as an
              RGB tuple such as: (10, 40, 23). Border width is specified in 
              pixels.
        """
        self.tile_list = []
        img_idx = 0
        n_rows = math.ceil(len(img_list)/float(n_cols))

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.scroll_width = scroll_width
        self.cell_width = int((width - x_pad*n_cols - scroll_width)/n_cols)
        self.cell_height = self.cell_width
        self.log = log
        self.disp = disp
        self.bg_color = bg_color
        self.scrollbar_color = (100,100,100)
        self.slider_color = (80, 80, 80)

        # create the scroll bar elements
        self.canvas_height = (self.cell_height+y_pad)*n_rows
        self.min_canvas_pos = 0
        self.max_canvas_pos = (self.cell_height+y_pad)*(n_rows-1)
        self.canvas_pos = 0
        canvas_area = (self.x_pos, self.y_pos, self.width-self.scroll_width, 
            self.height)

        self.log.debug("images: {}".format(img_list))
        self.log.debug("num cells: {}".format(len(img_list)))
        self.log.debug('num rows: {}'.format(n_rows))
        self.log.debug('canvas height: {}'.format(self.canvas_height))
        self.log.debug('cell width: {}'.format(self.cell_width))

        fraction_visible = self.height / (self.canvas_height)
        if fraction_visible > 1:
            fraction_visible = 1

        self.scroll_button_height = 20
        self.slide_area_height = self.height - self.scroll_button_height*2
        self.slider_height = fraction_visible * self.slide_area_height
        self.scroll_incr = int((self.max_canvas_pos - self.min_canvas_pos) 
            * (0.01*scroll_incr_percent))
        
        self.down_button = game_button.PGButton(
                x_pos=self.x_pos+self.width-self.scroll_width,
                y_pos=self.y_pos+self.height-self.scroll_button_height,
                width=self.scroll_width,
                height=self.scroll_button_height,
                log=self.log,
                color=(96, 96, 96),
                click_color=(64, 64, 64),
                border_width=border_width,
                text='v',
                disp=self.disp,
                idx_grid=None,
                callback=self.scroll_down
            )
        
        self.up_button = game_button.PGButton(
                x_pos=self.x_pos+self.width-self.scroll_width,
                y_pos=self.y_pos,
                width=self.scroll_width,
                height=self.scroll_button_height,
                log=self.log,
                color=(96, 96, 96),
                click_color=(64, 64, 64),
                border_width=border_width,
                text='^',
                disp=self.disp,
                idx_grid=None,
                callback=self.scroll_up
            )

        # create all images
        for row in range(n_rows):
            for col in range(n_cols):
                if img_idx < len(img_list) and img_list[img_idx] is not None:
                    img_x_pos = self.x_pos + (self.cell_width+x_pad)*col + 0.5*x_pad
                    img_y_pos = self.y_pos + (self.cell_height+y_pad)*row + 0.5*y_pad
                    self.tile_list.append(ImageCell(
                        x_pos=img_x_pos,
                        y_pos=img_y_pos,
                        width=self.cell_width,
                        height=self.cell_height,
                        img_path=img_list[img_idx],
                        disp=self.disp,
                        bg_color=(255,255,255,255),
                        border_color=(255,255,255,255),
                        log=self.log,
                        draw_background_en=False,
                        canvas_area=canvas_area,
                        border_width=border_width))
                    self.tile_list[-1].resize_img(
                        width=self.cell_width, height=self.cell_height)
                    self.tile_list[-1].set_clip(self.get_rect())
                img_idx += 1
        self.draw()
        self.scroll_up() # force render
        
    def get_buttons(self):
        return [self.up_button, self.down_button]
    
    def occlude_frame(self, img):
        # case 1: image occluded by top of canvas
        if self.y_pos > img.y_pos:
            y_canvas = self.y_pos-img.y_pos
            y_canvas_height = img.height

        # case 1: image occluded by bottom of canvase
        elif (self.y_pos+self.height) < (img.y_pos+img.height):
            y_canvas = 0
            y_canvas_height =  (img.y_pos+img.height) - (self.y_pos+self.height)
            if y_canvas_height < 0:
                y_canvas_height = 0

        # case 3: image inside canvas entirely
        else:
            y_canvas = img.y_pos
            y_canvas_height = img.height

        draw_area = (0, y_canvas, img.width, y_canvas_height)
        return draw_area

    def scroll_up(self):
        prev_pos = self.canvas_pos
        if self.canvas_pos - self.scroll_incr < self.min_canvas_pos:
            self.canvas_pos = self.min_canvas_pos
        else:
            self.canvas_pos -= self.scroll_incr
        self.log.debug("canvas pos: {}, limit: {}".format(self.canvas_pos, self.min_canvas_pos))

        shift = self.canvas_pos - prev_pos

        for img in self.tile_list:
            draw_area = self.occlude_frame(img)
            img.scroll_y(shift_pixels=-1*shift, clip=self.get_rect())
        self.draw()
                
    def scroll_down(self):
        prev_pos = self.canvas_pos
        if self.canvas_pos + self.scroll_incr > self.max_canvas_pos:
            self.canvas_pos = self.max_canvas_pos
        else:
            self.canvas_pos += self.scroll_incr

        self.log.debug("canvas pos: {}, limit: {}".format(self.canvas_pos, self.max_canvas_pos))

        shift = self.canvas_pos - prev_pos

        for img in self.tile_list:
            draw_area = self.occlude_frame(img)
            img.scroll_y(shift_pixels=-1*shift,clip=self.get_rect())
        self.draw()

    def get_rect(self):
        return (self.x_pos, self.y_pos, self.width-self.scroll_width, 
            self.height)

    def check_collision(self, pos):
        for img in self.tile_list:
            if img.check_collision(pos):
                self.log.debug("user clicked on sprite with orig img: {}".format(img.orig_img_path))
                return img.orig_img_path
        return None

    def draw(self):
        # create the background and the scrollbar
        self.scroll_area = pygame.draw.rect(
                self.disp,
                self.scrollbar_color,
                (self.x_pos+self.width-self.scroll_width,
                 self.y_pos+self.scroll_button_height,
                 self.scroll_width,
                 self.slide_area_height)
            )
        slider_pos = ((self.slide_area_height-self.slider_height) * 
            (self.canvas_pos/(self.max_canvas_pos - self.min_canvas_pos)))
        self.slider = pygame.draw.rect(
                self.disp,
                self.slider_color,
                (self.x_pos+self.width-self.scroll_width,
                 self.y_pos+self.scroll_button_height+slider_pos,
                 self.scroll_width,
                 self.slider_height)
            )
        self.canvas_area = pygame.draw.rect(
                self.disp,
                self.bg_color,
                (self.x_pos, self.y_pos, self.width-self.scroll_width, self.height)
            )
        #self.up_button.draw_unclicked()
        #self.down_button.draw_unclicked()

        # draw the initial set of tiles
        for img in self.tile_list:
            img.draw()
