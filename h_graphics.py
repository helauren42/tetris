from colors import BLACK, CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, PURPLE, WHITE, tetris_to_pygame_color
from tetronimos import Tetromino,Straight, Square, LeftLShape, RightLShape, ZShape, SShape, TShape, JShape, STILL, FALLING, Falling
import pygame

# CONST GLOBAL VARIABLES
_WINDOW_HEIGHT = 800
_WINDOW_WIDTH = 400
BLOCK_LEN = 40
pygame.init()
WINDOW = pygame.display.set_mode((_WINDOW_WIDTH, _WINDOW_HEIGHT))
pygame.display.set_caption("Tetris Window")
WHITE_COLOR = tetris_to_pygame_color(WHITE)
