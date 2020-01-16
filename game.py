# pypi imports
import os
import psutil
import pygame
import random
import logging
import argparse

# local imports
import env
import map_object
import constants as _c
import utils
import soundboard 
import game_button
import button_grid
import pg_title
import image_grid_cell
import scroll_grid as sg

class aDnDias:
    def __init__(self, log_level=logging.WARN):
        self.log = utils.logging_init(log_level=log_level)
        self.run_loop_debug_count = 0
        self.process = psutil.Process(os.getpid())

        # set up the game window and resources 
        pygame.init()
        self.clock = pygame.time.Clock()
        self.disp = pygame.display.set_mode((_c.DISP_WIDTH, _c.DISP_HEIGHT))
        pygame.display.set_caption(_c.TITLE_STR)
        self.buttons = []
        self.disp.fill(_c.BG_COLOR)

        # game status variables
        self.status = _c.RUNNING_STATUS
        self.tile_update_type = 'floor'
        self.mouse_clicked = False
        
        # mapping region
        self.mo = map_object.MapObject(
            x_pos=_c.GRID_WIDTH*1,
            y_pos=_c.GRID_HEIGHT*1,
            width=_c.GRID_WIDTH*10,
            height=_c.GRID_HEIGHT*5,
            game_disp=self.disp, 
            log=self.log)
        self.mo.render()
        
        # soundboard section
        self.sounds = soundboard.Soundboard()
        sb_title = pg_title.PgTitle(
            x_pos=_c.GRID_WIDTH*1, 
            y_pos=_c.GRID_HEIGHT*12, 
            width=_c.GRID_WIDTH*10, 
            height=_c.GRID_HEIGHT*1, 
            text="Soundboard",
            font_height=0.4,
            color=_c.BG_COLOR, 
            disp=self.disp, 
            log=self.log)
        soundboard_bg = button_grid.ButtonGrid(
                n_rows=2, 
                n_cols=10, 
                col_width=_c.GRID_WIDTH*1, 
                row_height=_c.GRID_HEIGHT*1,
                label_list=[
                    'Start 1', 'Stop 1', 
                    'Start 2', 'Stop 2', 
                    'Start 3', 'Stop 3', 
                    'Start 4', 'Stop 4', 
                    'Start 5', 'Stop 5', 
                    'Start 6', 'Stop 6', 
                    'Start 7', 'Stop 7', 
                    'Start 8', 'Stop 8', 
                    'Start 9', 'Stop 9', 
                    'Start 10', 'Stop 10', 
                ],
                callback_list=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], 
                disp=self.disp, 
                x_pos=_c.GRID_WIDTH*1, 
                y_pos=_c.GRID_HEIGHT*13, 
                fit_to_text=False, 
                x_pad=10, 
                y_pad=10, 
                log=self.log)
        self.buttons.extend(soundboard_bg.get_buttons())

        # token section
        token_title = pg_title.PgTitle(
            x_pos=_c.GRID_WIDTH*1, 
            y_pos=_c.GRID_HEIGHT*7, 
            width=_c.GRID_WIDTH*4, 
            height=_c.GRID_HEIGHT*1, 
            text="Token Status", 
            font_height=0.4,
            color=_c.BG_COLOR,
            disp=self.disp, 
            log=self.log)
        token_sprite = image_grid_cell.ImageCell(
            img_path=random.choice(_c.AVAILABLE_SPRITES),
            border_width=4,
            x_pos=_c.GRID_WIDTH*1, 
            y_pos=_c.GRID_HEIGHT*8, 
            width=_c.GRID_WIDTH*2, 
            height=_c.GRID_HEIGHT*2, 
            disp=self.disp, 
            log=self.log)
        token_hp = pg_title.PgTitle(
            x_pos=_c.GRID_WIDTH*1, 
            y_pos=_c.GRID_HEIGHT*10, 
            width=_c.GRID_WIDTH*2, 
            height=_c.GRID_HEIGHT*1,
            color=_c.BG_COLOR, 
            font_height=0.33,
            text="HP: #/#", 
            disp=self.disp, 
            log=self.log)
        token_bg = button_grid.ButtonGrid(
                n_rows=3, 
                n_cols=1, 
                col_width=_c.GRID_WIDTH*2, 
                row_height=_c.GRID_HEIGHT*1,
                label_list=['Set HP', 'Damage', 'Heal'],
                callback_list=[None]*3, 
                disp=self.disp, 
                x_pos=_c.GRID_WIDTH*3, 
                y_pos=_c.GRID_HEIGHT*8, 
                fit_to_text=False, 
                x_pad=10, 
                y_pad=10, 
                log=self.log)
        self.buttons.extend(token_bg.get_buttons())

        # Map Selection
        map_title = pg_title.PgTitle(
            x_pos=_c.GRID_WIDTH*6, 
            y_pos=_c.GRID_HEIGHT*7, 
            width=_c.GRID_WIDTH*3, 
            height=_c.GRID_HEIGHT*1, 
            text="Map Editor",
            font_height=0.4,
            color=_c.BG_COLOR, 
            disp=self.disp, 
            log=self.log)
        map_tile_table = sg.ScrollGrid(
            x_pos=_c.GRID_WIDTH*6, 
            y_pos=_c.GRID_HEIGHT*8, 
            width=_c.GRID_WIDTH*3, 
            height=_c.GRID_HEIGHT*3, 
            n_cols=3, 
            scroll_width=20,
            disp=self.disp, 
            img_list=_c.AVAILABLE_SPRITES+_c.AVAILABLE_TILES,
            bg_color=_c.BUTTON_TEXT_COLOR,
            log=self.log)
        self.buttons.extend(map_tile_table.get_buttons())

        # User Buttons
        user_bg = button_grid.ButtonGrid(
                n_rows=3, 
                n_cols=1, 
                col_width=_c.GRID_WIDTH*1, 
                row_height=_c.GRID_HEIGHT*1,
                label_list=['Save', 'Load', 'Quit'],
                callback_list=[self.save, self.load, self.quit], 
                disp=self.disp, 
                x_pos=_c.GRID_WIDTH*10, 
                y_pos=_c.GRID_HEIGHT*8, 
                fit_to_text=False, 
                x_pad=10, 
                y_pad=10, 
                log=self.log)
        self.buttons.extend(user_bg.get_buttons())

    def quit(self):
        self.log.info("attempting to quit game")
        self.status = _c.QUIT_STATUS

    def save(self):
        self.log.info("request to save game")
        self.log.warn("NOT YET IMPLEMENTED!")

    def load(self):
        self.log.info("request to load previous state")
        self.log.warn("NOT YET IMPLEMENTED!")

    def mouse_up_handler(self, event):
        self.mouse_clicked = False
        self.mo.set_tile_at_position(event.pos, self.tile_update_type)

        # check through all buttons being tracked, act if they are clicked
        for b in self.buttons:
            if b.check_collision(event.pos):
                b.mouse_up_event()

    def mouse_down_handler(self, event):
        self.mouse_clicked = True

        # check through all buttons being tracked, act if they are clicked
        for b in self.buttons:
            if b.check_collision(event.pos):
                b.mouse_down_event()

    def mouse_motion_clicked_handler(self, event):
        self.mo.set_tile_at_position(event.pos, self.tile_update_type)

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
        self.log.debug("tiles will update to: {}"
            .format(_c.TILE_IMAGES.get(self.tile_update_type)))

    def run(self):
        self.log.info("about to start main loop")
        while self.status not in [_c.QUIT_STATUS]:
            # event handlers
            for event in pygame.event.get():
                if not event.type == pygame.MOUSEMOTION:
                    self.log.debug("handling event: {}".format(event))
                if event.type == pygame.QUIT:
                    self.status = _c.QUIT_STATUS
                    self.log.debug("quitting game")
                if event.type == pygame.KEYDOWN:
                    self.keypress_event_handler(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_up_handler(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down_handler(event)
                if event.type == pygame.MOUSEMOTION and self.mouse_clicked:
                    self.mouse_motion_clicked_handler(event)
                    
                if event.type in _c.UNUSED_EVENTS:
                    self.log.debug("captured unused event of type: {}"
                        .format(event.type))

            # draw everything that's happened
            pygame.display.update()

            if self.run_loop_debug_count == _c.FRAMES_PER_DEBUG:
                # perform debuggin actions here
                self.run_loop_debug_count = 0
                mem_B = self.process.memory_info().rss
                mem_mB =  mem_B // (2**20)
                self.log.debug("memory usage: {} B ({} MB)".format(mem_B, mem_mB))
            else:
                self.run_loop_debug_count += 1
            
            # wait for the next frame
            self.clock.tick(_c.FPS)

        pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='store_true', default=False)
    parser.add_argument('-vvv', action='store_true', default=False)
    args = parser.parse_args()

    if args.vvv:
        log_level = logging.DEBUG
    elif args.v:
        log_level = logging.INFO
    else:
        log_level = logging.WARN
    myGame = aDnDias(log_level=log_level)
    myGame.run()