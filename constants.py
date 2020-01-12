import pygame

# game parameters
FPS = 60 # frame rate of the game
DISP_WIDTH = 800
DISP_HEIGHT = 400
TILE_WIDTH = DISP_WIDTH//40
TILE_HEIGHT = TILE_WIDTH
TITLE_STR = "a-D'n'D-ias"

# colors
BG_COLOR = (102, 102, 153)
FG_COLOR = (51, 102, 153)
BUTTON_COLOR = (102, 153, 153)
DEFAULT_TILE = (204, 0, 153)
DEPRESSED_BUTTON = tuple([val*0.8 for val in BUTTON_COLOR])
BORDER_COLOR = (51, 76, 76)
DEPRESSED_BORDER = BORDER_COLOR
BUTTON_TEXT_COLOR = (190, 190, 190)
DEPRESSED_TEXT_COLOR =tuple([val*0.8 for val in BUTTON_TEXT_COLOR])

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
CRASHED_STATUS = 'crashed'
QUIT_STATUS = 'quit game'

# event types
UNUSED_EVENTS = [pygame.KEYDOWN]

# music urls
MEGALOVANIA = 'https://archive.org/download/TobyFoxMegalovania/Toby%20Fox%20-%20Megalovania.mp3'

# error types
# ...


# logical constants
# ...