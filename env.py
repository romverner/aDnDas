import logging
import constants as _c

class EnvObject():
    def __init__(self, x_pos, y_pos, tile_type):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.tile_type = tile_type
        self.highlighted = False
        self.sprite = _c.TILE_IMAGES.get(tile_type, _c.DEFAULT_TILE)

    def get_sprite(self):
        if self.highlighted:
            return _c.TILE_IMAGES.get(_c.HIGHLIGHTED)
        else:
            return self.sprite

    def highlight(self):
        self.highlighted = True

    def get_rect(self):
        return self.x_pos, self.y_pos, _c.TILE_WIDTH, _c.TILE_HEIGHT

    def set_tile_sprite(self, tile):
        self.sprite = _c.TILE_IMAGES.get(tile, _c.DEFAULT_TILE)

    def __repr__(self):
        return "tile {} at {},{}".format(self.tile_type, self.x_pos, self.y_pos)