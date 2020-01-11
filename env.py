import pygame
import logging
import random
import math
import constants as _c


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
                                                tile_type = random.choice(list(_c.TILE_IMAGES.keys()))
                                            )
                                      )

        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile in enumerate(row):
                self.log.debug("row {}, col {} -- {}".format(row_idx, col_idx, tile))

    def get_tile_at_pos(self, pos):
        x_pos = x_pos - self.x_pos
        y_pos = y_pos - self.y_pos
        col_idx = math.floor(x_pos / self.width * self.width_in_tiles)
        row_idx = math.floor(y_pos / self.height * self.height_in_tiles)
        return self.tiles[row_idx][col_idx]

    def render(self):
        self.log.debug("about to render tiles onto board")
        for row in self.tiles:
            for tile in row:
                pygame.draw.rect(self.disp,
                    tile.get_sprite(),
                    (tile.x_pos, tile.y_pos, _c.TILE_WIDTH, _c.TILE_HEIGHT))

class EnvObject():
    def __init__(self, x_pos, y_pos, tile_type):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.tile_type = tile_type
        self.highlighted = False
        self.sprite = _c.TILE_IMAGES.get(tile_type, _c.DEFAULT_TILE)

    def do_work(self):
        self.x_pos = self.x_pos + 2

    def get_sprite(self):
        if self.highlighted:
            return _c.TILE_IMAGES.get(_c.HIGHLIGHTED)
        else:
            return self.sprite

    def highlight(self):
        self.highlighted = True

    def __repr__(self):
        return "tile {} at {},{}".format(self.tile_type, self.x_pos, self.y_pos)


if __name__ == "__main__":
    logging.info("in main of env")
    eo = EnvObject(4, 8)
    eo.do_work()