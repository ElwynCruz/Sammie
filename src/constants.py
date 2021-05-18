import pygame
import os

from spritesheet import spritesheet

WIDTH, HEIGHT = 1024, 768
TILE_SIZE = 32
GRID_WIDTH, GRID_HEIGHT = WIDTH / TILE_SIZE, HEIGHT / TILE_SIZE
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SPRITESHEET_PATH = os.path.join('src', 'assets', 'Spritesheet','roguelikeChar_transparent.png')
UI_PATH = os.path.join('src', 'assets', 'Spritesheet','UIpacksheet_transparent.png')
# CHARACTER LOCATIONS
SAMMIE_DEFAULT = (0, 0, 16, 16)
SAMMIE_WIDTH, SAMMIE_HEIGHT = 32, 32
ACTOR_WIDTH, ACTOR_HEIGHT = 32, 32

INTERACT_BUTTON = (378, 108, 16, 16)
FILLER_DOODAD = (108, 0, 16, 16)
