# pypi imports
import pygame
import logging

# local imports
import env
import constants as _c

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    logging.debug("env constants: {}".format(env.env_const))
    status = _c.RUNNING_STATUS

    while status not in [_c.QUIT_STATUS, _c.CRASHED_STATUS]:
        # do things here that reflect game updates

        # event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = _c.QUIT_STATUS
                logging.debug("")

        # wait for the next frame
        clock.tick(_c.FPS)