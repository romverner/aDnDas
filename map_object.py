import pygame
import logging
import math
import constants as _c

from env import EnvObject
from image_grid_cell import ImageCell

class MapObject():
    def __init__(self, 
            game_disp,
            log,
            width=_c.DISP_WIDTH*0.8, 
            height=_c.DISP_HEIGHT*0.4, 
            x_pos=_c.DISP_WIDTH*0.1, 
            y_pos=_c.DISP_HEIGHT*0.1):
        self.width = width
        self.height = height
        self.log = log
        self.disp = game_disp
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width_in_tiles = int(width // _c.TILE_WIDTH)
        self.height_in_tiles = int(height // _c.TILE_HEIGHT)
        self.tiles = []
        for row in range(self.height_in_tiles):
            self.tiles.append([])
            for col in range(self.width_in_tiles):
                self.tiles[-1].append(ImageCell(
                    x_pos=self.x_pos + _c.TILE_WIDTH * col, 
                    y_pos=self.y_pos + _c.TILE_HEIGHT * row, 
                    width=_c.TILE_WIDTH, 
                    height=_c.TILE_HEIGHT, 
                    img_path=_c.TILE_IMAGES.get(_c.FLOOR), 
                    disp=self.disp, 
                    draw_background_en=True,
                    log=self.log,
                    border_color=_c.BORDER_COLOR,
                    border_width=1
                ))

        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile in enumerate(row):
                self.log.debug("row {}, col {} -- {}".format(row_idx, col_idx, tile))

    def get_tile_at_pos(self, pos):
        x_pos, y_pos = pos
        x_pos = x_pos - self.x_pos
        y_pos = y_pos - self.y_pos
        col_idx = math.floor(x_pos / self.width * self.width_in_tiles)
        row_idx = math.floor(y_pos / self.height * self.height_in_tiles)

        if row_idx < 0 or row_idx >= self.height_in_tiles:
            return None

        if col_idx < 0 or col_idx >= self.width_in_tiles:
            return None

        return self.tiles[row_idx][col_idx]

    def set_tile_at_position(self, pos, tile):
        selected_tile = self.get_tile_at_pos(pos)
        if selected_tile is not None:
            if 'png' in tile:
                selected_tile.set_tile_sprite(tile)
            else:
                selected_tile.set_tile_sprite(_c.TILE_IMAGES.get(tile))
            selected_tile.draw()

    def render(self):
        self.log.debug("about to render tiles onto board")
        for row in self.tiles:
            for tile in row:
                tile.draw()
