import pygame
import logging
import math
import constants as _c

from env import EnvObject

class MapObject():
    def __init__(self, 
            game_disp,
            log,
            width=_c.DISP_WIDTH*0.8, 
            height=_c.DISP_HEIGHT*0.6, 
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
                self.tiles[-1].append(EnvObject(x_pos = self.x_pos + _c.TILE_WIDTH * col,
                                                y_pos = self.y_pos + _c.TILE_HEIGHT * row,
                                                tile_type = _c.FLOOR
                                            )
                                      )

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
            selected_tile.set_tile_sprite(tile)
            pygame.draw.rect(self.disp, selected_tile.get_sprite(), 
                selected_tile.get_rect())

    def render(self):
        self.log.debug("about to render tiles onto board")
        for row in self.tiles:
            for tile in row:
                self.log.debug(tile.get_sprite())
                pygame.draw.rect(self.disp,
                    tile.get_sprite(),
                    tile.get_rect())