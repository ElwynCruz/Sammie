import pygame
import os

from spritesheet import spritesheet

WIDTH, HEIGHT = 1024, 768
TILE_SIZE = 32
GRID_WIDTH, GRID_HEIGHT = WIDTH / TILE_SIZE, HEIGHT / TILE_SIZE
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (66, 135, 245)
FILLER = (3, 252, 40)
SPRITESHEET_PATH = os.path.join('src', 'assets', 'Sammie_Draft.png')
BREATHE_SPRITESHEET = os.path.join('src', 'assets', 'Spritesheet', 'breathe64.png')
MISS_SPRITESHEET = os.path.join('src', 'assets', 'Spritesheet', 'miss64.png')
WALK_SPRITESHEET = os.path.join('src', 'assets', 'Spritesheet', 'left_walk.png')
BUBBLE = os.path.join('src', 'assets', 'Spritesheet', 'bubble-sheet.png')
GROUND = os.path.join('src', 'assets', 'ground.png')
BENEATH = os.path.join('src', 'assets', 'beneath.png')
END_TEXT = os.path.join('src', 'assets', 'task_over.png')
TIMER = os.path.join('src', 'assets', 'Spritesheet', 'timer.png')
STRESS_BAR = os.path.join('src', 'assets', 'Spritesheet', 'stressBar.png')
CLOUDS = os.path.join('src', 'assets', 'clouds.png')
BACKGROUND = os.path.join('src', 'assets', 'Spritesheet', 'background.png')
BACKGROUND_HEIGHT = 64
BACKGROUND_WIDTH = 64
# CHARACTER LOCATIONS
SAMMIE_DEFAULT = (0, 0, 64, 64)
SAMMIE_WIDTH, SAMMIE_HEIGHT = 64, 64
ACTOR_WIDTH, ACTOR_HEIGHT = 32, 32

INTERACT_BUTTON = (378, 108, 16, 16)
FILLER_DOODAD = (108, 0, 16, 16)

# LAYER SETTINGS
BACKGROUND_LAYER = 0
TERRAIN_LAYER = 1
PLAYER_LAYER = 2
