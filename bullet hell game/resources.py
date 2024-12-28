import pygame
import math
from pygame import mixer

pygame.font.init()
pygame.init()

# Window size and scalling
SCREEN_WIDTH = 432
SCREEN_HEIGHT = 500

SCALE_FACTOR = 2

SCALED_WIDTH = SCREEN_WIDTH * SCALE_FACTOR
SCALED_HEIGHT = SCREEN_HEIGHT * SCALE_FACTOR

scaled_screen = pygame.display.set_mode((SCALED_WIDTH, SCALED_HEIGHT))
pygame.display.set_caption('Game')

# Base surface (where all drawing happens)
base_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

# background menu music
mixer.music.load("assets/backgroundmusic.mp3")
mixer.music.play(-1)
mixer.music.set_volume(0.4)

# Font
MAIN_FONT = pygame.font.SysFont("arialblack", 25)
FONT_COLOR = (255, 255, 255)

# Tile sheet
cursor_image = pygame.image.load('assets/cursor.png').convert_alpha()
tile = 16

def get_cursor_image(row, col):
    x = col * tile
    y = row * tile
    cursor = cursor_image.subsurface(pygame.Rect(x, y, tile, tile))

    return cursor

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
health_bar_color = (32, 62, 86)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

