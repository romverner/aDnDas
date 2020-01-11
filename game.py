# pypi imports
import pygame
import logging

# local imports
import env
import constants as _c
import utils


class aDnDias:
    def __init__(self):
        self.log = utils.logging_init()

        # set up the game window and resources 
        pygame.init()
        self.clock = pygame.time.Clock()
        self.disp = pygame.display.set_mode((_c.DISP_WIDTH, _c.DISP_HEIGHT))
        pygame.display.set_caption(_c.TITLE_STR)
        self.disp.fill(_c.BG_COLOR)
        self.mo = env.MapObject(game_disp=self.disp, log=self.log)
        self.mo.render()

        # game status variables
        self.status = _c.RUNNING_STATUS
        self.tile_update_type = 'floor'

    def mouse_motion_handler(self, event):
        self.mo.get_tile_at_pos(event.pos).highlight()
        self.mo.render()

    def keypress_event_handler(self, event):
        self.log.debug("key was pressed")
        if event.key == pygame.K_0:
            self.tile_update_type = _c.TILE_ORDER[0]
        if event.key == pygame.K_1:
            self.tile_update_type = _c.TILE_ORDER[1]
        if event.key == pygame.K_2:
            self.tile_update_type = _c.TILE_ORDER[2]
        if event.key == pygame.K_3:
            self.tile_update_type = _c.TILE_ORDER[3]
        if event.key == pygame.K_4:
            self.tile_update_type = _c.TILE_ORDER[4]
        if event.key == pygame.K_5:
            self.tile_update_type = _c.TILE_ORDER[5]
        if event.key == pygame.K_6:
            self.tile_update_type = _c.TILE_ORDER[6]
        if event.key == pygame.K_7:
            self.tile_update_type = _c.TILE_ORDER[7]
        if event.key == pygame.K_8:
            self.tile_update_type = _c.TILE_ORDER[8]
        if event.key == pygame.K_9:
            self.tile_update_type = _c.TILE_ORDER[9]

    def run(self):
        self.log.info("about to start main loop")
        while self.status not in [_c.QUIT_STATUS, _c.CRASHED_STATUS]:
            # do things here that reflect game updates

            # event handlers
            for event in pygame.event.get():
                self.log.debug("handling event: {}".format(event))
                if event.type == pygame.QUIT:
                    self.status = _c.QUIT_STATUS
                    self.log.debug("quitting game")
                if event.type == pygame.KEYDOWN:
                    self.keypress_event_handler(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_motion_handler(event)

                    
                if event.type in _c.UNUSED_EVENTS:
                    self.log.debug("captured unused event of type: {}".format(event.type))

            # wait for the next frame
            pygame.display.update()
            self.clock.tick(_c.FPS)

        pygame.quit()


if __name__ == "__main__":
    myGame = aDnDias()
    myGame.run()