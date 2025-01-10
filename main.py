from dataclasses import dataclass
from abc import ABC, abstractmethod
import pygame
import time
import random
from typing import Optional
import logging

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
from handleKeys import HandleKeys
from h_graphics import _WINDOW_HEIGHT, _WINDOW_WIDTH, WINDOW, drawField
from field import PlayField


def resetScreen():
	full_screen = pygame.Rect(0, 0, _WINDOW_WIDTH, _WINDOW_HEIGHT)
	WINDOW.fill(pygame.Color(0, 0, 0), full_screen, 0)


def animateRemoveLine(playField: PlayField):
	playField.removeLines()
	resetScreen()
	drawField(playField)
	time.sleep(0.6)

	pygame.display.flip()

	time.sleep(0.6)

	playField.levelDown()
	resetScreen()
	drawField(playField)
	pygame.display.flip()

	time.sleep(0.6)


def displayGameOver(playField: PlayField):
	grey_color = pygame.Color(200, 200, 200)
	full_screen = pygame.Rect(0, 0, _WINDOW_WIDTH, _WINDOW_HEIGHT)
	WINDOW.fill(pygame.Color(0, 0, 0), full_screen, 0)
	drawField(playField)
	pygame.display.flip()
	time.sleep(0.2)

	text_surface = pygame.font.Font(None, 60).render("Game", True, grey_color)
	WINDOW.blit(text_surface, (150, 320))
	text_surface = pygame.font.Font(None, 60).render("Over", True, grey_color)
	WINDOW.blit(text_surface, (150, 380))
	pygame.display.flip()
	time.sleep(0.8)

def main():

	playField = PlayField()
	handleKeys = HandleKeys()
	logging.basicConfig(filename="tetris.log", level=logging.DEBUG, filemode="w")

	closeApp = False
	gameOver = False
	while not closeApp:
		now = time.time()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				closeApp = True
			if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				handleKeys.updateKeys(event, playField)

		if gameOver:
			displayGameOver(playField)
			continue
		if playField.makeMoves(handleKeys, now):
			continue
		if playField.falling == STILL and playField.fullLine():
			animateRemoveLine(playField)
			continue

		if playField.falling != FALLING:
			print("not falling")
			print ("still time: ", playField.still_time)
			print("now: ", now)
		if playField.falling != FALLING and now - playField.still_time >= 0.5:
			print("time to generate piece")
		if playField.falling != FALLING and now - playField.still_time >= 0.5:
			playField.immobilizeFallingPiece()
			playField.piece = None
			playField.generatePiece()
			if not playField.canMoveDown():
				gameOver = True
		elif playField.falling == FALLING:
			if now - playField.last_move_down >= 0.5:
				print("move down here")
				playField.moveDown()
				playField.last_move_down = now

		playField.printPiece()

		resetScreen()

		drawField(playField)

		time.sleep(0.016)
		pygame.display.flip()


if __name__ == "__main__":
	main()
