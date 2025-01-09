from colors import BLACK
from tetronimos import Tetromino,Straight, Square, LeftLShape, RightLShape, ZShape, SShape, TShape, JShape, STILL, FALLING, Falling
import pygame
import random

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
		move_delay = 0.08
		playField.updateFallingAndField()
		if playField.piece == None:
			return
		num = random.randint(0, 99)
		if self.keys["DOWN"] and now - self.lastMove["DOWN"] >= move_delay:
			if playField.canMoveDown():
				playField.moveDown()
				self.lastMove["DOWN"] = now
				playField.last_move_down = now
		elif self.keys["LEFT"] and now - self.lastMove["LEFT"] >= move_delay:
			print(f"{num}: move left")
			start_x = playField.piece.position["x"]
			start_y = playField.piece.position["y"]
			end_x = min(start_x + len(playField.piece.shape[0]), 10)
			end_y = min(start_y + len(playField.piece.shape), 20)
			for y in range(start_y, end_y):
				for x in range(start_x, end_x):
					color = playField.piece.shape[y - start_y][x - start_x]
					if color != BLACK:
						if x > 0 and (playField.field[y][x -1][0] != BLACK and playField.field[y][x -1][1] == STILL):
							print("RET!!!")
							return
			playField.piece.moveLeft()
			self.lastMove["LEFT"] = now
		elif self.keys["RIGHT"] and now - self.lastMove["RIGHT"] >= move_delay:
			print(f"{num}: move right")
			start_x = playField.piece.position["x"]
			start_y = playField.piece.position["y"]
			end_x = min(start_x + len(playField.piece.shape[0]), 10)
			end_y = min(start_y + len(playField.piece.shape), 20)
			for y in range(start_y, end_y):
				for x in range(start_x, end_x):
					color = playField.piece.shape[y - start_y][x - start_x]
					if color != BLACK:
						if x < 9 and (playField.field[y][x +1][0] != BLACK and playField.field[y][x +1][1] == STILL):
							print("RET!!!")
							return
			playField.piece.moveRight()
			self.lastMove["RIGHT"] = now

		elif self.keys["UP"] and now - self.lastMove["UP"] >= 0.2:
			playField.clearFallingPiece()
			playField.piece.rotate(playField.field)
			self.lastMove["UP"] = now
