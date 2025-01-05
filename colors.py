from enum import Enum
import pygame

class TetrisColor(Enum):
	BLACK = 0
	CYAN = 1        # I (Straight)
	BLUE = 2        # J (Left L-shape)
	ORANGE = 3      # L (Right L-shape)
	YELLOW = 4      # O (Square)
	GREEN = 5       # S (Z-shape, left)
	RED = 6         # Z (Z-shape, right)
	PURPLE = 7      # T (T-shape)
	WHITE = 8

	def __str__(self):
		return self.name.capitalize()

BLACK, CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, PURPLE, WHITE = (
	TetrisColor.BLACK, TetrisColor.CYAN, TetrisColor.BLUE, TetrisColor.ORANGE,
	TetrisColor.YELLOW, TetrisColor.GREEN, TetrisColor.RED,
	TetrisColor.PURPLE, TetrisColor.WHITE
)

# RGB converter function
def tetris_to_pygame_color(color):
	"""
	Converts a TetrisColor enum value to its corresponding RGB tuple.
	"""
	rgb_map = {
		TetrisColor.BLACK: (0, 0, 0),
		TetrisColor.CYAN: (0, 255, 255),
		TetrisColor.BLUE: (0, 0, 255),
		TetrisColor.ORANGE: (255, 165, 0),
		TetrisColor.YELLOW: (255, 255, 0),
		TetrisColor.GREEN: (0, 255, 0),
		TetrisColor.RED: (255, 0, 0),
		TetrisColor.PURPLE: (128, 0, 128),
		TetrisColor.WHITE: (255, 255, 255),
	}
	tup = rgb_map[color]
	return pygame.Color(tup[0], tup[1], tup[2])

def box_outter_color_rgb(color):
	if color is BLACK:
		return (255, 255, 255)
	return (0, 0, 0)
