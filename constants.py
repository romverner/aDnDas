import os
import glob
import pygame

# game parameters
FPS = 60 # frame rate of the game
DISP_WIDTH = 850
DISP_HEIGHT = 1000
TILE_WIDTH = DISP_WIDTH//40
TILE_HEIGHT = TILE_WIDTH
TITLE_STR = "a-D'n'D-ias"
FRAMES_PER_DEBUG = 60

# grid spacing
NUM_GRID_ROWS = 16
NUM_GRID_COLS = 12
GRID_HEIGHT = int(DISP_HEIGHT//NUM_GRID_ROWS)
GRID_WIDTH = int(DISP_WIDTH//NUM_GRID_COLS)

# colors
BG_COLOR = (102, 102, 153)
FG_COLOR = (51, 102, 153)
FG_BORDER_COLOR = (25, 51, 76)
BUTTON_COLOR = (102, 153, 153)
DEFAULT_TILE = (204, 0, 153)
DEPRESSED_BUTTON = tuple([val*0.8 for val in BUTTON_COLOR])
BORDER_COLOR = (51, 76, 76)
DEPRESSED_BORDER = BORDER_COLOR
BUTTON_TEXT_COLOR = (190, 190, 190)
DEPRESSED_TEXT_COLOR =tuple([val*0.8 for val in BUTTON_TEXT_COLOR])
DEFAULT_SPRITE_BACKGROUND = (200, 200, 200)

# types
W_WALL = 'west_wall'
NW_WALL = 'nw_wall'
SW_WALL = 'sw_wall'
NE_WALL = 'ne_wall'
SE_WALL = 'se_wall'
E_WALL = 'east_wall'
N_WALL = 'n_wall'
S_WALL = 's_wall'
FLOOR = 'floor'
WATER = 'water'
NO_TEXTURE = 'default'
HIGHLIGHTED = 'highlighted'
TILE_IMAGES = {
    W_WALL: (51, 51, 51),
    E_WALL: (51, 51, 51),
    N_WALL: (51, 51, 51),
    S_WALL: (51, 51, 51),
    NE_WALL: (51, 51, 51),
    NW_WALL: (51, 51, 51),
    SE_WALL: (51, 51, 51),
    SW_WALL: (51, 51, 51), 
    FLOOR: (51, 153, 102),
    WATER: 'resources/images/water.jpg',
    NO_TEXTURE: DEFAULT_TILE,
    HIGHLIGHTED: (255, 255, 255)
}
TILE_ORDER = [W_WALL, E_WALL, S_WALL, N_WALL, NW_WALL,
    SW_WALL, NE_WALL, SE_WALL, FLOOR, WATER    
]

# status options for the state of the game
RUNNING_STATUS = 'running'
ERROR_STATUS = 'error'
QUIT_STATUS = 'quit game'

# sprite constants
AVAILABLE_SPRITES = glob.glob(
        os.path.join(os.path.dirname(os.path.realpath(__file__)),
            'resources', 'sprites', '*.png')
    )
MISSING_SPRITE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
            'resources', 'sprites', 'missing.png')
TEMP_IMAGE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),
            'resources', 'sprites', 'temp')

# event types
UNUSED_EVENTS = [pygame.KEYDOWN]

# music urls
MEGALOVANIA = 'https://archive.org/download/TobyFoxMegalovania/Toby%20Fox%20-%20Megalovania.mp3'

# error types
# ...


# logical constants
# ...