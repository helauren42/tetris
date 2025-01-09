from dataclasses import dataclass
from abc import ABC, abstractmethod
import pygame
import time
import random
from typing import Optional
import logging

from colors import BLACK, CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, PURPLE, WHITE, tetris_to_pygame_color
from tetronimos import Tetromino,Straight, Square, LeftLShape, RightLShape, ZShape, SShape, TShape, JShape, STILL, FALLING, Falling
from handleKeys import HandleKeys

# CONST GLOBAL VARIABLES
_WINDOW_HEIGHT = 800
_WINDOW_WIDTH = 400
BLOCK_LEN = 40
pygame.init()
WINDOW = pygame.display.set_mode((_WINDOW_WIDTH, _WINDOW_HEIGHT))
pygame.display.set_caption("Tetris Window")
WHITE_COLOR = tetris_to_pygame_color(WHITE)

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
		self.falling : Falling = STILL
		self.last_move_down = 0
		self.piece : Optional[Tetromino] = None
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

	def updateFallingAndField(self):
		if(self.piece == None or self.falling == STILL):
			return
		start_x = self.piece.position["x"]
		start_y = self.piece.position["y"]
		end_x = min(start_x + len(self.piece.shape[0]), 10)
		end_y = min(start_y + len(self.piece.shape), 20)
		for y in range(start_y, end_y):
			for x in range(start_x, end_x):
				color = self.piece.shape[y - start_y][x - start_x]
				if color != BLACK:
					self.field[y][x] = (self.piece.shape[y - start_y][x - start_x], FALLING)
					if y >= 19 or (self.field[y +1][x][0] != BLACK and self.field[y +1][x][1] == STILL):
						self.falling = STILL
						self.stillifyFallingPiece()
						self.still_time = time.time()
	
class PlayField(BaseField):
	def __init__(self):
		self.last_move_down = 0
		self.falling = STILL
		self.remove_y : Optional[int] = None
		super().__init__()

	def isEmpty(self):
		for y in range(self._height):
			for x in range(self._width):
				if self.field[y][x][0] != BLACK:
					return False
		print("!!!is empty")
		return True

	def getColor(self, x: int, y: int):
		return self.field[y][x]

	def resetField(self):
		self.field = self.createField()
		self.last_move_down = 0

	def canMoveDown(self):
		if self.falling == STILL:
			return False
		start_x = self.piece.position["x"]
		start_y = self.piece.position["y"]
		end_x = min(start_x + len(self.piece.shape[0]), 10)
		end_y = min(start_y + len(self.piece.shape), 20)
		for y in range(start_y, end_y):
			for x in range(start_x, end_x):
				color = self.piece.shape[y - start_y][x - start_x]
				if color != BLACK:
					if y >= 19 or (self.field[y +1][x][0] != BLACK and self.field[y +1][x][1] == STILL):
						return False
		return True

	def moveDown(self):
		if self.falling == STILL or self.piece == None or not self.canMoveDown():
			return
		self.piece.moveDown()

	def printPiece(self):
		self.clearFallingPiece()
		self.updateFallingAndField()

	def generatePiece(self):
		self.last_move_down = time.time()
		self.falling = FALLING
		self.piece = random.choice([T_STRAIGHT, T_SQUARE, T_LEFTL, T_RIGHTL, T_Z, T_S, T_T, T_J])
		self.piece.reset()
		self.updateFallingAndField()

	def levelDown(self):
		if self.remove_y == None:
			return
		for y in range(self.remove_y, 0, -1):
			self.field[y] = self.field[y -1]
		self.field[0] = [(BLACK, STILL)] * 10
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
			self.field[self.remove_y][x] = (BLACK, STILL)

	def drawField(self):
		for y in range(0, self._height):
			for x in range(0, self._width):
				rect = pygame.Rect(x * BLOCK_LEN, y * BLOCK_LEN, BLOCK_LEN, BLOCK_LEN)
				block_color = tetris_to_pygame_color(self.getColor(x, y)[0])
				pygame.draw.rect(WINDOW, (block_color), rect=rect)
				pygame.draw.rect(WINDOW, (WHITE_COLOR), rect=rect, width=1)

def resetScreen():
	full_screen = pygame.Rect(0, 0, _WINDOW_WIDTH, _WINDOW_HEIGHT)
	WINDOW.fill(pygame.Color(0, 0, 0), full_screen, 0)

def animateRemoveLine(playField: PlayField):
	playField.removeLines()
	resetScreen()
	playField.drawField()
	time.sleep(0.6)

	pygame.display.flip()

	time.sleep(0.6)

	playField.levelDown()
	resetScreen()
	playField.drawField()
	pygame.display.flip()
	
	time.sleep(0.6)

def displayGameOver(playField: PlayField):
	grey_color = pygame.Color(200, 200, 200)
	full_screen = pygame.Rect(0, 0, _WINDOW_WIDTH, _WINDOW_HEIGHT)
	WINDOW.fill(pygame.Color(0, 0, 0), full_screen, 0)
	playField.drawField()
	pygame.display.flip()
	time.sleep(0.2)

	text_surface = pygame.font.Font(None , 60).render("Game", True, grey_color)
	WINDOW.blit(text_surface, (150, 320))
	text_surface = pygame.font.Font(None , 60).render("Over", True, grey_color)
	WINDOW.blit(text_surface, (150, 380))
	pygame.display.flip()
	time.sleep(0.8)

def main():

	playField = PlayField()
	handleKeys = HandleKeys()
	logging.basicConfig(filename="tetris.log", level=logging.DEBUG, filemode="w")

	closeApp = False
	gameOver = False
	while(not closeApp):
		now = time.time()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				closeApp = True
			if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				handleKeys.updateKeys(event, playField)

		if gameOver:
			displayGameOver(playField)
			continue
		if handleKeys.makeMoves(playField, now):
			continue
		if playField.falling == STILL and playField.fullLine():
			animateRemoveLine(playField)
			continue

		if playField.falling == STILL and time.time() - playField.still_time >= 0.5:
			playField.piece = None
			playField.generatePiece()
			if not playField.canMoveDown():
				gameOver = True
		elif playField.falling == FALLING:
			if now - playField.last_move_down >= 0.5:
				playField.moveDown()
				playField.last_move_down = now

		playField.printPiece()

		resetScreen()

		playField.drawField()

		time.sleep(0.016)
		pygame.display.flip()

if __name__ == "__main__":
	main()
