from abc import ABC, abstractmethod
from colors import BLACK, CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, PURPLE, WHITE
import logging
from enum import Enum

# kickbacks = [
# 	[0, 0],
# 	[1, 0],
# 	[0, 1],
# 	[1, 1],
# 	[-1, 0],
# 	[0, -1],
# 	[-1, -1],
# ]

class Falling(Enum):
	STILL = 0
	FALLING = 1
	IMMOBILE = 2


STILL, FALLING, IMMOBILE = (Falling.STILL, Falling.FALLING, Falling.IMMOBILE)

class Tetromino(ABC):
	current_rotation: int
	shape = []
	position = {}

	shapes = {}
	color = BLACK

	def __init__(self):
		self.resetPos()
		self.initShape()

	def __str__(self):
		ret = ""
		for y in range(len(self.shape)):
			for x in range(len(self.shape[y])):
				ret += str(self.shape[y][x]) + ","
			ret += "\n"
		return ret

	@abstractmethod
	def setColor():
		pass

	@abstractmethod
	def setShapes():
		pass

	@abstractmethod
	def reset():
		pass

	def resetPos(self):
		self.position["x"] = 3
		self.position["y"] = 0

	def initShape(self):
		self.current_rotation = 0
		self.shape = self.shapes[0]

	def rotate(self, field: list):
		print("rotate attempt")
		prev = self.current_rotation
		self.current_rotation += 1
		if self.current_rotation >= len(self.shapes):
			self.current_rotation = 0

		curr_shape = self.shapes[self.current_rotation]
		can_be_done = True
		start_x = self.position["x"]
		start_y = self.position["y"]

		found_first = False
		first_block_y = start_y
		last_block_y = first_block_y
		for y in range(len(curr_shape)):
			for x in range(len(curr_shape[y])):
				if curr_shape[y][x] != BLACK:
					found_first = True
					continue
			if not found_first:
				first_block_y += 1
				last_block_y = first_block_y
			else:
				last_block_y += 1

		found_first = False
		first_block_x = start_x
		last_block_x = first_block_x
		for x in range(len(curr_shape[0])):

			for y in range(len(curr_shape)):
				if curr_shape[y][x] != BLACK:
					found_first = True
					continue
			if not found_first:
				first_block_x += 1
				last_block_x = first_block_x
			else:
				last_block_x += 1

		logging.info(
			f"first_block_x: {first_block_x} last_block_x: {last_block_x} first_block_y: {first_block_y} last_block_y: {last_block_y}"
		)

		if first_block_x < 0 or last_block_x > 10 or last_block_y >= 20:
			logging.info(
				"CANT ROTATE: first_block_x: "
				+ str(first_block_x)
				+ " last_block_x: "
				+ str(last_block_x)
				+ " first_block_y: "
				+ str(first_block_y)
				+ " last_block_y: "
				+ str(last_block_y)
			)
			logging.info("curr_shape: " + str(curr_shape))
			self.current_rotation = prev
			self.shape = self.shapes[prev]
			return

		for y in range(len(curr_shape)):
			for x in range(len(curr_shape[y])):
				if (
					y + start_y < 0
					or y + start_y >= 20
					or x + start_x < 0
					or x + start_x >= 10
				):
					continue
				if (curr_shape[y][x] != BLACK) and field[y + start_y][x + start_x][0] != BLACK:
					logging.info(f"\n\ntetronimo can't be rotated: {self}")
					field_str = "\n".join(
						" ".join(str(cell[0]) for cell in row) for row in field
					)
					can_be_done = False
					break
		if can_be_done == False:
			self.current_rotation = prev
		logging.info("can be done: " + str(can_be_done))
		self.shape = self.shapes[self.current_rotation]

	def moveDown(self):
		self.position["y"] += 1

	def checkX(self):
		logging.info(f"checkX: {9 - self.position['x']}")
		if self.position["x"] < 0:
			x = 0 - self.position["x"] - 1
			return x
		else:
			return 10 - self.position["x"]

	def moveLeft(self):
		print("PIECE MOVE LEFT")
		self.position["x"] -= 1
		text = self.__str__()
		logging.info(f"shape: {text}")
		logging.info(f"position: {self.position}")
		if self.position["x"] < 0:
			x = self.checkX()
			for y in range(len(self.shape)):
				if self.shape[y][x] != BLACK:
					self.position["x"] += 1
					break

	def moveRight(self):
		print("PIECE MOVE RIGHT")
		self.position["x"] += 1
		if self.position["x"] + len(self.shape[0]) > 10:
			for y in range(len(self.shape)):
				x = self.checkX()
				if self.shape[y][x] != BLACK:
					self.position["x"] -= 1
					break

class Straight(Tetromino):
	def setColor(self):
		self.color = CYAN

	def setShapes(self):
		self.shapes = {
			0: [[BLACK, BLACK, BLACK, BLACK], [CYAN, CYAN, CYAN, CYAN]],
			1: [
				[BLACK, CYAN, BLACK, BLACK],
				[BLACK, CYAN, BLACK, BLACK],
				[BLACK, CYAN, BLACK, BLACK],
				[BLACK, CYAN, BLACK, BLACK],
			],
		}

	def reset(self):
		self.resetPos()
		self.initShape()
		self.shapes_width = {0: 3, 1: 3}

	def __init__(self):

		self.setColor()
		self.setShapes()
		self.initShape()


class Square(Tetromino):
	def setColor(self):
		self.color = YELLOW

	def setShapes(self):
		self.shapes = {0: [[YELLOW, YELLOW], [YELLOW, YELLOW]]}

	def rotate(self, field: list):
		pass

	def reset(self):
		self.resetPos()
		self.initShape()
		self.shapes_width = {0: 2}

	def __init__(self):
		self.setColor()
		self.setShapes()
		self.initShape()


class LeftLShape(Tetromino):
	def setColor(self):
		self.color = BLUE

	def setShapes(self):
		self.shapes = {
			0: [[BLUE, BLACK, BLACK], [BLUE, BLUE, BLUE]],
			1: [[BLACK, BLUE, BLUE], [BLACK, BLUE, BLACK], [BLACK, BLUE, BLACK]],
			2: [[BLUE, BLUE, BLUE], [BLACK, BLACK, BLUE]],
			3: [[BLACK, BLACK, BLUE], [BLACK, BLACK, BLUE], [BLACK, BLUE, BLUE]],
		}

	def reset(self):
		self.resetPos()
		self.initShape()
		self.shapes_width = {0: 3, 1: 3, 2: 3, 3: 3}

	def __init__(self):
		self.setColor()
		self.setShapes()
		self.initShape()


class RightLShape(Tetromino):
	def setColor(self):
		self.color = ORANGE

	def setShapes(self):
		self.shapes = {
			0: [[BLACK, BLACK, ORANGE], [ORANGE, ORANGE, ORANGE]],
			1: [
				[BLACK, ORANGE, BLACK],
				[BLACK, ORANGE, BLACK],
				[BLACK, ORANGE, ORANGE],
			],
			2: [[ORANGE, ORANGE, ORANGE], [ORANGE, BLACK, BLACK]],
			3: [
				[BLACK, ORANGE, ORANGE],
				[BLACK, BLACK, ORANGE],
				[BLACK, BLACK, ORANGE],
			],
		}

	def reset(self):
		self.resetPos()
		self.initShape()
		self.shapes_width = {0: 3, 1: 3, 2: 3, 3: 3}

	def __init__(self):
		self.setColor()
		self.setShapes()
		self.initShape()


class ZShape(Tetromino):
	def setColor(self):
		self.color = RED

	def setShapes(self):
		self.shapes = {
			0: [[RED, RED, BLACK], [BLACK, RED, RED]],
			1: [[BLACK, BLACK, RED], [BLACK, RED, RED], [BLACK, RED, BLACK]],
		}

	def reset(self):
		self.resetPos()
		self.initShape()
		self.shapes_width = {0: 3, 1: 3}

	def __init__(self):
		self.setColor()
		self.setShapes()
		self.initShape()


class SShape(Tetromino):
	def setColor(self):
		self.color = GREEN

	def setShapes(self):
		self.shapes = {
			0: [[BLACK, GREEN, GREEN], [GREEN, GREEN, BLACK]],
			1: [[BLACK, GREEN, BLACK], [BLACK, GREEN, GREEN], [BLACK, BLACK, GREEN]],
		}

	def reset(self):
		self.resetPos()
		self.initShape()
		self.shapes_width = {0: 3, 1: 3}

	def __init__(self):
		self.setColor()
		self.setShapes()
		self.initShape()


class TShape(Tetromino):
	def setColor(self):
		self.color = PURPLE

	def setShapes(self):
		self.shapes = {
			0: [[BLACK, PURPLE, BLACK], [PURPLE, PURPLE, PURPLE]],
			1: [
				[BLACK, PURPLE, BLACK],
				[BLACK, PURPLE, PURPLE],
				[BLACK, PURPLE, BLACK],
			],
			2: [[PURPLE, PURPLE, PURPLE], [BLACK, PURPLE, BLACK]],
			3: [
				[BLACK, BLACK, PURPLE],
				[BLACK, PURPLE, PURPLE],
				[BLACK, BLACK, PURPLE],
			],
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


class JShape(Tetromino):
	def setColor(self):
		self.color = BLUE

	def setShapes(self):
		self.shapes = {
			0: [[BLUE, BLACK, BLACK], [BLUE, BLUE, BLUE], [BLACK, BLACK, BLACK]],
			1: [[BLACK, BLUE, BLUE], [BLACK, BLUE, BLACK], [BLACK, BLUE, BLACK]],
			2: [[BLACK, BLACK, BLACK], [BLUE, BLUE, BLUE], [BLACK, BLACK, BLUE]],
			3: [[BLACK, BLUE, BLACK], [BLACK, BLUE, BLACK], [BLUE, BLUE, BLACK]],
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
