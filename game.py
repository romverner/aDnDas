# pypi imports
import pygame
import logging

# local imports
import env
import constants as _c
import utils

if __name__ == "__main__":
    log = utils.logging_init()

    # set up the game window and resources 
    pygame.init()
    clock = pygame.time.Clock()
    disp = pygame.display.set_mode((_c.DISP_WIDTH, _c.DISP_HEIGHT))
    pygame.display.set_caption(_c.TITLE_STR)
    disp.fill(_c.BG_COLOR)

    log.debug("env constants: {}".format(env.env_const))
    status = _c.RUNNING_STATUS

    log.info("about to start main loop")
    while status not in [_c.QUIT_STATUS, _c.CRASHED_STATUS]:
        # do things here that reflect game updates

        # event handlers
        for event in pygame.event.get():
            log.debug("handling event: {}".format(event))
            if event.type == pygame.QUIT:
                status = _c.QUIT_STATUS
                log.debug("quitting game")

            if event.type in _c.UNUSED_EVENTS:
                log.debug("captured unused event of type: {}".format(event.type))

        # wait for the next frame
        pygame.display.update()
        clock.tick(_c.FPS)

    pygame.quit()