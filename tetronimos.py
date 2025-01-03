from abc import ABC, abstractmethod
from enum import Enum

class TetrisColor(Enum):
	BLACK = 0
	CYAN = 1        # I (Straight)
	BLUE = 2        # J (Left L-shape)
	ORANGE = 3      # L (Right L-shape)
	YELLOW = 4      # O (Square)
	GREEN = 5       # S (Z-shape, left)
	RED = 6         # Z (Z-shape, right)
	PURPLE = 7      # T (T-shape)

BLACK, CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, PURPLE = (
	TetrisColor.BLACK, TetrisColor.CYAN, TetrisColor.BLUE, TetrisColor.ORANGE,
	TetrisColor.YELLOW, TetrisColor.GREEN, TetrisColor.RED,
	TetrisColor.PURPLE
)

class tetromino(ABC):
	starting_pos = {}
	current_rotation : int
	width_difference : int
	shape = []
	position = {}

	shapes = {}
	color = BLACK

	@abstractmethod
	def setColor():
		pass

	@abstractmethod
	def setShapes():
		pass

	def resetPos(self):
		self.position["x"] = 4
		self.position["y"] = 0

	def __init__(self):
		self.resetPos()
		self.current_rotation = 0
		self.width_difference = 0

	def initShape(self):
		self.shape = self.shapes[0]

	def rotate(self):
		self.current_rotation += 1
		if(self.current_rotation >= len(self.shapes)):
			self.current_rotation = 0
		self.shape = self.shapes[self.current_rotation]

	def moveDown(self):
		self.position["y"] += 1

	def moveLeft(self):
		self.position["x"] -= 1

	def moveRight(self):
		self.position["x"] += 1

class Straight(tetromino):
	def setColor(self):
		self.color =  CYAN

	def setShapes(self):
		self.shapes = { 0: [[BLACK, BLACK, BLACK, BLACK],
				[CYAN, CYAN, CYAN, CYAN]],
			1: [[BLACK, CYAN, BLACK, BLACK],
					[BLACK, CYAN, BLACK, BLACK],
					[BLACK, CYAN, BLACK, BLACK],
					[BLACK, CYAN, BLACK, BLACK]]}

	def reset(self):
		self.resetPos()
		self.initShape()
		self.shapes_width = {0: 3, 1: 3}

	def __init__(self):

		self.setColor()
		self.setShapes()
		self.initShape()

class Square(tetromino):
	def setColor(self):
		self.color = YELLOW

	def setShapes(self):
		self.shapes = {
			0: [[YELLOW, YELLOW],
				[YELLOW, YELLOW]]
		}

	def rotate(self):
		pass

	def reset(self):
		self.resetPos()
		self.initShape()
		self.shapes_width = {0: 2}

	def __init__(self):
		self.setColor()
		self.setShapes()
		self.initShape()

class LeftLShape(tetromino):
	def setColor(self):
		self.color = BLUE

	def setShapes(self):
		self.shapes = {
			0: [[BLUE, BLACK, BLACK],
				[BLUE, BLUE, BLUE]],
			1: [[BLACK, BLUE, BLUE],
				[BLACK, BLUE, BLACK],
				[BLACK, BLUE, BLACK]],
			2: [[BLUE, BLUE, BLUE],
				[BLACK, BLACK, BLUE]],
			3: [[BLACK, BLACK, BLUE],
				[BLACK, BLACK, BLUE],
				[BLACK, BLUE, BLUE]]
		}

	def reset(self):
		self.resetPos()
		self.initShape()
		self.shapes_width = {0: 3, 1: 3, 2: 3, 3: 3}

	def __init__(self):
		self.setColor()
		self.setShapes()
		self.initShape()

class RightLShape(tetromino):
	def setColor(self):
		self.color = ORANGE

	def setShapes(self):
		self.shapes = {
			0: [[BLACK, BLACK, ORANGE],
				[ORANGE, ORANGE, ORANGE]],
			1: [[BLACK, ORANGE, BLACK],
				[BLACK, ORANGE, BLACK],
				[BLACK, ORANGE, ORANGE]],
			2: [[ORANGE, ORANGE, ORANGE],
				[ORANGE, BLACK, BLACK]],
			3: [[BLACK, ORANGE, ORANGE],
				[BLACK, BLACK, ORANGE],
				[BLACK, BLACK, ORANGE]]
		}

	def reset(self):
		self.resetPos()
		self.initShape()
		self.shapes_width = {0: 3, 1: 3, 2: 3, 3: 3}

	def __init__(self):
		self.setColor()
		self.setShapes()
		self.initShape()

class ZShape(tetromino):
	def setColor(self):
		self.color = RED

	def setShapes(self):
		self.shapes = {
			0: [[RED, RED, BLACK],
				[BLACK, RED, RED]],
			1: [[BLACK, BLACK, RED],
				[BLACK, RED, RED],
				[BLACK, RED, BLACK]]
		}

	def reset(self):
		self.resetPos()
		self.initShape()
		self.shapes_width = {0: 3, 1: 3}

	def __init__(self):
		self.setColor()
		self.setShapes()
		self.initShape()

class SShape(tetromino):
	def setColor(self):
		self.color = GREEN

	def setShapes(self):
		self.shapes = {
			0: [[BLACK, GREEN, GREEN],
				[GREEN, GREEN, BLACK]],
			1: [[BLACK, GREEN, BLACK],
				[BLACK, GREEN, GREEN],
				[BLACK, BLACK, GREEN]]
		}

	def reset(self):
		self.resetPos()
		self.initShape()
		self.shapes_width = {0: 3, 1: 3}

	def __init__(self):
		self.setColor()
		self.setShapes()
		self.initShape()

class TShape(tetromino):
	def setColor(self):
		self.color = PURPLE

	def setShapes(self):
		self.shapes = {
			0: [[BLACK, PURPLE, BLACK],
				[PURPLE, PURPLE, PURPLE]],
			1: [[BLACK, PURPLE, BLACK],
				[BLACK, PURPLE, PURPLE],
				[BLACK, PURPLE, BLACK]],
			2: [[PURPLE, PURPLE, PURPLE],
				[BLACK, PURPLE, BLACK]],
			3: [[BLACK, BLACK, PURPLE],
				[BLACK, PURPLE, PURPLE],
				[BLACK, BLACK, PURPLE]]
		}

	def reset(self):
		self.resetPos()
		self.initShape()
		self.shapes_width = {0: 3, 1: 3}
		self.shapes_width = {0: 3, 1: 3, 2: 3, 3: 3}

	def __init__(self):
		self.setColor()
		self.setShapes()
		self.initShape()

class JShape(tetromino):
	def setColor(self):
		self.color = BLUE

	def setShapes(self):
		self.shapes = {
			0: [[BLUE, BLACK, BLACK],
				[BLUE, BLUE, BLUE],
				[BLACK, BLACK, BLACK]],
			1: [[BLACK, BLUE, BLUE],
				[BLACK, BLUE, BLACK],
				[BLACK, BLUE, BLACK]],
			2: [[BLACK, BLACK, BLACK],
				[BLUE, BLUE, BLUE],
				[BLACK, BLACK, BLUE]],
			3: [[BLACK, BLUE, BLACK],
				[BLACK, BLUE, BLACK],
				[BLUE, BLUE, BLACK]]
		}

	def reset(self):
		self.resetPos()
		self.initShape()
		self.shapes_width = {0: 3, 1: 3}
		self.shapes_width = {0: 3, 1: 3, 2: 3, 3: 3}

	def __init__(self):
		self.setColor()
		self.setShapes()
		self.initShape()

# class TetrisGame:
# 	def __init__(self, width=10, height=20):
# 		self.width = width
# 		self.height = height
# 		self.board = [[BLACK for _ in range(width)] for _ in range(height)]
# 		self.current_piece = None
# 		self.spawn_new_piece()

# 	def spawn_new_piece(self):
# 		# Example of spawning a new piece. This can be randomized to pick a random shape.
# 		self.current_piece = Straight()

# 	def rotate_piece(self):
# 		# Rotate the current piece
# 		self.current_piece.rotate()

# 	def move_piece(self, direction):
# 		# Update the piece's position based on the direction
# 		pass

# 	def drop_piece(self):
# 		# Drop the piece to the bottom of the board
# 		pass
