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
            draw_background_en=False,
            canvas_area=None):
        self.log = log
        self.draw_background_en=draw_background_en
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

        if self.canvas_area is not None:
            self.set_draw_area(self.canvas_area)

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
            self.set_draw_area(clip)
        self.draw()

    def set_draw_area(self, clip):
        # the top of the image is cut off (but not the whole image)
        self.canvas_area = clip
        if clip[1] >= (self.y_pos+self.border_width) and (clip[1]+clip[3]) > (self.y_pos + self.height):
            self.log.debug("cut at top")
            clip_x = 0
            clip_y = self.y_pos - clip[1] + self.border_width
            clip_width = self.width
            clip_height = self.height
            #clip_height = self.height - clip[1] + self.y_pos - self.border_width
        # the bottom of the image is cut off
        elif (clip[1]+clip[3]) > self.y_pos and (clip[1]+clip[3]) < (self.y_pos+self.height):
            self.log.debug("cut at bottom")
            clip_x = 0
            clip_y = 0
            clip_width = self.width
            clip_height = (clip[1]+clip[3]) - self.y_pos - self.border_width
        # the image is entirely outside the bounds
        elif self.y_pos >= (clip[1]+clip[3]) or (self.y_pos+self.height <= clip[1]):
            self.log.debug("entirely in bounds")
            clip_x = 0
            clip_y = 0
            clip_width = 0
            clip_height = 0
        # the image is entirely inside the bounds
        else:
            self.log.debug('entirely out of bounds')
            clip_x = 0
            clip_y = 0
            clip_width = self.width
            clip_height = self.height - self.border_width
        clip_height = max(0, clip_height)
        img_area = (clip_x, clip_y, clip_width, clip_height)
        if 'floor' in self.img_path:
            self.log.debug("image path: {}".format(self.orig_img_path))
            self.log.debug("setting new area to {}".format(img_area))
            self.log.debug("current rectangle is: {}".format(self.get_rect()))
            self.log.debug("")
        self.draw_area = img_area

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

        if self.draw_background_en:
            if self.canvas_area is None:
                border_rect = self.get_rect()
            else:
                if self.y_pos < self.canvas_area[1]:
                    border_height = self.height - (self.canvas_area[1]-self.y_pos) + 2*self.border_width
                elif self.y_pos + self.height > self.canvas_area[1] + self.canvas_area[3]:
                    border_height = self.height - ((self.y_pos + self.height) - (self.canvas_area[1] + self.canvas_area[3]))
                else:
                    border_height = self.height
                border_rect = (
                        self.x_pos,
                        max(self.y_pos, self.canvas_area[1]),
                        self.draw_area[2],
                        max(0, border_height)
                    )
            top_rect = (   
                self.x_pos+self.border_width, 
                border_rect[1]+self.border_width, 
                max(0, border_rect[2]-2*self.border_width), 
                max(0, border_rect[3]-2*self.border_width)
            )
            self.log.debug("border rect: {}".format(border_rect))
            self.log.debug('top rect: {}'.format(top_rect))
            self.log.debug("draw area: {}".format(self.draw_area))
            if border_rect[3] > 0:
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
        r = self.img.get_rect()
        r = (r[0]+self.x_pos, r[1]+self.y_pos, r[2], r[3])
        return pygame.Rect(r).collidepoint(pos)

    def __repr__(self):
        return "image of {}".format(self.orig_img_path)

    def __delete__(self):
        if self.img_path is not None:
            self.log.debug("ImageCell is removing temp file at {}"
                .format(self.img_path)
            )
            os.remove(self.img_path)
