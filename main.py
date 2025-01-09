from dataclasses import dataclass
from abc import ABC, abstractmethod
import pygame
import time
import random
from colors import BLACK, CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, PURPLE, WHITE, tetris_to_pygame_color
from tetronimos import Tetromino,Straight, Square, LeftLShape, RightLShape, ZShape, SShape, TShape, JShape, STILL, FALLING, Falling
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

class BaseField(ABC):
	falling : Falling = STILL
	last_move_down = 0
	piece : Optional[Tetromino] = None

	def __init__(self):
		self._width = 10
		self._height = 20
		self.field = self.createField()

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
		self.piece = None

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

		if self.falling == STILL:
			self.stillifyFallingPiece()

class PlayField(BaseField):
	def __init__(self):
		self.last_move_down = 0
		self.falling = STILL
		self.remove_y : Optional[int] = None
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
		self.updateFallingAndField()

	def generatePiece(self):
		self.last_move_down = time.time()
		self.falling = FALLING
		self.piece = random.choice([T_STRAIGHT, T_SQUARE, T_LEFTL, T_RIGHTL, T_Z, T_S, T_T, T_J])
		# self.piece = T_STRAIGHT
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
		# self.levelDown()

	def drawField(self):
		for y in range(0, self._height):
			for x in range(0, self._width):
				rect = pygame.Rect(x * BLOCK_LEN, y * BLOCK_LEN, BLOCK_LEN, BLOCK_LEN)
				block_color = tetris_to_pygame_color(self.getColor(x, y)[0])
				pygame.draw.rect(WINDOW, (block_color), rect=rect)
				pygame.draw.rect(WINDOW, (WHITE_COLOR), rect=rect, width=1)

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
		
	def canMoveDown(self, playField):
		if playField.falling == STILL:
			return False
		start_x = playField.piece.position["x"]
		start_y = playField.piece.position["y"]
		end_x = min(start_x + len(playField.piece.shape[0]), 10)
		end_y = min(start_y + len(playField.piece.shape), 20)
		for y in range(start_y, end_y):
			for x in range(start_x, end_x):
				color = playField.piece.shape[y - start_y][x - start_x]
				if color != BLACK:
					if y >= 19 or (playField.field[y +1][x][0] != BLACK and playField.field[y +1][x][1] == STILL):
						return False
		return True

	def makeMoves(self, playField, now):
		playField.updateFallingAndField()
		if playField.piece == None or playField.falling == STILL:
			return
		if self.keys["DOWN"] and now - self.lastMove["DOWN"] >= 0.05:
			if self.canMoveDown(playField):
				playField.moveDown()
				self.lastMove["DOWN"] = now
				playField.last_move_down = now
		elif self.keys["LEFT"] and now - self.lastMove["LEFT"] >= 0.05:
			start_x = playField.piece.position["x"]
			start_y = playField.piece.position["y"]
			end_x = min(start_x + len(playField.piece.shape[0]), 10)
			end_y = min(start_y + len(playField.piece.shape), 20)
			for y in range(start_y, end_y):
				for x in range(start_x, end_x):
					color = playField.piece.shape[y - start_y][x - start_x]
					if color != BLACK:
						if x > 0 and (playField.field[y][x -1][0] != BLACK and playField.field[y][x -1][1] == STILL):
							return
			playField.piece.moveLeft()
			self.lastMove["LEFT"] = now
		elif self.keys["RIGHT"] and now - self.lastMove["RIGHT"] >= 0.05:
			start_x = playField.piece.position["x"]
			start_y = playField.piece.position["y"]
			end_x = min(start_x + len(playField.piece.shape[0]), 10)
			end_y = min(start_y + len(playField.piece.shape), 20)
			for y in range(start_y, end_y):
				for x in range(start_x, end_x):
					color = playField.piece.shape[y - start_y][x - start_x]
					if color != BLACK:
						if x < 9 and (playField.field[y][x +1][0] != BLACK and playField.field[y][x +1][1] == STILL):
							return
			playField.piece.moveRight()
			self.lastMove["RIGHT"] = now

		elif self.keys["UP"] and now - self.lastMove["UP"] >= 0.2:
			playField.clearFallingPiece()
			playField.piece.rotate(playField.field)
			self.lastMove["UP"] = now

def resetScreen():
	full_screen = pygame.Rect(0, 0, _WINDOW_WIDTH, _WINDOW_HEIGHT)
	WINDOW.fill(pygame.Color(0, 0, 0), full_screen, 0)

def animateRemoveLine(playField: PlayField):
	print("remove line")
	playField.removeLines()
	resetScreen()
	playField.drawField()
	time.sleep(0.8)

	pygame.display.flip()

	time.sleep(0.8)

	playField.levelDown()
	resetScreen()
	playField.drawField()
	pygame.display.flip()
	
	time.sleep(0.8)

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

		if playField.falling == FALLING:
			if now - playField.last_move_down >= 0.5:
				playField.moveDown()
				playField.last_move_down = now
		else:
			playField.generatePiece()
			if not handleKeys.canMoveDown(playField):
				gameOver = True
		playField.printPiece()

		resetScreen()

		playField.drawField()

		time.sleep(0.016)
		pygame.display.flip()

if __name__ == "__main__":
	main()
