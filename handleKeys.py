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

