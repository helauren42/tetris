from dataclasses import dataclass
from abc import ABC, abstractmethod
import pygame
import time
import random
from colors import BLACK, CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, PURPLE, WHITE, tetris_to_pygame_color
from tetronimos import Tetromino,Straight, Square, LeftLShape, RightLShape, ZShape, SShape, TShape, JShape
from enum import Enum
from typing import Optional
import logging

# CONST GLOBAL VARIABLES
_WINDOW_HEIGHT = 800
_WINDOW_WIDTH = 400
BLOCK_LEN = 40
pygame.init()
WINDOW = pygame.display.set_mode((_WINDOW_WIDTH, _WINDOW_HEIGHT))
pygame.display.set_caption("Tetris Window")
WHITE_COLOR = tetris_to_pygame_color(WHITE)

# GLOBAL VARIABLES
# Tetromino objects
T_STRAIGHT = Straight()
T_SQUARE = Square()
T_LEFTL = LeftLShape()
T_RIGHTL = RightLShape()
T_Z = ZShape()
T_S = SShape()
T_T = TShape()
T_J = JShape()

class Falling(Enum):
	STILL = 0
	FALLING = 1

STILL, FALLING = (Falling.STILL, Falling.FALLING)

class BaseField(ABC):
	falling : Falling = STILL
	last_move_down = 0
	piece : Optional[Tetromino] = None

	def __init__(self):
		self._width = 10
		self._height = 20
		self.field = self.createField()

	def createField(self):
		field = []
		for y in range(self._height):
			line = []
			for x in range(self._width):
				line.append((BLACK, STILL))
			field.append(line)
		return field

	def clearFallingPiece(self):
		for y in range(self._height):
			for x in range(self._width):
				if self.field[y][x][1] == FALLING:
					self.field[y][x] = (BLACK, STILL)

	def stillifyFallingPiece(self):
		for y in range(self._height):
			for x in range(self._width):
				if self.field[y][x][1] == FALLING:
					self.field[y][x] = (self.field[y][x][0], STILL)
		self.piece = None

	def addPieceToField(self):
		if(self.piece == None or self.falling == STILL):
			return
		start_x = self.piece.position["x"]
		start_y = self.piece.position["y"]
		end_x = start_x + len(self.piece.shape[0])
		end_y = start_y + len(self.piece.shape)
		for y in range(start_y, end_y):
			for x in range(start_x, end_x):
				color = self.piece.shape[y - start_y][x - start_x]
				if color != BLACK:
					self.field[y][x] = (self.piece.shape[y - start_y][x - start_x], FALLING)
					if y >= 19 or (self.field[y +1][x][0] != BLACK and self.field[y +1][x][1] == STILL):
						self.falling = STILL

		if self.falling == STILL:
			self.stillifyFallingPiece()

class PlayField(BaseField):
	def __init__(self):
		self.last_move_down = 0
		self.falling = STILL
		super().__init__()

	def getColor(self, x: int, y: int):
		return self.field[y][x]

	def resetField(self):
		self.field = self.createField()
		self.last_move_down = 0

	def moveDown(self):
		if self.falling == STILL or self.piece == None:
			return
		self.piece.moveDown()

	def printPiece(self):
		self.clearFallingPiece()
		self.addPieceToField()

	def generatePiece(self):
		self.last_move_down = time.time()
		self.falling = FALLING
		self.piece = random.choice([T_STRAIGHT, T_SQUARE, T_LEFTL, T_RIGHTL, T_Z, T_S, T_T, T_J])
		# self.piece = T_STRAIGHT
		self.piece.reset()
		self.addPieceToField()

class HandleKeys():
	keys = {}
	lastMove = {}

	def __init__(self):
		self.reset()
	
	def reset(self):
		self.keys = {
			"UP": False,
			"DOWN": False,
			"LEFT": False,
			"RIGHT": False,
		}
		self.lastMove = {
			"UP": 0,
			"DOWN": 0,
			"LEFT": 0,
			"RIGHT": 0,
		}

	def updateKeys(self, event, playField):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				self.keys["DOWN"] = True
			if event.key == pygame.K_LEFT:
				self.keys["LEFT"] = True
			if event.key == pygame.K_RIGHT:
				self.keys["RIGHT"] = True
			if event.key == pygame.K_UP:
				self.keys["UP"] = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				self.keys["DOWN"] = False
			if event.key == pygame.K_LEFT:
				self.keys["LEFT"] = False
			if event.key == pygame.K_RIGHT:
				self.keys["RIGHT"] = False
			if event.key == pygame.K_UP:
				self.keys["UP"] = False

	def makeMoves(self, playField, now):
		if playField.piece == None or playField.falling == STILL:
			return
		if self.keys["DOWN"] and now - self.lastMove["DOWN"] >= 0.1:
			playField.moveDown()
			self.lastMove["DOWN"] = now
		if self.keys["LEFT"] and now - self.lastMove["LEFT"] >= 0.1:
			playField.piece.moveLeft()
			self.lastMove["LEFT"] = now
		if self.keys["RIGHT"] and now - self.lastMove["RIGHT"] >= 0.1:
			playField.piece.moveRight()
			self.lastMove["RIGHT"] = now
		if self.keys["UP"] and now - self.lastMove["UP"] >= 0.2:
			playField.piece.rotate()
			self.lastMove["UP"] = now

def main():

	playField = PlayField()
	handleKeys = HandleKeys()
	logging.basicConfig(filename="tetris.log", level=logging.DEBUG, filemode="w")

	endGame = False
	while(not endGame):

		now = time.time()
		if playField.falling == FALLING:
			if now - playField.last_move_down >= 0.5:
				playField.moveDown()
				playField.last_move_down = now
		else:
			playField.generatePiece()

		playField.printPiece()

		handleKeys.makeMoves(playField, now)

		# register key events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				endGame = True
			# if event.type == pygame.KEYDOWN:
			if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				handleKeys.updateKeys(event, playField)

		full_screen = pygame.Rect(0, 0, _WINDOW_WIDTH, _WINDOW_HEIGHT)
		WINDOW.fill(pygame.Color(0, 0, 0), full_screen, 0)

		for y in range(0, playField._height):
			for x in range(0, playField._width):
				rect = pygame.Rect(x * BLOCK_LEN, y * BLOCK_LEN, BLOCK_LEN, BLOCK_LEN)
				block_color = tetris_to_pygame_color(playField.getColor(x, y)[0])
				pygame.draw.rect(WINDOW, (block_color), rect=rect)
				pygame.draw.rect(WINDOW, (WHITE_COLOR), rect=rect, width=1)

		time.sleep(0.016)
		pygame.display.flip()

if __name__ == "__main__":
	main()
