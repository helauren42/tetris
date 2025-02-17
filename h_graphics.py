from colors import (
	BLACK,
	CYAN,
	BLUE,
	ORANGE,
	YELLOW,
	GREEN,
	RED,
	PURPLE,
	WHITE,
	tetris_to_pygame_color,
)
from tetronimos import (
	Tetromino,
	Straight,
	Square,
	LeftLShape,
	RightLShape,
	ZShape,
	SShape,
	TShape,
	JShape,
	STILL,
	FALLING,
	Falling,
)
import pygame

from field import PlayField

# CONST GLOBAL VARIABLES
_WINDOW_HEIGHT = 800
_WINDOW_WIDTH = 400
BLOCK_LEN = 40
pygame.init()
WINDOW = pygame.display.set_mode((_WINDOW_WIDTH, _WINDOW_HEIGHT))
pygame.display.set_caption("Tetris Window")
WHITE_COLOR = tetris_to_pygame_color(WHITE)


def drawField(playField: PlayField):
	for y in range(0, playField._height):
		for x in range(0, playField._width):
			rect = pygame.Rect(x * BLOCK_LEN, y * BLOCK_LEN, BLOCK_LEN, BLOCK_LEN)
			block_color = tetris_to_pygame_color(playField.getColor(x, y)[0])
			pygame.draw.rect(WINDOW, (block_color), rect=rect)
			pygame.draw.rect(WINDOW, (WHITE_COLOR), rect=rect, width=1)
