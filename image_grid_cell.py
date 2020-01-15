import os
import random
import atexit
import shutil
import pygame
import logging
from PIL import Image
import constants as _c

class ImageCell:
    """
    Class for a button in pygame
    """
    def __init__(self, x_pos, y_pos, width, height, img_path, disp, 
            log=logging.getLogger(),
            expand=False,
            bg_color=_c.DEFAULT_SPRITE_BACKGROUND,
            border_color=_c.BORDER_COLOR,
            border_width=4,
            canvas_area=None):
        self.log = log
        self.orig_img_path = img_path
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.disp = disp
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.expand = expand
        self.highlighted = False
        self.img_path = None
        self.set_tile_sprite(img_path)
        self.draw_area = None
        self.canvas_area=canvas_area

        # make sure that the temporary files are cleaned on exit
        atexit.register(self.__delete__)

        # initial render
        self.draw(width=self.width, height=self.height) # force resize

    def hightlight(self):
        self.highlighted = True

    def dehighlight(self):
        self.highlighted = False

    def set_clip(self, rect):
        """
        set the clipping region of the drawn resources to the specified
        rectangle (in format of (x, y, width, height)).
        """
        self.draw_area = rect

    def get_clips(self):
        return self.draw_area

    def scroll_y(self, shift_pixels, clip=None):
        """
        transpose the image and boarder in the y axis in units of pixels. 
        Note that a positive argument will move the object down.
        
        By default, the surface clip will be moved with the scroll to prevent
        cropping the image.
        """
        self.y_pos += shift_pixels
        if clip is not None:
            if 'floor' in self.img_path:
                self.log.info("image path: {}".format(self.orig_img_path))
                self.log.info("setting new area to {}".format(clip))
                self.log.info("current rectangle is: {}".format(self.get_rect()))
                self.log.info("")
            self.draw_area = clip
        self.draw()

    def make_temp_path(self):
        """
        Helper to avoid conflicts in the temporary directory when multiple cells
        are referring to the same original sprite. 
        """
        img_base = os.path.splitext(os.path.basename(self.orig_img_path))[0]
        letters = list('abcdefghijklmnopqrstuvwxyz0123456789')
        random_str = ''.join([random.choice(letters) for _ in range(12)])
        tmp_path = os.path.join(
            _c.TEMP_IMAGE_DIR, 
            os.path.basename(self.orig_img_path)+random_str+'.png'
        )
        while os.path.isfile(tmp_path):
            random_str = ''.join([random.choice(letters) for _ in range(12)])
            tmp_path = os.path.join(
                _c.TEMP_IMAGE_DIR, 
                os.path.basename(self.orig_img_path)+random_str+'.png'
            )
        return tmp_path

    def resize_img(self, width, height):
        """
        helper method to resample the image provided to the specified width
        and height.This will automatically scale to account for the border
        width (the resized image will be 2*border_width smaller in each 
        dimension)
        """
        self.log.debug("resizing image at {} to {}x{}"
            .format(self.img_path, 
                width-2*self.border_width, 
                height-2*self.border_width
            )
        )
        img = Image.open(self.img_path)
        img = img.resize(
            (width-2*self.border_width,height-2*self.border_width), 
            Image.ANTIALIAS
        )
        img.save(self.img_path)
        self.img = pygame.image.load(self.img_path)

    def draw(self, x_pos=None, y_pos=None, width=None, height=None):
        """
        Helper method to draw the image at the provided position. If no
        position is given, it will remain at is previous location but will
        be rendered again. The same behavior is true with scaling if new 
        width and height values are provided
        """
        # update position if arguments are provided
        if x_pos is not None:
            self.x_pos = x_pos

        if y_pos is not None:
            self.y_pos = y_pos

        if width is not None:
            self.width = width

        if height is not None:
            self.height = height

        if width is not None or height is not None:
            self.resize_img(self.width, self.height)

        # draw rectangles for the image cell
        if self.highlighted:
            bcolor = _c.HIGHLIGHT_BORDER_COLOR
        else:
            bcolor = self.border_color

        if self.draw_area is None:
            border_rect = self.get_rect()
        else:
            border_rect = (self.x_pos, self.y_pos+self.draw_area[1],
                self.draw_area[2], self.draw_area[3])
        top_rect = (   
            self.x_pos+self.border_width, 
            border_rect[1]+self.border_width, 
            border_rect[2]-2*self.border_width, 
            border_rect[3]-2*self.border_width
        )
        self.button_border = pygame.draw.rect(
            self.disp,  
            bcolor,
            border_rect
        )
        self.button_top = pygame.draw.rect(
            self.disp,
            self.bg_color,
            top_rect
        )
        if self.canvas_area is not None:
            self.button_border.clip(self.canvas_area)
            self.button_top.clip(self.canvas_area)

        # reposition the image
        if self.draw_area is None:
            self.disp.blit(
                self.img, 
                (self.x_pos+self.border_width, self.y_pos+self.border_width)
            )
        else:
            self.disp.blit(
                self.img, 
                (self.x_pos+self.border_width, self.y_pos+self.border_width),
                self.draw_area
            )

    def set_tile_sprite(self, img_path):
        # clear any previous temp files that may exist
        self.__delete__()
        self.orig_img_path = img_path

        # error checking
        if not os.path.isfile(img_path):
            self.log.warn("missing sprite file. {} not found".format(img_path))
            self.orig_img_path = _c.MISSING_SPRITE_PATH

        # move the image to a new temp location to perform adjustments
        if not os.path.isdir(_c.TEMP_IMAGE_DIR):
            os.mkdir(_c.TEMP_IMAGE_DIR)
        self.img_path = self.make_temp_path()
        shutil.copyfile(
            self.orig_img_path, 
            self.img_path
        )
        self.resize_img(width=self.width, height=self.height)
        self.img = pygame.image.load(self.img_path)

    def get_rect(self):
        return (self.x_pos, self.y_pos, self.width, self.height)

    def check_collision(self, pos):
        return self.button_border.collidepoint(pos)

    def __repr__(self):
        return "image of {}".format(self.orig_img_path)

    def __delete__(self):
        if self.img_path is not None:
            self.log.debug("ImageCell is removing temp file at {}"
                .format(self.img_path)
            )
            os.remove(self.img_path)
