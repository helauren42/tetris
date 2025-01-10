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
	IMMOBILE,
	Falling,
)
from abc import ABC, abstractmethod
from typing import Optional
import time
import pygame
import random

# Tetromino objects
T_STRAIGHT = Straight()
T_SQUARE = Square()
T_LEFTL = LeftLShape()
T_RIGHTL = RightLShape()
T_Z = ZShape()
T_S = SShape()
T_T = TShape()
T_J = JShape()


class BaseField(ABC):

	def __init__(self):
		self._width = 10
		self._height = 20
		self.field = self.createField()
		self.falling: Falling = STILL
		self.last_move_down = 0
		self.piece: Optional[Tetromino] = None
		self.still_time = 0

	def __str__(self):
		field_str = ""
		for row in self.field:
			field_str += " ".join(str(cell[0]) for cell in row) + "\n"
		return field_str

	def createField(self):
		field = []
		for y in range(self._height):
			line = []
			for x in range(self._width):
				line.append((BLACK, IMMOBILE))
			field.append(line)
		return field

	def clearFallingPiece(self):
		for y in range(self._height):
			for x in range(self._width):
				if self.field[y][x][1] != IMMOBILE:
					self.field[y][x] = (BLACK, IMMOBILE)

	def stillifyFallingPiece(self):
		self.still_time = time.time()
		for y in range(self._height):
			for x in range(self._width):
				if self.field[y][x][1] == FALLING:
					self.field[y][x] = (self.field[y][x][0], STILL)
	
	def immobilizeFallingPiece(self):
		for y in range(self._height):
			for x in range(self._width):
				if self.field[y][x][1] != IMMOBILE:
					self.field[y][x] = (self.field[y][x][0], IMMOBILE)

	def updateFallingAndField(self):
		if self.piece == None:
			return
		already_still = self.falling == STILL
		start_x = self.piece.position["x"]
		start_y = self.piece.position["y"]
		end_x = min(start_x + len(self.piece.shape[0]), 10)
		end_y = min(start_y + len(self.piece.shape), 20)
		for y in range(start_y, end_y):
			for x in range(start_x, end_x):
				color = self.piece.shape[y - start_y][x - start_x]
				if color != BLACK:
					self.field[y][x] = (
						self.piece.shape[y - start_y][x - start_x],
						FALLING,
					)
					if y >= 19 or (
						self.field[y + 1][x][0] != BLACK
						and self.field[y + 1][x][1] != FALLING
					):
						self.falling = STILL
		if not already_still and self.falling == STILL:
			self.stillifyFallingPiece()

	def getColor(self, x: int, y: int):
		return self.field[y][x]

	# debug
	def isEmpty(self):
		for y in range(self._height):
			for x in range(self._width):
				if self.field[y][x][0] != BLACK:
					return False
		print("!!!is empty")
		return True


class PlayField(BaseField):
	def __init__(self):
		self.last_move_down = 0
		self.falling = STILL
		self.remove_y: Optional[int] = None
		super().__init__()

	def resetField(self):
		self.field = self.createField()
		self.last_move_down = 0

	def printPiece(self):
		self.clearFallingPiece()
		self.updateFallingAndField()

	def canMoveDown(self):
		if self.falling != FALLING or self.piece == None:
			return False
		start_x = self.piece.position["x"]
		start_y = self.piece.position["y"]
		end_x = min(start_x + len(self.piece.shape[0]), 10)
		end_y = min(start_y + len(self.piece.shape), 20)
		for y in range(start_y, end_y):
			for x in range(start_x, end_x):
				color = self.piece.shape[y - start_y][x - start_x]
				if color != BLACK:
					if y >= 19 or (
						self.field[y + 1][x][0] != BLACK
						and self.field[y + 1][x][1] != FALLING
					):
						return False
		return True

	def moveDown(self):
		if self.falling != FALLING or self.piece == None or not self.canMoveDown():
			return
		self.piece.moveDown()

	def levelDown(self):
		if self.remove_y == None:
			return
		for y in range(self.remove_y, 0, -1):
			self.field[y] = self.field[y - 1]
		self.field[0] = [(BLACK, IMMOBILE)] * 10
		self.remove_y = None

	def fullLine(self):
		for y in range(20):
			remove = True
			for x in range(10):
				if self.field[y][x][0] == BLACK:
					remove = False
					break
			if remove:
				self.remove_y = y
				return True
		return False

	def removeLines(self):
		if self.remove_y == None:
			return
		for x in range(10):
			self.field[self.remove_y][x] = (BLACK, IMMOBILE)

	def generatePiece(self):
		self.last_move_down = time.time()
		self.falling = FALLING
		self.piece = random.choice(
			[T_STRAIGHT, T_SQUARE, T_LEFTL, T_RIGHTL, T_Z, T_S, T_T, T_J]
		)
		self.piece.reset()
		self.printPiece()

	def makeMoves(self, handle_keys, now):
		move_delay = 0.08
		if self.piece == None:
			return
		num = random.randint(0, 99)
		if (
			handle_keys.keys["DOWN"]
			and now - handle_keys.lastMove["DOWN"] >= move_delay
		):
			if self.canMoveDown():
				self.moveDown()
				handle_keys.lastMove["DOWN"] = now
				self.last_move_down = now
		elif (
			handle_keys.keys["LEFT"]
			and now - handle_keys.lastMove["LEFT"] >= move_delay
		):
			start_x = self.piece.position["x"]
			start_y = self.piece.position["y"]
			end_x = min(start_x + len(self.piece.shape[0]), 10)
			end_y = min(start_y + len(self.piece.shape), 20)
			for y in range(start_y, end_y):
				for x in range(start_x, end_x):
					color = self.piece.shape[y - start_y][x - start_x]
					if color != BLACK:
						print("not black")
						if x > 0 and (
							self.field[y][x - 1][0] != BLACK
							and self.field[y][x - 1][1] == IMMOBILE
						):
							print(f"RET: x: {x}, color: {self.field[y][x - 1][0]}, state: {self.field[y][x - 1][1]}")
							return
			self.piece.moveLeft()
			handle_keys.lastMove["LEFT"] = now
		elif (
			handle_keys.keys["RIGHT"]
			and now - handle_keys.lastMove["RIGHT"] >= move_delay
		):
			start_x = self.piece.position["x"]
			start_y = self.piece.position["y"]
			end_x = min(start_x + len(self.piece.shape[0]), 10)
			end_y = min(start_y + len(self.piece.shape), 20)
			for y in range(start_y, end_y):
				for x in range(start_x, end_x):
					color = self.piece.shape[y - start_y][x - start_x]
					if color != BLACK:
						print("not black")
						if x < 9 and (
							self.field[y][x + 1][0] != BLACK
							and self.field[y][x + 1][1] == IMMOBILE
						):
							print(f"RET: x: {x}, color: {self.field[y][x - 1][0]}, state: {self.field[y][x - 1][1]}")
							return
			self.piece.moveRight()
			handle_keys.lastMove["RIGHT"] = now

		elif handle_keys.keys["UP"] and now - handle_keys.lastMove["UP"] >= 0.2:
			self.clearFallingPiece()
			self.piece.rotate(self.field)
			handle_keys.lastMove["UP"] = now
			
		self.printPiece()
